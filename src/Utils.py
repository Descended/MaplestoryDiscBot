import json
from ruamel.yaml import YAML
from src.settings import Config
from src.Main import GENERAL_SETTINGS
yaml = YAML(typ="safe", pure=True)


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
        """
            Checks if a given string is a command the bot has.
            Is used to check whether to log a command in command_log.txt
            cmd: string
            Return: boolean
        """
        for command in Config.COMMANDS:
            # if cmd == Config.PREFIX + command:
            if cmd == GENERAL_SETTINGS['PREFIX'] + command:
                return True
        return False

    # Design choice: Have the bot ead the YAML contents into memory, and then hold it in memory,
    #   because when the player base is large, player commands can be quite frequent.
    #   It would not be ideal for the bot to need to perform expensive IO operations too often.
    @staticmethod
    def yaml_load(filepath) -> "Reads the contents of a single-document YAML file":
        """
        Uses the load() function from the ruamel.yaml library to read the contexts of
        a single-document YAML file. Note that only UTF-8 and UTF-16 are supported.
        Author: KOOKIIE

        Args:
            filepath: path to the YAML file

        Returns:
            data: contents of the YAML file
        """
        try:
            with open(filepath, "r") as file_data:
                data = yaml.load(file_data)
        # In case of OS error from invalid file/path
        except Exception as e:
            print(f"Error! The following exception was encountered while trying to read a YAML file: {e}")
        return data

    @staticmethod
    def get_general(data) -> "Get general settings (dict) from config.yaml":
        """
        Obtain the general settings by extracting the relevant dictionary from the nest.
        Author: KOOKIIE

        Args:
            data: contents of the YAML file (extracted with ruamel.yaml)

        Returns:
            general_settings: dictionary of the general settings
        """
        try:
            general_settings = data['general']
            return general_settings
        except Exception as e:
            print(f"Error! The following exception was encountered while trying to get general settings: {e}")
            return -1

    @staticmethod
    def get_connection(data) -> "Get connection settings (tuple of dict) from config.yaml":
        """
        Obtain the connection settings by extracting the relevant dictionaries from the nest
        Author: KOOKIIE

        Args:
            data: contents of the YAML file (extracted with ruamel.yaml)

        Returns:
            db_settings: dictionary of the database settings
            api_settings: dictionary of the proprietary API settings for HeavenMS-based sources
            io_api_settings: dictionary of the Maple.io settings
        """
        try:
            db_settings = data['connection']['database']
            api_settings = data['connection']['API']
            io_api_settings = data['connection']['IO_API']
            return db_settings, api_settings, io_api_settings
        except Exception as e:
            print(f"Error! The following exception was encountered while trying to get connection settings: {e}")
            return -1

    @staticmethod
    def get_toggle(data) -> "Get toggle status of commands (dict) from config.yaml":
        """
        Obtain the toggle status of commands by extracting the relevant dictionary from the nest
        Author: KOOKIIE

        Args:
            data: contents of the YAML file (extracted with ruamel.yaml)

        Returns:
            toggle: dictionary of toggle status of commands
        """
        try:
            toggle = data['toggle']
            return toggle
        except Exception as e:
            print(f"Error! The following exception was encountered while trying to get connection settings: {e}")
            return -1

    @staticmethod
    def get_literals(data) -> "Get String constants (dict) from constants.yaml":
        """
        Obtain the String constants by extracting the relevant dictionary from the nest
        Author: KOOKIIE

        Args:
            data: contents of the YAML file (extracted with ruamel.yaml)

        Returns:
            literals: dictionary of String constants
        """
        try:
            literals = data['literals']
            return literals
        except Exception as e:
            print(f"Error! The following exception was encountered while trying to get connection settings: {e}")
            return -1

    @staticmethod
    def get_info(data) -> "Get server info constants (dict) from constants.yaml":
        """
        Obtain the server info constants by extracting the relevant dictionary from the nest
        Author: KOOKIIE

        Args:
            data: contents of the YAML file (extracted with ruamel.yaml)

        Returns:
            info: dictionary of server info constants
        """
        try:
            info = data['info']
            return info
        except Exception as e:
            print(f"Error! The following exception was encountered while trying to get connection settings: {e}")
            return -1

    @staticmethod
    def get_commands(info) -> "Get commands list from constants.yaml":
        """
        Obtain the commands list by extracting the relevant list from the dictionary
        Author: KOOKIIE

        Args:
            info: dictionary generated by Utils.get_info(data)

        Returns:
            commands: list of commands to log
        """
        try:
            commands = info['COMMANDS']
            return commands
        except Exception as e:
            print(f"Error! The following exception was encountered while trying to get connection settings: {e}")
            return -1

    @staticmethod
    def get_credits(data) -> "Get credit constants (dict) from constants.yaml":
        """
        Obtain the credit constants by extracting the relevant dictionary from the nest
        Author: KOOKIIE

        Args:
            data: contents of the YAML file (extracted with ruamel.yaml)

        Returns:
            credits: dictionary of credit constants
        """
        try:
            credit = data['credits']
            return credit
        except Exception as e:
            print(f"Error! The following exception was encountered while trying to get connection settings: {e}")
            return -1
