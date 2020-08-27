import discord
from discord.ext import commands
import random
from datetime import datetime, date, time
import time

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.command(description="Bans a user")
    @commands.guild_only()
    async def ban(self, ctx, target:discord.User=None, *, reason=None):
        config = await self.db.guildconfigs.find_one({"_id":ctx.message.guild.id})
        staffroleid = int(config["staffrole"])
        staffrole = discord.utils.get(ctx.guild.roles, id=staffroleid)
        adminroleid = int(config["adminrole"])
        adminrole = discord.utils.get(ctx.guild.roles, id=adminroleid)
        if staffrole not in ctx.message.author.roles:
            if adminrole not in ctx.message.author.roles:
                missingperms = discord.Embed(title="Not so fast", description="You do not have permission to use this command",color=0xff0000)
                return await ctx.send(embed=missingperms)
        logchannelidstr = config["actionlog"]
        logchannelid = int(logchannelidstr)
        logchannel = discord.utils.get(ctx.guild.text_channels, id=logchannelid)
        casenumber = random.randint(1000000000, 9999999999)
        log = discord.Embed(
            description=f"**{target} banned**", 
            color=0xff1919
            )
        log.add_field(
            name = "User",
            value = f"{target.mention} ({target.id})"
        )
        log.add_field(
            name = "Responsible Moderator",
            value = f"{ctx.message.author.mention} ({ctx.message.author.id})"
        )
        log.add_field(
            name = "Reason",
            value = reason
        )
        log.add_field(
            name = "Ban Duration",
            value = "Indefinite"
        )
        log.set_footer(text = casenumber)
        log.timestamp = datetime.utcnow()
        log.set_author(name = "Punishment Log", icon_url = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/237/hammer_1f528.png")
        if target == None:
            invaliduser = discord.Embed(
                description = "You must provide a valid user to ban",
                color = 0xf34141
            )
            invaliduser.set_author(name = "Error")
            return await ctx.send(embed = invaliduser)
        if target == ctx.message.author:
            silly = discord.Embed(
                description = "You cannot ban yourself",
                color = 0xf34141
            )
            silly.set_author(name = "Error")
            return await ctx.send(embed =  silly)
        try:
            await ctx.guild.ban(target, reason=f"Action by {ctx.message.author} for {reason}")
            confirmation = discord.Embed(
                description = f"Banned {target} ({target.id})",
                color = 0x5c92ff
            )
            confirmation.set_author(name = "Punishment Submitted Successfully")
            confirmation.set_footer(text =  casenumber)
            confirmation.timestamp = datetime.utcnow()
            await ctx.send(embed = confirmation)
        except discord.Forbidden:
            banforbidden = discord.Embed(
                description = "I was unable to ban this user. Make sure my highest role is above their's and I have ban members permissions",
                color = 0xf34141
            )
            banforbidden.set_author(name = "Error")
            banforbidden.timestamp = datetime.utcnow()
            return await ctx.send(embed = banforbidden)
        if not logchannel:
            pass
        else:
            try:
                await logchannel.send(embed=log)
            except discord.Forbidden:
                logforbidden = discord.Embed(
                    description = "I was unable to log this action because I can't send messages in the designated log channel",
                    color = 0xf34141
                )
                logforbidden.set_author(name = "Error")
                logforbidden.timestamp = datetime.utcnow()
                await ctx.send(embed = logforbidden)
        post = {"_id": f"{target.id}{casenumber}", "Case Number":casenumber, "Punishment Type":"Ban","Target":target.id,"Target Name":f"{target}","Mod":ctx.message.author.id,"Mod Name":f"{ctx.message.author}","Reason":f"{reason}","Timestamp":datetime.utcnow(),"Status":"active","Guild":ctx.message.guild.id}
        await self.db.infractions.insert_one(post)
        dm = config["dm_on_ban"]
        if dm == "true":
            dmem = discord.Embed(
                title = ":hammer: Punishent Notification: Ban",
                description = f"**Reason:** {reason}\n**Case ID:** {casenumber}",
                color = 0xff1919
            )
            dmem.set_footer(text = f"Guild ID: {ctx.message.guild.id}")
            dmem.set_author(
                name = ctx.message.guild,
                icon_url = ctx.message.guild.icon_url
            )
            try:
                await target.send(embed=dmem)
            except:
                return
        if dm == "false":
            return

    @commands.command(description="Removes a user's ban")
    @commands.guild_only()
    async def unban(self, ctx, id:int=None, *, reason=None):
        target = await self.bot.fetch_user(id)
        config = await self.db.guildconfigs.find_one({"_id":ctx.message.guild.id})
        staffroleid = int(config["staffrole"])
        staffrole = discord.utils.get(ctx.guild.roles, id=staffroleid)
        adminroleid = int(config["adminrole"])
        adminrole = discord.utils.get(ctx.guild.roles, id=adminroleid)
        if staffrole not in ctx.message.author.roles:
            if adminrole not in ctx.message.author.roles:
                missingperms = discord.Embed(
                    title="Not so fast",
                    description="You do not have permission to use this command",
                    color=0xff0000
                    )
                return await ctx.send(embed=missingperms)
        logchannelidstr = config["actionlog"]
        logchannelid = int(logchannelidstr)
        logchannel = discord.utils.get(ctx.guild.text_channels, id=logchannelid)
        log = discord.Embed(
            description=f"**{target} unbanned**", 
            color=0x6dff88
            )
        log.add_field(
            name = "User",
            value = f"{target.mention} ({target.id})"
        )
        log.add_field(
            name = "Responsible Moderator",
            value = f"{ctx.message.author.mention} ({ctx.message.author.id})"
        )
        log.add_field(
            name = "Reason",
            value = reason
        )
        log.timestamp = datetime.utcnow()
        log.set_author(name = "Punishment Log", icon_url = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/237/open-lock_1f513.png")
        if target == None:
            invaliduser = discord.Embed(
                description = "You must provide a valid user to unban",
                color = 0xf34141
            )
            invaliduser.set_author(name = "Error")
            return await ctx.send(embed = invaliduser)
        if target == ctx.message.author:
            return await ctx.send("<:error:696628928458129488> You cannot unban yourself")
        try:
            await ctx.guild.unban(target, reason=f"Action by {ctx.message.author} for {reason}")
            await ctx.send(f":ok_hand: Unbanned **{target}** for *{reason}*")
        except discord.Forbidden:
            unbanforbidden = discord.Embed(
                description = "I was unable to unban this user. Make sure my highest role is above their's and I have ban members permissions",
                color = 0xf34141
            )
            unbanforbidden.set_author(name = "Error")
            unbanforbidden.timestamp = datetime.utcnow()
            return await ctx.send(embed = unbanforbidden)
        if not logchannel:
            await ctx.send("<:error:696628928458129488> I couldn't log this action, no log channel found")
        else:
            try:
                pass
            except discord.Forbidden:
                logforbidden = discord.Embed(
                    description = "I was unable to log this action because I can't send messages in the designated log channel",
                    color = 0xf34141
                )
                logforbidden.set_author(name = "Error")
                logforbidden.timestamp = datetime.utcnow()
                await ctx.send(embed = logforbidden)
        dm = config["dm_on_unban"]
        if dm == "true":
            dmem = discord.Embed(
                title = ":unlock: Punishent Updated: Unban",
                description = f"**Reason:** {reason}",
                color = 0x6dff88
            )
            dmem.set_footer(text = f"Guild ID: {ctx.message.guild.id}")
            dmem.set_author(
                name = ctx.message.guild,
                icon_url = ctx.message.guild.icon_url
            )
            try:
                await target.send(embed=dmem)
            except:
                return
        if dm == "false":
            return

    @commands.command(description="Kicks a user")
    @commands.guild_only()
    async def kick(self, ctx, target:discord.User=None, *, reason=None):
        config = await self.db.guildconfigs.find_one({"_id":ctx.message.guild.id})
        staffroleid = int(config["staffrole"])
        staffrole = discord.utils.get(ctx.guild.roles, id=staffroleid)
        adminroleid = int(config["adminrole"])
        adminrole = discord.utils.get(ctx.guild.roles, id=adminroleid)
        if staffrole not in ctx.message.author.roles:
            if adminrole not in ctx.message.author.roles:
                missingperms = discord.Embed(title="Not so fast", description="You do not have permission to use this command",color=0xff0000)
                return await ctx.send(embed=missingperms)
        logchannelidstr = config["actionlog"]
        logchannelid = int(logchannelidstr)
        logchannel = discord.utils.get(ctx.guild.text_channels, id=logchannelid)
        casenumber = random.randint(1000000000, 9999999999)
        log = discord.Embed(
            description=f"**{target} kicked**", 
            color=0xff8500
            )
        log.add_field(
            name = "User",
            value = f"{target.mention} ({target.id})"
        )
        log.add_field(
            name = "Responsible Moderator",
            value = f"{ctx.message.author.mention} ({ctx.message.author.id})"
        )
        log.add_field(
            name = "Reason",
            value = reason
        )
        log.set_footer(text = casenumber)
        log.timestamp = datetime.utcnow()
        log.set_author(name = "Punishment Log", icon_url = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/237/womans-boots_1f462.png")
        if target == None:
            invaliduser = discord.Embed(
                description = "You must provide a valid user to kick",
                color = 0xf34141
            )
            invaliduser.set_author(name = "Error")
            return await ctx.send(embed = invaliduser)
        if target == ctx.message.author:
            return await ctx.send("<:error:696628928458129488> You cannot kick yourself")
        try:
            await ctx.guild.kick(target, reason=f"Action by {ctx.message.author} for {reason}")
            await ctx.send(f":ok_hand: Kicked **{target}** for *{reason}*")
        except discord.Forbidden:
            kickforbidden = discord.Embed(
                description = "I was unable to kick this user. Make sure my highest role is above their's and I have kick members permissions",
                color = 0xf34141
            )
            kickforbidden.set_author(name = "Error")
            kickforbidden.timestamp = datetime.utcnow()
            return await ctx.send(embed = kickforbidden)
        if not logchannel:
            pass
        else:
            try:
                await logchannel.send(embed=log)
            except discord.Forbidden:
                logforbidden = discord.Embed(
                    description = "I was unable to log this action because I can't send messages in the designated log channel",
                    color = 0xf34141
                )
                logforbidden.set_author(name = "Error")
                logforbidden.timestamp = datetime.utcnow()
                await ctx.send(embed = logforbidden)
        casenumber = random.randint(1000000000, 9999999999)
        post = {"_id": f"{target.id}{casenumber}", "Case Number":casenumber, "Punishment Type":"Kick","Target":target.id,"Target Name":f"{target}","Mod":ctx.message.author.id,"Mod Name":f"{ctx.message.author}","Reason":f"{reason}","Timestamp":datetime.utcnow(),"Status":"Active","Guild":ctx.message.guild.id}
        await self.db.infractions.insert_one(post)
        dm = config["dm_on_kick"]
        if dm == "true":
            dmem = discord.Embed(
                title = ":boot: Punishent Notification: Kick",
                description = f"**Reason:** {reason}\n**Case ID:** {casenumber}",
                color = 0xff8500
            )
            dmem.set_footer(text = f"Guild ID: {ctx.message.guild.id}")
            dmem.set_author(
                name = ctx.message.guild,
                icon_url = ctx.message.guild.icon_url
            )
            try:
                await target.send(embed=dmem)
            except:
                return
        if dm == "false":
            return

    @commands.command(description="Mutes a user")
    @commands.guild_only()
    async def mute(self, ctx, target:discord.Member=None, *, reason=None):
        config = await self.db.guildconfigs.find_one({"_id":ctx.message.guild.id})
        staffroleid = int(config["staffrole"])
        staffrole = discord.utils.get(ctx.guild.roles, id=staffroleid)
        adminroleid = int(config["adminrole"])
        adminrole = discord.utils.get(ctx.guild.roles, id=adminroleid)
        if staffrole not in ctx.message.author.roles:
            if adminrole not in ctx.message.author.roles:
                missingperms = discord.Embed(title="Not so fast", description="You do not have permission to use this command",color=0xff0000)
                return await ctx.send(embed=missingperms)
        logchannelidstr = config["actionlog"]
        logchannelid = int(logchannelidstr)
        logchannel = discord.utils.get(ctx.guild.text_channels, id=logchannelid)
        muteroleidstr = config["muterole"]
        muteroleid = int(muteroleidstr)
        muterole = discord.utils.get(ctx.guild.roles, id=muteroleid)
        casenumber = random.randint(1000000000, 9999999999)
        log = discord.Embed(
            description=f"**{target} muted**", 
            color=0xff8500
            )
        log.add_field(
            name = "User",
            value = f"{target.mention} ({target.id})"
        )
        log.add_field(
            name = "Responsible Moderator",
            value = f"{ctx.message.author.mention} ({ctx.message.author.id})"
        )
        log.add_field(
            name = "Reason",
            value = reason
        )
        log.add_field(
            name = "Mute Duration",
            value = "Indefinite"
        )
        log.set_footer(text = casenumber)
        log.timestamp = datetime.utcnow()
        log.set_author(name = "Punishment Log", icon_url = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/237/speaker-with-cancellation-stroke_1f507.png")
        if target == None:
            invaliduser = discord.Embed(
                description = "You must provide a valid user to mute",
                color = 0xf34141
            )
            invaliduser.set_author(name = "Error")
            return await ctx.send(embed = invaliduser)
        if target == ctx.message.author:
            return await ctx.send("<:error:696628928458129488> You cannot mute yourself")
        if not muterole:
            await ctx.send("<:error:696628928458129488> No mute role found, create a role called Muted")
        else:
            try:
                await target.add_roles(muterole, reason=f"User muted by {ctx.message.author} for {reason}")
                await ctx.send(f":ok_hand: Muted **{target}** for *{reason}*")
            except discord.Forbidden:
                muteforbidden = discord.Embed(
                    description = "I was unable to mute this user. Make sure my highest role is above the mute role and I have manage roles permissions",
                    color = 0xf34141
                )
                muteforbidden.set_author(name = "Error")
                muteforbidden.timestamp = datetime.utcnow()
                return await ctx.send(embed = muteforbidden)
        if not logchannel:
            await ctx.send("<:error:696628928458129488> I couldn't log this action, no log channel found")
        else:
            try:
                await logchannel.send(embed=log)
            except discord.Forbidden:
                logforbidden = discord.Embed(
                    description = "I was unable to log this action because I can't send messages in the designated log channel",
                    color = 0xf34141
                )
                logforbidden.set_author(name = "Error")
                logforbidden.timestamp = datetime.utcnow()
                await ctx.send(embed = logforbidden)
        post = {"_id": f"{target.id}{casenumber}", "Case Number":casenumber, "Punishment Type":"Mute","Target":target.id,"Target Name":f"{target}","Mod":ctx.message.author.id,"Mod Name":f"{ctx.message.author}","Reason":f"{reason}","Timestamp":datetime.utcnow(),"Status":"Active","Guild":ctx.message.guild.id}
        await self.db.infractions.insert_one(post)
        dm = config["dm_on_mute"]
        if dm == "true":
            dmem = discord.Embed(
                title = ":mute: Punishent Notification: Mute",
                description = f"**Reason:** {reason}\n**Case ID:** {casenumber}",
                color = 0xff8500
            )
            dmem.set_footer(text = f"Guild ID: {ctx.message.guild.id}")
            dmem.set_author(
                name = ctx.message.guild,
                icon_url = ctx.message.guild.icon_url
            )
            try:
                await target.send(embed=dmem)
            except:
                return
        if dm == "false":
            return

    @commands.command(description="Removes a user's mute")
    @commands.guild_only()
    async def unmute(self, ctx, target:discord.Member=None, *, reason=None):
        config = await self.db.guildconfigs.find_one({"_id":ctx.message.guild.id})
        staffroleid = int(config["staffrole"])
        staffrole = discord.utils.get(ctx.guild.roles, id=staffroleid)
        adminroleid = int(config["adminrole"])
        adminrole = discord.utils.get(ctx.guild.roles, id=adminroleid)
        if staffrole not in ctx.message.author.roles:
            if adminrole not in ctx.message.author.roles:
                missingperms = discord.Embed(title="Not so fast", description="You do not have permission to use this command",color=0xff0000)
                return await ctx.send(embed=missingperms)
        logchannelidstr = config["actionlog"]
        logchannelid = int(logchannelidstr)
        logchannel = discord.utils.get(ctx.guild.text_channels, id=logchannelid)
        muteroleidstr = config["muterole"]
        muteroleid = int(muteroleidstr)
        muterole = discord.utils.get(ctx.guild.roles, id=muteroleid)
        log = discord.Embed(
            description=f"**{target} unmuted**", 
            color=0x6dff88
            )
        log.add_field(
            name = "User",
            value = f"{target.mention} ({target.id})"
        )
        log.add_field(
            name = "Responsible Moderator",
            value = f"{ctx.message.author.mention} ({ctx.message.author.id})"
        )
        log.add_field(
            name = "Reason",
            value = reason
        )
        log.timestamp = datetime.utcnow()
        log.set_author(name = "Punishment Log", icon_url = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/237/speaker-with-three-sound-waves_1f50a.png")
        if target == None:
            invaliduser = discord.Embed(
                description = "You must provide a valid user to unmute",
                color = 0xf34141
            )
            invaliduser.set_author(name = "Error")
            return await ctx.send(embed = invaliduser)
        if target == ctx.message.author:
            return await ctx.send("<:error:696628928458129488> You cannot unmute yourself")
        if not muterole:
            await ctx.send("<:error:696628928458129488> No mute role found, create a role called Muted")
        else:
            try:
                await target.remove_roles(muterole, reason=f"User unmuted by {ctx.message.author} for {reason}")
                await ctx.send(f":ok_hand: Unmuted **{target}** for *{reason}*")
            except discord.Forbidden:
                banforbidden = discord.Embed(
                    description = "I was unable to unmute this user. Make sure my highest role is above the mute role and I have manage roles permissions",
                    color = 0xf34141
                )
                banforbidden.set_author(name = "Error")
                banforbidden.timestamp = datetime.utcnow()
                return await ctx.send(embed = banforbidden)
        if not logchannel:
            await ctx.send("<:error:696628928458129488> I couldn't log this action, no log channel found")
        else:
            try:
                await logchannel.send(embed=log)
            except discord.Forbidden:
                await ctx.send("<:error:696628928458129488> I couldn't log this action because I can't send messages in the log channel")
        dm = config["dm_on_unmute"]
        if dm == "true":
            dmem = discord.Embed(
                title = ":loud_sound: Punishent Updated: Unmute",
                description = f"""
                **Reason:** {reason}
                """,
                color = 0x6dff88
            )
            dmem.set_footer(text = f"Guild ID: {ctx.message.guild.id}")
            dmem.set_author(
                name = ctx.message.guild,
                icon_url = ctx.message.guild.icon_url
            )
            try:
                await target.send(embed=dmem)
            except:
                return
        if dm == "false":
            return

    @commands.command(description="Issues a user a warning")
    @commands.guild_only()
    async def warn(self, ctx, target:discord.Member=None, *, reason=None):
        config = await self.db.guildconfigs.find_one({"_id":ctx.message.guild.id})
        staffroleid = int(config["staffrole"])
        staffrole = discord.utils.get(ctx.guild.roles, id=staffroleid)
        adminroleid = int(config["adminrole"])
        adminrole = discord.utils.get(ctx.guild.roles, id=adminroleid)
        if staffrole not in ctx.message.author.roles:
            if adminrole not in ctx.message.author.roles:
                missingperms = discord.Embed(title="Not so fast", description="You do not have permission to use this command",color=0xff0000)
                return await ctx.send(embed=missingperms)
        logchannelidstr = config["actionlog"]
        logchannelid = int(logchannelidstr)
        logchannel = discord.utils.get(ctx.guild.text_channels, id=logchannelid)
        casenumber = random.randint(1000000000, 9999999999)
        log = discord.Embed(
            description=f"**{target} warned**", 
            color=0xfff25f
            )
        log.add_field(
            name = "User",
            value = f"{target.mention} ({target.id})"
        )
        log.add_field(
            name = "Responsible Moderator",
            value = f"{ctx.message.author.mention} ({ctx.message.author.id})"
        )
        log.add_field(
            name = "Reason",
            value = reason
        )
        log.set_footer(text = casenumber)
        log.timestamp = datetime.utcnow()
        log.set_author(name = "Punishment Log", icon_url = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/apple/155/warning-sign_26a0.png")
        if target == None:
            invaliduser = discord.Embed(
                description = "You must provide a valid user to warn",
                color = 0xf34141
            )
            invaliduser.set_author(name = "Error")
            return await ctx.send(embed = invaliduser)
        if target == ctx.message.author:
           return await ctx.send("<:error:696628928458129488> You cannot warn yourself")
        else:
            post = {"_id": f"{target.id}{casenumber}", "Case Number":casenumber, "Punishment Type":"Warning","Target":target.id,"Target Name":f"{target}","Mod":ctx.message.author.id,"Mod Name":f"{ctx.message.author}","Reason":f"{reason}","Timestamp":datetime.utcnow(),"Status":"Active","Guild":ctx.message.guild.id}
            await self.db.infractions.insert_one(post)
            dm = config["dm_on_warn"]
            if dm == "true":
                dmem = discord.Embed(
                    title = "Punishment Notification",
                    description = f"You have been warned in *{ctx.message.guild}*.\nReason: {reason}\nPunishment ID: {casenumber}",
                    color = 0xfff25f
                )
                dmem.set_footer(text = f"Guild ID: {ctx.message.guild.id}")
                dmem.set_author(
                    name = ctx.message.guild,
                    icon_url = ctx.message.guild.icon_url
                )
                dmem.set_thumbnail(url = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/apple/155/warning-sign_26a0.png")
                try:
                    await target.send(embed=dmem)
                    confirmation = discord.Embed(
                        description = f"{target} ({target.id}) has been warned\nReason: {reason}",
                        color = 0x5c92ff
                    )
                    confirmation.set_author(name = "Punishment Submitted Successfully")
                    confirmation.set_footer(text = casenumber)
                    await ctx.send(embed = confirmation)
                except:
                    confirmation = discord.Embed(
                        description = f"A warning has been added to {target} ({target.id})\nReason: {reason}\nI wasn't able to DM them to notify them of their warning",
                        color = 0x5c92ff
                    )
                    confirmation.set_author(name = "Punishment Submitted Successfully")
                    confirmation.set_footer(text = casenumber)
                    await ctx.send(embed = confirmation)
            if dm == "false":
                confirmation = discord.Embed(
                    description = f"{target} ({target.id}) has been warned\nReason: {reason}",
                    color = 0x5c92ff
                )
                confirmation.set_author(name = "Punishment Submitted Successfully")
                confirmation.set_footer(text = casenumber)
                await ctx.send(embed = confirmation)
        try:
            await logchannel.send(embed=log)
        except:
            await ctx.send(":(")

def setup(bot):
    bot.add_cog(Moderation(bot))
