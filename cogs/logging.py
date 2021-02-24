from datetime import datetime, date, time
from datetime import datetime, date, time
import discord
from discord.ext import commands
import time

class Logging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.config = bot.config

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not self.config.message_delete_log:
            return
        ctx: commands.Context = await self.bot.get_context(message)
        try:
            channel = discord.utils.get(ctx.guild.text_channels, id = self.config.message_delete_log)
        except:
            print(f"Unable to log deletion of message {ctx.message.id} because the provided message_delete_log channel ID was invalid.\n__________")
        if not ctx.message.content:
            message_content = "[No Content]"
        else:
            message_content = ctx.message.content
        message_author = self.bot.get_user(ctx.message.author.id)
        embed = discord.Embed(
            description = f"{message_author.mention}'s message was deleted from {ctx.message.channel.mention}:",
            color = 0xff6f00
        )
        embed.add_field(
            name = "Content",
            value = message_content,
            inline = False
        )
        embed.set_author(
            name = f"{message_author} ({message_author.id})",
            icon_url = message_author.avatar_url
        )
        embed.set_footer(text = ctx.message.id)
        embed.timestamp = datetime.datetime.utcnow()
        if ctx.message.attachments:
            message_attachments = ctx.message.attachments
            viewable_attachment_list = ""
            for message_attachment in message_attachments:
                if not message_attachment.url.endswith((".jpg", ".jpeg", ".png", ".gif", ".wepb", ".mp4", ".mov", ".wmv", ".avi", ".txt", ".docx", ".csv", ".xlxs")):
                    viewable_attachment_list = f"{viewable_attachment_list}\n{message_attachment.filename}"
                else:
                    viewable_attachment_list = f"{viewable_attachment_list}\n[{message_attachment.filename}]({message_attachment.proxy_url})"
            embed.add_field(
                name = "Attachments",
                value = viewable_attachment_list,
                inline = False
            )
        try:
            await channel.send(embed = embed)
        except:
            print(f"Unable to log deletion of message {ctx.message.id} because I don't have permission to send messages in the provided message_delete_log channel.\n__________")


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not self.config.message_edit_log:
            return
        ctx: commands.Context = await self.bot.get_context(before)
        if before.content == after.content:
            return
        try:
            channel = discord.utils.get(ctx.guild.text_channels, id = self.config.message_edit_log)
        except:
            print(f"Unable to log edit to message {ctx.message.id} because the provided message_edit_log channel ID was invalid.\n__________")
        if not before.content:
            before_content = "[No Content]"
        else:
            before_content = before.content
            if len(before_content) >= 1024:
                before_content = f"{before_content[0:1021]}..."
        if not after.content:
            after_content = "[No Content]"
        else:
            after_content = after.content
            if len(after_content) >= 1024:
                after_content = f"{after_content[:1021]}..."
        embed = discord.Embed(
            description = f"[Jump to message]({ctx.message.jump_url})\n{ctx.message.author.mention} edited their message in {ctx.message.channel.mention}:",
            color = 0xe9da24
        )
        embed.add_field(
            name = "Before",
            value = before_content,
            inline = False
        )
        embed.add_field(
            name = "After",
            value = after_content,
            inline = False
        )
        embed.set_author(
            icon_url = ctx.message.author.avatar_url,
            name = f"{ctx.message.author} ({ctx.message.author.id})"
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text = ctx.message.id)
        try:
            await channel.send(embed = embed)
        except:
            print(f"Unable to log edit of message {ctx.message.id} because I don't have permission to send messages in the provided message_edit_log channel.\n__________")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not self.config.user_join_log:
            return
        try:
            channel = discord.utils.get(member.guild.text_channels, id = self.config.user_join_log)
        except:
            print(f"Unable to log user {member.id} joining because the provided user_join_log channel ID was invalid.\n__________")
        account_created = str((datetime.datetime.utcfromtimestamp(time.time()) - member.created_at))
        account_created = account_created.split(',')[0]
        embed = discord.Embed(
            description = f"{member.mention} joined the server\nAccount created {account_created} ago", 
            color = 0x298000
            )
        embed.set_thumbnail(url = member.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(
            icon_url = member.avatar_url,
            name = f"{member} ({member.id})"
            )
        embed.set_footer(text=f"Member Count: {member.guild.member_count}")
        try:
            await channel.send(embed = embed)
        except:
            print(f"Unable to log user {member.id} joining because I don't have permission to send messages in the provided user_join_log channel.\n__________")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not self.config.user_leave_log:
            return
        try:
            channel = discord.utils.get(member.guild.text_channels, id = self.config.user_leave_log)
        except:
            print(f"Unable to log user {member.id} leaving because the provided user_leave_log channel ID was invalid.\n__________")
        joined = str((datetime.datetime.utcfromtimestamp(time.time()) - member.joined_at))
        joined = joined.split(',')[0]
        embed = discord.Embed(
            description = f"{member.mention} left the server\nJoined {joined} ago", 
            color = 0xFF7FFF
            )
        embed.set_thumbnail(url = member.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(
            icon_url = member.avatar_url,
            name = f"{member} ({member.id})"
            )
        embed.set_footer(text=f"Member Count: {member.guild.member_count}")
        try:
            await channel.send(embed = embed)
        except:
            print(f"Unable to log user {member.id} leaving because I don't have permission to send messages in the provided user_join_log channel.\n__________")

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if not self.config.user_nickname_log:
            return
        if before.nick == after.nick:
            return
        member = before
        try:
            channel = discord.utils.get(member.guild.text_channels, id = self.config.user_nickname_log)
        except:
            print(f"Unable to log user {member.id} leaving because the provided user_nickname_log channel ID was invalid.\n__________")
        if before.nick == None:
            before.nick = "[No nickname]"
        if after.nick == None:
            after.nick = "[No nickname]"
        embed = discord.Embed(
            description = f"{before.mention} updated their nickname:",
            color = 0xeb88ff
        )
        embed.add_field(
            name = "Before",
            value = before.nick
        )
        embed.add_field(
            name = "After",
            value = after.nick
        )
        embed.set_author(
            icon_url = before.avatar_url,
            name = f"{after} ({after.id})"
        )
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed = embed)


def setup(bot):
    bot.add_cog(Logging(bot))
