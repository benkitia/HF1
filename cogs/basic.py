import discord
from discord.ext import commands
from datetime import datetime, date, time
import time

class Basic(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(description="Returns bot response time")
    async def ping(self, ctx):
        t1 = time.perf_counter()
        async with ctx.typing():
            pass
        t2 = time.perf_counter()
        await ctx.send(":ping_pong: Pong! It took {}ms".format(round((t2-t1)*1000)))

def setup(bot):
    bot.add_cog(Basic(bot))