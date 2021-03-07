import json
import urllib.request

from src.settings import config
import src.generic_logger as logger

spirit_logger = logger.get_logger("command.utils")


def get_ordinal_number(num):
    # spirit_logger.debug("Getting ordinal number")
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        suffix = suffixes.get(num % 10, 'th')
    spirit_logger.debug(f"Ordinal number: {str(num) + suffix}")
    return str(num) + suffix


def get_job_by_id(job_id):
    try:
        # spirit_logger.debug("Getting job by ID")
        with open("src/settings/jobs.json", "r") as json_file:
            data = json.load(json_file)
            job_name = data[str(job_id)]
            spirit_logger.debug(f"Job name: {job_name}")
            return job_name
    except Exception as e:
        spirit_logger.error(f"Error occurred whilst attempting to get job by ID:\n  {e}")
        return "Unknown"


def get_guild_logo(guild_mark_id, guild_mark_color_id, guild_background_id, guild_background_color_id):
    # spirit_logger.debug("Getting guild logo")
    url = f"https://maplestory.io/api/{config.REGION}/{config.VERSION}/GuildMark/background/{guild_background_id}/{guild_background_color_id}/mark/{guild_mark_id}/{guild_mark_color_id}"
    spirit_logger.debug(f"Guild logo: {url}")
    return url


def get_giveaway_info():
    spirit_logger.debug("Getting Giveaway event info")
    return "Soon"


def is_command(cmd):
    """
        Checks if a given string is a command the bot has.
        Is used to check whether to log a command in command_log.txt
        cmd: string
        Return: boolean
    """
    # spirit_logger.debug("Checking if command should be logged")
    for command in config.COMMANDS:
        if cmd == config.PREFIX + command:
            spirit_logger.debug(f"{cmd} should be logged")
            return True
    spirit_logger.debug(f"{cmd} should not be logged")
    return False


# Workaround because String.isascii() was only introduced in Python 3.7
def is_ascii(string):
    try:
        string.encode('ascii')
    except UnicodeEncodeError:
        spirit_logger.debug(f"The string {string} is not ASCII")
        return False
    else:
        spirit_logger.debug(f"The string {string} is indeed ASCII")
        return True
