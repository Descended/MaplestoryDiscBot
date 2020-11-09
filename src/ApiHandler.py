import requests
from src.settings import Config


class API:
    """
        Static class that handles all requests to API server
    """

    @staticmethod
    def get_server_info():
        try:
            payload = {
                "key": Config.API_KEY
            }
            r = requests.get(f"{Config.API_HOST}info", params=payload)
            return r.text
        except EnvironmentError:
            return Config.OFFLINE_MESSAGE
        except Exception as e:
            print(f"Unknown error encountered whilst fetching server info via web API: \n{e}")
            return e

    @staticmethod
    def dc_player(name):
        try:
            payload = {
                "key": Config.API_KEY,
                "name": name
            }
            r = requests.get(f"{Config.API_HOST}dc", params=payload)
            return r.text
        except EnvironmentError:
            return Config.OFFLINE_MESSAGE
        except Exception as e:
            print(f"Unknown error encountered whilst disconnecting player via web API: \n{e}")
            return e

    @staticmethod
    def bot_check(name):
        return "S"

    @staticmethod
    def whisper(name, message):
        try:
            payload = {
                "key": Config.API_KEY,
                "name": name,
                "message": message
            }
            r = requests.get(f"{Config.API_HOST}whisper", params=payload)
            return r.text
        except EnvironmentError:
            return Config.OFFLINE_MESSAGE
        except Exception as e:
            print(f"Unknown error encountered whilst attempting to whisper via web API: \n{e}")
            return e

    @staticmethod
    def notice(message):
        try:
            payload = {
                "key": Config.API_KEY,
                "message": message
            }
            r = requests.get(f"{Config.API_HOST}notice", params=payload)
            return r.text
        except EnvironmentError:
            return Config.OFFLINE_MESSAGE
        except Exception as e:
            print(f"Unknown error encountered whilst attempting to send in-game notice via web API: \n{e}")
            return e

    @staticmethod
    def duey(item, amount, name):
        try:
            payload = {
                "key": Config.API_KEY,
                "item": item,
                "amount": amount,
                "character": name
            }
            r = requests.get(f"{Config.API_HOST}duey", params=payload)
            return r.text
        except EnvironmentError:
            return Config.OFFLINE_MESSAGE
        except Exception as e:
            print(f"Unknown error encountered whilst attempting to send item(s) in-game via web API: \n{e}")
            return e

    @staticmethod
    def set_gm_level(name, level):
        try:
            payload = {
                "key": Config.API_KEY,
                "level": level,
                "character": name
            }
            r = requests.get(f"{Config.API_HOST}setgmlevel", params=payload)
            return r.text
        except EnvironmentError:
            return Config.OFFLINE_MESSAGE
        except Exception as e:
            print(f"Unknown error encountered whilst attempting to set GM level via web API: \n{e}")
            return e

    @staticmethod
    def give_vp(name, amount):
        try:
            payload = {
                "key": Config.API_KEY,
                "amount": amount,
                "character": name
            }
            r = requests.get(f"{Config.API_HOST}givevp", params=payload)
            return r.text
        except EnvironmentError:
            return Config.OFFLINE_MESSAGE
        except Exception as e:
            print(f"Unknown error encountered whilst attempting to allocate vote points in-game via web API: \n{e}")
            return e

