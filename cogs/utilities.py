import asyncio
import discord
from discord.ext import commands
import time

class Utilities(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.db = bot.db
		self.functions = bot.functions

	@commands.command(description = "Creates a poll")
	async def poll(self, ctx):
		await ctx.message.add_reaction('<:upvote:711293005583220807>')
		await ctx.message.add_reaction('<:downvote:711293020993093743>')

	@commands.command(aliases = ['purge', 'purgeall'])
	async def clear(self, ctx, amount=10):
		staff = await self.functions.check_if_staff(ctx, ctx.message.author)
		if not staff:
			return
		if amount > 300:
			return await self.functions.handle_error(ctx, "You can only purge up to 300 messages at a time")
		try:
			await ctx.channel.purge(limit = amount+1)
		except discord.Forbidden:
			return await self.functions.handle_error(ctx, "Unable to purge messages", "Make sure I have permission to manage messages in this channnel")
		except discord.HTTPException:
			return await self.functions.handle_error(ctx, "Unable to purge messages", "An unknown Dicord error occured. Try again later.")
		confirmation_message = await self.functions.confirm_action_return_message(ctx, f"Cleared {amount} message(s)")
		await asyncio.sleep(5)
		await confirmation_message.delete()

	@commands.command(description = "Returns information about a user", aliases = ['profile', 'info'])
	async def userinfo(self, ctx, user_id = None):
		if user_id is None:
			user_id = ctx.message.author.id
		try: 
			user = await self.bot.fetch_user(int(user_id))
		except:
			await self.functions.handle_error(ctx, "Invalid user", "This command only accepts user IDs")
		if ctx.guild.get_member(user.id) is not None:
			user = ctx.guild.get_member(user.id)
			in_guild = True
		else:
			in_guild = False
		infraction_count = await self.db.infractions.count_documents({"target": str(user.id), "guild": str(ctx.message.guild.id), "status": "active"})
		embed = discord.Embed(
			title = str(user),
			color = user.color
		)
		embed.add_field(
			name = "Name",
			value = user.name,
		)
		embed.add_field(
			name = "ID",
			value = user.id
		)
		if in_guild:
			embed.add_field(
				name = "Status",
				value = user.status
			)
			embed.add_field(
				name = "Joined at",
				value = user.joined_at
			)
		embed.add_field(
			name = "Created at",
			value = user.created_at
		)
		if in_guild:
			embed.add_field(
				name = "Highest Role",
				value = user.top_role
			)
		embed.add_field(
			name = "Infractions",
			value = infraction_count
		)
		embed.set_thumbnail(url = user.avatar_url)
		embed.set_footer(text = f"Requested by {ctx.message.author}")
		await ctx.send(embed = embed)

	@commands.command(description =" Returns bot response time")
	async def ping(self, ctx):
		t1 = time.perf_counter()
		async with ctx.typing():
			pass
		t2 = time.perf_counter()
		await ctx.send(":ping_pong: Pong! It took {}ms".format(round((t2-t1)*1000)))

	@commands.command(description = "Returns a user's avatar in one of many formats", aliases = ['avi'])
	async def avatar(self, ctx, user:  discord.Member = None, avatar_format = 'png'):
		if user is None:
			user = ctx.message.author
		try:
			avi = user.avatar_url_as(format = avatar_format)
		except:
			return self.functions.handle_error(ctx, "Invalid format", "Valid formats include ‘webp’, ‘jpeg’, ‘jpg’, ‘png’ or ‘gif’ (for animated avatars)")
		embed = discord.Embed(
			title = "Avatar",
			color = user.color
		)
		embed.set_author(name = user, icon_url = user.avatar_url)
		embed.set_footer(text = f"Requested by {ctx.message.author}")
		embed.set_image(url = avi)
		await ctx.send(embed = embed)

	@commands.command(description = "Returns an enlarged version of an emoji. This does not work on default Discord emojis.", aliases = ['jumbo', 'bigify'])
	async def enlarge(self, ctx, emoji: discord.Emoji):
		try:
			await ctx.send(emoji.url)
		except:
			await self.functions.handle_error(ctx, "This command only works with server emojis")

	@commands.command(description = "Returns information about a server", aliases = ['server'])
	async def serverinfo(self, ctx, guild_id : int = None):
		guild = ctx.message.guild if not guild_id else self.bot.get_guild(guild_id)
		embed = discord.Embed(title=guild.name, color=0xFED870)
		embed.add_field(
			name = "Guild ID",
			value = ctx.guild.id,
			inline = False
			)
		embed.add_field(
			name = "Owner",
			value = ctx.guild.owner,
			inline = False
			)
		embed.add_field(
			name = "Member Count",
			value = ctx.guild.member_count,
			inline = False
			)
		embed.add_field(
			name = "Bot Count",
			value = sum(1 for member in ctx.guild.members if member.bot),
			inline = False
			)
		embed.add_field(
			name = "Channel Count",
			value = len(guild.channels))
		embed.add_field(
			name = "Region",
			value = ctx.guild.region,
			inline = False
			)
		embed.add_field(
			name = "Verification Level",
			value = guild.verification_level,
			inline = False
			)
		embed.add_field(
			name = "Created At",
			value = guild.created_at,
			inline = False
			)
		embed.add_field(
			name = "Nitro Boost Info",
			value = f"Nitro Boost Tier: {guild.premium_tier}\nNitro Boost Count: {guild.premium_subscription_count}",
			inline = False
		)
		if guild.splash:
			embed.add_field(
				name = "Splash Page URL",
				value = guild.splash_url_as(format = "png"),
				inline = False
			)
		embed.set_footer(text=f"Requested by {ctx.message.author}")
		try:
			embed.set_thumbnail(url = guild.icon_url_as(format = "gif"))
		except: 
			embed.set_thumbnail(url = guild.icon_url_as(format = "png"))
		if guild.banner:
			embed.set_image(url = guild.banner_url_as(format = 'png'))
		await ctx.send(embed = embed)

	@commands.command(description = "Returns some bot statistics")
	async def stats(self, ctx):
		embed = discord.Embed(
			title = "Bot Statistics",
			color=0x5c92ff
			)
		embed.add_field(
			name = "Guild Count",
			value = len(list(self.bot.guilds))
			)
		embed.add_field(
			name = "Total Members",
			value = len(set(self.bot.get_all_members()))
			)
		await ctx.send(embed = embed)

	@commands.command(description = "Add or removes a role")
	async def role(self, ctx, add_or_remove, target: discord.Member, role: discord.Role):
		staff = await self.functions.check_if_staff(ctx, ctx.message.author)
		if not staff:
			return
		if add_or_remove == "add":
			try:
				await target.add_roles(role)
			except discord.Forbidden:
				return await self.functions.handle_error(ctx, "Unable to assign role", "Make sure my highest role is above it and I have manage roles permissions")
			await self.functions.confirm_action(ctx, f"Added role {role.name} to {target.mention}")
		if add_or_remove == "remove":
			try:
				await target.remove_roles(role)
			except discord.Forbidden:
				return await self.functions.handle_error(ctx, "Unable to remove role", "Make sure my highest role is above it and I have manage roles permissions")
			await self.functions.confirm_action(ctx, f"Removed role {role.name} from {target.mention}")
		if add_or_remove not in ["add", "remove"]:
			return await self.functions.handle_error(ctx, "Specify add or remove")

def setup(bot):
	bot.add_cog(Utilities(bot))
