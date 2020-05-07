import discord
from discord.ext import commands
import datetime
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://wafflebot:fkKi2m2Eg2UjjJWZHiBVuWihAi9fdHpw@waffledev.derw.xyz/?ssl=false")
db = cluster["wafflebot"]
infractions = db["infractions"]
guildconfig = db["server configs"]

class Logging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        ctx: commands.Context = await self.bot.get_context(message)
        getvars = guildconfig.find_one({"_id":ctx.message.guild.id})
        logchannelname = getvars["user log"]
        if logchannelname is None or message.author.bot:
            return
        logchannel = discord.utils.get(ctx.guild.text_channels, name=logchannelname)
        msgdellogem = discord.Embed(title=f"Message deleted in #{ctx.message.channel}", description=f"""
        **Author:** {ctx.message.author} ({ctx.message.author.id})
        **Content:** ```{ctx.message.content}```
        **Message ID:** {ctx.message.id}
        """, color=0xff1919)
        msgdellogem.timestamp = datetime.datetime.utcnow()
        await logchannel.send(embed=msgdellogem)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        ctx: commands.Context = await self.bot.get_context(before)
        getvars = guildconfig.find_one({"_id":ctx.message.guild.id})
        logchannelname = getvars["user log"]
        if logchannelname is None or ctx.author.bot:
            return
        logchannel = discord.utils.get(ctx.guild.text_channels, name=logchannelname)
        msgeditlogem = discord.Embed(title=f"Message edited in #{ctx.message.channel}", description=f"""
        **Author:** {ctx.message.author} ({ctx.message.author.id})
        **Before:** ```{before.content}```
        **After:** ```{after.content}```
        **Message ID:** {ctx.message.id}
        """, color=0xff8500)
        msgeditlogem.timestamp = datetime.datetime.utcnow()
        await logchannel.send(embed=msgeditlogem)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        getvars = guildconfig.find_one({"_id":member.guild.id})
        logchannelname = getvars["user log"]
        if logchannelname is None:
            return
        logchannel = discord.utils.get(member.guild.text_channels, name=logchannelname)
        global_inf_count = infractions.count_documents({"Target":member.id, "Status":"Active"})
        memjoinem = discord.Embed(title="User Joined",description=f"""**User** {member} ({member.id})
        **Created At:** {member.created_at}
        **Global Infraction Count:** {global_inf_count}
        """, color=0x48ff99)
        memjoinem.set_thumbnail(url=member.avatar_url)
        memjoinem.timestamp = datetime.datetime.utcnow()
        await logchannel.send(embed=memjoinem)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        getvars = guildconfig.find_one({"_id":member.guild.id})
        logchannelname = getvars["user log"]
        if logchannelname is None:
            return
        logchannel = discord.utils.get(member.guild.text_channels, name=logchannelname)
        inf_count = infractions.count_documents({"Target":member.id, "Guild":member.guild.id,"Status":"Active"})
        memleaveem = discord.Embed(title="User Left",description=f"""**User** {member} ({member.id})
        **Joined at:** {member.joined_at}
        **Infraction Count:** {inf_count}
        """, color=0xff7d7d)
        memleaveem.set_thumbnail(url=member.avatar_url)
        memleaveem.timestamp = datetime.datetime.utcnow()
        await logchannel.send(embed=memleaveem)

def setup(bot):
    bot.add_cog(Logging(bot))