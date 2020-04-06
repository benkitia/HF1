import discord
from discord.ext import commands
from datetime import datetime, date, time
import time
from config import config_bot_log_channel

class Backend(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        logchannel = self.bot.get_channel(config_bot_log_channel)
        errorembed = discord.Embed(title="Command Error",description=f"**Error:** ```{error}```\n**Server:** {ctx.message.guild} ({ctx.message.guild.id})\n**Channel:** <#{ctx.message.channel.id}>- {ctx.message.channel} ({ctx.message.channel.id})\n**User:** {ctx.message.author} ({ctx.message.author.id})", color=0xff0000)
        errorembed.timestamp=datetime.utcnow()
        await logchannel.send(embed=errorembed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        log_channel = self.bot.get_channel(config_bot_log_channel)
        botjoinembed = discord.Embed(title="Bot Joined Guild", description=f"**Guild:** {guild.name} ({guild.id})\n **Owner:** {guild.owner} ({guild.owner.id})", color=0x00cfff)
        botjoinembed.timestamp=datetime.utcnow()
        await log_channel.send(embed=botjoinembed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        log_channel = self.bot.get_channel(config_bot_log_channel)
        botleaveembed = discord.Embed(title="Bot Removed From Guild", description=f"**Guild:** {guild.name} ({guild.id})\n **Owner:** {guild.owner} ({guild.owner.id})", color=0xff960c)
        botleaveembed.timestamp=datetime.utcnow()
        await log_channel.send(embed=botleaveembed)

def setup(bot):
    bot.add_cog(Backend(bot))