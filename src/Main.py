import sys
from os import path
import time
import discord
from discord.ext import commands
# Necessary to run from a batch file unfortunately
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.commands.CommandHandler import CommandHandler
from src.Utils import Utils
# from src.settings import Config  # Disabled in YAML mode

# Global Constants
GENERAL_SETTINGS = {}
DB_SETTINGS = {}
API_SETTINGS = {}
IO_API_SETTINGS = {}
TOGGLE = {}
LITERALS = {}
INFO = {}
COMMANDS = []
CREDITS = {}

start_time = time.time()

intents = discord.Intents.default()
intents.members = True

# client = commands.Bot(command_prefix=Config.PREFIX, intents=intents)
client = commands.Bot(command_prefix=GENERAL_SETTINGS['PREFIX'], intents=intents)


@client.event
async def on_ready():  # method that is called when bot is online
    print("[DONE] Bot is now online.")
    end_time = time.time()
    print(f"[DONE] Successfully loaded bot in {end_time - start_time} seconds")
    # await client.change_presence(activity=discord.Game(name=Config.BOT_STATUS))
    await client.change_presence(activity=discord.Game(name=GENERAL_SETTINGS['BOT_STATUS']))


@client.event
async def on_member_join(member):  # method that is called when a member joins the discord server
    # if Config.ADD_ROLE:
    if GENERAL_SETTINGS['ADD_ROLE']:
        # role = discord.utils.get(member.guild.roles, name=Config.ROLE_TO_GIVE)
        role = discord.utils.get(member.guild.roles, name=GENERAL_SETTINGS['ROLE_TO_GIVE'])
        print(member.name + " has joined the discord server")
        await member.add_roles(role)


@client.event
async def on_message(ctx):  # method that is called whenever a message is sent into discord server
    await CommandHandler.handle_commands(client, ctx)


def main():  # main function
    global GENERAL_SETTINGS
    global DB_SETTINGS
    global API_SETTINGS
    global IO_API_SETTINGS
    global TOGGLE
    global LITERALS
    global INFO
    global COMMANDS
    global CREDITS

    # Load YAML files
    # Try-catch already part of the internal API, so no need to add it here
    config = Utils.yaml_load("src/settings/config.yaml")
    constants = Utils.yaml_load("src/settings/constants.yaml")
    # print(config)  # To check if the contents are read
    # print(constants)  # To check if the contents are read
    GENERAL_SETTINGS = Utils.get_general(config)
    DB_SETTINGS, API_SETTINGS, IO_API_SETTINGS = Utils.get_connection(config)
    TOGGLE = Utils.get_toggle(config)
    LITERALS = Utils.get_literals(constants)
    INFO = Utils.get_info(constants)
    COMMANDS = Utils.get_commands(INFO)
    CREDITS = Utils.get_credits(constants)
    # print("YAML loaded!")

    # client.run(Config.BOT_TOKEN)
    client.run(GENERAL_SETTINGS['BOT_TOKEN'])


if __name__ == '__main__':
    main()
