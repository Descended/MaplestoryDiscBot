import sys
from os import path

# Necessary to run from a batch file unfortunately

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import time
import discord
from discord.ext import commands

from src.commands.CommandHandler import CommandHandler
from src.settings import Config
from discord.ext import tasks
from src.ApiHandler import API

start_time = time.time()

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=Config.PREFIX, intents=intents)


# Keep updating every n seconds the amount of online players in server
@tasks.loop(seconds=Config.SEC_PER_UPDATE)
async def track_online_players():
    try:
        await client.change_presence(activity=discord.Game(name=API.get_server_info()))
    except Exception as e:
        print(e)


@client.event
async def on_ready():  # method that is called when bot is online
    print("[DONE] Bot is now online.")
    end_time = time.time()
    print(f"[DONE] Successfully loaded bot in {end_time - start_time} seconds")
    await client.change_presence(activity=discord.Game(name=Config.BOT_STATUS))

    if Config.SHOW_ONLINE_PLAYERS:
        print("Starting online players tracker...")
        track_online_players.start()  # Starting the looping tasks


@client.event
async def on_member_join(member):  # method that is called when a member joins the discord server
    if Config.ADD_ROLE:
        role = discord.utils.get(member.guild.roles, name=Config.ROLE_TO_GIVE)
        print(member.name + " has joined the discord server")
        await member.add_roles(role)


@client.event
async def on_message(ctx):  # method that is called whenever a message is sent into discord server
    await CommandHandler.handle_commands(client, ctx)


def main():  # main function
    client.run(Config.BOT_TOKEN)


if __name__ == '__main__':
    main()
