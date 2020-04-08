import discord
from discord.ext import commands
from config import config_action_log_channel, config_mute_role

class Moderation(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(description="Bans a user")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, target:discord.User=None, reason=None):
        logchannel = discord.utils.get(ctx.guild.text_channels, name="mod-log")
        banlog = discord.Embed(title=f"{target} banned", description=f"""**User:** {target} ({target.id})
        **Reason:** {reason}
        **Responsible Moderator:** {ctx.message.author}
        """, color=0xff1919)
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

    @commands.command(description="Removes a user's ban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id:int=None, reason=None):
        target = await self.bot.fetch_user(id)
        logchannel = discord.utils.get(ctx.guild.text_channels, name="mod-log")
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


    @commands.command(description="Kicks a user")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, target:discord.User=None, reason=None):
        logchannel = discord.utils.get(ctx.guild.text_channels, name="mod-log")
        kicklog = discord.Embed(title=f"{target} kicked", description=f"""**User:** {target} ({target.id})
        **Reason:** {reason}
        **Responsible Moderator:** {ctx.message.author}
        """, color=0xff8500)
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

    @commands.command(description="Mutes a user")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, target:discord.Member=None, reason=None):
        muterole = discord.utils.get(ctx.guild.roles, name="Muted")
        logchannel = discord.utils.get(ctx.guild.text_channels, name="mod-log")
        mutelog = discord.Embed(title=f"{target} muted", description=f"""**User:** {target} ({target.id})
        **Reason:** {reason}
        **Responsible Moderator:** {ctx.message.author}
        """, color=0xff8500)
        if target == None:
            return await ctx.send("<:error:696628928458129488> You must provide a valid user to mute")
        if target == ctx.message.author:
            return await ctx.send("<:error:696628928458129488> You cannot mute yourself")
        if not muterole:
            await ctx.send("<:error:696628928458129488> No mute role found, create a role called Muted")
        else:
            try:
                await target.add_roles(muterole, reason=f"User muted by {ctx.message.author} for {reason}")
                await target.mute(reason=f"User muted by {ctx.message.author} for {reason}")
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

    @commands.command(description="Removes a user's mute")
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, target:discord.Member=None, reason=None):
        muterole = discord.utils.get(ctx.guild.roles, name="Muted")
        logchannel = discord.utils.get(ctx.guild.text_channels, name="mod-log")
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

    @commands.command(description="Issues a user a warning")
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, target:discord.Member=None, reason=None):
        logchannel = discord.utils.get(ctx.guild.text_channels, name="mod-log")
        warnlog = discord.Embed(title=f"{target} warned", description=f"""**User:** {target} ({target.id})
        **Reason:** {reason}
        **Responsible Moderator:** {ctx.message.author}
        """, color=0xfff25f)
        if target == None:
            return await ctx.send("<:error:696628928458129488> You must provide a valid user to warn")
        if target == ctx.message.author:
           return await ctx.send("<:error:696628928458129488> You cannot warn yourself")
        else:
            try:
                await target.send(f":warning: You've been warned for **{reason}** in **{ctx.message.guild}**")
                await ctx.send(f":ok_hand: Warned **{target}** for *{reason}*")
            except:
                return await ctx.send(f":ok_hand: A warning has been added to **{target}** for *{reason}\n(I couldn't DM them to notify them of their warning)*") 
        if not logchannel:
            await ctx.send("<:error:696628928458129488> I couldn't log this action, no log channel found")
        else:
            try:
                await logchannel.send(embed=warnlog)
            except discord.Forbidden:
                await ctx.send("<:error:696628928458129488> I couldn't log this action because I can't send messages in the log channel")


        

def setup(bot):
    bot.add_cog(Moderation(bot))