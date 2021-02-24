import os
import sys
import asyncio
import discord
from discord.ext import commands
from datetime import datetime
from config import Config
from functions import Functions
from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError
import pymongo
from pymongo import MongoClient

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://127.0.0.1")

cogs = ['cogs.admin','cogs.automod','cogs.boosters','cogs.errhandle','cogs.infractions','cogs.logging','cogs.moderation','cogs.utilities']


class HF1(commands.Bot):

	def __init__(self):
		super().__init__(
			command_prefix='!',
			description="A simple yet powerful moderation bot. Written in discord.py",
			intents=intents
		)

		self.config = Config()
		self.db: AsyncIOMotorDatabase
		self.functions = Functions()

	async def on_ready(self):
		print(f"{self.user.name} ({self.user.id}) is online")
		print("______________")
		pstatus = f"github.com/iphonediscord/hf1"
		await self.change_presence(activity=discord.Game(name=pstatus), status=discord.Status.online)
		print(f'\n Bot presence set to "{pstatus}"')
		print("______________")
		print("Loading extensions...")
	  	for cog in cogs:
	  		self.load_extension(cog)
	   	print("Loaded extensions")
	   	print("______________")

	async def init_http(self):
		self.session = ClientSession()

	async def init_mongo(self) -> None:
		self.mongo = AsyncIOMotorClient(MONGO_URI)
		await self.mongo.admin.command("ismaster")
		self.db = self.mongo.HF1
		print("Connected to mongo")
		print("______________")

	async def close(self):
		await super().close()
		await self.session.close()
		self.mongo.close()


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	bot = HF1()

	loop.run_until_complete(bot.init_http())

	try:
		loop.run_until_complete(bot.init_mongo())
	except ServerSelectionTimeoutError:
		print("Could not connect to mongo, timed out\nExiting.")
		sys.exit(0)

	bot.run(DISCORD_TOKEN)
