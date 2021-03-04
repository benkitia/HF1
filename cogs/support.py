import discord

from discord.ext import commands


class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.functions = bot.functions

        @commands.command(description="Describes the two main flaws with the iPhone 7", aliases=['iphone 7', 'iPhone7', 'iPhone 7'])
        async def iphone7(ctx):
            await ctx.send("The iPhone 7 and iPhone 7+ are some of the most problematic iPhones. Here are the two main "
                     "issues: \n \n **1) No Service Issue**, which you can read about here: "
                     "https://support.apple.com/iphone-7-no-service. This recall **has expired**, forcing thousands "
                     "of users to pay for their own repair. \n \n **2) Audio IC Issue**, which was caused by the poor "
                     "design of the iPhone 7. This defect causes the Audio IC to become separated from the board, "
                     "which will result in a loss of audio. Every speaker and microphone on the phone will stop "
                     "working, and so will any wired headphones. When this happens, you can either get it repaired or "
                     "use wireless headphones. It is worth noting that, even if you get it repaired, **this defect "
                     "will happen again**. There is no permanent solution.")

        @commands.command(description="Asks people to ask their question rather than saying 'Can someone help me?' or similar")
        async def ask(ctx):
            await ctx.send("Please just ask your question. Don't ask to ask. Don't say 'I have a problem'. Please be "
                     "specific so that the people who have a solution can and will provide it. "
                     "https://dontasktoask.com/")

        @commands.command(description="Provides a guide for cleaning AirPods (not AirPods Pro or AirPods Max)", aliases=["airpods cleaning"])
        async def airpodscleaning(ctx):
            await ctx.send("The best way to clean your AirPods is with an old fine bristle toothbrush, a can of compressed "
                     "air, hydrogen peroxide, isopropyl alcohol, and a q tip. Here is what you do: \n \n - Soak the q "
                     "tip in a bit of hydrogen peroxide \n - Rub it on the large opening that faces your ear and "
                     "smaller one as well if it's clogged. Be careful not to put too much because you don't want to "
                     "water damage your AirPod; you only to only get it on the mesh. \n - Use the toothbrush with a "
                     "bit of isopropyl alcohol to agitate the wax, again being careful to not hurt the AirPod \n - "
                     "Blow compressed air from the opposite hole (since the holes are connected) so the wax gets "
                     "forced out of the AirPod. \n \n Repeat as many times as needed. The hydrogen peroxide works to "
                     "actually break down the earwax and the isopropyl alcohol works best for disinfecting it. \n \n "
                     "To gauge how clogged your AirPod is, shine a phone's flashlight in the opposite hole and check "
                     "the color. If it's brownish/orange or you can see visible patches, there is buildup there. A "
                     "clean AirPod will only reflect white light.")

        @commands.command(desciption="Links to a list of all MFI certified accessories")
        async def mfi(ctx):
            await ctx.send("https://mfi.apple.com/account/accessory-search")

def setup(bot):
    bot.add_cog(Support(bot))