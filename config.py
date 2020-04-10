import os

BOT_GUILD_ID = int(os.environ.get("BOT_GUILD_ID"))
BOT_MUTE_ROLE = int(os.environ.get("BOT_MUTE_ROLE"))

class Config:
    tester = [
            477556772220043278, # Avocado#5614
            615089766404325386, # Deadones#1090
            380882346737664022, # jemes#5573
            409092993094516737  # ppiso#8682
        ]
    support = [
            508350582457761813, # waffles#4918
            73502284083900416   # xlite#1709
        ]
    dev = [
            508350582457761813, # waffles#4918
            297567836254240768, # Moo#8008
            167726726451953664  # derw#0387
        ]
    guild_id = BOT_GUILD_ID
    mute_role = BOT_MUTE_ROLE
