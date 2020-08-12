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

## Commands

All commands must be preceeded with the bot's prefix. Default is `-`, but your server may have a different prefix set.

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
