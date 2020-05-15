import discord
from discord.ext import commands
import datetime

class Logging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        ctx: commands.Context = await self.bot.get_context(message)
        getvars = await self.db.guildconfigs.find_one({"_id":ctx.message.guild.id})
        logchannelidstr = getvars["message log"]
        if logchannelidstr == "disabled" or message.author.bot:
            return
        logchannelid = int(logchannelidstr)
        logchannel = discord.utils.get(ctx.guild.text_channels, id=logchannelid)
        content = ctx.message.content
        if not content:
            content = "[No Content]"
        msgdellogem = discord.Embed(description=f"Message {ctx.message.id} deleted from <#{ctx.message.channel.id}>:\n**Content:** {content}", color=0xff1919)
        msgdellogem.timestamp = datetime.datetime.utcnow()
        msgdellogem.set_author(icon_url=ctx.message.author.avatar_url, name=f"{ctx.message.author} ({ctx.message.author.id})")
        if ctx.message.attachments:
            attachments = ctx.message.attachments
            for attachment in attachments:
                url = attachment.url
                name = attachment.filename
                if not url.endswith((".jpg", ".jpeg", ".png", ".gif", ".wepb")):
                    msgdellogem.add_field(name="Attachment",value=name)
                elif url.endswith((".jpg", ".jpeg", ".png", ".gif", ".wepb")):
                    channel = self.bot.get_channel(710566693742706728)
                    await channel.send(attachment.proxy_url)
                    msgdellogem.add_field(name="Attachment",value=f"[{name}]({attachment.proxy_url})")
        await logchannel.send(embed=msgdellogem)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        ctx: commands.Context = await self.bot.get_context(before)
        getvars = await self.db.guildconfigs.find_one({"_id":ctx.message.guild.id})
        logchannelidstr = getvars["message log"]
        if logchannelidstr == "disabled" or before.author.bot:
            return
        logchannelid = int(logchannelidstr)
        logchannel = discord.utils.get(ctx.guild.text_channels, id=logchannelid)
        before_content = before.content
        if not before_content:
            before_content = "[No Content]"
        after_content = after.content
        if not after_content:
            after_content = "[No Content]"
        msgeditlogem = discord.Embed(description=f"Message {ctx.message.id} edited in <#{ctx.message.channel.id}>:\n**Before:** {before_content}\n**After:** {after_content}", color=0xff8500)
        msgeditlogem.set_author(icon_url=ctx.message.author.avatar_url, name=f"{ctx.message.author} ({ctx.message.author.id})")
        msgeditlogem.timestamp = datetime.datetime.utcnow()
        await logchannel.send(embed=msgeditlogem)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        getvars = await self.db.guildconfigs.find_one({"_id":member.guild.id})
        logchannelidstr = getvars["travel log"]
        if logchannelidstr == "disabled":
            return
        logchannelid = int(logchannelidstr)
        logchannel = discord.utils.get(member.guild.text_channels, id=logchannelid)
        global_inf_count = await self.db.infractions.count_documents({"Target":member.id, "Status":"Active"})
        memjoinem = discord.Embed(description=f"{member.name} has joined the server\nThey have {global_inf_count} global infraction(s)\nThere are now {member.guild.member_count} members",color=0x48ff99)
        memjoinem.set_thumbnail(url=member.avatar_url)
        memjoinem.timestamp = datetime.datetime.utcnow()
        memjoinem.set_author(icon_url=member.avatar_url, name=f"{member} ({member.id})")
        await logchannel.send(embed=memjoinem)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        getvars = await self.db.guildconfigs.find_one({"_id":member.guild.id})
        logchannelidstr = getvars["travel log"]
        if logchannelidstr == "disabled":
            return
        logchannelid = int(logchannelidstr)
        logchannel = discord.utils.get(member.guild.text_channels, id=logchannelid)
        inf_count = await self.db.infractions.count_documents({"Target":member.id, "Guild":member.guild.id,"Status":"Active"})
        memleaveem = discord.Embed(description=f"{member.name} has left the server\nThey had {inf_count} infraction(s)\nThere are now {member.guild.member_count} members",color=0xff7d7d)
        memleaveem.set_thumbnail(url=member.avatar_url)
        memleaveem.timestamp = datetime.datetime.utcnow()
        memleaveem.set_author(icon_url=member.avatar_url, name=f"{member} ({member.id})")
        await logchannel.send(embed=memleaveem)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.nick == after.nick:
            return
        getvars = await self.db.guildconfigs.find_one({"_id":before.guild.id})
        logchannelidstr = getvars["user log"]
        if logchannelidstr == "disabled":
            return
        logchannelid = int(logchannelidstr)
        logchannel = discord.utils.get(before.guild.text_channels, id=logchannelid)
        nickem = discord.Embed(description=f"Nickname changed\n**Before:** {before.nick}\n**After:** {after.nick}",color=0xeb88ff)
        nickem.set_author(icon_url=before.avatar_url, name=f"{before} ({before.id})")
        nickem.timestamp = datetime.datetime.utcnow()
        await logchannel.send(embed=nickem)

def setup(bot):
    bot.add_cog(Logging(bot))