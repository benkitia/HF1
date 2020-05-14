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
        content = f"```{ctx.message.content}```"
        if content == "``````":
            content = "[No Content]"
        msgdellogem = discord.Embed(title=f"Message deleted in #{ctx.message.channel}", description=f"""
        **Author:** {ctx.message.author} ({ctx.message.author.id})
        **Content:** {content}
        **Message ID:** {ctx.message.id}
        """, color=0xff1919)
        msgdellogem.timestamp = datetime.datetime.utcnow()
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
        getvars = await self.db.guildconfigs.find_one({"_id":member.guild.id})
        logchannelidstr = getvars["travel log"]
        if logchannelidstr == "disabled":
            return
        logchannelid = int(logchannelidstr)
        logchannel = discord.utils.get(member.guild.text_channels, id=logchannelid)
        global_inf_count = await self.db.infractions.count_documents({"Target":member.id, "Status":"Active"})
        memjoinem = discord.Embed(title="User Joined",description=f"""**User** {member} ({member.id})
        **Created At:** {member.created_at}
        **Global Infraction Count:** {global_inf_count}
        """, color=0x48ff99)
        memjoinem.set_thumbnail(url=member.avatar_url)
        memjoinem.timestamp = datetime.datetime.utcnow()
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
        memleaveem = discord.Embed(title="User Left",description=f"""**User** {member} ({member.id})
        **Joined at:** {member.joined_at}
        **Infraction Count:** {inf_count}
        """, color=0xff7d7d)
        memleaveem.set_thumbnail(url=member.avatar_url)
        memleaveem.timestamp = datetime.datetime.utcnow()
        await logchannel.send(embed=memleaveem)

def setup(bot):
    bot.add_cog(Logging(bot))