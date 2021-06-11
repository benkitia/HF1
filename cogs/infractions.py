import discord
from discord.ext import commands
import pymongo

class Utilities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.functions = bot.functions

    @commands.command(description="Pulls information about an infraction", aliases=['inf', 'punishinfo'])
    async def infraction(self, ctx, infraction_id):
        staff = await self.functions.check_if_staff(ctx, ctx.message.author)
        if not staff:
            return
        if len(infraction_id) != 12:
            return await self.functions.handle_error(ctx, "Invalid infraction ID", "infraction IDs are 12 characters")
        infraction = await self.db.infractions.find_one({"_id": infraction_id})
        target_id = infraction["target"]
        infraction_type = infraction["infraction_type"]
        mod_id = infraction["mod"]
        reason = infraction["reason"]
        timestamp = infraction["timestamp"]
        status = infraction["status"]
        duration = infraction["duration"]
        if infraction_type in ["ban", "tempban"]:
            color = 0xff0000
        elif infraction_type in ["kick", "mute"]:
            color = 0xf34141
        elif infraction_type == "warning":
            color = 0xfff25f
        embed = discord.Embed(
            title = f"{infraction_type.capitalize()}: {infraction_id}", 
            color = color
        )
        try:
            target = await self.bot.fetch_user(int(target_id))
            if ctx.guild.get_member(target.id) is not None:
                target = f"{target.mention} ({target.id})"
            else:
                target = f"{str(target)} ({target.id})"
        except:
            target = target_id
        embed.add_field(
            name = "Target",
            value = target,
            inline = False
        )
        embed.add_field(
            name = "Reason",
            value = reason,
            inline = False
        )
        try:
            mod = await self.bot.fetch_user(int(mod_id))
            if ctx.guild.get_member(mod.id) is not None:
                mod = f"{mod.mention} ({mod.id})"
            else:
                mod = f"{str(mod)} ({mod.id})"
        except:
            mod = mod_id
        embed.add_field(
            name = "Moderator",
            value = mod,
            inline = False
        )
        if duration:
            embed.add_field(
                name = "Duration",
                value = duration,
                inline = False
            )
        embed.add_field(
            name = "Status",
            value = status.capitalize(),
            inline = False
        )
        embed.add_field(
            name = "Timestamp",
            value = timestamp,
            inline = False
        )
        await ctx.send(embed = embed)

    @commands.command(description="Pulls user's active infractions", aliases=['infs','search'])
    async def infractions(self, ctx, user_id):
        staff = await self.functions.check_if_staff(ctx, ctx.message.author)
        if not staff:
            return
        try: 
            user = await self.bot.fetch_user(int(user_id))
        except:
            await self.functions.handle_error(ctx, "Invalid user", "This command only accepts user IDs")
        infractions = self.db.infractions.find({
            "target": str(user.id),
            "status": "active"
        }).sort("timestamp", pymongo.DESCENDING)
        infraction_count = await self.db.infractions.count_documents({
            "target": str(user.id),
            "status": "active"
        })
        if infraction_count >= 25:
            warning = "Only the most recent infractions may be displayed"
        else:
            warning = ""
        embed = discord.Embed(
            title = f"{str(user)}'s Infractions", 
            description = f'{infraction_count} infractions\n{warning}',
            color = 0xffc0aa
        )
        async for infraction in infractions:
            infraction_id = infraction["_id"]
            infraction_type = infraction["infraction_type"]
            reason = infraction["reason"]
            embed.add_field(
                name = f"{infraction_id}",
                value = f"{infraction_type} - {reason}", 
                inline = False
            )
        embed.set_footer(text = f"Requested by {ctx.message.author}")
        embed.set_thumbnail(url = user.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(description = "Pulls user's active and inactive infractions", aliases=['searchall','allinfs'])
    async def allinfractions(self, ctx, user_id):
        staff = await self.functions.check_if_staff(ctx, ctx.message.author)
        if not staff:
            return
        try: 
            user = await self.bot.fetch_user(int(user_id))
        except:
            await self.functions.handle_error(ctx, "Invalid user", "This command only accepts user IDs")
        infractions = self.db.infractions.find({
            "target": str(user.id)
        }).sort("timestamp", pymongo.DESCENDING)
        infraction_count = await self.db.infractions.count_documents({
            "target": str(user.id)
        })
        if infraction_count >= 25:
            warning = "Only the most recent infractions may be displayed"
        else:
            warning = ""
        embed = discord.Embed(
            title = f"{str(user)}'s Infractions", 
            description = f'{infraction_count} infractions\n{warning}',
            color = 0xffc0aa
        )
        async for infraction in infractions:
            infraction_id = infraction["_id"]
            infraction_type = infraction["infraction_type"]
            reason = infraction["reason"]
            embed.add_field(
                name = f"{infraction_id}",
                value = f"{infraction_type} - {reason}", 
                inline = False
            )
        embed.set_footer(text = f"Requested by {ctx.message.author}")
        embed.set_thumbnail(url = user.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(description = "Sets the reason of an infraction", aliases = ['reason'])
    async def infreason(self, ctx, infraction_id, *, reason):
        staff = await self.functions.check_if_staff(ctx, ctx.message.author)
        if not staff:
            return
        if len(infraction_id) != 12:
            return await self.functions.handle_error(ctx, "Invalid infraction ID", "infraction IDs are 12 characters")
        infraction = await self.db.infractions.find_one({"_id": infraction_id})
        if not infraction:
            return await self.functions.handle_error(ctx, "Invalid infraction ID", "infraction not found")
        try:
            await self.db.infractions.update_one({"_id": infraction_id}, {"$set": {"reason": reason}})
        except:
            return await self.functions.handle_error(ctx, "Invalid infraction ID", "infraction not found")
        await self.functions.confirm_action(ctx, "Infraction reason updated")

    @commands.command(description = "Removes an infraction from a user", aliases = ['rmpunish','delinf'])
    async def delinfraction(self, ctx, infraction_id):
        staff = await self.functions.check_if_staff(ctx, ctx.message.author)
        if not staff:
            return
        if len(infraction_id) != 12:
            return await self.functions.handle_error(ctx, "Invalid infraction ID", "infraction IDs are 12 characters")
        infraction = await self.db.infractions.find_one({"_id": infraction_id})
        if not infraction:
            return await self.functions.handle_error(ctx, "Invalid infraction ID", "infraction not found")
        try:
            await self.db.infractions.update_one({"_id": infraction_id}, {"$set": {"status": "inactive"}})
        except:
            return await self.functions.handle_error(ctx, "Invalid infraction ID", "infraction not found")
        await self.functions.confirm_action(ctx, "infraction removed")

    @commands.command(description = "Deletes all of a user's infractions", aliases = ['clearinfractions','clearinfs','delallinfs'])
    async def delallinfractions(self, ctx, target: discord.User):
        staff = await self.functions.check_if_staff(ctx, ctx.message.author)
        if not staff:
            return
        await self.db.infractions.update_many({"target": target.id, "status": "active"}, {"$set": {"status": "inactive"}})
        await self.functions.confirm_action(ctx, "infractions cleared")


def setup(bot):
    bot.add_cog(Utilities(bot))
