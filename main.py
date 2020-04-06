import discord
from discord.ext import commands
from datetime import datetime, date, time
import time

token = 'NTgyMzgwOTM4NjY3ODg0NTQ4.XnfB7A.4_fWpCfLOCQ5VqJ0wcjeFgZuUNY'

bot = commands.Bot(command_prefix='-', description='A multipurpose bot by Waffle Development', owner_id=508350582457761813)

cogs = ['cogs.moderation','cogs.backend']

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
@commands.is_owner()
async def load(ctx, *, module):
    try:
        bot.load_extension(f'cogs.{module}')
    except commands.ExtensionError as e:
        await ctx.send(f':x: Failed to load {module} extension: {e.__class__.__name__}: {e}')
        print(f"Error (force)loading {module} extension: {e.__class__.__name__}: {e}")
        print("______________")
    else:
        await ctx.send(f':ok_hand: Loaded extension: {module}')
        print(f"Successfully loaded extension: {module}")
        print("______________")

# @bot.command(hidden=True)
# async def test(ctx):
#     await ctx.send(":waffle:")

# # @bot.command()
# # @commands.is_owner
# # async def say(ctx, *, content):
# #     await ctx.send(content)
# #     await ctx.message.delete()

# # @bot.command()
# # async def embedsay(ctx, *, Title:, *, title, Content:, content, Color:, color):
# #     sayembed = discord.Embed(title=f"{title}", description=f"content", color= {color})
# #     await ctx.send(embed=sayembed)

# @bot.command()
# async def pendingchanges(ctx):
#     await ctx.send(f'https://github.com/WaffleDevelopment/Craig/compare/{bot.version}...master')

# @bot.command()
# @commands.is_owner()
# async def setstatus(ctx, type:int, *, status:str):
#     await bot.change_presence(activity=discord.Game(name=status, type=type))
#     await ctx.send(f":ok_hand::computer: Bot presence set to `{status}`")
#     print(f'Bot presence set to "{status}"')
#     print("______________")


bot.run(token)