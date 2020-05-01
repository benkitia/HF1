import discord
from discord.ext import commands
from datetime import datetime, date, time
import time

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

    @commands.command()
    async def avatar(self, ctx, user:discord.Member=None, avi_format='png'):
        if user==None:
            user = ctx.message.author
        try:
            avi = user.avatar_url_as(format=avi_format)
            await ctx.send(avi)
        except:
            return await ctx.send("<:error:696628928458129488> Invalid format. Valid formats include ‘webp’, ‘jpeg’, ‘jpg’, ‘png’ or ‘gif’ (for animated avatars)")

def setup(bot):
    bot.add_cog(Basic(bot))
