import discord
from discord.ext import commands
from copy import deepcopy

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, module):
        try:
            self.bot.load_extension(f'cogs.{module}')
        except commands.ExtensionError as e:
            await ctx.send(f':x: Failed to load {module} extension: {e.__class__.__name__}: {e}')
        else:
            await ctx.send(f':ok_hand: Loaded extension: {module}')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, module):
        try:
            self.bot.unload_extension(f'cogs.{module}')
        except commands.ExtensionError as e:
            await ctx.send(f':x: Failed to unload {module} extension: {e.__class__.__name__}: {e}')
        else:
            await ctx.send(f':ok_hand: Unloaded extension: {module}')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, module):
        try:
            self.bot.reload_extension(f'cogs.{module}')
        except commands.ExtensionError as e:
            await ctx.send(f':x: Failed to reload {module} extension: {e.__class__.__name__}: {e}')
        else:
            await ctx.send(f':ok_hand: reloaded extension: {module}')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def say(self, ctx, *, content):
        arthur = ctx.message.author
        try:
            await ctx.send(f"{content}")
        except discord.Forbidden:
            return await arthur.send("<:error:696628928458129488> I couldn't say that because I don't have sufficient permissions")
        try:
           await ctx.message.delete()
        except discord.Forbidden:
            return await arthur.send("<:error:696628928458129488> I couldn't delete your invocation message because I don't have sufficient permissions")

    @commands.command()
    async def setpresence(self, ctx, type:int, *, presence:str):
        await self.bot.change_presence(activity=discord.Activity(name=presence, type=type))
        await ctx.send(f":ok_hand: Bot presence set to `{presence}`")

    @commands.command(aliases=['logout'], description="Logs the bot out", hidden=True)
    @commands.is_owner()
    async def close(self, ctx):
        await self.bot.close()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def messageuser(self, ctx, member:discord.Member, *, message):
        try:
            await member.send(message)
            await ctx.send(f":incoming_envelope: Sent message to {member}: `{message}`")
        except:
            await ctx.send(":x: Failed to send message to {member.name}. Their DMs are likely closed.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sudo(self, ctx, user: discord.Member, *, command):
        new_msg = ctx.message
        new_msg.author = user
        new_msg.content = f"{ctx.prefix}{command}"
        await self.bot.process_commands(new_msg)


def setup(bot):
    bot.add_cog(Admin(bot))
