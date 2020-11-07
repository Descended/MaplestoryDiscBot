# This is the configuration file for the bot.
# This file stores commonly used constants.

# General Settings
BOT_TOKEN = ""  # REQUIRED; see README for info on how to generate bot token
BOT_STATUS = "SpiritMS"  # What the bot will appear to be playing on discord
THUMBNAIL_URL = ""  # WARNING: UNUSED
PREFIX = "!"  # REQUIRED; prefix used for commands (e.g. prefix "!" for commands like "!online")
ADMIN_ROLE = "Admin"  # REQUIRED; role for admin commands
LOG_COMMANDS = True  # Toggle logger on/off

SERVER_NAME = "SpiritMS"  # Display server name
EMBED_COLOR = 0x03fcc6  # Colour of bot message (no need to touch)
ICON_URL = "https://cdn.discordapp.com/icons/722153430457647104/ad8368ee9d687dc73aaa8f47ce0c0026.png?size=128"  # Display icon


# Connection Settings
# For use in DatabaseHandler.py:
DATABASE_HOST = "localhost"  # REQUIRED; DB Host (no need to touch if bot and DB are hosted on the same machine)
DATABASE_NAME = "heavenms"  # REQUIRED; DB connection/schema name
DATABASE_USER = "root"  # REQUIRED; DB connection username
DATABASE_PASS = ""  # REQUIRED; DB connection password

# For use in ApiHandler.py:
API_KEY = "PUTAPIKEYHERE"  # REQUIRED; proprietary API key for web-requests
API_HOST = "http://localhost:8080/"  # REQUIRED; server location (no need to touch if bot and server are hosted on the same machine)
OFFLINE_MESSAGE = "Server is currently offline"  # Error message (no need to touch)
DATABASE_OFFLINE_MESSAGE = "The database is offline"  # Error message (no need to touch)

# For use with MapleStory.io API:
# Used for loading the graphical assets - no need to touch unless you're using a newer version
REGION = "GMS"
VERSION = "216"


# Other Constants
# Warning: Do NOT remove original credits! You are legally required to keep them!
CREDITS = {
    # A dictionary to store credits for the !credits command
    # add to this dictionary if you'd like to expand the credits command
    # "DiscordUser": "for <reason>"
    "@Desc#0416": " - Author",
    "@Not Brandon#4444": " - Contributor",
    "@KOOKIIE#9770": " - Contributor"
}

# List of commands tracked by the logger:
# Add new commands to the list to allow their usage to be tracked
COMMANDS = [
    "help",
    "commands",
    "character",
    "char",
    "player",
    "guild",
    "guildinfo",
    "duey",
    "giveitem",
    "rankings",
    "rankings",
    "ranktop",
    "dc",
    "whisper",
    "msg",
    "notice",
    "online",
    "credits",
    "credit"
]

# Text in help command
BOT_VER = "v0.0.15 Alpha"
