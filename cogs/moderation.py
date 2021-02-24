import datetime
import discord
from discord.ext import commands
import random
import string
import dateparser
import time

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.db = bot.db
        self.functions = bot.functions

    async def confirm_infraction(self, ctx, verb : str, target : discord.User, notified : bool, infraction_id = None):
        embed = discord.Embed(
            description = f"{target.mention} has been {verb}",
            color = 0x43e286
        )
        embed.set_author(name = "Infraction Submitted Successfully")
        if not notified:
            notified = "Unable to notify user"
        else:
            notified = "User notified"
        if not infraction_id:
            infraction_id = ''
        embed.set_footer(text = f"{infraction_id} • {notified}")
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed = embed)
    
    async def generate_infraction_id(self):
        letters = ''.join(random.choice(string.ascii_letters) for i in range(6)).upper()
        numbers = str(random.randint(100000, 999999))
        return letters + numbers
    
    async def check_hierarchy(self, ctx, mod : discord.Member, target : discord.User):
        try:
            target = ctx.guild.get_member(target.id)
        except:
            return True
        if target not in ctx.guild.members:
            return True
        if mod.top_role <= target.top_role:
            return False
        elif mod.top_role > target.top_role:
            return True

    async def log_action(self, ctx, verb : str, color, target : discord.User, mod : discord.User, reason : str, icon_url : str, infraction_id : str = None, infraction_type : str = None, duration : str = None):
        if not self.config.moderation_log:
            return
        embed = discord.Embed(description = f"{target} {verb}", color = color)
        embed.add_field(
            name = "User",
            value = f"{target.mention} ({target.id})"
        )
        embed.add_field(
            name = "Moderator",
            value = f"{mod.mention} ({mod.id})"
        )
        embed.add_field(
            name = "Reason",
            value = reason
        )
        if duration:
            embed.add_field(
                name = "Duration",
                value = duration
            )
        embed.set_footer(text = infraction_id)
        embed.timestamp = datetime.utcnow()
        embed.set_author(name = "Infraction Log", icon_url = icon_url)
        try:
            log_channel = discord.utils.get(ctx.guild.text_channels, id=self.config.moderation_log)
        except:
            return await self.functions.handle_error(ctx, "Unable to locate log channel", "Double-check the log channel ID in my config file")
        try:
            await log_channel.send(embed = embed)
        except:
            return await self.functions.handle_error(ctx, "Unable to log action", "Double-check the log channel ID in my config file and ensure I have send messages permissions in that channel")
        if not infraction_id:
            return
        infraction = {
            "_id": str(infraction_id),
            "guild": str(ctx.message.guild.id),
            "infraction_type": infraction_type,
            "target": str(target.id),
            "mod": str(mod.id),
            "reason": reason,
            "duration": duration,
            "status": "active",
            "timestamp": datetime.utcnow()
        }
        await self.db.infractions.insert_one(infraction)

    async def notify_target(self, ctx, infraction_type : str, target : discord.User, reason : str, color : str, guild : discord.Guild, icon_url : str, duration : str = None, infraction_id : str = None):
        embed = discord.Embed(
            description = f"Infraction Notification: {infraction_type}",
            color = color
        )
        embed.add_field(
            name = "Reason",
            value = reason
        )
        embed.set_author(name = ctx.message.guild.name, icon_url = ctx.message.guild.icon_url)
        if duration:
            embed.add_field(
                name = "Duration",
                value = duration
            )
        if infraction_id:
            embed.add_field(
                name = "Infraction ID",
                value = infraction_id
            )
        embed.timestamp = datetime.utcnow()
        try:
            await target.send(embed = embed)
            return True
        except:
            return False

    @commands.command()
    @commands.guild_only()
    async def ban(self, ctx, target: discord.User = None, *, reason = None):
        staff = await self.functions.check_if_staff(ctx, ctx.message.author)
        if not staff:
            return
        if target == None:
            return await self.functions.handle_error(ctx, "Invalid target", "Try @mentioning the user, or make sure you have the right ID")
        if target == ctx.message.author:
            return await self.functions.handle_error(ctx, "You can't ban yourself")
        superior = await self.check_hierarchy(ctx, ctx.message.author, target)
        if not superior:
            return await self.functions.handle_error(ctx, "You don't have permission to ban this user", "Your highest role must be higher than theirs")
        try:
            await ctx.guild.ban(target, reason=f"Action by {ctx.message.author} for {reason}")        
        except:
            return await self.functions.handle_error(ctx, "Unable to ban this user", "Make sure my role is above theirs and I have been granted ban members permissions")
        infraction_id = await self.generate_infraction_id()
        notified = await self.notify_target(
            ctx,
            infraction_type = "Ban",
            target = target,
            reason = reason,
            color = 0xff0000,
            guild = ctx.message.guild,
            icon_url = "https://i.postimg.cc/YCPNT1Mb/hammer-1f528-4.png",
            infraction_id = infraction_id
        )
        await self.confirm_infraction(
            ctx,
            verb = "banned",
            target = target,
            notified = notified,
            infraction_id = infraction_id
        )
        await self.log_action(
            ctx,
            verb = "banned",
            color = 0xff0000,
            target = target,
            mod = ctx.message.author,
            reason = reason,
            duration = "Indefinite",
            icon_url = "https://i.postimg.cc/YCPNT1Mb/hammer-1f528-4.png",
            infraction_id = infraction_id,
            infraction_type = "ban"
        )

    @commands.command()
    @commands.guild_only()
    async def tempban(self, ctx, target: discord.User = None, duration = None, *, reason = None):
        staff = await self.functions.check_if_staff(ctx, ctx.message.author)
        if not staff:
            return
        if target == None:
            return await self.functions.handle_error(ctx, "Invalid target", "Try @mentioning the user, or make sure you have the right ID")
        if duration == None:
            return await self.functions.handle_error(ctx, "Invalid duration", "Try 1h, 1d, etc.")
        if target == ctx.message.author:
            return await self.functions.handle_error(ctx, "You can't ban yourself")
        superior = await self.check_hierarchy(ctx, ctx.message.author, target)
        if not superior:
            return await self.functions.handle_error(ctx, "You don't have permission to ban this user", "Your highest role must be higher than theirs")
        duration_pre_parse = duration
        duration = dateparser.parse(f"in {duration}")
        if type(duration) != datetime:
            return await self.functions.handle_error(ctx, "Invalid duration", "Try 1h, 1d, etc.")
        try:
            await ctx.guild.ban(target, reason=f"Action by {ctx.message.author} for {reason}")        
        except:
            return await self.functions.handle_error(ctx, "Unable to ban this user", "Make sure my role is above theirs and I have been granted ban members permissions")
        infraction_id = await self.generate_infraction_id()
        notified = await self.notify_target(
            ctx,
            infraction_type = "Temporary ban",
            target = target,
            reason = reason,
            color = 0xff0000,
            guild = ctx.message.guild,
            icon_url = "https://i.postimg.cc/YCPNT1Mb/hammer-1f528-4.png",
            duration = duration_pre_parse,
            infraction_id = infraction_id
        )
        await self.confirm_infraction(
            ctx,
            verb = "temporarily banned",
            target = target,
            notified = notified,
            infraction_id = infraction_id
        )
        await self.log_action(
            ctx,
            verb = "temporarily banned",
            color = 0xff0000,
            target = target,
            mod = ctx.message.author,
            reason = reason,
            duration = duration_pre_parse,
            icon_url = "https://i.postimg.cc/YCPNT1Mb/hammer-1f528-4.png",
            infraction_id = infraction_id,
            infraction_type = "tempban"
        )
        pause.until(duration)
        target = await self.bot.fetch_user(target.id)
        await ctx.guild.unban(target, reason = f"Temporary ban {infraction_id} expired")
        await self.log_action(
            ctx,
            verb = "automatically unbanned",
            color = 0x6dff88,
            target = target,
            mod = self.bot.user,
            reason = f"temporary ban {infraction_id} expired",
            icon_url = "https://i.postimg.cc/HLp2wpWC/open-lock-1f513.png"
        )

    @commands.command()
    @commands.guild_only()
    async def forceban(self, ctx, target_id = None, *, reason = None):
        staff = await self.functions.check_if_staff(ctx, ctx.message.author)
        if not staff:
            return
        if target_id == None:
            return await self.functions.handle_error(ctx, "Invalid target", "Try @mentioning the user, or make sure you have the right ID")
        try:
            target_id = int(target_id)
        except:
            return await self.functions.handle_error(ctx, "Invalid user ID", "Forceban accepts user IDs only")
        try:
            target = await self.bot.fetch_user(target_id)
        except:
            return await self.functions.handle_error(ctx, "Invalid user", "Make sure you have the right user ID")
        if target == ctx.message.author:
            return await self.functions.handle_error(ctx, "You can't ban yourself")
        superior = await self.check_hierarchy(ctx, ctx.message.author, target)
        if not superior:
            return await self.functions.handle_error(ctx, "You don't have permission to ban this user", "Your highest role must be higher than theirs")
        try:
            await ctx.guild.ban(target, reason=f"Action by {ctx.message.author} for {reason}")        
        except:
            return await self.functions.handle_error(ctx, "Unable to ban this user", "Make sure my role is above theirs and I have been granted ban members permissions")
        infraction_id = await self.generate_infraction_id()
        notified = await self.notify_target(
            ctx,
            infraction_type = "Ban",
            target = target,
            reason = reason,
            color = 0xff0000,
            guild = ctx.message.guild,
            icon_url = "https://i.postimg.cc/YCPNT1Mb/hammer-1f528-4.png",
            infraction_id = infraction_id
        )
        await self.confirm_infraction(
            ctx,
            verb = "banned",
            target = target,
            notified = notified,
            infraction_id = infraction_id
        )
        await self.log_action(
            ctx,
            verb = "banned",
            color = 0xff0000,
            target = target,
            mod = ctx.message.author,
            reason = reason,
            duration = "Indefinite",
            icon_url = "https://i.postimg.cc/YCPNT1Mb/hammer-1f528-4.png",
            infraction_id = infraction_id,
            infraction_type = "ban"
        )

    @commands.command()
    @commands.guild_only()
    async def unban(self, ctx, target_id = None, *, reason = None):
        staff = await self.functions.check_if_staff(ctx, ctx.message.author)
        if not staff:
            return
        try:
            target_id = int(target_id)
        except:
            return await self.functions.handle_error(ctx, "Invalid user ID", "Unban accepts user IDs only")
        try:
            target = await self.bot.fetch_user(target_id)
        except:
            return await self.functions.handle_error(ctx, "Invalid user", "Make sure you have the right user ID")
        try:
            await ctx.guild.unban(target, reason = f"Action by {ctx.message.author} for {reason}")
        except:
            return await self.functions.handle_error(ctx, "Unable to unban user", "Make sure I have ban members permissions and the user is indeed banned")
        notified = await self.notify_target(
            ctx,
            infraction_type = "Unban",
            target = target,
            reason = reason,
            color = 0x6dff88,
            guild = ctx.message.guild,
            icon_url = "https://i.postimg.cc/HLp2wpWC/open-lock-1f513.png",
        )
        await self.confirm_infraction(
            ctx,
            verb = "unbanned",
            target = target,
            notified = notified
        )
        await self.log_action(
            ctx,
            verb = "unbanned",
            color = 0x6dff88,
            target = target,
            mod = ctx.message.author,
            reason = reason,
            icon_url = "https://i.postimg.cc/HLp2wpWC/open-lock-1f513.png"
        )
    
    @commands.command()
    @commands.guild_only()
    async def kick(self, ctx, target: discord.User = None, *, reason = None):
        staff = await self.functions.check_if_staff(ctx, ctx.message.author)
        if not staff:
            return
        if target == None:
            return await self.functions.handle_error(ctx, "Invalid target", "Try @mentioning the user, or make sure you have the right ID")
        if target == ctx.message.author:
            return await self.functions.handle_error(ctx, "You can't kick yourself")
        superior = await self.check_hierarchy(ctx, ctx.message.author, target)
        if not superior:
            return await self.functions.handle_error(ctx, "You don't have permission to kick this user", "Your highest role must be higher than theirs")
        try:
            await ctx.guild.kick(target, reason=f"Action by {ctx.message.author} for {reason}")        
        except:
            return await self.functions.handle_error(ctx, "Unable to kick this user", "Make sure my role is above theirs and I have been granted kick members permissions")
        infraction_id = await self.generate_infraction_id()
        notified = await self.notify_target(
            ctx,
            infraction_type = "Kick",
            target = target,
            reason = reason,
            color = 0xf34141,
            guild = ctx.message.guild,
            icon_url = "https://i.postimg.cc/DyG0gLmq/hiking-boot-1f97e.png",
            infraction_id = infraction_id
        )
        await self.confirm_infraction(
            ctx,
            verb = "kicked",
            target = target,
            notified = notified,
            infraction_id = infraction_id
        )
        await self.log_action(
            ctx,
            verb = "kicked",
            color = 0xf34141,
            target = target,
            mod = ctx.message.author,
            reason = reason,
            icon_url = "https://i.postimg.cc/DyG0gLmq/hiking-boot-1f97e.png",
            infraction_id = infraction_id,
            infraction_type = "kick"
        )

    @commands.command()
    @commands.guild_only()
    async def mute(self, ctx, target: discord.Member = None, duration = None, *, reason = None):
        staff = await self.functions.check_if_staff(ctx, ctx.message.author)
        if not staff:
            return
        if target == None:
            return await self.functions.handle_error(ctx, "Invalid target", "Try @mentioning the user, or make sure you have the right ID")
        if duration == None:
            return await self.functions.handle_error(ctx, "Invalid duration", "Try 1h, 1d, etc.")
        if target == ctx.message.author:
            return await self.functions.handle_error(ctx, "You can't mute yourself")
        superior = await self.check_hierarchy(ctx, ctx.message.author, target)
        if not superior:
            return await self.functions.handle_error(ctx, "You don't have permission to mute this user", "Your highest role must be higher than theirs")
        duration_pre_parse = duration
        duration = dateparser.parse(f"in {duration}")
        if type(duration) != datetime:
            return await self.functions.handle_error(ctx, "Invalid duration", "Try 1h, 1d, etc.")
        if not self.config.mute_role:
            return await self.functions.handle_error(ctx, "No mute role found", "No mute role has been defined in bot config file")
        try:
            mute_role = discord.utils.get(ctx.guild.roles, id = self.config.mute_role)
        except:
            return await self.functions.handle_error(ctx, "Invalid mute role", "Double check the mute role in the bot config file")
        try:
            await target.add_roles(mute_role, reason=f"Action by {ctx.message.author} for {reason}")        
        except:
            return await self.functions.handle_error(ctx, "Unable to mute this user", "Make sure my role is above theirs and I have been granted manage roles permissions")
        infraction_id = await self.generate_infraction_id()
        notified = await self.notify_target(
            ctx,
            infraction_type = "Mute",
            target = target,
            reason = reason,
            color = 0xf34141,
            guild = ctx.message.guild,
            icon_url = "https://i.postimg.cc/Tw8fhHqF/speaker-with-cancellation-stroke-1f507.png",
            duration = duration_pre_parse,
            infraction_id = infraction_id
        )
        await self.confirm_infraction(
            ctx,
            verb = "temporarily muted",
            target = target,
            notified = notified,
            infraction_id = infraction_id
        )
        await self.log_action(
            ctx,
            verb = "muted",
            color = 0xf34141,
            target = target,
            mod = ctx.message.author,
            reason = reason,
            duration = duration_pre_parse,
            icon_url = "https://i.postimg.cc/Tw8fhHqF/speaker-with-cancellation-stroke-1f507.png",
            infraction_id = infraction_id,
            infraction_type = "mute"
        )
        while dateparser.parse("in 1s") < duration:
            await asyncio.sleep(1)
        await target.remove_roles(mute_role, reason=f"Temporary mute {infraction_id} expired")        
        await self.log_action(
            ctx,
            verb = "automatically unmuted",
            color = 0x6dff88,
            target = target,
            mod = self.bot.user,
            reason = f"temporary mute {infraction_id} expired",
            icon_url = "https://i.postimg.cc/QNyS5GWF/speaker-with-three-sound-waves-1f50a.png"
        )

    @commands.command()
    @commands.guild_only()
    async def unmute(self, ctx, target: discord.Member = None, *, reason = None):
        staff = await self.functions.check_if_staff(ctx, ctx.message.author)
        if not staff:
            return
        if target == None:
            return await self.functions.handle_error(ctx, "Invalid target", "Try @mentioning the user, or make sure you have the right ID")
        if target == ctx.message.author:
            return await self.functions.handle_error(ctx, "You can't unmute yourself")
        if not self.config.mute_role:
            return await self.functions.handle_error(ctx, "No mute role found", "No mute role has been defined in bot config file")
        try:
            mute_role = discord.utils.get(ctx.guild.roles, id = self.config.mute_role)
        except:
            return await self.functions.handle_error(ctx, "Invalid mute role", "Double check the mute role in the bot config file")
        if mute_role not in target.roles:
            return await self.functions.handle_error(ctx, "User is not muted")
        try:
            await target.remove_roles(mute_role, reason=f"Action by {ctx.message.author} for {reason}")        
        except:
            return await self.functions.handle_error(ctx, "Unable to unmute this user", "Make sure my role is above theirs and I have been granted manage roles permissions")
        notified = await self.notify_target(
            ctx,
            infraction_type = "Unmute",
            target = target,
            reason = reason,
            color = 0x6dff88,
            guild = ctx.message.guild,
            icon_url = "https://i.postimg.cc/QNyS5GWF/speaker-with-three-sound-waves-1f50a.png",
        )
        await self.confirm_infraction(
            ctx,
            verb = "unmuted",
            target = target,
            notified = notified
        )
        await self.log_action(
            ctx,
            verb = "unmuted",
            color = 0x6dff88,
            target = target,
            mod = ctx.message.author,
            reason = reason,
            icon_url = "https://i.postimg.cc/QNyS5GWF/speaker-with-three-sound-waves-1f50a.png",
        )

    @commands.command(aliases=['strike'])
    @commands.guild_only()
    async def warn(self, ctx, target: discord.User = None, *, reason = None):
        staff = await self.functions.check_if_staff(ctx, ctx.message.author)
        if not staff:
            return
        if target == None:
            return await self.functions.handle_error(ctx, "Invalid target", "Try @mentioning the user, or make sure you have the right ID")
        if target == ctx.message.author:
            return await self.functions.handle_error(ctx, "You can't kick yourself")
        superior = await self.check_hierarchy(ctx, ctx.message.author, target)
        if not superior:
            return await self.functions.handle_error(ctx, "You don't have permission to warn this user", "Your highest role must be higher than theirs")
        infraction_id = await self.generate_infraction_id()
        notified = await self.notify_target(
            ctx,
            infraction_type = "Warning",
            target = target,
            reason = reason,
            color = 0xfff25f,
            guild = ctx.message.guild,
            icon_url = "https://i.postimg.cc/hjvHg481/warning-sign-26a0.png",
            infraction_id = infraction_id
        )
        await self.confirm_infraction(
            ctx,
            verb = "warned",
            target = target,
            notified = notified,
            infraction_id = infraction_id
        )
        await self.log_action(
            ctx,
            verb = "warned",
            color = 0xfff25f,
            target = target,
            mod = ctx.message.author,
            reason = reason,
            icon_url = "https://i.postimg.cc/hjvHg481/warning-sign-26a0.png",
            infraction_id = infraction_id,
            infraction_type = "warning"
        )

def setup(bot):
    bot.add_cog(Moderation(bot))

