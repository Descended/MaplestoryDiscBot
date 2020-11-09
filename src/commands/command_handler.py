from discord import Member, Guild, TextChannel

from src.command_logger import Logger
from src.utils import Utils
from src.commands.command import Command
from src.settings import config


class CommandHandler:
    @staticmethod
    async def handle_commands(client, message):
        author = message.author
        msg = message.content
        guild = message.guild
        txt_channel = message.channel

        if not str(msg).startswith(config.PREFIX):
            return

        can_use = author != client

        if not can_use:
            return

        # Get the list of Command methods in the Command module
        cmds = [func for func in dir(Command) if callable(getattr(Command, func)) and not func.startswith("__")]

        if config.LOG_COMMANDS and Utils.is_command(msg.split(" ")[0]):
            # If the message is a command we log it to command_log.txt
            Logger.log_command(author, msg.split(" ")[0])

        for cmd in cmds:
            await getattr(Command, cmd)(client, txt_channel, author, msg, message)
            # Attempt to pass in:
            # client, txt_channel, author, msg, message
            # for every method in the Command module


    @staticmethod
    async def print_stacktrace(client, message, stacktrace):
        author = Member(message.author)
        msg = message.content
        guild = Guild(message.guild)
        txt_channel = TextChannel(message.channel)
        await txt_channel.send(str(stacktrace))
