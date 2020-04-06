import discord
from discord.ext import commands
from datetime import datetime, date, time
import time
from config import config_token, config_prefix, config_description, config_owner_id

token = config_token

bot = commands.Bot(command_prefix=config_prefix, description=config_description, owner_id=config_owner_id)

cogs = ['cogs.admin']

@bot.event
async def on_ready():
    print(f"{bot.user.name} ({bot.user.id}) is online")
    print("______________")
    onready = discord.Embed(title="Bot logged on", description=f"{bot.user.name} ({bot.user.id}) is online",color=0x4bff92)
    onready.timestamp=datetime.utcnow()
    pstatus = f"eating breakfast"
    await bot.change_presence(activity=discord.Game(name=pstatus), status=discord.Status.online)
    print(f'\n Bot presence set to "{pstatus}"')
    print("______________")
    setstatus = discord.Embed(title="Bot presence set", description=f"Bot status set to `{pstatus}`", color=0xad6dff)
    setstatus.timestamp=datetime.utcnow()
    for cog in cogs: 
    	bot.load_extension(cog)
        

@bot.command(hidden=True)
async def test(ctx):
    await ctx.send(":waffle:")

bot.run(token)