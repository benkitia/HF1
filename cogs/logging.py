import discord
from discord.ext import commands
import datetime

class Logging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild != self.bot.config.guild_id or self.bot.message_log_channel is None or message.author.bot:
            return
        ctx: commands.Context = await self.bot.get_context(message)
        msgdellogem = discord.Embed(title=f"Message deleted in #{ctx.message.channel}", description=f"""
        **Author:** {ctx.message.author} ({ctx.message.author.id})
        **Content:** ```{ctx.message.content}```
        **Message ID:** {ctx.message.id}
        """, color=0xff1919)
        msgdellogem.timestamp = datetime.datetime.utcnow()
        await self.bot.message_log_channel.send(embed=msgdellogem)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.guild.id != self.bot.config.guild_id or self.bot.message_log_channel is None or before.author.bot:
            return
        ctx: commands.Context = await self.bot.get_context(before)
        msgeditlogem = discord.Embed(title=f"Message edited in #{ctx.message.channel}", description=f"""
        **Author:** {ctx.message.author} ({ctx.message.author.id})
        **Before:** ```{before.content}```
        **After:** ```{after.content}```
        **Message ID:** {ctx.message.id}
        """, color=0xff8500)
        msgeditlogem.timestamp = datetime.datetime.utcnow()
        await self.bot.message_log_channel.send(embed=msgeditlogem)

def setup(bot):
    bot.add_cog(Logging(bot))
