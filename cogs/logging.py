import discord
from discord.ext import commands
import datetime
import time

class Logging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        ctx: commands.Context = await self.bot.get_context(message)
        getvars = await self.db.guildconfigs.find_one({"_id":ctx.message.guild.id})
        logchannelid = getvars["messagelog"]
        if logchannelid == "disabled" or message.author.bot:
            return
        logchannelid = int(logchannelid)
        logchannel = discord.utils.get(ctx.guild.text_channels, id=logchannelid)
        content = ctx.message.content
        if not content:
            content = "[No Content]"
        log = discord.Embed(description=f"{ctx.message.author.mention}'s message was deleted from {ctx.message.channel.mention}:", color=0xff1919)
        log.add_field(
            name = "Content",
            value = content,
            inline = False
            )
        log.timestamp = datetime.datetime.utcnow()
        log.set_author(icon_url = ctx.message.author.avatar_url, name=f"{ctx.message.author} ({ctx.message.author.id})")
        log.set_footer(text = ctx.message.id)
        if ctx.message.attachments:
            attachments = ctx.message.attachments
            attachmentlist = ""
            for attachment in attachments:
                url = attachment.url
                name = attachment.filename
                if not url.endswith((".jpg", ".jpeg", ".png", ".gif", ".wepb",".mp4",".mov",".wmv",".avi",".txt",".docx",".csv",".xlxs")):
                    attachmentlist = f"{attachmentlist}\n{name}"
                elif url.endswith((".jpg", ".jpeg", ".png", ".gif", ".wepb",".mp4",".mov",".wmv",".avi",".txt",".docx",".csv",".xlxs")):
                    attachmentlist = f"{attachmentlist}\n[{name}]({attachment.proxy_url})"
            log.add_field(
                name="Attachments",
                value=attachmentlist,
                inline = False
                )
        await logchannel.send(embed=log)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        ctx: commands.Context = await self.bot.get_context(before)
        getvars = await self.db.guildconfigs.find_one({"_id":ctx.message.guild.id})
        logchannelid = getvars["messagelog"]
        if logchannelid == "disabled" or before.author.bot:
            return
        logchannelid = int(logchannelid)
        logchannel = discord.utils.get(ctx.guild.text_channels, id=logchannelid)
        before_content = before.content
        if not before_content:
            before_content = "[No Content]"
        after_content = after.content
        if not after_content:
            after_content = "[No Content]"
        if before == after:
            return
        if before_content == after_content:
            return
        log = discord.Embed(
            description=f"[Jump to message]({ctx.message.jump_url})\n{ctx.message.author.mention} edited a message in {ctx.message.channel.mention}:", 
            color=0xff8500
            )
        log.add_field(
            name = "Before",
            value = before_content,
            inline = False
        )
        log.add_field(
            name = "After",
            value = after_content,
            inline = False
        )
        log.set_author(icon_url=ctx.message.author.avatar_url, name=f"{ctx.message.author} ({ctx.message.author.id})")
        log.timestamp = datetime.datetime.utcnow()
        log.set_footer(text = ctx.message.id)
        await logchannel.send(embed=log)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        getvars = await self.db.guildconfigs.find_one({"_id":member.guild.id})
        logchannelid = getvars["travellog"]
        if logchannelid == "disabled":
            return
        logchannelid = int(logchannelid)
        logchannel = discord.utils.get(member.guild.text_channels, id=logchannelid)
        global_inf_count = await self.db.infractions.count_documents({"Target":member.id, "Status":"Active"})
        dif = (datetime.datetime.utcfromtimestamp(time.time()) - member.created_at)
        dif = str(dif)
        print(dif.split(','))
        dif = dif.split(',')[0]
        log = discord.Embed(description=f"{member.mention} joined the server\n{global_inf_count} global infraction(s)\nAccount created {dif} ago",color=0x48ff99)
        log.set_thumbnail(url=member.avatar_url)
        log.timestamp = datetime.datetime.utcnow()
        log.set_author(icon_url=member.avatar_url, name=f"{member} ({member.id})")
        log.set_footer(text = f"Member Count: {member.guild.member_count}")
        await logchannel.send(embed=log)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        getvars = await self.db.guildconfigs.find_one({"_id":member.guild.id})
        logchannelid = getvars["travellog"]
        if logchannelid == "disabled":
            return
        logchannelid = int(logchannelid)
        logchannel = discord.utils.get(member.guild.text_channels, id=logchannelid)
        inf_count = await self.db.infractions.count_documents({"Target":member.id, "Guild":member.guild.id,"Status":"Active"})
        dif = (datetime.datetime.utcfromtimestamp(time.time()) - member.joined_at)
        dif = str(dif)
        print(dif.split(','))
        dif = dif.split(',')[0]
        log = discord.Embed(
            description=f"{member.mention} left the server\n{inf_count} local infraction(s)\nStayed for {dif}",
            color=0xff7d7d
            )
        log.set_thumbnail(url=member.avatar_url)
        log.timestamp = datetime.datetime.utcnow()
        log.set_author(icon_url=member.avatar_url, name=f"{member} ({member.id})")
        log.set_footer(text = f"Member Count: {member.guild.member_count}")
        await logchannel.send(embed=log)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.nick != after.nick:
            getvars = await self.db.guildconfigs.find_one({"_id":before.guild.id})
            logchannelid = getvars["userlog"]
            if logchannelid == "disabled":
                return
            logchannelid = int(logchannelid)
            logchannel = discord.utils.get(before.guild.text_channels, id=logchannelid)
            if before.nick == None:
                before.nick = "[No nickname]"
            if after.nick == None:
                after.nick = "[No nickname]"
            log = discord.Embed(
                description=f"{before.mention} updated their nickname:",
                color=0xeb88ff
                )
            log.add_field(
                name = "Before",
                value = before.nick
            )
            log.add_field(
                name = "After",
                value = after.nick
            )
            log.set_author(icon_url=before.avatar_url, name=f"{after} ({after.id})")
            log.timestamp = datetime.datetime.utcnow()
            await logchannel.send(embed=log)

def setup(bot):
    bot.add_cog(Logging(bot))