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
    @commands.is_owner()
    async def set(self, ctx, setting, *, value):
        valid_settings = ['staffrole','adminrole','actionlog','messagelog','travellog','userlog','muterole','dm_on_warn','dm_on_mute','dm_on_kick','dm_on_ban','dm_on_unmute','dm_on_unban']
        if setting not in valid_settings:
            return await ctx.send(f"<:error:696628928458129488> Invalid setting. Valid settings include: `{valid_settings}``")
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
        if "log" or "imagecache" in setting:
            try:
                channel = await TextChannelConverter().convert(ctx, value)
                value = str(channel.id)
            except:
                await ctx.send("<:error:696628928458129488> Invalid channel")
        if "role" in setting:
            try:
                role = await RoleConverter().convert(ctx, value)
            except:
                return await ctx.send("<:error:696628928458129488> Invalid role")
            value = str(role.id)
        self.db.beta_guildconfigs.update_one({"_id":int(ctx.message.guild.id)},{"$set":{setting:value}})
        await ctx.send(f":ok_hand: Changed {setting} to {value}")

def setup(bot):
    bot.add_cog(GuildConfig(bot))
