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
import pymongo
from pymongo import MongoClient

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://127.0.0.1")

cogs = ['cogs.admin']


class WaffleBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix='-',
            description="A simple yet powerful moderation bot. Written in discord.py"
        )

        self.config = Config()
        self.db: AsyncIOMotorDatabase

        for cog in cogs:
            self.load_extension(cog)

    async def on_ready(self):
        print(f"{self.user.name} ({self.user.id}) is online")
        print("______________")
        pstatus = f"eating breakfast"
        await self.change_presence(activity=discord.Game(name=pstatus), status=discord.Status.online)
        print(f'\n Bot presence set to "{pstatus}"')
        print("______________")

    async def init_http(self):
        self.session = ClientSession()

    async def init_mongo(self) -> None:
        self.mongo = AsyncIOMotorClient(MONGO_URI)
        await self.mongo.admin.command("ismaster")
        self.db = self.mongo.wafflebot
        print("Connected to mongo")
        print("______________")

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
