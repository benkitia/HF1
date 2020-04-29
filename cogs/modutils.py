import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://wafflebot:fkKi2m2Eg2UjjJWZHiBVuWihAi9fdHpw@waffledev.derw.xyz/?ssl=false")
db = cluster["wafflebot"]
collection = db["infractions"]

class Modutils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Returns information about a user", aliases=['profile','info'])
    async def userinfo(self, ctx, user:discord.Member):
        inf_count = collection.count_documents({"Target":user.id, "Guild":ctx.message.guild.id,"Status":"Active"})
        global_inf_count = collection.count_documents({"Target":user.id, "Status":"Active"})
        userinfoem = discord.Embed(title=f"{user}", colour=0xa558ff)
        userinfoem.add_field(name = "Name: ", value = user.name, inline = True)
        userinfoem.add_field(name = "ID: ", value = user.id, inline = True)
        userinfoem.add_field(name = "Status: ", value = user.status, inline = True)
        userinfoem.add_field(name = "Highest Role: ", value = user.top_role)
        userinfoem.add_field(name = "Joined at: ", value = user.joined_at)
        userinfoem.add_field(name = "Created at: ", value = user.created_at)
        userinfoem.add_field(name = "Infractions: ", value = inf_count)
        userinfoem.add_field(name = "Global Infractions: ", value = global_inf_count)
        specials = ""
        if user.id in self.bot.config.dev:
            specials = "Developer"
        if user.id in self.bot.owner_ids or user.id == self.bot.owner_id:
            specials = f"{specials}, Global Admin"
        if user.id in self.bot.config.support:
            specials = f"{specials}, Official Bot Support"
        if user.id in self.bot.config.tester:
            specials = f"{specials}, Beta Tester"
        userinfoem.add_field(name = "Acknowledgements:", value = specials)
        userinfoem.set_thumbnail(url=user.avatar_url)
        userinfoem.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed = userinfoem)

    @commands.command(aliases=['purge','purgeall'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        if amount>300:
            return await ctx.send("<:error:696628928458129488> You can only purge up to 300 messages at a time")
        await ctx.channel.purge(limit=amount+1)

    @commands.command(description="Pulls information about an infraction")
    @commands.has_permissions(kick_members=True)
    async def punishinfo(self, ctx, casenumber):
        try:
            case = int(casenumber)
        except:
            return await ctx.send("<:error:696628928458129488> Invalid case number: not a number")
        if len(casenumber) != 10:
            return await ctx.send("<:error:696628928458129488> Invalid case number: not 10 digits")
        result = collection.find_one({"Case Number":case})
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
        lookupembed = discord.Embed(title=f"{punishtype}: {case}", description = f"""
        **User:** {target} ({targetid})
        **Reason:** {reason}
        **Moderator:** {mod}
        **Timestamp:** {stamp}
        **Status:** {infstatus}
        """, color=0xffc0aa)
        await ctx.send(embed=lookupembed)

    @commands.command(description="Pulls user's active infractions",aliases=['infractions'])
    @commands.has_permissions(kick_members=True)
    async def search(self, ctx, target:discord.Member):
        results=collection.find({"Target":target.id, "Guild":ctx.message.guild.id,"Status":"Active"})
        inf_count = collection.count_documents({"Target":target.id, "Guild":ctx.message.guild.id,"Status":"Active"})
        searchem = discord.Embed(title=f"{target}'s Infractions",description=f'{inf_count} infractions',color=0xffc0aa)
        for result in results:
                case = result["Case Number"]
                punishtype = result["Punishment Type"]
                reason = result["Reason"]
                searchem.add_field(name=f"{case}", value=f"{punishtype} - {reason}", inline=False)
        searchem.set_footer(text=f"Requested by {ctx.message.author}")
        searchem.set_thumbnail(url=target.avatar_url)
        await ctx.send(embed=searchem)

    @commands.command(description="Pulls user's active infractions",aliases=['allinfractions'])
    @commands.has_permissions(kick_members=True)
    async def searchall(self, ctx, target:discord.Member):
        results=collection.find({"Target":target.id, "Guild":ctx.message.guild.id})
        searchem = discord.Embed(title=f"{target}'s Infractions", description='*This list includes deleted infractions, use search command to search for active infractions*',color=0xffc0aa)
        for result in results:
                case = result["Case Number"]
                punishtype = result["Punishment Type"]
                reason = result["Reason"]
                searchem.add_field(name=f"{case}", value=f"{punishtype} - {reason}", inline=False)
        searchem.set_footer(text=f"Requested by {ctx.message.author}")
        searchem.set_thumbnail(url=target.avatar_url)
        await ctx.send(embed=searchem)

    @commands.command(description="Removes an infraction from a user",aliases=['delinfraction'])
    @commands.has_permissions(kick_members=True)
    async def rmpunish(self, ctx, casenumber):
        try:
            case = int(casenumber)
        except:
            return await ctx.send("<:error:696628928458129488> Invalid case number: not a number")
        if len(casenumber) != 10:
            return await ctx.send("<:error:696628928458129488> Invalid case number: not 10 digits")
        try:
            collection.update_one({"Case Number":case},{"$set":{"Status":"Inactive"}})
        except:
            return await ctx.send("<:error:696628928458129488> Error deleting infraction")
        await ctx.send(f":ok_hand: Deleted infraction {casenumber}")

def setup(bot):
    bot.add_cog(Modutils(bot))
