import discord
from discord.ext import commands


class Modutils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.command(description="Returns information about a user", aliases=['profile', 'info'])
    async def userinfo(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.message.author
        inf_count = await self.db.infractions.count_documents({"Target": user.id, "Guild": ctx.message.guild.id, "Status": "Active"})
        global_inf_count = await self.db.infractions.count_documents({"Target": user.id, "Status": "Active"})
        userinfoem = discord.Embed(title=f"{user}", colour=user.color)
        userinfoem.add_field(name="Name: ", value=user.name, inline=True)
        userinfoem.add_field(name="ID: ", value=user.id, inline=True)
        userinfoem.add_field(name="Status: ", value=user.status, inline=True)
        userinfoem.add_field(name="Highest Role: ", value=user.top_role)
        userinfoem.add_field(name="Joined at: ", value=user.joined_at)
        userinfoem.add_field(name="Created at: ", value=user.created_at)
        userinfoem.add_field(name="Infractions: ", value=inf_count)
        userinfoem.add_field(name="Global Infractions: ",
                             value=global_inf_count)
        userinfoem.set_thumbnail(url=user.avatar_url)
        userinfoem.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=userinfoem)

    @commands.command(aliases=['purge', 'purgeall'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        if amount > 300:
            return await ctx.send("<:error:696628928458129488> You can only purge up to 300 messages at a time")
        await ctx.channel.purge(limit=amount+1)

    @commands.command(description="Pulls information about an infraction", aliases=['inf', 'infraction'])
    @commands.has_permissions(kick_members=True)
    async def punishinfo(self, ctx, casenumber):
        try:
            case = int(casenumber)
        except:
            return await ctx.send("<:error:696628928458129488> Invalid case number: not a number")
        if len(casenumber) != 10:
            if len(casenumber) != 15:
                return await ctx.send("<:error:696628928458129488> Invalid case number: not 10 or 15 digits")
        result = await self.db.infractions.find_one({"Case Number": case, "Guild": ctx.message.guild.id})
        targetid = result["Target"]
        punishtype = result["Punishment Type"]
        target = result["Target Name"]
        mod = result["Mod Name"]
        reason = result["Reason"]
        stamp = result["Timestamp"]
        if result["Status"] == "Active":
            infstatus = "Active"
        if result["Status"] == "Inactive":
            infstatus = "Deleted"
        lookupembed = discord.Embed(title=f"{punishtype}: {case}", description=f"""
        **User:** {target} ({targetid})
        **Reason:** {reason}
        **Moderator:** {mod}
        **Timestamp:** {stamp}
        **Status:** {infstatus}
        """, color=0xffc0aa)
        await ctx.send(embed=lookupembed)

    @commands.command(description="Pulls user's active infractions", aliases=['infractions'])
    @commands.has_permissions(kick_members=True)
    async def search(self, ctx, target: discord.User):
        results = self.db.infractions.find(
            {"Target": target.id, "Guild": ctx.message.guild.id, "Status": "Active"})
        inf_count = await self.db.infractions.count_documents({"Target": target.id, "Guild": ctx.message.guild.id, "Status": "Active"})
        searchem = discord.Embed(
            title=f"{target}'s Infractions", description=f'{inf_count} infractions', color=0xffc0aa)
        async for result in results:
            case = result["Case Number"]
            punishtype = result["Punishment Type"]
            reason = result["Reason"]
            searchem.add_field(
                name=f"{case}", value=f"{punishtype} - {reason}", inline=False)
        searchem.set_footer(text=f"Requested by {ctx.message.author}")
        searchem.set_thumbnail(url=target.avatar_url)
        await ctx.send(embed=searchem)

    @commands.command(description="Pulls user's active infractions", aliases=['allinfractions'])
    @commands.has_permissions(kick_members=True)
    async def searchall(self, ctx, target: discord.User):
        results = self.db.infractions.find(
            {"Target": target.id, "Guild": ctx.message.guild.id})
        searchem = discord.Embed(
            title=f"{target}'s Infractions", description='*This list includes deleted infractions, use search command to search for active infractions*', color=0xffc0aa)
        async for result in results:
            case = result["Case Number"]
            punishtype = result["Punishment Type"]
            reason = result["Reason"]
            searchem.add_field(
                name=f"{case}", value=f"{punishtype} - {reason}", inline=False)
        searchem.set_footer(text=f"Requested by {ctx.message.author}")
        searchem.set_thumbnail(url=target.avatar_url)
        await ctx.send(embed=searchem)

    @commands.command(description="Removes an infraction from a user", aliases=['delinfraction'])
    @commands.has_permissions(kick_members=True)
    async def rmpunish(self, ctx, casenumber):
        try:
            case = int(casenumber)
        except:
            return await ctx.send("<:error:696628928458129488> Invalid case number: not a number")
        if len(casenumber) != 10:
            return await ctx.send("<:error:696628928458129488> Invalid case number: not 10 digits")
        try:
            await self.db.infractions.update_one({"Case Number": case}, {"$set": {"Status": "Inactive"}})
        except:
            return await ctx.send("<:error:696628928458129488> Error deleting infraction")
        await ctx.send(f":ok_hand: Deleted infraction {casenumber}")

    @commands.command(description="Deletes all of a user's punishments")
    @commands.has_permissions(kick_members=True)
    async def clearpunishments(self, ctx, target: discord.User):
        await self.db.infractions.update_many({"Target": target.id, "Guild": ctx.message.guild.id, "Status": "Active"}, {"$set": {"Status": "Inactive"}})
        await ctx.send(f":ok_hand: Deleted all infractions for {target}")

    @commands.command(description="Add or removes a role")
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, addorrm, target: discord.Member, role: discord.Role):
        if addorrm == "add":
            try:
                await target.add_roles(role)
            except discord.Forbidden:
                return await ctx.send("<:error:696628928458129488> I couldn't assign the role, make sure my highest role is above it")
            await ctx.send(f":ok_hand: Added {role.name} to {target}")
        if addorrm == "remove":
            try:
                await target.remove_roles(role)
            except discord.Forbidden:
                return await ctx.send("<:error:696628928458129488> I couldn't remove the role, make sure my highest role is above it")
            await ctx.send(f":ok_hand: Removed {role.name} from {target}")
        if addorrm != "add":
            if addorrm != "remove":
                return await ctx.send('<:error:696628928458129488> Specify add or remove')


def setup(bot):
    bot.add_cog(Modutils(bot))
