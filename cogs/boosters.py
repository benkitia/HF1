import discord
from discord.ext import commands
from discord.utils import get

class Boosters(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.functions = bot.functions

    async def remove_all_color_roles(self, ctx, user : discord.Member, reason = None):
        red = discord.utils.get(ctx.guild.roles, id = 737709284187439154)
        orange = discord.utils.get(ctx.guild.roles, id = 737709452458852373)
        yellow = discord.utils.get(ctx.guild.roles, id = 737709652820754523)
        green = discord.utils.get(ctx.guild.roles, id = 737709682856034375)
        blue = discord.utils.get(ctx.guild.roles, id = 737709713881301012)
        purple = discord.utils.get(ctx.guild.roles, id = 760327521148600340)
        color_roles = [red, orange, yellow, green, blue, purple]
        try:
            for color_role in color_roles:
                if color_role in user.roles:
                    await user.remove_roles(color_role, reason = reason)
        except:
            await self.functions.handle_error(ctx, "Unknown error in removing color roles", "Notify waffles or try again later")

    @commands.command(description="Assigns a color for Nitro Boosters",aliases=['colors','colour','colours'])
    async def color(self, ctx, color):
        booster_role = discord.utils.get(ctx.guild.roles, id = 588162647568941074)
        if booster_role not in ctx.message.author.roles:
            return await self.functions.handle_error(ctx, "This command is for Nitro boosters only")
        accepted_colors = ['red','orange','yellow','green','blue','remove']
        color = color.lower()
        if color not in accepted_colors:
            await self.functions.handle_error(ctx, "Invalid color", "Valid colors include red, orange, yellow, green, blue, and purple. If you want to remove all color roles, use !color remove")
        if color == "remove":
            await self.remove_all_color_roles(ctx, ctx.message.author, "Manual color role removal")
            return await self.functions.confirm_action(ctx, "Any color roles assigned to you have been removed")
        if color == "red":
            color = discord.utils.get(ctx.guild.roles, id = 737709284187439154)
        elif color == "orange":
            color = discord.utils.get(ctx.guild.roles, id = 737709452458852373)
        elif color == "yellow":
            color = discord.utils.get(ctx.guild.roles, id = 737709652820754523)
        elif color == "green":
            color = discord.utils.get(ctx.guild.roles, id = 737709682856034375)
        elif color == "blue":
            color = discord.utils.get(ctx.guild.roles, id = 737709713881301012)
        elif color == "purple":
            color = discord.utils.get(ctx.guild.coles, id = 760327521148600340)
        if color in ctx.message.author.roles:
            return await self.functions.handle_error(ctx, "You already have this color role")
        await self.remove_all_color_roles(ctx, ctx.message.author)
        try:
            await ctx.message.author.add_roles(color, reason = "Color role manual assignment")
            return await self.functions.confirm_action(ctx, f"The {str(color)} role has been added")
        except:
            return await self.functions.handle_error(ctx, "Unknown error assigning color role", "Notify waffles or try again later")

    @commands.Cog.listener()
    async def on_member_update(self, before:discord.Member, after:discord.Member):
        booster_role = discord.utils.get(before.roles, id = 588162647568941074)
        if booster_role not in before.roles:
            return
        if before.roles == after.roles:
            return
        if booster_role not in after.roles:
            await self.remove_all_color_roles(before, ctx.message.author, "Automatic color role removal")

def setup(bot):
    bot.add_cog(Boosters(bot))