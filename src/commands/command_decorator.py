# Python Decorator
import time
from functools import wraps
from src.settings import config
import src.generic_logger as logger

spirit_logger = logger.get_logger("command.decorator")


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

            spirit_logger.debug(f"author: {author}; msg: {msg}")
            for key, value in kwargs.items():

                # spirit_logger.debug(f"Key: {key}; Value: {value}")
                # Command name check
                # Check if the start of the message matches the command aliases defined in the decorator
                # If not, don't carry out (i.e. empty return)
                if "cmd" in key:
                    # Sanity check - for single String command name (never used, as far as I can tell)
                    # spirit_logger.debug("Performing command name check")
                    if isinstance(value, str):
                        c = "{}{}".format(config.PREFIX, value)
                        if not msg.startswith(c):
                            return
                    elif isinstance(value, list):
                        right_cmd = False
                        for cmd in value:
                            c = "{}{}".format(config.PREFIX, cmd)
                            if msg.startswith(c):
                                right_cmd = True
                                break
                        if not right_cmd:
                            return

                # Toggle status check - KOOKIIE
                if "toggle" in key:
                    # Sanity check - make sure it's of Boolean type
                    # spirit_logger.debug("Performing toggle status check")
                    if isinstance(value, bool):
                        if not value:  # if toggle status is false
                            await txt_channel.send(config.DISABLED_TEXT)  # send out error message, and don't carry out
                            return

                # Role checks
                if "role" in key:  # Role the author must have for the command to be executed
                    # spirit_logger.debug("Performing role check")
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
                    # spirit_logger.debug("Performing channel exclusion check")
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
                    # spirit_logger.debug("Performing channel inclusion check")
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
