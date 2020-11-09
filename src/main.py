import sys
from os import path
import time
import discord
from discord.ext import commands
from discord.ext import tasks
# Necessary to run from a batch file unfortunately
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.commands.command_handler import CommandHandler
from src.settings import config
from src.api_handler import API
import src.generic_logger as logger

spirit_logger = logger.get_logger("main")
start_time = time.time()

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=config.PREFIX, intents=intents)


# Keep updating every n seconds the amount of online players in server
@tasks.loop(seconds=config.SEC_PER_UPDATE)
async def track_online_players():
    try:
        spirit_logger.debug("Attempting to update with number of players online")
        await client.change_presence(activity=discord.Game(name=API.get_server_info()))
    except Exception as e:
        print(f"Error encountered whilst tracking online players: \n{e}")
        spirit_logger.error("Could not load online players!")


@client.event
async def on_ready():  # method that is called when bot is online
    print("[DONE] Bot is now online.")
    end_time = time.time()
    print(f"[DONE] Successfully loaded bot in {end_time - start_time} seconds")
    spirit_logger.info(f"The bot has successfully loaded! Time taken: {end_time - start_time}s")
    await client.change_presence(activity=discord.Game(name=config.BOT_STATUS))

    if config.SHOW_ONLINE_PLAYERS:
        print("Starting online players tracker...")
        track_online_players.start()  # Starting the looping tasks


@client.event
async def on_member_join(member):  # method that is called when a member joins the discord server
    spirit_logger.debug(f"{member} has joined the server")
    if config.ADD_ROLE:
        spirit_logger.debug(f"Attempting to add role for {member}")
        try:
            role = discord.utils.get(member.guild.roles, name=config.ROLE_TO_GIVE)
            spirit_logger.info(member.name + " has joined the discord server")
            await member.add_roles(role)
        except Exception as e:
            spirit_logger.error(f"Error encountered whilst attempting to assign role: \n{e}")


@client.event
async def on_message(ctx):  # method that is called whenever a message is sent into discord server
    await CommandHandler.handle_commands(client, ctx)


def main():  # main function
    spirit_logger.info("Starting main routine...")
    client.run(config.BOT_TOKEN)


if __name__ == '__main__':
    spirit_logger.info("Logger started up...")
    main()
    spirit_logger.info("Shutting down logger...")
    logger.shutdown_logger()
    spirit_logger.info("Raising system exit...")
    sys.exit(0)
