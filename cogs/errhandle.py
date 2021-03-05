import discord
from discord.ext import commands
class Errhandle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.functions = bot.functions

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            return await self.functions.handle_error(ctx, "Invalid user")
        if isinstance(error, commands.errors.RoleNotFound):
            return await self.functions.handle_error(ctx, "Invalid role")
        if isinstance(error, commands.UserInputError):
            return await self.functions.handle_error(ctx, "Invalid command syntax", "Run help for help")
        

def setup(bot):
    bot.add_cog(Errhandle(bot))
