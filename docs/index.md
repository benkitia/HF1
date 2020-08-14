# wafflebot

A powerfully simple moderation bot by [wAffles](https://bensonkitia.me), written in discord.py

## Getting support

If you looked for a solution to your problem in the docs below but couldn't find it, you can [DM me on Twitter](https://twitter.com/bensonkitia) or join the [Discord support server](https://discord.gg/zrBqN2v)

## Getting started

You can add wafflebot to your server [here](https://discord.com/oauth2/authorize?client_id=582380938667884548&permissions=8&scope=bot)  

When wafflebot is first added to the server, many commands won't work without a staff and admin role set. The server owner should run the `help set` command and set all the values listed. You'll want to have a staff and/or admin role, and you can set the two values to be the same

## FAQ

Q: Can I host my own instance of wafflebot? Is it open-source
A: No, you cannot host your own instance of wafflebot and the bot is closed-source  

Q: What language is wafflebot written in?
A: wafflebot is written in [discord.py](https://github.com/Rapptz/discord.py)  

## Credits  

[wAffles#0001](https://bensonkitia.me) - Lead Developer  
[derw#0387](https://derw.xyz) - Technical assistance + DB hosting  
[Blue#9588](https://nambiar.dev) - discord.py assistance  
[Moo#8008](https://twitter.com/TwoOneOink) - discord.py assistance and emotional support  

# Privacy

In summary, the bot only collects user and server IDs when neccessary (mostly for infractions). The bot does not store any user account data beyond user IDs.  
More info/privacy policy is available [here](https://wafflebot.rocks/privacy)

## Commands

All commands must be preceeded with the bot's prefix. Default is `-`, but your server may have a different prefix set.  
<indicates required arguements> [indicates optional arguements]. You SHOULD NOT include <> [] when running the command

### Basic

#### ping

Tests the bot's latency and returns the bot's response time in milliseconds.  
Syntax: `ping`

#### botinfo

Returns information about the bot  
Syntax: `botinfo`

#### avatar

Returns a user's avatar in your desired file format  
Syntax: `avatar <user> [format]`  
The default format is png, so if you don't specify a format that's what the bot will return  
Accepted formats include: webp, jpeg, jpg, png or gif (for animated avatars only)

#### serverinfo

Returns information about a server  
Syntax: `serverinfo [guild ID]`  
Aliases: server  
If you don't specify a guild it will default to the guild the command is run in

### Guild Config

#### set

Edits guild settings  
Syntax: `set <setting> <value>`  
Accepted settings include: staffrole, adminrole, actionlog, messagelog, travellog, userlog, muterole, dm_on_warn, dm_on_mute, dm_on_kick, dm_on_ban, dm_on_unmute, dm_on_unban, auto_dehoist  
Values for role settings should be a role ID, role mention, or role name  
Values for log/channel settings should be a channel ID, channel mention, or channel name  
Values for dm_on_x settings should be true or false  

#### settings

Shows a list of the guild's current configuration  
Syntax: `settings`  

### Moderation

#### ban

Bans a user  
Syntax: `ban <user> [reason]`  

#### unban

Unbans a user  
Syntax: `unban <user> [reason]`  

#### kick

Kicks a user  
Syntax: `kick <user> [reason]`

#### mute

Applies the designated mute role to a user  
Syntax: `mute <user> [reason]`

#### unmute

Removes the designated mute role from a user  
Syntax: `unmute <user> [reason]`

#### warn

Warns a user/applies a warning infraction  
Syntax: `warn <user> [reason]`

### (Staff) Utilities

#### userinfo

Retrieves information about a user's account and presents it in an easy-to-read embed format  
Sytax: `userinfo [user]`  
Aliases: profile, info  
If you don't specify a user it will retrieve your information

#### clear

Purges a specified amount of messages from the current channel  
Sytax: `clear <amount>`  
Aliases: purge, purgeall  
Limit is 300 messages per command use to avoid accidental nuking

#### punishinfo

Retrieves information about an infraction  
Syntax: `punishinfo <case/punishment ID>`  
Aliases: inf, infraction

#### search

Retrieves a list of a user's active infractions  
Syntax: `search <user>`  
Aliases: infractions

#### searchall

Retrieves a list of all infractions issued to a user, inacive or deleted  
Syntax: `searchall <user>`  
Aliases: allinfractions

#### rmpunish

Deletes an infraction  
Sytax: `rmpunish <case/punishment ID>`  
Aliases: delinfraction

#### clearpunishments

Deletes all of a user's active infractions  
Syntax: `clearpunishments <user>`

#### role

Adds or removes a role from a user  
Syntax: `role <add|remove> <user> <role>`
