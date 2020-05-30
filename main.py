import os
import sys
import asyncio
import discord
from discord.ext import commands
from datetime import datetime
from config import Config

from aiohttp import ClientSession

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

BOT_LOG_CHANNEL = int(os.environ.get("BOT_LOG_CHANNEL"))

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://127.0.0.1")

cogs = ['cogs.admin']
cogs = ['cogs.admin','cogs.backend','cause.basic','cogs.logging','cogs.moderation','cogs.modutils']

# a very breif description of the bot
description = """
A multipurpose bot by Waffle Development
"""

class WaffleBot(commands.Bot):
    def __init__(self):
        super().__init__(
                # the character(s) preceding a command to define a message as a command
                command_prefix = '-',
                description = description
            )

        self.config = Config()
        self.db: AsyncIOMotorDatabase

        for cog in cogs:
            self.load_extension(cog)

    @property
    def log_channel(self):
        return self.get_channel(BOT_LOG_CHANNEL)

    async def on_ready(self):
        print(f"{self.user.name} ({self.user.id}) is online")
        print("______________")
        onready = discord.Embed(title="Bot logged on", description=f"{self.user.name} ({self.user.id}) is online",color=0x4bff92)
        onready.timestamp=datetime.utcnow()
        pstatus = f"eating breakfast"
        await self.change_presence(activity=discord.Game(name=pstatus), status=discord.Status.online)
        print(f'\n Bot presence set to "{pstatus}"')
        print("______________")
        setstatus = discord.Embed(title="Bot presence set", description=f"Bot status set to `{pstatus}`", color=0xad6dff)
        setstatus.timestamp=datetime.utcnow()

    async def init_http(self):
        self.session = ClientSession()

    async def init_mongo(self) -> None:
        self.mongo = AsyncIOMotorClient(MONGO_URI)
        # motor doesnt attempt a connection until you try to do something
        await self.mongo.admin.command("ismaster")
        self.db = self.mongo.wafflebot
        print("Connected to mongo")

    async def close(self):
        await super().close()
        await self.session.close()
        self.mongo.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    bot = WaffleBot()

    loop.run_until_complete(bot.init_http())

    try:
        loop.run_until_complete(bot.init_mongo())
    except ServerSelectionTimeoutError:
        print("Could not connect to mongo, timed out\nExiting.")
        sys.exit(0)

    bot.run(DISCORD_TOKEN)
