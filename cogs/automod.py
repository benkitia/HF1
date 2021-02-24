import discord
from discord.ext import commands

class Automod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.config = bot.config

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.nick == after.nick:
            return
        if after.nick == None:
            return
        if not self.config.auto_dehoist:
            return
        hoist_ characters = ['!', '@', '#', '$', '%', '^', '&', '*',
                            '(', ')', '-', '_', '+', '=', '[', ']', ':', ';', '"', "'", '<', ',', '>', '.', '?', '?', '`']
        for hoist_ character in hoist_ characters:
            if after.nick.startswith(hoist_ character):
                await before.edit(nick = "I need a new nickname", reason = "Auto dehoist")

def setup(bot):
    bot.add_cog(Automod(bot))
