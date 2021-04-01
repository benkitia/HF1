import discord
from discord.ext import commands
import os
from config import Config
from discord.ext.commands import UserConverter

class Functions:

    async def handle_error(self, ctx, description : str, troubleshooting : str = None):
        embed = discord.Embed(
            description = description,
            color = 0xf34141
            )
        embed.set_author(name = "Error")
        if troubleshooting:
            embed.set_footer(text = troubleshooting)
        await ctx.send(embed = embed)
    
    async def confirm_action(self, ctx, description : str, additional_info: str = None):
        embed = discord.Embed(
            description = description,
            color = 0x43e286
        )
        embed.set_author(name = "Success")
        if additional_info:
            embed.set_footer(text = additional_info)
        await ctx.send(embed = embed)

    async def confirm_action_return_message(self, ctx, description : str, additional_info: str = None):
        embed = discord.Embed(
            description = description,
            color = 0x43e286
        )
        embed.set_author(name = "Success")
        if additional_info:
            embed.set_footer(text = additional_info)
        message = await ctx.send(embed = embed)
        return message

    async def check_if_staff(self, ctx, user : discord.User):
        for staff_role in Config.staff_roles:
            staff_role = discord.utils.get(ctx.guild.roles, id = staff_role)
            if staff_role in ctx.message.author.roles:
                return True
        for admin_role in Config.admin_roles:
            admin_role = discord.utils.get(ctx.guild.roles, id = admin_role)
            if admin_role in ctx.message.author.roles:
                return True
        await self.handle_error(ctx, "You do not have permission to run this command")
        return False