import sys
from os import path
# Necessary to run from a batch file unfortunately
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import time
import discord
from discord.ext import commands

from src.commands.CommandHandler import CommandHandler
from src.settings import Config

start_time = time.time()

client = commands.Bot(command_prefix=Config.PREFIX)


@client.event
async def on_ready():  # method that is called when bot is online
    print("[DONE] Bot is now online.")
    end_time = time.time()
    print(f"[DONE] Successfully loaded bot in {end_time - start_time} seconds")
    await client.change_presence(activity=discord.Game(name=Config.BOT_STATUS))


@client.event
async def on_message(ctx):  # method that is called whenever a message is sent into discord server
    await CommandHandler.handle_commands(client, ctx)


def main():  # main function
    client.run(Config.BOT_TOKEN)


if __name__ == '__main__':
    main()
