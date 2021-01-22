import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime, date, time
import time
from discord.ext.commands.cooldowns import BucketType

class Boosters(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Assigns a color for Nitro Boosters",aliases=['colors','colour','colours'])
    async def color(self, ctx, color):
        role = discord.utils.get(ctx.guild.roles, id=588162647568941074)
        if role not in ctx.message.author.roles:
            accessdenied = discord.Embed(
                description = "This command is only available for Nitro Boosters. Boost the server if you'd like to get a custom color role.\nFeel free to contact modmail for more info about Nitro Boosting and perks",
                color = 0xe74c33
            )
            accessdenied.set_author(
                name = "Not so fast!",
                icon_url = "https://hotemoji.com/images/dl/r/cross-mark-emoji-by-google.png"
            )
            return await ctx.send(embed=accessdenied)
        accepted_colors = ['red','orange','yellow','green','blue','remove']
        color = color.lower()
        if color not in accepted_colors:
            badcolor = discord.Embed(
                description = "Valid colors include: <@&737709284187439154>\n<@&737709452458852373>\n<@&737709652820754523>\n<@&737709682856034375>\n<@&737709713881301012>",
                color = 0xe74c33
            )
            badcolor.set_author(
                name = "Invalid color",
                icon_url = "https://labmuffin.com/labmuffin/wp-content/uploads/2012/06/382px-BYR_color_wheel.svg_.png"
            )
        redrole = discord.utils.get(ctx.guild.roles, id=737709284187439154)
        orangerole = discord.utils.get(ctx.guild.roles, id=737709452458852373)
        yellowrole = discord.utils.get(ctx.guild.roles, id=737709652820754523)
        greenrole = discord.utils.get(ctx.guild.roles, id=737709682856034375)
        bluerole = discord.utils.get(ctx.guild.roles, id=737709713881301012)
        colorroles = [redrole,orangerole,yellowrole,greenrole,bluerole]
        if color == "remove":
            for colorrole in colorroles:
                if colorrole in ctx.message.author.roles:
                    await ctx.message.author.remove_roles(colorrole, reason=f"Nitro colors user removal")
                    removed = discord.Embed(
                        description = "Any booster color roles assigned to you have been removed",
                        color = 0x82e070
                    )
                    removed.set_author(
                        name = "Done!",
                        icon_url = "https://labmuffin.com/labmuffin/wp-content/uploads/2012/06/382px-BYR_color_wheel.svg_.png"
                    )
                    return await ctx.send(embed=removed)
        if color == "red":
            if redrole in ctx.message.author.roles:
                rolenotfound = discord.Embed(
                    description = "You already have this role",
                    color = 0xe74c33
                )
                rolenotfound.set_author(
                    name = "This role is already assigned to you!",
                    icon_url = "https://labmuffin.com/labmuffin/wp-content/uploads/2012/06/382px-BYR_color_wheel.svg_.png"
                )
                return await ctx.send(embed=rolenotfound)
            for colorrole in colorroles:
                if colorrole in ctx.message.author.roles:
                    await ctx.message.author.remove_roles(colorrole, reason=f"Nitro colors assignment")
            try:
                await ctx.message.author.add_roles(redrole, reason=f"Nitro colors assignment")
            except:
                return await ctx.send("There's been an error. Let waffles know or try again later")
            added = discord.Embed(
                description = "The red color role has been added",
                color = 0x82e070
            )
            added.set_author(
                name = "Done!",
                icon_url = "https://labmuffin.com/labmuffin/wp-content/uploads/2012/06/382px-BYR_color_wheel.svg_.png"
            )
            return await ctx.send(embed=added)
        if color == "orange":
            if orangerole in ctx.message.author.roles:
                rolenotfound = discord.Embed(
                    description = "You already have this role",
                    color = 0xe74c33
                )
                rolenotfound.set_author(
                    name = "This role is already assigned to you!",
                    icon_url = "https://labmuffin.com/labmuffin/wp-content/uploads/2012/06/382px-BYR_color_wheel.svg_.png"
                )
                return await ctx.send(embed=rolenotfound)
            for colorrole in colorroles:
                if colorrole in ctx.message.author.roles:
                    await ctx.message.author.remove_roles(colorrole, reason=f"Nitro colors assignment")
            try:
                await ctx.message.author.add_roles(orangerole, reason=f"Nitro colors assignment")
            except:
                return await ctx.send("There's been an error. Let waffles know or try again later")
            added = discord.Embed(
                description = "The orange color role has been added",
                color = 0x82e070
            )
            added.set_author(
                name = "Done!",
                icon_url = "https://labmuffin.com/labmuffin/wp-content/uploads/2012/06/382px-BYR_color_wheel.svg_.png"
            )
            return await ctx.send(embed=added)
        if color == "yellow":
            if yellowrole in ctx.message.author.roles:
                rolenotfound = discord.Embed(
                    description = "You already have this role",
                    color = 0xe74c33
                )
                rolenotfound.set_author(
                    name = "This role is already assigned to you!",
                    icon_url = "https://labmuffin.com/labmuffin/wp-content/uploads/2012/06/382px-BYR_color_wheel.svg_.png"
                )
                return await ctx.send(embed=rolenotfound)
            for colorrole in colorroles:
                if colorrole in ctx.message.author.roles:
                    await ctx.message.author.remove_roles(colorrole, reason=f"Nitro colors assignment")
            try:
                await ctx.message.author.add_roles(yellowrole, reason=f"Nitro colors assignment")
            except:
                return await ctx.send("There's been an error. Let waffles know or try again later")
            added = discord.Embed(
                description = "The yellow color role has been added",
                color = 0x82e070
            )
            added.set_author(
                name = "Done!",
                icon_url = "https://labmuffin.com/labmuffin/wp-content/uploads/2012/06/382px-BYR_color_wheel.svg_.png"
            )
            return await ctx.send(embed=added)
        if color == "green":
            if greenrole in ctx.message.author.roles:
                rolenotfound = discord.Embed(
                    description = "You already have this role",
                    color = 0xe74c33
                )
                rolenotfound.set_author(
                    name = "This role is already assigned to you!",
                    icon_url = "https://labmuffin.com/labmuffin/wp-content/uploads/2012/06/382px-BYR_color_wheel.svg_.png"
                )
                return await ctx.send(embed=rolenotfound)
            for colorrole in colorroles:
                if colorrole in ctx.message.author.roles:
                    await ctx.message.author.remove_roles(colorrole, reason=f"Nitro colors assignment")
            try:
                await ctx.message.author.add_roles(greenrole, reason=f"Nitro colors assignment")
            except:
                return await ctx.send("There's been an error. Let waffles know or try again later")
            added = discord.Embed(
                description = "The green color role has been added",
                color = 0x82e070
            )
            added.set_author(
                name = "Done!",
                icon_url = "https://labmuffin.com/labmuffin/wp-content/uploads/2012/06/382px-BYR_color_wheel.svg_.png"
            )
            return await ctx.send(embed=added)
        if color == "blue":
            if bluerole in ctx.message.author.roles:
                rolenotfound = discord.Embed(
                    description = "You already have this role",
                    color = 0xe74c33
                )
                rolenotfound.set_author(
                    name = "This role is already assigned to you!",
                    icon_url = "https://labmuffin.com/labmuffin/wp-content/uploads/2012/06/382px-BYR_color_wheel.svg_.png"
                )
                return await ctx.send(embed=rolenotfound)
            for colorrole in colorroles:
                if colorrole in ctx.message.author.roles:
                    await ctx.message.author.remove_roles(colorrole, reason=f"Nitro colors assignment")
            try:
                await ctx.message.author.add_roles(bluerole, reason=f"Nitro colors assignment")
            except:
                return await ctx.send("There's been an error. Let waffles know or try again later")
            added = discord.Embed(
                description = "The blue color role has been added",
                color = 0x82e070
            )
            added.set_author(
                name = "Done!",
                icon_url = "https://labmuffin.com/labmuffin/wp-content/uploads/2012/06/382px-BYR_color_wheel.svg_.png"
            )
            return await ctx.send(embed=added)

    @commands.Cog.listener()
    async def on_member_update(self, before:discord.Member, after:discord.Member):
        boosterrole = discord.utils.get(before.guild.roles, id=588162647568941074)
        if boosterrole not in before.roles:
            return
        if before.roles == after.roles:
            return
        if boosterrole not in after.roles:
            redrole = discord.utils.get(before.guild.roles, id=737709284187439154)
            orangerole = discord.utils.get(before.guild.roles, id=737709452458852373)
            yellowrole = discord.utils.get(before.guild.roles, id=737709652820754523)
            greenrole = discord.utils.get(before.guild.roles, id=737709682856034375)
            bluerole = discord.utils.get(before.guild.roles, id=737709713881301012)
            colorroles = [redrole,orangerole,yellowrole,greenrole,bluerole]
        for colorrole in colorroles:
            if colorrole in after.roles:
                await before.remove_roles(colorrole, reason=f"Auto nitro color removal - boost expired")

def setup(bot):
    bot.add_cog(Boosters(bot))