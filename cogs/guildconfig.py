import discord
from discord.ext import commands
from discord.ext.commands import RoleConverter, TextChannelConverter
from datetime import datetime, date, time
import time

class GuildConfig(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.command()
    async def set(self, ctx, setting, *, value):
        config = await self.db.guildconfigs.find_one({"_id":ctx.message.guild.id})
        if ctx.message.author.id != ctx.message.guild.owner.id:
            adminroleid = int(config["adminrole"])
            adminrole = discord.utils.get(ctx.guild.roles, id=adminroleid)
            if adminrole not in ctx.message.author.roles:
                missingperms = discord.Embed(title="Not so fast", description="You do not have permission to use this command",color=0xff0000)
                return await ctx.send(embed=missingperms)
        valid_settings = ['staffrole','adminrole','actionlog','messagelog','travellog','userlog','muterole','dm_on_warn','dm_on_mute','dm_on_kick','dm_on_ban','dm_on_unmute','dm_on_unban','auto_dehoist']
        if setting not in valid_settings:
            return await ctx.send(f"<:error:696628928458129488> Invalid setting. Valid settings include: `{valid_settings}`")
        if "dm_on_" in setting:
            if value == "on":
                value = "true"
            if value == "off":
                value = "false"
            if value == "yes":
                value = "true"
            if value == "no":
                value = "false"
            if value != "on":
                if value != "true":
                    if value != "yes":
                        if value != "off":
                            if value != "false":
                                if value != "no":
                                    return await ctx.send("<:error:696628928458129488> Invalid option, choose true or false")
        if "auto_" in setting:
            if value == "on":
                value = "true"
            if value == "off":
                value = "false"
            if value == "yes":
                value = "true"
            if value == "no":
                value = "false"
            if value != "on":
                if value != "true":
                    if value != "yes":
                        if value != "off":
                            if value != "false":
                                if value != "no":
                                    return await ctx.send("<:error:696628928458129488> Invalid option, choose true or false")
        if "log" in setting:
            try:
                channel = await TextChannelConverter().convert(ctx, value)
                value = str(channel.id)
            except:
                return await ctx.send("<:error:696628928458129488> Invalid channel")
        if "role" in setting:
            try:
                role = await RoleConverter().convert(ctx, value)
            except:
                return await ctx.send("<:error:696628928458129488> Invalid role")
            value = str(role.id)
        self.db.guildconfigs.update_one({"_id":int(ctx.message.guild.id)},{"$set":{setting:value}})
        await ctx.send(f":ok_hand: Changed {setting} to {value}")

    @commands.command(description='Returns a list of settings')
    @commands.is_owner()
    async def settings(self, ctx):
        config = await self.db.guildconfigs.find_one({"_id":ctx.message.guild.id})
        if ctx.message.author.id != ctx.message.guild.owner.id:
            adminroleid = int(config["adminrole"])
            adminrole = discord.utils.get(ctx.guild.roles, id=adminroleid)
            if adminrole not in ctx.message.author.roles:
                missingperms = discord.Embed(title="Not so fast", description="You do not have permission to use this command",color=0xff0000)
                await ctx.send(embed=missingperms)
        try:
            staffroleid = int(config["staffrole"])
            staffrole = discord.utils.get(ctx.guild.roles, id=staffroleid)
            staffrole = staffrole.mention
        except:
            staffrole = "Unset; do -set muterole"
        try:
            adminroleid = int(config["adminrole"])
            adminrole = discord.utils.get(ctx.guild.roles, id=adminroleid)
            adminrole = adminrole.mention
        except:
            adminrole = "Unset; do -set adminrole"
        try:
            muteroleid = int(config["muterole"])
            muterole = discord.utils.get(ctx.guild.roles, id=muteroleid)
            muterole = muterole.mention
        except:
            muterole = "Unset; do -set muterole"
        embed = discord.Embed(
            title = "Server Settings",
            color = 0xD99740
        )
        embed.add_field(
            name = "Roles",
            value = f"**Staff role:** {staffrole}\n**Admin role:** {adminrole}\n**Mute role:** {muterole}",
            inline = False
        )
        try:
            actionlogid = int(config["actionlog"])
            actionlog = discord.utils.get(ctx.guild.channels, id=actionlogid)
            actionlog = actionlog.mention
        except:
            actionlog = "disabled"
        try:
            messagelogid = int(config["messagelog"])
            messagelog = discord.utils.get(ctx.guild.channels, id=messagelogid)
            messagelog = messagelog.mention
        except:
            messagelog = "disabled"
        try:
            travellogid = int(config["travellog"])
            travellog = discord.utils.get(ctx.guild.channels, id=travellogid)
            travellog = travellog.mention
        except:
            travellog = "disabled"
        try:
            userlogid = int(config["userlog"])
            userlog = discord.utils.get(ctx.guild.channels, id=userlogid)
            userlog = userlog.mention
        except:
            userlog = "disabled"
        try:
            automodlogid = int(config["automodlog"])
            automodlog = discord.utils.get(ctx.guild.channels, id=automodlogid)
            automodlog = automodlog.mention
        except:
            automodlog = "disabled"
        try:
            imagecacheid = int(config["imagecache"])
            imagecache = discord.utils.get(ctx.guild.channels, id=imagecacheid)
            imagecache = imagecache.mention
        except:
            imagecache = "disabled"
        embed.add_field(
            name = "Channels",
            value = f"**Action log:** {actionlog}\n**Message log:** {messagelog}\n**Travel log:** {travellog}\n**User log:** {userlog}\n**Auto Moderation log:** {automodlog}\n**Image Cache Channel:** {imagecache}",
            inline = False
        )
        dm_on_warn = config["dm_on_warn"]
        dm_on_mute = config["dm_on_mute"]
        dm_on_kick = config["dm_on_kick"]
        dm_on_ban = config["dm_on_ban"]
        dm_on_unban = config["dm_on_unban"]
        dm_on_unmute = config["dm_on_unmute"]
        embed.add_field(
            name = "Infraction Settings",
            value = f"**DM on warn:** {dm_on_warn}\n**DM on mute:** {dm_on_mute}\n**DM on kick:** {dm_on_kick}\n**DM on ban:** {dm_on_ban}\n**DM on unmute:** {dm_on_unmute}\n**DM on unban:** {dm_on_unban}",
            inline = False
        )
        autodehoist = config["auto_dehoist"]
        embed.add_field(
            name = "Auto Moderation Settings",
            value = f"**Auto Dehoist:** {autodehoist}",
            inline = False
        )
        embed.set_author(icon_url=ctx.message.guild.icon_url, name=ctx.message.guild)
        await ctx.send(embed=embed)

        

def setup(bot):
    bot.add_cog(GuildConfig(bot))
