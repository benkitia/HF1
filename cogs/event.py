
import discord
from discord.ext import commands


class Event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx: commands.Context = await self.bot.get_context(message)
        if ctx.message.channel.id != self.config.photo_of_the_week_channel:
            return
        if ctx.message.content:
            return await ctx.message.delete()
        if len(ctx.message.attachments) != 1:
            return await ctx.message.delete()
        await ctx.message.add_reaction('<:upvote:711293005583220807>')


def setup(bot):
    bot.add_cog(Event(bot))