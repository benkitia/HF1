import discord
from discord.ext import commands

class Modutils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Returns information about a user", aliases=['profile','info','lookup'])
    async def userinfo(self, ctx, user:discord.Member):
        userinfoem = discord.Embed(title=f"{user}", colour=0xa558ff)
        userinfoem.add_field(name = "Name: ", value = user.name, inline = True)
        userinfoem.add_field(name = "ID: ", value = user.id, inline = True)
        userinfoem.add_field(name = "Status: ", value = user.status, inline = True)
        userinfoem.add_field(name = "Highest Role: ", value = user.top_role)
        userinfoem.add_field(name = "Joined at: ", value = user.joined_at)
        userinfoem.add_field(name = "Created at: ", value = user.created_at)
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
    async def clear(self, ctx, amount=10):
        await ctx.channel.purge(limit=amount+1)

def setup(bot):
    bot.add_cog(Modutils(bot))
