import discord

from src.api_handler import API
from src.utils import Utils
from src.database_handler import DatabaseHandler

from src.commands.command_decorator import command
from src.settings import config
import src.generic_logger as logger
from src.main import spirit_logger as main_logger

spirit_logger = logger.get_logger("main.command")  # Start logging commands


# General and Admin commands
# Note that the return values from commands are not currently used
class Command:
    """
        Class for adding commands

        Structure/Format:

        @staticmethod
        @command(
            cmd=["anycommandnamehere"],  # required; list of command aliases - single String allowed: cmd="my_command"
            toggle=Config.TOGGLE_ON_OFF['handle_foo'],  # optional; enable toggle on/off in config - MUST BE BOOL
            role = ["anyrole"]  # optional; restrict usage to this list of roles - single String allowed
            excl_channel = ["anychanel"]  # optional; ban the use of this command in these channels - single String allowed
            channel = ["anychanel"]  # optional; restrict usage to certain channels - single String allowed
        )
        async def handle_foo(client, txt_channel, author, msg, message) \
            -> "Description of commands go here":
            # CODE GOES HERE
    """

    # -----------------
    # GENERAL COMMANDS
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    @command(
        cmd=["help", "commands"],  # Command Aliases
        toggle=config.TOGGLE_ON_OFF['handle_help']  # Toggle status (use handler method name)
        # channel = ""
        # role = ""
        # excl_channel = ""
        # so other examples for args
    )
    async def handle_help(client, txt_channel, author, msg, message) \
            -> "Shows All Commands":  # Standard Help Command to start it off
        reply = "Commands are prefixed with a {}\n\n".format(config.PREFIX)

        cmds = [func for func in dir(Command) if callable(getattr(Command, func)) and not func.startswith("__")]
        for cmd in sorted(cmds):
            f = getattr(Command, cmd)
            annotations = f.__annotations__
            decorators = f.dec
            if "role" in decorators.keys():
                continue
            help_txt = annotations['return']
            cmd_txt = "/".join(decorators['cmd']) if isinstance(decorators['cmd'], list) else decorators['cmd']
            reply += "{} - {}\n".format(cmd_txt, help_txt)
        e = discord.Embed(title="Commands List", description="List of available commands", colour=config.EMBED_COLOR)
        e.add_field(name="Commands", value=reply, inline=True)
        e.set_thumbnail(url=config.THUMBNAIL_URL)
        e.set_footer(text=f"Bot Version: {config.BOT_VER}\n", icon_url=config.ICON_URL)
        await txt_channel.send(embed=e)
        return True

    @staticmethod
    @command(cmd=["info"], toggle=config.TOGGLE_ON_OFF['handle_info'])
    async def handle_info(client, txt_channel, author, msg, message) \
            -> "Shows server information":
        embed = discord.Embed(title="Server Info", description=config.INFO_VERSION, colour=config.EMBED_COLOR)
        embed.set_thumbnail(url=config.THUMBNAIL_URL)
        embed.add_field(name="Exp", value=config.INFO_EXP, inline=True)  # Exp
        embed.add_field(name="Drop", value=config.INFO_DROP, inline=True)  # Drop
        embed.add_field(name="Meso", value=config.INFO_MESO, inline=True)  # Meso
        embed.add_field(name="Server State", value=config.INFO_STATE, inline=False)
        embed.add_field(name="Server Location", value=config.INFO_LOCATION, inline=False)
        await txt_channel.send(embed=embed)
        return True

    @staticmethod
    @command(
        cmd=["character", "char", "player"],
        toggle=config.TOGGLE_ON_OFF['handle_character']
    )
    async def handle_character(client, txt_channel, author, msg, message) \
            -> "Shows character info":
        args = msg.split(" ")
        if len(args) <= 1:
            await txt_channel.send("Usage: !character <name>")
            return False
        character_name = args[1]
        rows, result = DatabaseHandler.get_character_stats(character_name)
        # A tuple is returned, result being false means the database is off and vice versa

        if not result:
            await txt_channel.send(config.DATABASE_OFFLINE_MESSAGE)
            return False
        elif len(rows) == 0:
            await txt_channel.send("Character not found")
            return False

        # It is always 0, cause no two characters should have the same name.
        char = rows[0]

        id = char["id"]
        name = char["name"]
        level = char["level"]
        job = char["job"]
        str = char["str"]
        dex = char["dex"]
        luk = char["luk"]
        int = char["int"]
        meso = char["meso"]
        rank = char["rank"]
        face = char["face"]
        hair = char["hair"]
        skin = char["skincolor"]  # Other Databases may have this column named "skin", rename accordingly
        guildid = char["guildid"]

        character_img = DatabaseHandler.get_character_look(id, hair, face, skin)  # sends the hair, face and skin id's
        # character_img is a link from maplestory.io API that lets us draw any character given the correct params

        guild_name = DatabaseHandler.get_guild_name(guildid)
        e = discord.Embed(title="Character stats", colour=config.EMBED_COLOR)
        e.set_thumbnail(url=character_img)
        e.set_footer(text=config.SERVER_NAME,
                     icon_url=config.ICON_URL)
        e.add_field(name="Name", value=name, inline=True)
        e.add_field(name="Level", value=level, inline=True)
        e.add_field(name="Job", value=Utils.get_job_by_id(job), inline=True)
        e.add_field(name="STR", value=str, inline=True)
        e.add_field(name="DEX", value=dex, inline=True)
        e.add_field(name="Guild", value=guild_name, inline=True)
        e.add_field(name="LUK", value=luk, inline=True)
        e.add_field(name="INT", value=int, inline=True)
        e.add_field(name="Rank", value=rank, inline=True)
        await txt_channel.send(embed=e)
        return True

    @staticmethod
    @command(
        cmd=["guild", "guildinfo"],
        toggle=config.TOGGLE_ON_OFF['handle_guild']
    )
    async def handle_guild(client, txt_channel, author, msg, message) \
            -> "Shows guild info":
        args = msg.split(" ")
        if len(args) <= 1:
            await txt_channel.send("Usage: !guild <name>")
            return False
        guild_name = args[1]
        rows, result = DatabaseHandler.get_guild_info(guild_name)
        if not result:  # If the result is false the database is offline
            await txt_channel.send(config.DATABASE_OFFLINE_MESSAGE)
            return False
        elif len(rows) == 0:
            await txt_channel.send("Guild not found")
            return False

        # rows[0] because no two guilds will have the same name
        guild_info = rows[0]

        guild = guild_info["name"]
        guild_leader = guild_info["leader"]
        logo = guild_info["logo"]
        logo_color = guild_info["logoColor"]
        logo_bg = guild_info["logoBG"]
        logo_bg_color = guild_info["logoBGColor"]
        notice = guild_info["notice"]
        gp = guild_info["GP"]
        alliance_id = guild_info["allianceId"]

        guild_img = Utils.get_guild_logo(guild_mark_id=logo, guild_mark_color_id=logo_color,
                                         guild_background_id=logo_bg, guild_background_color_id=logo_bg_color)
        e = discord.Embed(title="Guild info", colour=config.EMBED_COLOR)
        e.set_footer(text=config.SERVER_NAME,
                     icon_url=config.ICON_URL)
        e.set_thumbnail(url=guild_img)
        e.add_field(name="Name", value=guild, inline=True)
        e.add_field(name="Leader", value=DatabaseHandler.get_character_name(guild_leader), inline=True)
        e.add_field(name="Alliance", value=DatabaseHandler.get_alliance_name(alliance_id), inline=True)
        e.add_field(name="Notice", value=notice, inline=True)
        await txt_channel.send(embed=e)
        return True

    @staticmethod
    @command(
        cmd=["rankings", "ranking", "ranktop"],
        toggle=config.TOGGLE_ON_OFF['handle_ranking']
    )
    async def handle_ranking(client, txt_channel, author, msg, message) \
            -> "Shows the rankings":
        args = msg.split(" ")
        if len(args) < 2:
            await txt_channel.send("Usage: !rankings <category>")
            # TODO: Add category list
            return False
        category = args[1]
        table, result = DatabaseHandler.get_rankings(category)
        if "column" in str(table):  # checks if the word "column" is in the table this means the column was not found
            await txt_channel.send("Can't find the category")
            return False
        elif not result:
            await txt_channel.send(config.DATABASE_OFFLINE_MESSAGE)
            return False
        e = discord.Embed(title=f"Rankings by {category}", colour=config.EMBED_COLOR)
        e.set_thumbnail(url=config.ICON_URL)
        for x in range(5):
            name = table[x]["name"]
            rank_type = table[x][category]
            job = Utils.get_job_by_id(table[x]["job"])

            e.add_field(name=f"{Utils.get_ordinal_number(x + 1)}.  {name} ({job})", value=f"{category}: {rank_type}",
                        inline=False)
        await txt_channel.send(embed=e)
        return True

    @staticmethod
    @command(
        cmd=["online"],
        toggle=config.TOGGLE_ON_OFF['handle_online']
    )
    async def handle_online(client, txt_channel, author, msg, message) \
            -> "Shows online players":
        online = API.get_server_info()
        await txt_channel.send(online)
        return True

    @staticmethod
    @command(
        cmd=["credits", "credit"],
        toggle=True  # MUST be set to True
    )
    async def handle_credits(client, txt_channel, author, msg, message) \
            -> "Shows the credits":
        credits_info = ""
        for key in config.CREDITS:
            credits_info += f"{key} {config.CREDITS[key]}\n"

        e = discord.Embed(title="Credits", colour=config.EMBED_COLOR, url="https://github.com/Descended"
                                                                          "/MaplestoryDiscBot")
        e.set_thumbnail(url="https://cdn.discordapp.com/emojis/755698200970657863.png?v=1")
        e.add_field(name="Contributors", value=credits_info, inline=True)
        await txt_channel.send(embed=e)
        return True

    # -----------------
    # ADMIN COMMANDS
    # ------------------------------------------------------------------------------------------------------------------

    # Indent is weird because of the commenting
    # @staticmethod
    # @command(
    #     cmd=["duey", "giveitem"],
    #     toggle=Config.TOGGLE_ON_OFF['handle_duey']
    #     role=[Config.ADMIN_ROLE]
    # )
    # async def handle_duey(client, txt_channel, author, msg, message) \
    #         -> "Give items through Duey":
    #     args = msg.split(" ")
    #     if len(args) <= 4:
    #         await txt_channel.send("Usage: !duey <name> <item> <quantity>")
    #         return False
    #     s = API.duey(amount=1, name="Desc")
    #     TODO: sort out logic and remove hard-coding
    #     await txt_channel.send(s)
    #     return True

    @staticmethod
    @command(
        cmd=["dc"],
        toggle=config.TOGGLE_ON_OFF['handle_dc'],
        role=[config.ADMIN_ROLE]
    )
    async def handle_dc(client, txt_channel, author, msg, message) \
            -> "DC a player":
        args = msg.split(" ")
        if len(args) < 2:
            await txt_channel.send("Usage: !dc <character>")
            return False
        player = args[1]
        s = API.dc_player(player)
        await txt_channel.send(s)
        return True

    @staticmethod
    @command(
        cmd=["whisper", "msg"],
        toggle=config.TOGGLE_ON_OFF['handle_whisper'],
        role=[config.ADMIN_ROLE]
    )
    async def handle_whisper(client, txt_channel, author, msg, message) \
            -> "Whisper a player in game":
        args = msg.split(" ")
        if len(args) < 2:
            await txt_channel.send("Usage: !whisper <name> <message>")
            return False
        player = args[1]
        i = 2
        message = ""
        while i < len(args):
            message += args[i] + " "
            i += 1
        m = API.whisper(player, message)
        await txt_channel.send(m)
        return True

    @staticmethod
    @command(
        cmd=["notice"],
        toggle=config.TOGGLE_ON_OFF['handle_notice'],
        role=[config.ADMIN_ROLE]
    )
    async def handle_notice(client, txt_channel, author, msg, message) \
            -> "Send a message to all players":
        args = msg.split(" ")
        if len(args) <= 1:
            await txt_channel.send("Usage: !notice <message>")
            return False
        i = 1
        messag = ""
        while i < len(args):  # for loop to get all arguments
            messag += args[i] + " "
            i += 1
        m = API.notice(messag)
        await txt_channel.send(m)
        return True

    @staticmethod
    @command(
        cmd=["unban", "pardon"],
        toggle=config.TOGGLE_ON_OFF['handle_unban'],
        role=[config.ADMIN_ROLE]
    )
    async def handle_unban(client, txt_channel, author, msg, message) \
            -> "Unbans a player":
        args = msg.split(" ")
        if len(args) < 2:
            await txt_channel.send("Usage: !unban <player>")
            return False
        player = args[1]
        m = DatabaseHandler.unban_account(player)
        await txt_channel.send(m)
        return True

    @staticmethod
    @command(
        cmd=["setgmlevel", "makegm"],
        toggle=config.TOGGLE_ON_OFF['handle_setgmlevel'],
        role=[config.ADMIN_ROLE]
    )
    async def handle_setgmlevel(client, txt_channel, author, msg, message) \
            -> "Makes a player a gm":

        args = msg.split(" ")
        if len(args) < 3:
            await txt_channel.send("Usage: !setgmlevel <player> <level>")
            return False
        player = args[1]
        level = int(args[2])
        r = API.set_gm_level(player, level)
        if "Successfully" in r:
            await txt_channel.send(r)
            return True
        else:
            e = DatabaseHandler.set_gm_level(player, level)
            await txt_channel.send(e)
            return True

    @staticmethod
    @command(
        cmd=["givevp", "addvp"],
        toggle=config.TOGGLE_ON_OFF['handle_give_vp'],
        role=[config.ADMIN_ROLE]
    )
    async def handle_give_vp(client, txt_channel, author, msg, message) \
            -> "Gives a player votepoints":

        args = msg.split(" ")
        if len(args) < 3:
            await txt_channel.send("Usage: !givevp <name> <amount>")
            return False
        player = args[1]
        vp = int(args[2])
        r = API.give_vp(player, vp)
        if "Server is" or "found" in r:
            r = DatabaseHandler.give_vp(player, vp)
        await txt_channel.send(r)
        return True

    # Indent is weird because of the commenting
    # @staticmethod
    # @command(
    #     cmd=["giveaway", "ga"],
    #     toggle=Config.TOGGLE_ON_OFF['handle_giveaway']
    #     role=[Config.ADMIN_ROLE]
    # )
    # async def handle_giveaway(client, txt_channel, author, msg, message) \
    #         -> "Starts a giveaway":
    #   args = msg.split(" ")
    #   if len(args) <= 1:
    #       await txt_channel.send("Usage: !giveaway <time in minutes> <description>")
    #       return
    #   else:
    #       duration = args[1]
    #       i = 2
    #       details = ""
    #       while i < len(args):
    #           details += args[i] + " "
    #            i += 1
    #   emoji = "🎉"
    #   end_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=float(duration))
    #   e = discord.Embed(title=details, description=f'React with  {emoji}  to win!', color=Config.EMBED_COLOR,
    #                       timestamp=end_time)
    #   e.set_footer(icon_url=Config.ICON_URL)
    #   bot_msg = await txt_channel.send(embed=e)
    #   await bot_msg.add_reaction(emoji)
    #
    #   await asyncio.sleep(float(duration))
    #   new_msg = await txt_channel.fetch_message(bot_msg.id)
    #   users = await new_msg.reactions[0].users().flatten()
    #   winner = random.choice(users)
    #
    #   while winner == client.user:
    #       winner = random.choice(users)
    #
    #   g = discord.Embed(title=f"{winner} won the giveaway for", description=details, color=Config.EMBED_COLOR)
    #   await txt_channel.send(embed=g)

    @staticmethod
    @command(
        cmd=["startlogging", "startlog", "onlogger"],
        toggle=True,  # Logger access should always be on for staff
        role=[config.ADMIN_ROLE]
    )
    async def handle_logger_on(client, txt_channel, author, msg, message) \
            -> "Turns the advanced logger on":
        try:
            main_logger.addHandler(logger.get_console_handler())
            main_logger.addHandler(logger.get_file_handler())
            main_logger.propagate = True
            main_logger.info("Logger turned on!")
            config.LOG_FLAG = True
            return True
        except Exception as e:
            print(f"Error occurred whilst trying to turn logger on: \n{e}")
            return False

    @staticmethod
    @command(
        cmd=["stoplogging", "stoplog", "offlogger"],
        toggle=True,  # Logger access should always be on for staff
        role=[config.ADMIN_ROLE]
    )
    async def handle_logger_off(client, txt_channel, author, msg, message) \
            -> "Turns the advanced logger off":
        try:
            main_logger.info("Turning logger off!")
            main_logger.removeHandler(logger.get_console_handler())
            main_logger.removeHandler(logger.get_file_handler())
            main_logger.propagate = False
            config.LOG_FLAG = False
            return True
        except Exception as e:
            print(f"Error occurred whilst trying to turn logger off: \n{e}")
            return False
