# This is the configuration file for the bot.
# This file stores commonly used constants.

# General Settings
BOT_TOKEN = ""  # REQUIRED; see README for info on how to generate bot token
BOT_STATUS = "SpiritMS"  # What the bot will appear to be playing on discord
THUMBNAIL_URL = ""  # Used in !info command to display a picture in the embedded message, please fill out
PREFIX = "!"  # REQUIRED; prefix used for commands (e.g. prefix "!" for commands like "!online")
ADMIN_ROLE = "Admin"  # REQUIRED; role for admin commands
LOG_COMMANDS = True  # Toggle logger on/off

ADD_ROLE = False  # When this is true, the bot will attempt to give newly joined users a role
ROLE_TO_GIVE = "Role Name Here"  # REQUIRED if ADD_ROLE is True, Enter Role Name

SHOW_ONLINE_PLAYERS = False  # Turn this to true, if you want the bot to display online players count in the presence
# I.E. "Playing Players Online: 53"
SEC_PER_UPDATE = 5  # In seconds, how long should the bot wait till updating player count in presence

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
OFFLINE_MESSAGE = "The server is currently offline"  # Error message (no need to touch)
DATABASE_OFFLINE_MESSAGE = "The database is currently offline"  # Error message (no need to touch)

# For use with MapleStory.io API:
# Used for loading the graphical assets - no need to touch unless you're using a newer version
REGION = "GMS"
VERSION = "216"

# Server Information
# Not required, but make sure to provide accurate info of your server.
INFO_VERSION = "GMS v83"  # Displays Server Version
INFO_EXP = "6x"  # Displays Exp Rate of Server
INFO_DROP = "2x"  # Displays Drop Rate of Server
INFO_MESO = "1x"  # Displays Meso Rate of Server
INFO_LOCATION = "Insert Server Location Here"  # Location of the physical server
INFO_STATE = "Open-Alpha Testing"  # Add what the current state of the server is here

# Other Constants
# Warning: Do NOT remove original credits! You are legally required to keep them!
CREDITS = {
    # A dictionary to store credits for the !credits command
    # add to this dictionary if you'd like to expand the credits command
    # "DiscordUser": "for <reason>"
    '@Desc#0416': ' - Author',
    '@Not Brandon#4444': ' - Contributor',
    '@KOOKIIE#9770': ' - Contributor'
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
    "credit",
    "info",
]

# Turn commands on (True) or off (False)
# To add new commands, use the handler method name as key
TOGGLE_ON_OFF = {
    'handle_help': True,
    'handle_info': True,
    'handle_character': True,
    'handle_guild': True,
    'handle_ranking': True,
    'handle_online': True,
    'handle_duey': False,
    'handle_dc': True,
    'handle_whisper': True,
    'handle_notice': True,
    'handle_unban': True,
    'handle_setgmlevel': True,
    'handle_give_vp': True,
    'handle_giveaway': False,
}
DISABLED_TEXT = "This command has been disabled"

# Text in help command
BOT_VER = "v0.3.1 Alpha"
