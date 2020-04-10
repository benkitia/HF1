import discord
from discord.ext import commands
from datetime import datetime, date, time
import time

class Backend(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(f"<:error:696628928458129488> Error: {error}")
        errorembed = discord.Embed(title="Command Error",description=f"**Error:** ```{error}```\n**Server:** {ctx.message.guild} ({ctx.message.guild.id})\n**Channel:** <#{ctx.message.channel.id}>- {ctx.message.channel} ({ctx.message.channel.id})\n**User:** {ctx.message.author} ({ctx.message.author.id})", color=0xff0000)
        errorembed.timestamp=datetime.utcnow()
        await self.bot.log_channel.send(embed=errorembed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        botjoinembed = discord.Embed(title="Bot Joined Guild", description=f"**Guild:** {guild.name} ({guild.id})\n **Owner:** {guild.owner} ({guild.owner.id})", color=0x00cfff)
        botjoinembed.timestamp=datetime.utcnow()
        await self.bot.log_channel.send(embed=botjoinembed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        botleaveembed = discord.Embed(title="Bot Removed From Guild", description=f"**Guild:** {guild.name} ({guild.id})\n **Owner:** {guild.owner} ({guild.owner.id})", color=0xff960c)
        botleaveembed.timestamp=datetime.utcnow()
        await self.bot.log_channel.send(embed=botleaveembed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None or message.author.id is self.bot.user.id:
            return
        ctx: commands.Context = await self.bot.get_context(message)
        if ctx.command is None:
            inboxembed = discord.Embed(title=f"New message from {ctx.message.author}", description=f"""
            **Author:** {message.author} ({message.author.id}) \n
            **Content:** {message.content}
            """, color=0x00ff6e)
            await self.bot.log_channel.send(embed=inboxembed)

def setup(bot):
    bot.add_cog(Backend(bot))
