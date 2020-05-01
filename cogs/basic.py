import discord
from discord.ext import commands
from datetime import datetime, date, time
import time
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://wafflebot:fkKi2m2Eg2UjjJWZHiBVuWihAi9fdHpw@waffledev.derw.xyz/?ssl=false")
db = cluster["wafflebot"]
collection = db["infractions"]

class Basic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Returns bot response time")
    async def ping(self, ctx):
        t1 = time.perf_counter()
        async with ctx.typing():
            pass
        t2 = time.perf_counter()
        await ctx.send(":ping_pong: Pong! It took {}ms".format(round((t2-t1)*1000)))

    @commands.command(description="Returns bot information")
    async def botinfo(self, ctx):
        botinfoem = discord.Embed(title="Bot Information",description=f"""
        {self.bot.user.name} is based on Wafflebot, a moderation and utility bot by Waffle Development written in [discord.py](https://github.com/Rapptz/discord.py)

        For general support with commands and bot functions join the Waffle Development Discord server: https://discord.gg/zrBqN2v

        For support with the bot's configuration or to report any bugs or add the bot to your own server join the server above or email support@waffledev.xyz
        """, color=0x5c92ff)
        botinfoem.add_field(name = "Docs:", value = "https://waffledev.xyz/wafflebot", inline = False)
        botinfoem.add_field(name = "Support server:", value = "https://discord.gg/zrBqN2v", inline = False)
        botinfoem.add_field(name = "Config support and inquiry email:", value = "support@waffledev.xyz", inline = False)
        botinfoem.add_field(name = "Credits:", value = """
        waffles#4918 - Main code
        derw#0387 - Database and infractions
        Moo#8008 - Database and infractions
        Blue#9588 - Support with development
        https://codeclimate.com/github/tekulvw/Squid-Plugins/admin/admin.py/source
        https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/admin.py#L137
        """, inline = False)
        await ctx.send(embed=botinfoem)

    @commands.command(description="Returns a user's avatar in one of many formats")
    async def avatar(self, ctx, user:discord.Member=None, avi_format='png'):
        if user==None:
            user = ctx.message.author
        try:
            avi = user.avatar_url_as(format=avi_format)
            await ctx.send(avi)
        except:
            return await ctx.send("<:error:696628928458129488> Invalid format. Valid formats include ‘webp’, ‘jpeg’, ‘jpg’, ‘png’ or ‘gif’ (for animated avatars)")

    @commands.command(description="Returns information about a server")
    async def serverinfo(self, ctx):
        guild = ctx.guild
        server_inf_count = collection.count_documents({"Guild":guild.id})
        findbots = sum(1 for member in ctx.guild.members if member.bot)
        iconurl = guild.icon_url_as(format='png')
        serverinfoem=discord.Embed(title=guild.name, color=0xFED870)
        serverinfoem.add_field(name="Server ID", value=ctx.guild.id, inline=True)
        serverinfoem.add_field(name="Owner", value=ctx.guild.owner, inline=True)
        serverinfoem.add_field(name="Members", value=ctx.guild.member_count, inline=True)
        serverinfoem.add_field(name="Bots", value=findbots, inline=True)
        serverinfoem.add_field(name="Channels", value=len(guild.channels))
        serverinfoem.add_field(name="Region", value=ctx.guild.region, inline=True)
        serverinfoem.add_field(name="Verification Level", value=guild.verification_level)
        serverinfoem.add_field(name="Server Infractions", value=server_inf_count, inline=True)
        serverinfoem.add_field(name="Created At", value=guild.created_at)
        serverinfoem.set_footer(text=f"Requested by {ctx.message.author}")
        serverinfoem.set_thumbnail(url=iconurl)
        await ctx.send(embed=serverinfoem)

def setup(bot):
    bot.add_cog(Basic(bot))
