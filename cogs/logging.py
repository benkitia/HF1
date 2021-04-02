import datetime
import discord
from discord.ext import commands
import os
import random
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
        # checks if user is muted
        active_mute = await self.db.infractions.find_one({"target": str(member.id), "guild": str(member.guild.id), "infraction_type": "mute", "expired": False})
        if active_mute:
            try:
                mute_role = discord.utils.get(member.guild.roles, id = self.config.mute_role)
            except:
                print("Invalid mute role. Double check the mute role in the bot config file")        
            try:
                await member.add_roles(mute_role, reason=f"Mute evasion protection")        
            except:
                print("Make sure my role is above the mute role.")
        if not self.config.user_join_log:
            return
        try:
            channel = discord.utils.get(member.guild.text_channels, id = self.config.user_join_log)
        except:
            print(f"Unable to log user {member.id} joining because the provided user_join_log channel ID was invalid.\n__________")
        account_created = str((datetime.datetime.utcfromtimestamp(time.time()) - member.created_at))
        account_created = account_created.split(',')[0]
        if "days" in account_created.lower():
            account_created = f"{account_created} ago"
        else:
            account_created = "today :warning:"
        infraction_count = await self.db.infractions.count_documents({"target": str(member.id), "guild": str(member.guild.id), "status": "active"})
        if infraction_count > 0:
            infraction_count = f"\n{infraction_count} infraction(s) :warning:"
        else:
            infraction_count = ""
        embed = discord.Embed(
            description = f"{member.mention} joined the server\nAccount created {account_created}{infraction_count}", 
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
        if "days" in joined.lower():
            joined = f"{joined} ago"
        else:
            joined = "today"
        embed = discord.Embed(
            description = f"{member.mention} left the server\nJoined {joined}", 
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
            description = f"{before.mention}'s nickname was updated:",
            color = 0x00e3ff
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

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        if not self.config.message_delete_log:
            return
        ctx: commands.Context = await self.bot.get_context(messages[0])
        try:
            channel = discord.utils.get(ctx.guild.text_channels, id = self.config.message_delete_log)
        except:
            print(f"Unable to log deletion of message {ctx.message.id} because the provided message_delete_log channel ID was invalid.\n__________")
        log_id = str(random.randint(1000000000, 9999999999))
        log = open(f"temp/bulk_message_delete_log_{log_id}.txt","w")
        for message in messages:
            if not ctx.message.content:
                message_content = "[No Content]"
            else:
                message_content = ctx.message.content
            message_author = f"{message.author} ({message.author.id})"
            log.write(f"\n{message.id} - {message_author} at {message.created_at}: {message.content}")
        log.close()
        embed = discord.Embed(
            description = f"{len(messages)} message(s) were deleted in bulk from {messages[0].channel.mention}.\nView them in the attached file",
            color = 0xb14c00
        )
        file = discord.File(log.name)
        await channel.send(embed = embed, file = file)
        os.remove(log.name)

def setup(bot):
    bot.add_cog(Logging(bot))
