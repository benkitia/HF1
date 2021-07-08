import asyncio
import datetime
from datetime import datetime, date, time
import discord
from discord.ext import commands
from durations import Duration
import random
import string

class Moderation(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.config = bot.config
		self.db = bot.db
		self.functions = bot.functions

	async def confirm_infraction(self, ctx, verb : str, target: discord.User, infraction_id = None):
		embed = discord.Embed(
			description = f":ok_hand: {target.mention} ({target.id}) has been {verb}",
			color = self.config.embed_colors["positive"]
		)
		if infraction_id:
			embed.set_footer(text = infraction_id)
		embed.timestamp = datetime.utcnow()
		msg = await ctx.send(embed = embed)
		await asyncio.sleep(5)
		if ctx.message.channel.id != 410588985937625089:
			await msg.delete()
			await ctx.message.delete()

	async def generate_infraction_id(self):
		generated_id = ''.join(random.choice(string.ascii_letters) for i in range(12)).upper()
		duplicate_id = await self.db.infractions.find_one({"_id" : generated_id})
		while duplicate_id:
			generated_id = ''.join(random.choice(string.ascii_letters) for i in range(12)).upper()
		return generated_id
	
	async def check_hierarchy(self, ctx, mod : discord.Member, target : discord.User):
		try:
			target = ctx.guild.get_member(target.id)
		except:
			return True
		if target not in ctx.guild.members:
			return True
		return mod.top_role > target.top_role

	async def log_infraction(self, ctx, verb : str, target : discord.User, mod : discord.User, reason : str, infraction_type : str = None, notified : bool = None, infraction_id : str = None, duration : str = None):
		if self.config.private_inf_log:
			embed_private = discord.Embed(
				description = f"{target} {verb}",
				color = self.config.embed_colors["log_infraction"]
			)
			embed_private.set_author(
				name = "Infraction Log",
				icon_url = self.config.log_icon_urls[infraction_type]
			)
			embed_private.add_field(
				name = "Target",
				value = f"{target.mention} ({target.id})"
			)
			embed_private.add_field(
				name = "Moderator",
				value = f"{mod.mention} ({mod.id})"
			)
			embed_private.add_field(
				name = "Reason",
				value = reason
			)
			if duration:
				embed_private.add_field(
					name = "Duration",
					value = duration
				)
			if infraction_id:
				embed_private.set_footer(text = infraction_id)
			embed_private.timestamp = datetime.utcnow()
			private_inf_log = discord.utils.get(ctx.guild.text_channels, id = self.config.private_inf_log)
			await private_inf_log.send(embed = embed_private)
		if self.config.public_inf_log:
			embed_public = discord.Embed(
				description = f"{target} {verb}",
				color = self.config.embed_colors["log_infraction"]
			)
			embed_public.set_author(
				name = "Infraction Log",
				icon_url = self.config.log_icon_urls[infraction_type]
			)
			embed_public.add_field(
				name = "Target",
				value = f"{target.mention} ({target.id})"
			)
			embed_public.add_field(
				name = "Reason",
				value = reason
			)
			if duration:
				embed_public.add_field(
					name = "Duration",
					value = duration
				)
			if infraction_id:
				embed_public.set_footer(text = infraction_id)
			embed_public.timestamp = datetime.utcnow()
			public_inf_log = discord.utils.get(ctx.guild.text_channels, id = self.config.public_inf_log)
			ping = target.mention if not notified else None
			await public_inf_log.send(ping, embed = embed_public)

	async def store_infraction(self, ctx, infraction_id : str, infraction_type : str, target : discord.User, mod : discord.User, reason : str, duration : str = None, status : str = "active"):
		infraction = {
			"_id" : infraction_id,
			"infraction_type" : infraction_type,
			"target" : str(target.id),
			"mod" : str(mod.id),
			"reason" : reason,
			"status" : status,
			"duration" : duration,
			"timestamp" : datetime.utcnow()
		}
		await self.db.infractions.insert_one(infraction)

	async def notify_target(self, ctx, target : discord.User, infraction_type : str, reason : str, infraction_id : str = None, duration : str = None):
		embed = discord.Embed(
			description = f"Infraction Notification: {infraction_type}",
			color = 0xF53B30
		)
		embed.add_field(
			name = "Reason",
			value = reason
		)
		if duration:
			embed.add_field(
				name = "Duration",
				value = duration
			)
		if infraction_id:
			embed.add_field(
				name = "Infraction ID",
				value = infraction_id
			)
		if infraction_type == "ban":
			embed.add_field(
				name = "Appeal",
				value = "If you believe this ban is unjust, click here to appeal: https://discord.gg/PuXhxYTKu8"
			)
		embed.set_author(
			name = ctx.message.guild.name,
			icon_url = ctx.message.guild.icon_url
		)
		embed.timestamp = datetime.utcnow()
		try:
			await target.send(embed = embed)
			return True
		except:
			return False

	async def check_if_banned(self, ctx, target : discord.User, no_error : bool = False):
		try:
			await ctx.guild.fetch_ban(target)
			is_banned = True
		except discord.NotFound:
			is_banned = False
		if no_error:
			return is_banned
		if is_banned:
			await ctx.send("Target is already banned")
		return is_banned

	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def ban(self, ctx, target : discord.User = None, *, reason = None):
		if target is None:
			return await ctx.send("Specify a user to ban")
		allowed = await self.check_hierarchy(ctx, ctx.message.author, target)
		if not allowed:
			return await self.ctx.send("You don't have permission to ban that user")
		is_banned = await self.check_if_banned(ctx, target)
		if is_banned:
			return
		infraction_id = await self.generate_infraction_id()
		notified = await self.notify_target(
			ctx,
			target = target,
			infraction_type = "ban",
			reason = reason,
			infraction_id = infraction_id
		)
		try:
			await ctx.guild.ban(target, reason = f"By {ctx.message.author}: {reason}")
		except:
			await ctx.send("Error banning user")
		await self.log_infraction(
			ctx,
			verb = "banned",
			target = target,
			mod = ctx.message.author,
			reason = reason,
			infraction_type = "ban",
			notified = notified,
			infraction_id = infraction_id
		)
		await self.store_infraction(
			ctx,
			infraction_id = infraction_id,
			infraction_type = "ban",
			target = target,
			mod = ctx.message.author,
			reason = reason
		)
		await self.confirm_infraction(
			ctx,
			verb = "banned",
			target = target,
			infraction_id = infraction_id
		)

	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def unban(self, ctx, target_id : int = None, *, reason = None):
		if target_id is None:
			return await ctx.send("Specify a user to unban")
		try:
			target = await self.bot.fetch_user(target_id)
		except:
			return await ctx.send("Make sure you have the right user ID")
		is_banned = await self.check_if_banned(ctx, target, no_error = True)
		if not is_banned:
			return await ctx.send("User is not banned")
		try:
			await ctx.guild.unban(target, reason = f"By {ctx.message.author}: {reason}")
		except:
			await ctx.send("Error unbanning user")
		await self.log_infraction(
			ctx,
			verb = "unbanned",
			target = target,
			mod = ctx.message.author,
			reason = reason,
			infraction_type = "unban",
			notified = False
		)
		await self.confirm_infraction(
			ctx,
			verb = "unbanned",
			target = target
		)
		

	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def forceban(self, ctx, target_id : int = None, *, reason = None):
		if target_id is None:
			return await ctx.send("Specify a user to ban")
		try:
			target = await self.bot.fetch_user(target_id)
		except:
			return await ctx.send("Make sure you have the right user ID")
		allowed = await self.check_hierarchy(ctx, ctx.message.author, target)
		if not allowed:
			return await self.ctx.send("You don't have permission to ban that user")
		is_banned = await self.check_if_banned(ctx, target)
		if is_banned:
			return
		infraction_id = await self.generate_infraction_id()
		try:
			await ctx.guild.ban(target, reason = f"By {ctx.message.author}: {reason}")
		except:
			return await ctx.send("Error banning user")
		await self.log_infraction(
			ctx,
			verb = "banned",
			target = target,
			mod = ctx.message.author,
			reason = reason,
			infraction_type = "ban",
			notified = False,
			infraction_id = infraction_id
		)
		await self.store_infraction(
			ctx,
			infraction_id = infraction_id,
			infraction_type = "ban",
			target = target,
			mod = ctx.message.author,
			reason = reason
		)
		await self.confirm_infraction(
			ctx,
			verb = "banned",
			target = target,
			infraction_id = infraction_id
		)
		
	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def multiban(self, ctx, *, args):
		arguments = args.split()
		targets = []
		not_bans = []
		reason = ""
		async with ctx.typing():
			for argument in arguments:
				try:
					target = await commands.UserConverter().convert(ctx, argument)
					targets.append(target)
				except:
					try:
						argument = int(argument)
						if len(argument) < 20:
							not_bans.append(f"{argument} - Invalid UID")
						continue
					except:
						argument = str(argument)
						reason_start = arguments.index(argument)
						reason = ' '.join(arguments[reason_start::])
						break
			if not targets:
				return await ctx.send("No users found")
			if len(targets) > 15:
				await ctx.send("You can't ban more than 15 users at once")
			bans = []
			done = []
			for target in targets:
				if target in done:
					continue
				allowed = await self.check_hierarchy(ctx, ctx.message.author, target)
				if not allowed:
					not_bans.append(f"{target.mention} ({target.id}) - User has role >= you")
					continue
				if not reason:
					reason = "None"
				is_banned = await self.check_if_banned(ctx, target, no_error = True)
				if is_banned:
					not_bans.append(f"{target.mention} ({target.id}) - User is already banned")
					continue
				try:
					await ctx.guild.ban(target, reason=f"Action by {ctx.message.author} for {reason}")
				except:
					not_bans.append(f"{target.mention} ({target.id}) - Ban failed")
					continue
				infraction_id = await self.generate_infraction_id()
				bans.append(f"{target.mention} ({target.id}) - {infraction_id}")
				done.append(target)
				notified = await self.notify_target(
					ctx,
					target = target,
					infraction_type = "ban",
					reason = reason,
					infraction_id = infraction_id
				)
				await self.log_infraction(
					ctx,
					verb = "banned",
					target = target,
					mod = ctx.message.author,
					reason = reason,
					infraction_type = "ban",
					notified = notified,
					infraction_id = infraction_id
				)
				await self.store_infraction(
					ctx,
					infraction_id = infraction_id,
					infraction_type = "ban",
					target = target,
					mod = ctx.message.author,
					reason = reason
				)
		embed = discord.Embed()
		embed.set_author(name = "Multiban")
		if bans:
			ban_list = ""
			for ban in bans:
				ban_list = f"{ban_list}\n{ban}"
			embed.add_field(name = "Successfully banned", value = ban_list, inline = False)
		if not_bans:
			not_ban_list = ""
			for not_ban in not_bans:
				not_ban_list = f"{not_ban_list}\n{not_ban}"
			embed.add_field(name = "Failed to ban", value = not_ban_list, inline = False)
		await ctx.send(embed = embed)

	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def kick(self, ctx, target : discord.User, *, reason = None):
		if target is None:
			return await ctx.send("Specify a user to kick")
		allowed = await self.check_hierarchy(ctx, ctx.message.author, target)
		if not allowed:
			return await self.ctx.send("You don't have permission to kick that user")
		if target not in ctx.guild.members:
			return await ctx.send("User is not in guild")
		infraction_id = await self.generate_infraction_id()
		notified = await self.notify_target(
			ctx,
			target = target,
			infraction_type = "kick",
			reason = reason,
			infraction_id = infraction_id
		)
		try:
			await ctx.guild.kick(target, reason = f"By {ctx.message.author}: {reason}")
		except:
			await ctx.send("Error kicking user")
		await self.log_infraction(
			ctx,
			verb = "kicked",
			target = target,
			mod = ctx.message.author,
			reason = reason,
			infraction_type = "kick",
			notified = notified,
			infraction_id = infraction_id
		)
		await self.store_infraction(
			ctx,
			infraction_id = infraction_id,
			infraction_type = "kick",
			target = target,
			mod = ctx.message.author,
			reason = reason
		)
		await self.confirm_infraction(
			ctx,
			verb = "kicked",
			target = target,
			infraction_id = infraction_id
		)

	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def mute(self, ctx, target: discord.Member = None, duration = None, *, reason = None):
		if target is None:
			return await ctx.send("Specify a user to mute")
		if duration is None:
			return await ctx.send("Specify a duration")
		allowed = await self.check_hierarchy(ctx, ctx.message.author, target)
		if not allowed:
			return await self.ctx.send("You don't have permission to mute that user")
		if target not in ctx.guild.members:
			return await ctx.send("User is not in guild")
		duration_pre_parse = duration
		try:
			duration = Duration(duration)
			duration = duration.to_seconds()
		except:
			return await ctx.send("Invalid duration")
		infraction_id = await self.generate_infraction_id()
		notified = await self.notify_target(
			ctx,
			target = target,
			infraction_type = "mute",
			reason = reason,
			infraction_id = infraction_id,
			duration = duration_pre_parse
		)
		try:
			mute_role = discord.utils.get(ctx.guild.roles, id = self.config.mute_role)
		except:
			return await ctx.send("Invalid mute role, yell at waffles")
		try:
			await target.add_roles(mute_role, reason=f"Action by {ctx.message.author} for {reason}")
		except:
			await ctx.send("Error muting user")
		await self.log_infraction(
			ctx,
			verb = "muted",
			target = target,
			mod = ctx.message.author,
			reason = reason,
			infraction_type = "mute",
			notified = notified,
			infraction_id = infraction_id,
			duration = duration_pre_parse
		)
		await self.store_infraction(
			ctx,
			infraction_id = infraction_id,
			infraction_type = "mute",
			target = target,
			mod = ctx.message.author,
			reason = reason,
			duration = duration_pre_parse
		)
		await self.confirm_infraction(
			ctx,
			verb = "muted",
			target = target,
			infraction_id = infraction_id
		)
		await asyncio.sleep(duration)
		await target.remove_roles(mute_role, reason=f"Temporary mute {infraction_id} expired")
		notified = await self.notify_target(
			ctx,
			target = target,
			infraction_type = "unmute",
			reason = f"Temporary mute {infraction_id} expired"
		)
		await self.log_infraction(
			ctx,
			verb = "unmuted",
			target = target,
			mod = ctx.message.author,
			reason = f"Temporary mute {infraction_id} expired",
			infraction_type = "unmute",
			notified = notified
		)

	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def unmute(self, ctx, target: discord.Member = None, *, reason = None):
		if target is None:
			return await ctx.send("Specify a user to unmute")
		if target not in ctx.guild.members:
			return await ctx.send("User is not in guild")
		notified = await self.notify_target(
			ctx,
			target = target,
			infraction_type = "unmute",
			reason = reason
		)
		try:
			mute_role = discord.utils.get(ctx.guild.roles, id = self.config.mute_role)
		except:
			return await ctx.send("Invalid mute role, yell at waffles")
		if mute_role not in target.roles:
			return await ctx.send("User is not muted")
		try:
			await target.remove_roles(mute_role, reason=f"Action by {ctx.message.author} for {reason}")
		except:
			await ctx.send("Error unmuting user")
		await self.log_infraction(
			ctx,
			verb = "unmuted",
			target = target,
			mod = ctx.message.author,
			reason = reason,
			infraction_type = "unmute",
			notified = notified
		)
		await self.confirm_infraction(
			ctx,
			verb = "unmuted",
			target = target
		)

	@commands.command(aliases = ['strike'])
	@commands.has_permissions(ban_members = True)
	async def warn(self, ctx, target: discord.Member = None, *, reason = None):
		if target is None:
			return await ctx.send("Specify a user to warn")
		allowed = await self.check_hierarchy(ctx, ctx.message.author, target)
		if not allowed:
			return await self.ctx.send("You don't have permission to warn that user")
		if target not in ctx.guild.members:
			return await ctx.send("User is not in guild")
		infraction_id = await self.generate_infraction_id()
		notified = await self.notify_target(
			ctx,
			target = target,
			infraction_type = "warning",
			reason = reason,
			infraction_id = infraction_id
		)
		await self.log_infraction(
			ctx,
			verb = "warned",
			target = target,
			mod = ctx.message.author,
			reason = reason,
			infraction_type = "warning",
			notified = notified,
			infraction_id = infraction_id
		)
		await self.store_infraction(
			ctx,
			infraction_id = infraction_id,
			infraction_type = "warning",
			target = target,
			mod = ctx.message.author,
			reason = reason
		)
		await self.confirm_infraction(
			ctx,
			verb = "warned",
			target = target,
			infraction_id = infraction_id
		)

def setup(bot):
	bot.add_cog(Moderation(bot))