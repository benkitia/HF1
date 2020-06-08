import discord
from discord.ext import commands

class Name(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.nick == after.nick:
            return
        config = await self.db.guildconfigs.find_one({"_id":before.guild.id})
        auto_dehoist = config["auto_dehoist"]
        if auto_dehoist == "false":
            return
        hoist_charectars = ['!','@','#','$','%','^','&','*','(',')','-','_','+','=','[',']',':',';','"',"'",'<',',','>','.','?','?','`']
        for hoist_charectar in hoist_charectars:
            if after.nick.startswith(hoist_charectar):
                await before.edit(nick="Don't hoist your nickname",reason="Auto dehoist")
                logchannelid = int(config["automodlog"])
                logchannel = self.bot.get_channel(logchannelid)
                log = discord.Embed(
                    title = "Nickname dehoisted",
                    description = f"""**Hoist charectar:** {hoist_charectar}\n**Previous nickname:** {before.nick}""",
                    color = 0xff0000
                )
                log.set_author(name = f"{before} ({before.id})", icon_url = f"{before.avatar_url}")
                await logchannel.send(embed=log)

def setup(bot):
    bot.add_cog(Name(bot))