# Python Decorator
import time
from functools import wraps
from src.settings import Config


# Credits to Asura, for this beautiful decorator
def command(**kwargs):
    def inner_command(func):
        @wraps(func)
        async def wrapper(*args, **kwargs_wrap):

            if "cmd" not in kwargs.keys():
                return

            client = args[0]
            txt_channel = args[1]
            author = args[2]
            msg = args[3]

            for key, value in kwargs.items():

                # Command name check
                if "cmd" in key:
                    if isinstance(value, str):
                        c = "{}{}".format(Config.PREFIX, value)
                        if not msg.startswith(c):
                            return
                    elif isinstance(value, list):
                        right_cmd = False
                        for cmd in value:
                            c = "{}{}".format(Config.PREFIX, cmd)
                            if msg.startswith(c):
                                right_cmd = True
                                break
                        if not right_cmd:
                            return

                # Role checks
                if "role" in key:  # Role the author must have for the command to be executed
                    if isinstance(value, str):
                        if not author.roles == value:
                            return
                    elif isinstance(value, list):
                        has_role = False
                        roles_list = [roles.name for roles in author.roles]
                        for role in value:
                            if role in roles_list:
                                has_role = True
                                break
                        if not has_role:
                            return


                # Excluding Channel checks
                elif "excl_channel" in key:  # Channel(s) command is not allowed in.
                    if isinstance(value, str):
                        if txt_channel.get_channel_name() == value:
                            return
                    elif isinstance(value, list):
                        excluded_channel = False
                        for channel in value:
                            if txt_channel.get_channel_name() == channel:
                                excluded_channel = True
                                break
                        if excluded_channel:
                            return


                # Channel checks
                elif "channel" in key:  # Channel(s) command must be in.
                    if isinstance(value, str):
                        if not txt_channel.get_channel_name() == value:
                            return
                    elif isinstance(value, list):
                        correct_channel = False
                        for channel in value:
                            if txt_channel.get_channel_name() == channel:
                                correct_channel = True
                                break
                        if not correct_channel:
                            return

            client.last_command = time.time()
            await func(*args, **kwargs_wrap)

        wrapper.dec = kwargs
        return wrapper

    return inner_command
