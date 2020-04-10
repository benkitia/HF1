import os
import sys
import asyncio
import discord
from discord.ext import commands
from datetime import datetime
from config import Config

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

BOT_LOG_CHANNEL = int(os.environ.get("BOT_LOG_CHANNEL"))
BOT_ACTION_LOG_CHANNEL = int(os.environ.get("BOT_ACTION_LOG_CHANNEL"))
BOT_MESSAGE_LOG_CHANNEL = int(os.environ.get("BOT_MESSAGE_LOG_CHANNEL"))
BOT_SERVER_LOG_CHANNEL = int(os.environ.get("BOT_SERVER_LOG_CHANNEL"))
BOT_USER_LOG_CHANNEL = int(os.environ.get("BOT_USER_LOG_CHANNEL"))
BOT_ALERT_CHANNEL = int(os.environ.get("BOT_ALERT_CHANNEL"))

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://127.0.0.1")

cogs = ['cogs.admin']

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

    @property
    def action_log_channel(self):
        return self.get_channel(BOT_ACTION_LOG_CHANNEL)

    @property
    def message_log_channel(self):
        return self.get_channel(BOT_MESSAGE_LOG_CHANNEL)

    @property
    def server_log_channel(self):
        return self.get_channel(BOT_SERVER_LOG_CHANNEL)

    @property
    def user_log_channel(self):
        return self.get_channel(BOT_USER_LOG_CHANNEL)

    @property
    def alert_log_channel(self):
        return self.get_channel(BOT_ALERT_CHANNEL)

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

    async def init_mongo(self) -> None:
        self.mongo = AsyncIOMotorClient(MONGO_URI)
        # motor doesnt attempt a connection until you try to do something
        await self.mongo.admin.command("ismaster")
        self.db = self.mongo.wafflebot
        print("Connected to mongo")

    async def close(self):
        await super().close()
        self.mongo.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    bot = WaffleBot()

    try:
        loop.run_until_complete(bot.init_mongo())
    except ServerSelectionTimeoutError:
        print("Could not connect to mongo, timed out\nExiting.")
        sys.exit(0)

    bot.run(DISCORD_TOKEN)
