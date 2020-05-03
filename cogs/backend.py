import discord
from discord.ext import commands
from datetime import datetime, date, time
import time

class Backend(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        errorembed = discord.Embed(title="Command Error",description=f"**Error:** ```{error}```\n**Server:** {ctx.message.guild} ({ctx.message.guild.id})\n**Channel:** <#{ctx.message.channel.id}>- {ctx.message.channel} ({ctx.message.channel.id})\n**User:** {ctx.message.author} ({ctx.message.author.id})", color=0xff0000)
        errorembed.timestamp=datetime.utcnow()
        await self.bot.log_channel.send(embed=errorembed)
        if isinstance(error, commands.MissingPermissions):
            missingperms = discord.Embed(title="Not so fast", description="You do not have permission to use this command",color=0xff0000)
            await ctx.send(embed=missingperms)
            return
        if isinstance(error, commands.UserInputError):
            badinput = discord.Embed(title="Invalid syntax/input", description=f"Use the help command to find proper syntax",color=0xff0000)
            await ctx.send(embed=badinput)
            return
        miscerror = discord.Embed(title="Error", description=error)
        await ctx.send(embed=miscerror)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        botjoinembed = discord.Embed(title="Bot Joined Guild", description=f"**Guild:** {guild.name} ({guild.id})\n **Owner:** {guild.owner} ({guild.owner.id})", color=0x00cfff)
        botjoinembed.timestamp=datetime.utcnow()
        await self.bot.log_channel.send(embed=botjoinembed)
            # collection.insert_one(newconfig)
        # else:
        #     pass
        newconfig = {"_id":guild.id, "Guild Name":guild.name, "Owner":f"{guild.owner} ({guild.owner.id})","Blacklisted":False}
        collection.insert_one(newconfig)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        botleaveembed = discord.Embed(title="Bot Removed From Guild", description=f"**Guild:** {guild.name} ({guild.id})\n **Owner:** {guild.owner} ({guild.owner.id})", color=0xff960c)
        botleaveembed.timestamp=datetime.utcnow()
        await self.bot.log_channel.send(embed=botleaveembed)
        
def setup(bot):
    bot.add_cog(Backend(bot))
