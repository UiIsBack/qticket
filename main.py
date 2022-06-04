import asyncio
from fileinput import close
from nextcord import TextChannel
import nextcord, json
from nextcord.ext import commands



client = commands.Bot(command_prefix=">")

@client.event
async def on_ready():
    print("[+]")

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
        b = client.get_channel(md)
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
        members = client.get_all_members
        with open("config.json", "r") as f:
            s = json.load(f)
        d = s['guild']
        guild = client.get_guild(d); channel = await guild.create_text_channel(f"{numt}-ticket")
        await interaction.response.send_message("Created ticket", ephemeral=True)
        await channel.set_permissions(guild.default_role, view_channel=False)
        await channel.set_permissions(interaction.user, view_channel=True)
        with open("config.json", "r") as e:
            d = json.load(e)
        md = d['staff-log']
        b = client.get_channel(md)
        s = nextcord.Embed(title="Log's", description=f"""  Ticket created
                                                            Ticket: <#{channel.id}>
                                                            User: {interaction.user.mention}
                                                            """, color=nextcord.Color.green())
        await b.send(embed=s)
        embed = nextcord.Embed(title="Tickets", description="Welcome, how can we help you today?", color=nextcord.Color.blurple())
        view = Close()
        await channel.send(f"{interaction.user.mention}", embed=embed, view=view)
        await view.wait()
        
        


@client.command()
@commands.has_permissions(administrator=True)

async def setup(ctx):

    view = Confirm()
    embed= nextcord.Embed(title='Tickets', description="Press the button below to crerate ticket!", color=nextcord.Color.blurple())
    await ctx.send(embed=embed, view=view)

    await view.wait()
@client.command()
@commands.has_permissions(administrator=True)
async def closeall(ctx):
    f = nextcord.Embed(title="Tickets", description="Closing all tickets", color=nextcord.Color.blurple())  
    await ctx.send(embed = f)
    channels = ctx.guild.channels
    for channel in channels:
        name = channel.name
        if str(name).endswith("-ticket") or str(name).startswith("ticket-"):
            await channel.delete()
    with open("config.json", "r+") as f:
                t = json.load(f)
    t['num'] = 0
    ee = nextcord.Embed(title="Tickets", description="all tickets closed", color=nextcord.Color.green())  
    await ctx.send(embed = ee)
@client.command()
@commands.has_permissions(administrator=True)
async def closeticket(ctx):
        await ctx.send_message("Closing ticket", ephemeral=True); await asyncio.sleep(2)
        await ctx.channel.delete()
        with open("config.json", "r+") as f:
            t = json.load(f)
        t['num'] = t['num'] - 1
        json.dump(t, open("config.json", "w"), indent = 4)
        with open("config.json", "r") as e:
            d = json.load(e)
        md = d['staff-log']
        b = client.get_channel(md)
        s = nextcord.Embed(title="Log's", description=f"""  Ticket Closed
                                                            Ticket: #{ctx.channel}
                                                            User: {ctx.user.mention}
                                                            """, color=nextcord.Color.red())
        b.send(embed=s)
@client.command()
async def cmds(ctx):
    o = nextcord.Embed(title="Qticket", description="prefix = >\n>setup setups ticket sys in that channel\n>closeall closes all tickets\n>closeticket closes current ticket", color=nextcord.Color.blurple())
    await ctx.send(embed = o)
with open("config.json", "r") as a:
    k = json.load(a)
token = k['token']
client.run(token)
