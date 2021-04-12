
import discord
from discord.ext import commands


class Event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx: commands.Context = await self.bot.get_context(message)
        if ctx.message.channel.id != 822206729445048342:
            return
        if ctx.message.author.id == 508350582457761813 or self.bot.user.id:
            return
        if ctx.message.content:
            return await ctx.message.delete()
        if len(ctx.message.attachments) != 1:
            return await ctx.message.delete()
        await ctx.message.add_reaction('<:upvote:711293005583220807>')


def setup(bot):
    bot.add_cog(Event(bot))