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
            await ctx.send(":x: You must provide a valid user to ban")
        if target == ctx.message.author:
            await ctx.send(":x: You cannot ban yourself")
        try:
            await ctx.guild.ban(target, reason=f"Action by {ctx.message.author} for {reason}")
            await ctx.send(f":ok_hand: Banned **{target}** for *{reason}*")
        except discord.Forbidden:
            await ctx.send(":x: I can't ban this user, make sure my highest role is above their's and I have ban members permissions")
        if not logchannel:
            await ctx.send(":x: I couldn't log this action, create a channel called mod-log")
        else:
            try:
                await logchannel.send(embed=banlog)
            except discord.Forbidden:
                await ctx.send(":x: I can't log this action because I can't speak in the log channel")

    @commands.command(description="Removes a user's ban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id:int=None, reason=None):
        target = await self.bot.fetch_user(id)
        if target == None:
            await ctx.send(":x: You must provide a valid user to unban")
        if target == ctx.message.author:
            await ctx.send(":x: You cannot unban yourself")
        await ctx.guild.unban(target, reason=f"Action by {ctx.message.author} for {reason}")
        await ctx.send(f":ok_hand: Unbanned **{target}** for *{reason}*")
        unbanlog = discord.Embed(title=f"{target} unbanned", description=f"""**User:** {target} ({id})
        **Reason:** {reason}
        **Responsible Moderator:** {ctx.message.author}
        """, color=0x6dff88)
        logchannel = self.bot.get_channel(config_action_log_channel)
        await logchannel.send(embed=unbanlog)

    @commands.command(description="Kicks a user")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, target:discord.User=None, reason=None):
        if target ==  None:
            await ctx.send(":x: You must be provide a balid user to kick")
        if target == ctx.message.author:
            await ctx.send(":x: You cannot kick yourself")
        await ctx.guild.kick(target, reason=f"Action by {ctx.message.author} for {reason}")
        await ctx.send(f":ok_hand: Kicked **{target}** for *{reason}*")
        kicklog = discord.Embed(title=f"{target} kicked", description=f"""**User:** {target} ({target.id})
        **Reason:** {reason}
        **Responsible Moderator:** {ctx.message.author}
        """, color=0xff1919)
        logchannel = self.bot.get_channel(config_action_log_channel)
        await logchannel.send(embed=kicklog)

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
            await ctx.send(":x: You must provide a valid user to mute")
        if target == ctx.message.author:
            await ctx.send(":x: You cannot mute yourself")
        if not muterole:
            await ctx.send(":x: No mute role found, create a role called Muted")
        else:
            try:
                await target.add_roles(muterole, reason=f"User muted by {ctx.message.author} for {reason}")
                await ctx.send(f":ok_hand: Muted **{target}** for *{reason}*")
            except discord.Forbidden:
                return await ctx.send(":x: I can't give this user the mute role, make sure my role is above the mute role") 
        if not logchannel:
            await ctx.send(":x: I couldn't log this action, create a channel called mod-log")
        else:
            try:
                await logchannel.send(embed=mutelog)
            except discord.Forbidden:
                return await ctx.send(":x: I couldn't log this action because I can't send messages in the log channel")

        

def setup(bot):
    bot.add_cog(Moderation(bot))