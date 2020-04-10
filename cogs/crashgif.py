
from io import BytesIO
from discord.ext import commands
import discord
import hashlib

class Crashgif(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.badhashes = [
            "eb7ee72d9def4cef8dfcc1f1a8b075e2268d63bce271f679fa5f54b7e21d75fd",
            "b9c7e2d5af05217b518118de79b6d6f26441d178dd447bad5dd4c3be78787605",
            "379e084fc0c7ed12c6ae25465e19887e383c91160b3ac4753a8db7116e40dbb0"
        ]

    @commands.Cog.listener()
    async def on_message(self, msg):
        urls = set()

        for part in msg.content.split():
            if part.startswith("http"):
                urls.add(part)

        for a in msg.attachments:
            urls.add(a.proxy_url)

        for url in urls:
            buffer = BytesIO()

            async with self.bot.session.get(url) as resp:
                if resp.status != 200:
                    break

                while True:
                    chunk = await resp.content.read(10)
                    if not chunk:
                        break
                    buffer.write(chunk)

            buffer.seek(0)

            m = hashlib.sha256()
            m.update(buffer.getvalue())
            hdg = m.hexdigest()

            print(hdg)

            if hdg in self.badhashes:
                await msg.delete()

                author = msg.author
                guild = msg.guild

                for role in author.roles:
                    try:
                        await author.remove_roles(role)
                    except Exception as e:
                        print(e)

                role = guild.get_role(self.bot.config.mute_role)
                await author.add_roles(role)

                await self.sendEmbed(msg.author, msg.channel)

    async def sendEmbed(self, user, chnl):
        em = discord.Embed (
            title = "iOS Crash Gif Detected",
            description = f"{user} posted the iOS crash gif in {chnl.mention}. They've been muted, ban them with the user ID below.",
            colour = discord.Colour.red()
        )

        queue = self.bot.alert_channel

        await queue.send("@here", embed = em)
        await queue.send(f"{user.id}")

def setup(bot):
    bot.add_cog(Crashgif(bot))
