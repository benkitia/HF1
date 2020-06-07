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
        banlog = discord.Embed(title=f"{target} banned", description=f"""**User:** {target} ({target.id})
        **Reason:** {reason}
        **Responsible Moderator:** {ctx.message.author}
        """, color=0xff1919)
        banlog.set_footer(text=f"Case number {casenumber}")
        if target == None:
            return await ctx.send("<:error:696628928458129488> You must provide a valid user to ban")
        if target == ctx.message.author:
            return await ctx.send("<:error:696628928458129488> You cannot ban yourself")
        try:
            await ctx.guild.ban(target, reason=f"Action by {ctx.message.author} for {reason}")
            await ctx.send(f":ok_hand: Banned **{target}** for *{reason}*")
        except discord.Forbidden:
            return await ctx.send("<:error:696628928458129488> I can't ban this user, make sure my highest role is above their's and I have ban members permissions")
        if not logchannel:
            await ctx.send("<:error:696628928458129488> I couldn't log this action, no log channel found")
        else:
            try:
                await logchannel.send(embed=banlog)
            except discord.Forbidden:
                await ctx.send("<:error:696628928458129488> I can't log this action because I can't speak in the log channel")
        post = {"_id": f"{target.id}{casenumber}", "Case Number":casenumber, "Punishment Type":"Ban","Target":target.id,"Target Name":f"{target}","Mod":ctx.message.author.id,"Mod Name":f"{ctx.message.author}","Reason":f"{reason}","Timestamp":datetime.now(),"Status":"active","Guild":ctx.message.guild.id}
        await self.db.infractions.insert_one(post)
        dm = config["dm_on_ban"]
        if dm == "true":
            dmem = discord.Embed(
                title = ":hammer: Punishent Notification: Ban",
                description = f"""
                **Reason:** {reason}
                **Case ID:** {casenumber}
                """,
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
                missingperms = discord.Embed(title="Not so fast", description="You do not have permission to use this command",color=0xff0000)
                return await ctx.send(embed=missingperms)
        logchannelidstr = config["actionlog"]
        logchannelid = int(logchannelidstr)
        logchannel = discord.utils.get(ctx.guild.text_channels, id=logchannelid)
        unbanlog = discord.Embed(title=f"{target} unbanned", description=f"""**User:** {target} ({id})
        **Reason:** {reason}
        **Responsible Moderator:** {ctx.message.author}
        """, color=0x6dff88)
        if target == None:
            return await ctx.send("<:error:696628928458129488> You must provide a valid user to unban")
        if target == ctx.message.author:
            return await ctx.send("<:error:696628928458129488> You cannot unban yourself")
        try:
            await ctx.guild.unban(target, reason=f"Action by {ctx.message.author} for {reason}")
            await ctx.send(f":ok_hand: Unbanned **{target}** for *{reason}*")
        except discord.Forbidden:
            return await ctx.send("<:error:696628928458129488> I can't unban this user, make sure I have ban members permissions")
        if not logchannel:
            await ctx.send("<:error:696628928458129488> I couldn't log this action, no log channel found")
        else:
            try:
                await logchannel.send(embed=unbanlog)
            except discord.Forbidden:
                await ctx.send("<:error:696628928458129488> I can't log this action because I can't speak in the log channel")
        dm = config["dm_on_unban"]
        if dm == "true":
            dmem = discord.Embed(
                title = ":unlock: Punishent Updated: Unban",
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
        kicklog = discord.Embed(title=f"{target} kicked", description=f"""**User:** {target} ({target.id})
        **Reason:** {reason}
        **Responsible Moderator:** {ctx.message.author}
        """, color=0xff8500)
        kicklog.set_footer(text=f"Case number {casenumber}")
        if target == None:
            return await ctx.send("<:error:696628928458129488> You must provide a valid user to kick")
        if target == ctx.message.author:
            return await ctx.send("<:error:696628928458129488> You cannot kick yourself")
        try:
            await ctx.guild.kick(target, reason=f"Action by {ctx.message.author} for {reason}")
            await ctx.send(f":ok_hand: Kicked **{target}** for *{reason}*")
        except discord.Forbidden:
            return await ctx.send("<:error:696628928458129488> I can't kick this user, make sure my highest role is above their's and I have kick members permissions")
        if not logchannel:
            await ctx.send("<:error:696628928458129488> I couldn't log this action, no log channel found")
        else:
            try:
                await logchannel.send(embed=kicklog)
            except discord.Forbidden:
                await ctx.send("<:error:696628928458129488> I can't log this action because I can't speak in the log channel")
        casenumber = random.randint(1000000000, 9999999999)
        post = {"_id": f"{target.id}{casenumber}", "Case Number":casenumber, "Punishment Type":"Kick","Target":target.id,"Target Name":f"{target}","Mod":ctx.message.author.id,"Mod Name":f"{ctx.message.author}","Reason":f"{reason}","Timestamp":datetime.now(),"Status":"Active","Guild":ctx.message.guild.id}
        await self.db.infractions.insert_one(post)
        dm = config["dm_on_kick"]
        if dm == "true":
            dmem = discord.Embed(
                title = ":boot: Punishent Notification: Kick",
                description = f"""
                **Reason:** {reason}
                **Case ID:** {casenumber}
                """,
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
        mutelog = discord.Embed(title=f"{target} muted", description=f"""**User:** {target} ({target.id})
        **Reason:** {reason}
        **Responsible Moderator:** {ctx.message.author}
        """, color=0xff8500)
        mutelog.set_footer(text=f"Case number {casenumber}")
        if target == None:
            return await ctx.send("<:error:696628928458129488> You must provide a valid user to mute")
        if target == ctx.message.author:
            return await ctx.send("<:error:696628928458129488> You cannot mute yourself")
        if not muterole:
            await ctx.send("<:error:696628928458129488> No mute role found, create a role called Muted")
        else:
            try:
                await target.add_roles(muterole, reason=f"User muted by {ctx.message.author} for {reason}")
                await ctx.send(f":ok_hand: Muted **{target}** for *{reason}*")
            except discord.Forbidden:
                return await ctx.send("<:error:696628928458129488> I can't give this user the mute role, make sure my role is above the mute role")
        if not logchannel:
            await ctx.send("<:error:696628928458129488> I couldn't log this action, no log channel found")
        else:
            try:
                await logchannel.send(embed=mutelog)
            except discord.Forbidden:
                await ctx.send("<:error:696628928458129488> I couldn't log this action because I can't send messages in the log channel")
        post = {"_id": f"{target.id}{casenumber}", "Case Number":casenumber, "Punishment Type":"Mute","Target":target.id,"Target Name":f"{target}","Mod":ctx.message.author.id,"Mod Name":f"{ctx.message.author}","Reason":f"{reason}","Timestamp":datetime.now(),"Status":"Active","Guild":ctx.message.guild.id}
        await self.db.infractions.insert_one(post)
        dm = config["dm_on_mute"]
        if dm == "true":
            dmem = discord.Embed(
                title = ":mute: Punishent Notification: Mute",
                description = f"""
                **Reason:** {reason}
                **Case ID:** {casenumber}
                """,
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
        unmutelog = discord.Embed(title=f"{target} unmuted", description=f"""**User:** {target} ({target.id})
        **Reason:** {reason}
        **Responsible Moderator:** {ctx.message.author}
        """, color=0x6dff88)
        if target == None:
            return await ctx.send("<:error:696628928458129488> You must provide a valid user to unmute")
        if target == ctx.message.author:
            return await ctx.send("<:error:696628928458129488> You cannot unmute yourself")
        if not muterole:
            await ctx.send("<:error:696628928458129488> No mute role found, create a role called Muted")
        else:
            try:
                await target.remove_roles(muterole, reason=f"User unmuted by {ctx.message.author} for {reason}")
                await ctx.send(f":ok_hand: Unmuted **{target}** for *{reason}*")
            except discord.Forbidden:
                return await ctx.send("<:error:696628928458129488> I can't remove the mute role from this user, make sure my role is above the mute role")
        if not logchannel:
            await ctx.send("<:error:696628928458129488> I couldn't log this action, no log channel found")
        else:
            try:
                await logchannel.send(embed=unmutelog)
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
        warnlog = discord.Embed(title=f"{target} warned", description=f"""**User:** {target} ({target.id})
        **Reason:** {reason}
        **Responsible Moderator:** {ctx.message.author}
        """, color=0xfff25f)
        warnlog.set_footer(text=f"Case number {casenumber}")
        if target == None:
            return await ctx.send("<:error:696628928458129488> You must provide a valid user to warn")
        if target == ctx.message.author:
           return await ctx.send("<:error:696628928458129488> You cannot warn yourself")
        else:
            post = {"_id": f"{target.id}{casenumber}", "Case Number":casenumber, "Punishment Type":"Warning","Target":target.id,"Target Name":f"{target}","Mod":ctx.message.author.id,"Mod Name":f"{ctx.message.author}","Reason":f"{reason}","Timestamp":datetime.now(),"Status":"Active","Guild":ctx.message.guild.id}
            await self.db.infractions.insert_one(post)
            dm = config["dm_on_warn"]
            if dm == "true":
                dmem = discord.Embed(
                    title = ":warning: Punishent Notification: Warning",
                    description = f"""
                    **Reason:** {reason}
                    **Case ID:** {casenumber}
                    """,
                    color = 0xfff25f
                )
                dmem.set_footer(text = f"Guild ID: {ctx.message.guild.id}")
                dmem.set_author(
                    name = ctx.message.guild,
                    icon_url = ctx.message.guild.icon_url
                )
                try:
                    await target.send(embed=dmem)
                    await ctx.send(f":ok_hand: Warned {target} for **{reason}**")
                except:
                    await ctx.send(f":ok_hand: A warning has been added to **{target}** for *{reason}\n(I couldn't DM them to notify them of their warning)*")
            if dm == "false":
                await ctx.send(f":ok_hand: Warning added to **{target}** for *{reason}*")
        try:
            await logchannel.send(embed=warnlog)
        except:
            await ctx.send(":(")

def setup(bot):
    bot.add_cog(Moderation(bot))
