import asyncio
from nextcord import TextChannel
import nextcord, json
from nextcord.ext import commands
from nextcord import Colour, Interaction, SlashOption, ChannelType


bot = commands.Bot(command_prefix=">")

@bot.event
async def on_ready():
    print("[+]")
with open('config.json', "r") as a:
    data = json.load(a)
gid = data['guild']
class Close(nextcord.ui.View):
    def __init__(self):
        super().__init__()


    @nextcord.ui.button(label="Close ticket", style=nextcord.ButtonStyle.red)
    async def close(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Closing ticket", ephemeral=True); await asyncio.sleep(2)
        await interaction.channel.delete()
        with open("config.json", "r+") as f:
            t = json.load(f)
        t['num'] = t['num'] - 1
        json.dump(t, open("config.json", "w"), indent = 4)
        with open("config.json", "r") as e:
            d = json.load(e)
        md = d['staff-log']
        b = bot.get_channel(md)
        s = nextcord.Embed(title="Log's", description=f"""  Ticket Closed
                                                            Ticket: #{interaction.channel}
                                                            User: {interaction.user.mention}
                                                            """, color=nextcord.Color.red())
        await b.send(embed=s)
        
class Confirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
  

    @nextcord.ui.button(label="Create ticket", style=nextcord.ButtonStyle.blurple)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):


      
        with open("config.json", "r+") as f:
            t = json.load(f)
        t['num'] = t['num'] + 1
        json.dump(t, open("config.json", "w"), indent = 4)
        numt = t['num']
        members = bot.get_all_members

        guild = bot.get_guild(gid); channel = await guild.create_text_channel(f"{numt}-ticket")
        await interaction.response.send_message("Created ticket", ephemeral=True)
        await channel.set_permissions(guild.default_role, view_channel=False)
        await channel.set_permissions(interaction.user, view_channel=True)
        with open("config.json", "r") as e:
            d = json.load(e)
        md = d['staff-log']
        b = bot.get_channel(md)
        s = nextcord.Embed(title="Log's", description=f"""  Ticket created
                                                            Ticket: <#{channel.id}>
                                                            User: {interaction.user.mention}
                                                            """, color=nextcord.Color.green())
        await b.send(embed=s)
        embed = nextcord.Embed(title="Tickets", description="Welcome, how can we help you today?", color=nextcord.Color.blurple())
        view = Close()
        await channel.send(f"{interaction.user.mention}", embed=embed, view=view)
        await view.wait()
        
        


@bot.slash_command(description="Setsup ticket system!")
@commands.has_permissions(administrator=True)

async def setup(interaction: Interaction):

    view = Confirm()
    embed= nextcord.Embed(title='Tickets', description="Press the button below to crerate ticket!", color=nextcord.Color.blurple())
    await interaction.send(embed=embed, view=view)

    await view.wait()
@bot.slash_command(description="Closes all open tickets!")
@commands.has_permissions(administrator=True)
async def closeall(interaction: Interaction):
    f = nextcord.Embed(title="Tickets", description="Closing all tickets", color=nextcord.Color.blurple())  
    await interaction.send(embed = f)
    channels = interaction.guild.channels
    for channel in channels:
        name = channel.name
        if str(name).endswith("-ticket") or str(name).startswith("ticket-"):
            await channel.delete()
    with open("config.json", "r+") as f:
                t = json.load(f)
    t['num'] = 0
    ee = nextcord.Embed(title="Tickets", description="all tickets closed", color=nextcord.Color.green())  
    await interaction.send(embed = ee)
@bot.slash_command(description="Closes current ticket!")
@commands.has_permissions(administrator=True)
async def close(interaction: Interaction):
        await interaction.send("Closing ticket", ephemeral=True); await asyncio.sleep(2)
        await interaction.channel.delete()
        with open("config.json", "r+") as f:
            t = json.load(f)
        t['num'] = t['num'] - 1
        json.dump(t, open("config.json", "w"), indent = 4)
        with open("config.json", "r") as e:
            d = json.load(e)
        md = d['staff-log']
        b = bot.get_channel(md)
        s = nextcord.Embed(title="Log's", description=f"""  Ticket Closed
                                                            Ticket: #{interaction.channel}
                                                            User: {interaction.user.mention}
                                                            """, color=nextcord.Color.red())
        b.send(embed=s)
@bot.slash_command(description="Shows all commands!")
@commands.has_permissions(administrator=True)
async def cmds(interaction: Interaction):
    o = nextcord.Embed(title="Qticket", description="prefix = /\n/setup setups ticket sys in that channel\n/closeall closes all tickets\n/close closes current ticket", color=nextcord.Color.blurple())
    await interaction.send(embed = o)
with open("config.json", "r") as a:
    k = json.load(a)
token = k['token']
bot.run(token)
