import json

from src.settings import Config


class Utils:

    @staticmethod
    def get_ordinal_number(num):
        SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}
        if 10 <= num % 100 <= 20:
            suffix = 'th'
        else:
            suffix = SUFFIXES.get(num % 10, 'th')
        return str(num) + suffix

    @staticmethod
    def get_job_by_id(id):
        with open("settings/jobs.json", "r") as json_file:
            data = json.load(json_file)
            job_name = data[str(id)]
        return job_name

    @staticmethod
    def get_guild_logo(guild_mark_id, guild_mark_color_id, guild_background_id, guild_background_color_id):
        url = f"https://maplestory.io/api/{Config.REGION}/{Config.VERSION}/GuildMark/background/{guild_background_id}/{guild_background_color_id}/mark/{guild_mark_id}/{guild_mark_color_id}"
        return url

    @staticmethod
    def get_giveaway_info():
        return "Soon"

    @staticmethod
    def is_command(cmd):
        for command in Config.COMMANDS:
            if cmd == Config.PREFIX + command:
                return True
        return False
