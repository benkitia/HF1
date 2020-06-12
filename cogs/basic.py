import discord
from discord.ext import commands
from datetime import datetime, date, time
import time

class Basic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.command(description="Returns bot response time")
    async def ping(self, ctx):
        t1 = time.perf_counter()
        async with ctx.typing():
            pass
        t2 = time.perf_counter()
        await ctx.send(":ping_pong: Pong! It took {}ms".format(round((t2-t1)*1000)))

    @commands.command(description="Returns bot information",aliases=['invite','support'])
    async def botinfo(self, ctx):
        botinfoem = discord.Embed(title="Bot Information",description=f"""
        Wafflebot is a private moderation and utility bot by Waffle Development written in [discord.py](https://github.com/Rapptz/discord.py).

        Wafflebot is currently in the alpha stage. If you'd like to add it to your server, join the support server.

        For general support with commands and bot functions join the Waffle Development Discord server: https://discord.gg/zrBqN2v

        For support with the bot's configuration or to report any bugs or add the bot to your own server join the server above or email support@waffledev.xyz
        """, color=0x5c92ff)
        botinfoem.add_field(name = "Docs:", value = "Coming soon", inline = False)
        botinfoem.add_field(name = "Support server:", value = "https://discord.gg/zrBqN2v", inline = False)
        botinfoem.add_field(name = "Config support and inquiry email:", value = "support@waffledev.xyz", inline = False)
        botinfoem.add_field(name = "Credits:", value = """
        waffles#4918 - Main code
        derw#0387 - Help with development
        https://codeclimate.com/github/tekulvw/Squid-Plugins/admin/admin.py/source
        https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/admin.py#L137
        https://github.com/AEnterprise/GearBoat
        https://github.com/notderw/penelope
        """, inline = False)
        await ctx.send(embed=botinfoem)

    @commands.command(description="Returns a user's avatar in one of many formats",aliases=['avi'])
    async def avatar(self, ctx, user:discord.Member=None, avi_format='png'):
        if user==None:
            user = ctx.message.author
        try:
            avi = user.avatar_url_as(format=avi_format)
            await ctx.send(avi)
        except:
            return await ctx.send("<:error:696628928458129488> Invalid format. Valid formats include ‘webp’, ‘jpeg’, ‘jpg’, ‘png’ or ‘gif’ (for animated avatars)")

    @commands.command(description="Returns information about a server",aliases=['server'])
    async def serverinfo(self, ctx, guildid=None):
        if guildid==None:
            guildid = ctx.message.guild.id
        guildid = int(guildid)
        guild = self.bot.get_guild(guildid)
        guild = ctx.guild
        guild = self.bot.get_guild(guildid)
        server_inf_count = await self.db.infractions.count_documents({"Guild":guild.id})
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

    @commands.command(description="Returns some bot statistics")
    async def stats(self, ctx):
        embed=discord.Embed(title="Bot Statistics")
        embed.add_field(name="Guild Count",value=len(list(self.bot.guilds)))
        embed.add_field(name="Total Members",value=len(set(self.bot.get_all_members())))
        await ctx.send(embed=embed)

    @commands.command(description="Sends a request for any data the bot has related to you or your guild. Use this command sparingly")
    async def requestdata(self, ctx, purpose):
        if purpose != "self":
            if purpose != "server":
                return await ctx.send("Choose self or server")
        if purpose == "server":
            if ctx.message.author.id != ctx.message.guild.owner.id:
                return await ctx.send("You must be the server owner to request server data")
            serverrequest = discord.Embed(
                title = "Guild Data Request",
                description = f"Guild ID: {ctx.message.guild.id}\nOwner ID: {ctx.message.guild.owner.id}"
            )
            channel = self.bot.get_channel(720787306122051726)
            await channel.send(embed=serverrequest)
            await ctx.send(":ok_hand: Data request sent. You must be in this server in order to receive the data package: https://bit.ly/waffles-bots\nIf you don't receive an update within 72 hours, email privacy@bensonkitia.me\nWe care about your data and privacy, more info here http://privacy.bensonkitia.me")

def setup(bot):
    bot.add_cog(Basic(bot))
