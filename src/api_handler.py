import requests
from src.settings import config
import src.generic_logger as logger

spirit_logger = logger.get_logger("command.api")


class API:
    """
        Static class that handles all requests to API server
    """

    @staticmethod
    def get_server_info():
        # spirit_logger.debug("Attempting to fetch server info via API")
        try:
            payload = {
                "key": config.API_KEY
            }
            r = requests.get(f"{config.API_HOST}info", params=payload)
            spirit_logger.debug(f"Request: {r.text}")
            return r.text
        except EnvironmentError:
            spirit_logger.error(config.OFFLINE_MESSAGE)
            return config.OFFLINE_MESSAGE
        except Exception as e:
            spirit_logger.error(f"Unknown error encountered whilst fetching server info via web API: \n{e}")
            return e

    @staticmethod
    def dc_player(name):
        # spirit_logger.debug("Attempting to disconnecting player via API")
        try:
            payload = {
                "key": config.API_KEY,
                "name": name
            }
            r = requests.get(f"{config.API_HOST}dc", params=payload)
            spirit_logger.debug(f"Request: {r.text}")
            return r.text
        except EnvironmentError:
            spirit_logger.error(config.OFFLINE_MESSAGE)
            return config.OFFLINE_MESSAGE
        except Exception as e:
            spirit_logger.error(f"Unknown error encountered whilst disconnecting player via web API: \n{e}")
            return e

    @staticmethod
    def bot_check(name):
        spirit_logger.debug("Attempting bot check")
        return "S"

    @staticmethod
    def whisper(name, message):
        # spirit_logger.debug("Attempting to whisper via API")
        try:
            payload = {
                "key": config.API_KEY,
                "name": name,
                "message": message
            }
            r = requests.get(f"{config.API_HOST}whisper", params=payload)
            spirit_logger.debug(f"Request: {r.text}")
            return r.text
        except EnvironmentError:
            spirit_logger.error(config.OFFLINE_MESSAGE)
            return config.OFFLINE_MESSAGE
        except Exception as e:
            spirit_logger.error(f"Unknown error encountered whilst attempting to whisper via web API: \n{e}")
            return e

    @staticmethod
    def notice(message):
        # spirit_logger.debug("Attempting to send in-game notice via API")
        try:
            payload = {
                "key": config.API_KEY,
                "message": message
            }
            r = requests.get(f"{config.API_HOST}notice", params=payload)
            spirit_logger.debug(f"Request: {r.text}")
            return r.text
        except EnvironmentError:
            spirit_logger.error(config.OFFLINE_MESSAGE)
            return config.OFFLINE_MESSAGE
        except Exception as e:
            spirit_logger.error(f"Unknown error encountered whilst attempting to send in-game notice via web API: \n{e}")
            return e

    @staticmethod
    def duey(item, amount, name):
        # spirit_logger.debug("Attempting to send item(s) in-game via API")
        try:
            payload = {
                "key": config.API_KEY,
                "item": item,
                "amount": amount,
                "character": name
            }
            r = requests.get(f"{config.API_HOST}duey", params=payload)
            spirit_logger.debug(f"Request: {r.text}")
            return r.text
        except EnvironmentError:
            spirit_logger.error(config.OFFLINE_MESSAGE)
            return config.OFFLINE_MESSAGE
        except Exception as e:
            spirit_logger.error(f"Unknown error encountered whilst attempting to send item(s) in-game via web API: \n{e}")
            return e

    @staticmethod
    def set_gm_level(name, level):
        # spirit_logger.debug("Attempting to set GM level via API")
        try:
            payload = {
                "key": config.API_KEY,
                "level": level,
                "character": name
            }
            r = requests.get(f"{config.API_HOST}setgmlevel", params=payload)
            spirit_logger.debug(f"Request: {r.text}")
            return r.text
        except EnvironmentError:
            spirit_logger.error(config.OFFLINE_MESSAGE)
            return config.OFFLINE_MESSAGE
        except Exception as e:
            spirit_logger.error(f"Unknown error encountered whilst attempting to set GM level via web API: \n{e}")
            return e

    @staticmethod
    def give_vp(name, amount):
        # spirit_logger.debug("Attempting to allocate vote points in-game via API")
        try:
            payload = {
                "key": config.API_KEY,
                "amount": amount,
                "character": name
            }
            r = requests.get(f"{config.API_HOST}givevp", params=payload)
            spirit_logger.debug(f"Request: {r.text}")
            return r.text
        except EnvironmentError:
            spirit_logger.error(config.OFFLINE_MESSAGE)
            return config.OFFLINE_MESSAGE
        except Exception as e:
            spirit_logger.error(f"Unknown error encountered whilst attempting to allocate vote points in-game via web API: \n{e}")
            return e
