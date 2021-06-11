import discord
from discord.ext import commands

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.functions = bot.functions

    @commands.command(hidden = True)
    @commands.is_owner()
    async def load(self, ctx, *, module):
        try:
            self.bot.load_extension(f'cogs.{module}')
        except commands.ExtensionError as e:
            await self.functions.handle_error(ctx, f"Failed to load module {module}", f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send(f"Loaded extension: {module}")

    @commands.command(hidden = True)
    @commands.is_owner()
    async def unload(self, ctx, *, module):
        try:
            self.bot.unload_extension(f'cogs.{module}')
        except commands.ExtensionError as e:
            await self.functions.handle_error(ctx, f"Failed to load module {module}", f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send(f"Unloaded extension: {module}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, module):
        try:
            self.bot.reload_extension(f'cogs.{module}')
        except commands.ExtensionError as e:
            await self.functions.handle_error(ctx, f"Failed to reload module {module}", f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send(f"Reload extension: {module}")

    @commands.command(hidden = True)
    @commands.is_owner()
    async def say(self, ctx, *, content):
        await ctx.send(f"{content}")
        await ctx.message.delete()

    @commands.command(hidden = True)
    async def setpresence(self, ctx, activity_type: int, *, presence: str):
        await self.bot.change_presence(activity = discord.Activity(name = presence, type = activity_type))
        await ctx.send(f"Set presence to {presence}")

    @commands.command(aliases = ['logout'], hidden = True)
    @commands.is_owner()
    async def close(self, ctx):
        await ctx.send("Logging out...")
        await self.bot.close()

    @commands.command(hidden = True)
    @commands.is_owner()
    async def sudo(self, ctx, user: discord.Member, *, command):
        new_msg = ctx.message
        new_msg.author = user
        new_msg.content = f"{ctx.prefix}{command}"
        await self.bot.process_commands(new_msg)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def leave(self, ctx, *, guild_id : int):
        try:
            guild = self.bot.get_guild(guild_id)
        except:
            return await self.functions.handle_error(ctx, "Invalid guild", "Make sure you have the correct guild ID")
        try:
            await guild.leave()
            await ctx.send(f"Left guild: {guild.name}")
        except:
            return await self.functions.handle_error(ctx, "Unable to leave guild")

    @commands.command()
    @commands.is_owner()
    async def lookup_document(self, ctx, collection : str, document_id : str):
        if collection == "infractions":
            collection = self.db.infractions
        document = await collection.find_one({"_id" : document_id})
        await ctx.send(f"```{document}```")
        await ctx.send(type(document))

    @commands.command()
    @commands.is_owner()
    async def update_document(self, ctx, collection : str, document_id : str, field : str, new_value):
        if collection == "infractions":
            collection = self.db.infractions
        await collection.update_one({"_id" : document_id}, {"$set": {field : new_value}})
        await ctx.send(f"Updated document {document_id}:\nSet {field} to {new_value}")

    @commands.command()
    @commands.is_owner()
    async def delete_document(self, ctx, collection : str, document_id : str):
        if collection == "infractions":
            collection = self.db.infractions
        await collection.delete_one({"_id" : document_id})
        await ctx.send(f"Deleted document {document_id}")

    @commands.command()
    @commands.is_owner()
    async def insert_document(self, ctx, collection: str, document : dict):
        if collection == "infractions":
            collection = self.db.infractions
        await collection.insert_one(document)

def setup(bot):
    bot.add_cog(Admin(bot))
