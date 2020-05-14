import discord
from discord.ext import commands
from datetime import datetime, date, time
import time
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://wafflebot:fkKi2m2Eg2UjjJWZHiBVuWihAi9fdHpw@waffledev.derw.xyz/?ssl=false")
db = cluster["wafflebot"]
collection = db["server configs"]

class Backend(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send("<:error:696628928458129488> You do not have permission to run this command")
        if isinstance(error, commands.UserInputError):
            return await ctx.send("<:error:696628928458129488> Invalid arguement(s)")
        elif isinstance(error, commands.errors.NotOwner):
            return await ctx.send("<:error:696628928458129488> You do not have permission to run this command")
        errorembed = discord.Embed(title="Command Error",description=f"**Error:** ```{error}```\n**Server:** {ctx.message.guild} ({ctx.message.guild.id})\n**Channel:** <#{ctx.message.channel.id}>- {ctx.message.channel} ({ctx.message.channel.id})\n**User:** {ctx.message.author} ({ctx.message.author.id})", color=0xff0000)
        errorembed.timestamp=datetime.utcnow()
        await self.bot.log_channel.send(embed=errorembed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        botjoinembed = discord.Embed(title="Bot Joined Guild", description=f"**Guild:** {guild.name} ({guild.id})\n **Owner:** {guild.owner} ({guild.owner.id})", color=0x00cfff)
        botjoinembed.timestamp=datetime.utcnow()
        await self.bot.log_channel.send(embed=botjoinembed)
        newconfig = {"_id":guild.id,"Guild Name":guild.name,"prefix":"-","staff role":"placeholder","admin role":"placeholder","action log":"placeholder","user log":"placeholder","alert channel":"placeholder","mute role":"placeholder","filter invites":False,"filter bad words":False}
        self.db.guildconfigs.insert_one(newconfig)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        botleaveembed = discord.Embed(title="Bot Removed From Guild", description=f"**Guild:** {guild.name} ({guild.id})\n **Owner:** {guild.owner} ({guild.owner.id})", color=0xff960c)
        botleaveembed.timestamp=datetime.utcnow()
        await self.bot.log_channel.send(embed=botleaveembed)
        
def setup(bot):
    bot.add_cog(Backend(bot))
