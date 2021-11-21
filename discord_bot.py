import discord
from discord.ext import commands
# discord client(our bot)
client = commands.Bot(command_prefix='--')
#do stuff

@client.event
async def on_ready():
 print('We have logged in as {0.user}'.format(client))
 general_channel = client.get_channel(886889808843141154)
 await general_channel.send("Hello Guys!")

@client.command()
async def start(ctx):
    #general_channel = client.get_channel(886889808843141154)
    await ctx.send("The app has been started!")

@client.event
async def on_disconnect():
    general_channel = client.get_channel(886889808843141154)
    await general_channel.send("Goodbye Bro!")

@client.event
async def on_message(message):
    if message.content == '#search':
        general_channel = client.get_channel(886889808843141154)
        myEmbed = discord.Embed(title="Search Result" , description="Reliance Industries",color = 0x00ff00)
        myEmbed.add_field(name="Version Code:",value="1.0.0",inline=False)
        myEmbed.add_field(name="Date Released:",value="July 18th 2020",inline=False)
        myEmbed.set_footer(text="This is a sample footer")
        myEmbed.set_author(name="Yahoo Finance")
        await general_channel.send(embed = myEmbed)

client.run('os.getenv("TOKEN")')
