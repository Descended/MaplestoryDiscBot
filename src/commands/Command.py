import asyncio
import random

import discord

import datetime

from src.ApiHandler import API
from src.Utils import Utils
from src.DatabaseHandler import DatabaseHandler

from src.commands.CommandDecorator import command
from src.settings import Config


# General and Admin commands
class Command:
    """
        Class for adding commands

        Structure/Format:

        @staticmethod
        @command(cmd=["anyprefixnamehere"], role = ["anyrole"])
        async def handle_foo(client, txt_channel, author, msg, message) \
            -> "Description of commands go here":
            # CODE GOES HERE
    """

    # -----------------
    # GENERAL COMMANDS
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    @command(
        cmd=["help", "commands"]
        # channel = ""
        # role = ""
        # so other examples for args
    )
    async def handle_help(client, txt_channel, author, msg, message) \
            -> "Shows All Commands":  # Standard Help Command to start it off
        reply = "Commands are prefixed with a {}\n\n".format(Config.PREFIX)

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

        reply += f"Bot Version: {Config.BOT_VER}\n"
        await txt_channel.send(reply)
        return True

    @staticmethod
    @command(
        cmd=["character", "char", "player"]
    )
    async def handle_character(client, txt_channel, author, msg, message) \
            -> "Shows character info":
        args = msg.split(" ")
        if len(args) <= 1:
            await txt_channel.send("Usage: !character <name>")
            return False
        character_name = args[1]
        rows, result = DatabaseHandler.get_character_stats(character_name)
        if not result:
            await txt_channel.send(Config.DATABASE_OFFLINE_MESSAGE)
            return False
        elif len(rows) == 0:
            await txt_channel.send("Character not found")
            return False
        for row in rows:  # Gets the row values
            id = row["id"]
            name = row["name"]
            level = row["level"]
            job = row["job"]
            str = row["str"]
            dex = row["dex"]
            luk = row["luk"]
            int = row["int"]
            meso = row["meso"]
            rank = row["rank"]
            face = row["face"]
            hair = row["hair"]
            skin = row["skincolor"]
            guildid = row["guildid"]
        character_img = DatabaseHandler.get_character_look(id, hair, face, skin)  # sends the hair, face and skin id's
        guild_name = DatabaseHandler.get_guild_name(guildid)
        e = discord.Embed(title="Character stats", colour=Config.EMBED_COLOR)
        e.set_thumbnail(url=character_img)
        e.set_footer(text=Config.SERVER_NAME,
                     icon_url=Config.ICON_URL)
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
        cmd=["guild", "guildinfo"]
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
            await txt_channel.send(Config.DATABASE_OFFLINE_MESSAGE)
            return False
        elif len(rows) == 0:
            await txt_channel.send("Guild not found")
            return False
        for info in rows:  # gets all guild info
            guild = info["name"]
            guild_leader = info["leader"]
            logo = info["logo"]
            logo_color = info["logoColor"]
            logo_bg = info["logoBG"]
            logo_bg_color = info["logoBGColor"]
            notice = info["notice"]
            gp = info["GP"]
            alliance_id = info["allianceId"]
        guild_img = Utils.get_guild_logo(guild_mark_id=logo, guild_mark_color_id=logo_color,
                                         guild_background_id=logo_bg, guild_background_color_id=logo_bg_color)
        e = discord.Embed(title="Guild info", colour=Config.EMBED_COLOR)
        e.set_footer(text=Config.SERVER_NAME,
                     icon_url=Config.ICON_URL)
        e.set_thumbnail(url=guild_img)
        e.add_field(name="Name", value=guild, inline=True)
        e.add_field(name="Leader", value=DatabaseHandler.get_character_name(guild_leader), inline=True)
        e.add_field(name="Alliance", value=DatabaseHandler.get_alliance_name(alliance_id), inline=True)
        e.add_field(name="Notice", value=notice, inline=True)
        await txt_channel.send(embed=e)
        return True

    @staticmethod
    @command(
        cmd=["rankings", "ranking", "ranktop"]
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
        if "column" in str(table):  # checks if the word "column" is in the table this means the column was not foound
            await txt_channel.send("Can't find the category")
            return False
        elif not result:
            await txt_channel.send(Config.DATABASE_OFFLINE_MESSAGE)
            return False
        e = discord.Embed(title=f"Rankings by {category}", colour=Config.EMBED_COLOR)
        e.set_thumbnail(url=Config.ICON_URL)
        for x in range(5):
            name = table[x]["name"]
            type = table[x][category]
            job = Utils.get_job_by_id(table[x]["job"])
            e.add_field(name=f"{Utils.get_ordinal_number(x + 1)}.  {name} ({job})", value=f"{category}: {type}",
                        inline=False)
        await txt_channel.send(embed=e)
        return True

    @staticmethod
    @command(
        cmd=["online"]
    )
    async def handle_online(client, txt_channel, author, msg, message) \
            -> "Shows online players":
        online = API.get_server_info()
        await txt_channel.send(online)
        return True

    @staticmethod
    @command(
        cmd=["credits", "credit"]
    )
    async def handle_credits(client, txt_channel, author, msg, message) \
            -> "Shows the credits":

        credits_info = ""
        for key in Config.CREDITS:
            credits_info += f"{key} {Config.CREDITS[key]}\n"

        e = discord.Embed(title="Credits", colour=Config.EMBED_COLOR, url="https://github.com/Descended"
                                                                          "/MaplestoryDiscBot")
        e.set_thumbnail(url="https://cdn.discordapp.com/emojis/755698200970657863.png?v=1")
        e.add_field(name="Contributors", value=credits_info, inline=True)
        await txt_channel.send(embed=e)
        return True

    # -----------------
    # ADMIN COMMANDS
    # ------------------------------------------------------------------------------------------------------------------

    # @staticmethod
    # @command(
    #     cmd=["duey", "giveitem"],
    #     role=[Config.ADMIN_ROLE]
    # )
    # async def handle_duey(client, txt_channel, author, msg, message) \
    #         -> "Give items through Duey":
    #     args = msg.split(" ")
        # if len(args) <= 4:
        #     await txt_channel.send("Usage: !duey <name> <item> <quantity>")
        #     return
        # s = API.duey(amount=1, name="Desc")
        # TODO: sort out logic and remove hard-coding
        # await txt_channel.send(s)
        # return True

    @staticmethod
    @command(
        cmd=["dc"],
        role=[Config.ADMIN_ROLE]
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
        role=[Config.ADMIN_ROLE]
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
        role=[Config.ADMIN_ROLE]
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
        role=[Config.ADMIN_ROLE]
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
        role=[Config.ADMIN_ROLE]
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
        if "Server is" or "found" in r:
            r = DatabaseHandler.set_gm_level(player, level)
        await txt_channel.send(r)
        return True

    @staticmethod
    @command(
        cmd=["givevp", "addvp"],
        role=[Config.ADMIN_ROLE]
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

    # @staticmethod
    # @command(
    #     cmd=["giveaway", "ga"],
    #     role=[Config.ADMIN_ROLE]
    # )
    # async def handle_giveaway(client, txt_channel, author, msg, message) \
    #         -> "Starts a giveaway":
    #     args = msg.split(" ")
    #     if len(args) <= 1:
    #         await txt_channel.send("Usage: !giveaway <time in minutes> <description>")
    #         return
    #     else:
    #         duration = args[1]
    #         i = 2
    #         details = ""
    #         while i < len(args):
    #             details += args[i] + " "
    #             i += 1
    #     emoji = "🎉"
    #     end_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=float(duration))
    #     e = discord.Embed(title=details, description=f'React with  {emoji}  to win!', color=Config.EMBED_COLOR,
    #                       timestamp=end_time)
    #     e.set_footer(icon_url=Config.ICON_URL)
    #     bot_msg = await txt_channel.send(embed=e)
    #     await bot_msg.add_reaction(emoji)
    #
    #     await asyncio.sleep(float(duration))
    #     new_msg = await txt_channel.fetch_message(bot_msg.id)
    #     users = await new_msg.reactions[0].users().flatten()
    #     winner = random.choice(users)
    #
    #     while winner == client.user:
    #         winner = random.choice(users)
    #
    #     g = discord.Embed(title=f"{winner} won the giveaway for", description=details, color=Config.EMBED_COLOR)
    #     await txt_channel.send(embed=g)

