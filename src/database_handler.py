import mysql.connector

from src.settings import config
import src.generic_logger as logger

spirit_logger = logger.get_logger("command.db")


class DatabaseHandler:
    """
        Static class that handles all requests/calls to Database
    """

    @staticmethod
    def get_character_stats(character_name):
        try:
            # spirit_logger.debug(f"Attempting to get char stats from name via DB: {character_name}")
            con = mysql.connector.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER,
                                          password=config.DATABASE_PASS, database=config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM characters WHERE name = '{character_name}'")
            rows = cursor.fetchall()
            con.disconnect()
            spirit_logger.debug(f"{character_name}'s stats: {rows}")
            return rows, True
        except Exception as e:
            print(f"Error encountered whilst fetching character stats via SQL: \n{e}")
            spirit_logger.error(f"Error encountered whilst fetching character stats via SQL: \n{e}")
            return e, False

    @staticmethod
    def get_character_look(character_id, hair, face, skin):
        try:
            # spirit_logger.debug(f"Attempting to get char look via DB. ID: {character_id}; Hair: {hair}; Face: {face}; Skin: {skin}")
            con = mysql.connector.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER,
                                          password=config.DATABASE_PASS, database=config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(
                f"SELECT * FROM inventoryitems WHERE characterid = '{character_id}' AND inventorytype = '-1'")  # -1 = equipped
            rows = cursor.fetchall()
            itemId = [face, hair]
            for item in rows:  # saves all equipped items in a list
                item_id = item["itemid"]
                itemId.append(item_id)
            con.disconnect()
            url = f"https://maplestory.io/api/{config.REGION}/{config.VERSION}/Character/200{skin}/{str(itemId)[1:-1]}/stand1/1".replace(
                " ", "")  # gets the character img, and strip out whitespaces
            spirit_logger.debug(f"Character {character_id} look: {url}")
            return url
        except Exception as e:
            print(f"Error encountered whilst fetching character look via SQL: \n{e}")
            spirit_logger.error(f"Error encountered whilst fetching character look via SQL: \n{e}")
            return e, False

    @staticmethod
    def get_guild_name(guild_id):
        if guild_id == 0:  # No guild
            # spirit_logger.debug("Invalid guild")
            return "None"
        try:
            # spirit_logger.debug(f"Attempting to get guild name from id: {guild_id}")
            con = mysql.connector.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER,
                                          password=config.DATABASE_PASS, database=config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(
                f"SELECT name FROM guilds WHERE guildid = '{guild_id}'")  # gets the guild name through the guild id
            rows = cursor.fetchall()
            guild_name = rows[0]["name"]
            con.disconnect()
            spirit_logger.debug(f"Guild name: {guild_name}")
            return guild_name
        except Exception as e:
            print(f"Error encountered whilst fetching guild name via SQL: \n{e}")
            spirit_logger.error(f"Error encountered whilst fetching guild name via SQL: \n{e}")
            return e, False

    @staticmethod
    def get_guild_info(name):
        try:
            # spirit_logger.debug(f"Attempting to get guild info from id: {guild_id}")
            con = mysql.connector.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER,
                                          password=config.DATABASE_PASS, database=config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM guilds WHERE name = '{name}'")
            rows = cursor.fetchall()
            con.disconnect()
            spirit_logger.debug(f"Guild info: {rows}")
            return rows, True
        except Exception as e:
            print(f"Error encountered whilst fetching guild info via SQL: \n{e}")
            spirit_logger.error(f"Error encountered whilst fetching guild info via SQL: \n{e}")
            return e, False

    @staticmethod
    def get_alliance_name(alliance_id):
        # spirit_logger.debug(f"Attempting to get alliance info from id: {alliance_id}")
        if alliance_id == 0:
            # spirit_logger.debug("Invalid alliance")
            return "None"
        else:
            try:
                con = mysql.connector.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER,
                                              password=config.DATABASE_PASS, database=config.DATABASE_NAME)
                cursor = con.cursor(dictionary=True)
                cursor.execute(f"SELECT name FROM alliance WHERE id = '{alliance_id}'")
                rows = cursor.fetchall()
                alliance_name = rows[0]['name']
                con.disconnect()
                spirit_logger.debug(f"Alliance name: {alliance_name}")
                return alliance_name
            except Exception as e:
                print(f"Error encountered whilst fetching alliance name via SQL: \n{e}")
                spirit_logger.error(f"Error encountered whilst fetching alliance name via SQL: \n{e}")
                return e, False

    @staticmethod
    def get_character_name(char_id):
        try:
            # spirit_logger.debug(f"Attempting to get character name from id: {char_id}")
            con = mysql.connector.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER,
                                          password=config.DATABASE_PASS, database=config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(f"SELECT name FROM characters WHERE id = '{char_id}'")
            rows = cursor.fetchall()
            character_name = rows[0]['name']
            con.disconnect()
            spirit_logger.debug(f"Character name: {character_name}")
            return character_name
        except Exception as e:
            print(f"Error encountered whilst fetching character name via SQL: \n{e}")
            spirit_logger.error(f"Error encountered whilst fetching character name via SQL: \n{e}")
            return e, False

    @staticmethod
    def get_account_id(character_name):
        try:
            # spirit_logger.debug(f"Attempting to get account ID from character name: {character_name}")
            con = mysql.connector.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER,
                                          password=config.DATABASE_PASS, database=config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(f"SELECT accountid from characters WHERE name = '{character_name}'")
            rows = cursor.fetchall()
            if len(rows) == 0:  # checks if character exists
                return False
            account_id = rows[0]['accountid']
            con.disconnect()
            spirit_logger.debug(f"Account ID: {account_id}")
            return account_id
        except Exception as e:
            print(f"Error encountered whilst fetching account ID via SQL: \n{e}")
            spirit_logger.error(f"Error encountered whilst fetching account ID via SQL: \n{e}")
            return e, False

    @staticmethod
    def unban_account(name):
        try:
            # spirit_logger.debug(f"Attempting to unban account by name: {name}")
            account_id = DatabaseHandler.get_account_id(name)  # Don't use "id" as it is reserved by Python
            if not account_id:  # checks if id is false which means the character was not found
                return f"Couldn't find {name}"
            con = mysql.connector.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER,
                                          password=config.DATABASE_PASS, database=config.DATABASE_NAME)
            cursor = con.cursor()
            cursor.execute(f"UPDATE accounts SET banned = -1 WHERE id = '{account_id}'")
            cursor.execute(f"DELETE FROM macbans WHERE aid = '{account_id}'")  # aid = account_id
            cursor.execute(f"DELETE FROM ipbans WHERE aid = '{account_id}'")
            con.commit()
            con.disconnect()
            spirit_logger.debug(f"Successfully unbanned {name}")
            return f"Successfully unbanned {name}"
        except Exception as e:
            print(f"Error encountered whilst attempting account unban via SQL: \n{e}")
            spirit_logger.error(f"Error encountered whilst attempting account unban via SQL: \n{e}")
            return e, False

    @staticmethod
    def get_rankings(category):
        """
        Given a SQL Column (i.e. mesos, nx), order it Descending (Greatest to Least) and return the list
        category: string
        Return: dict, boolean
        """
        try:
            # spirit_logger.debug(f"Attempting to get rankings by category: {category}")
            con = mysql.connector.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER,
                                          password=config.DATABASE_PASS, database=config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(f"SELECT name, {category}, job FROM characters WHERE gm <= 0 ORDER BY level DESC")
            rows = cursor.fetchall()
            con.disconnect()
            spirit_logger.debug(f"{category} Rankings: {rows}")
            return rows, True
        except Exception as e:
            print(f"Error encountered whilst fetching rankings via SQL: \n{e}")
            spirit_logger.error(f"Error encountered whilst fetching rankings via SQL: \n{e}")
            return e, False

    @staticmethod
    def get_vp(account_id):
        try:
            # spirit_logger.debug(f"Attempting to get vote points by id: {account_id}")
            con = mysql.connector.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER,
                                          password=config.DATABASE_PASS, database=config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(f"SELECT votepoints from accounts WHERE id = '{account_id}'")
            rows = cursor.fetchall()
            con.disconnect()
            vp = rows[0]["votepoints"]
            spirit_logger.debug(f"{account_id} VP: {vp}")
            return vp
        except Exception as e:
            print(f"Error encountered whilst fetching vote points via SQL: \n{e}")
            spirit_logger.error(f"Error encountered whilst fetching vote points via SQL: \n{e}")
            return e, False

    @staticmethod
    def give_vp(name, amount):
        try:
            # spirit_logger.debug(f"Attempting to allocate {amount} vote points by name: {name}")
            account_id = DatabaseHandler.get_account_id(name)
            if not account_id:
                return f"Character {name} not found"
            vp = DatabaseHandler.get_vp(account_id)
            con = mysql.connector.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER,
                                          password=config.DATABASE_PASS, database=config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            total = amount + vp
            cursor.execute(f"UPDATE accounts SET votepoints = {total} where id = '{account_id}'")
            con.commit()
            con.disconnect()
            spirit_logger.debug(f"Successfully gave {amount} vote points to {name}")
            return f"Successfully gave {amount} vote points to {name}"
        except Exception as e:
            print(f"Error encountered whilst allocating vote points via SQL: \n{e}")
            spirit_logger.error(f"Error encountered whilst allocating vote points via SQL: \n{e}")
            return e, False

    @staticmethod
    def get_gm_level(name):
        try:
            # spirit_logger.debug(f"Attempting to get GM level by name: {name}")
            con = mysql.connector.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER,
                                          password=config.DATABASE_PASS, database=config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(
                f"SELECT gm from characters WHERE name = '{name}'")
            # selects gm level, most sources only have it so the characters are gm and not the accounts change this if ur source has account wide gm
            rows = cursor.fetchall()
            if len(rows) == 0:  # checks if character exists
                return False
            level = rows[0]["gm"]  # like mentioned above change this if the name is different
            con.disconnect()
            spirit_logger.debug(f"{name}'s GM level is: {level}")
            return level
        except Exception as e:
            print(f"Error encountered whilst fetching GM level via SQL: \n{e}")
            spirit_logger.error(f"Error encountered whilst fetching GM level via SQL: \n{e}")
            return e, False

    @staticmethod
    def set_gm_level(name, level):
        try:
            # spirit_logger.debug(f"Attempting to set GM level to {level} by name: {name}")
            lvl = DatabaseHandler.get_gm_level(name)
            if lvl is False:
                return f"Character {name} not found"
            if lvl == level:
                return f"{name} is already GM level: {level}"
            con = mysql.connector.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER,
                                          password=config.DATABASE_PASS, database=config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(f"UPDATE characters SET gm = {level} where name = '{name}'")
            # Updates gm level
            # This is on a per-character basis for most sources
            # Change this if ur source uses an account-wide gm system
            con.commit()  # commits all changes to the database
            con.disconnect()
            spirit_logger.debug(f"Successfully set {name}'s GM level to {level}")
            return f"Successfully gave GM level {level} to: {name}"
        except Exception as e:
            print(f"Error encountered whilst setting GM level via SQL: \n{e}")
            spirit_logger.error(f"Error encountered whilst setting GM level via SQL: \n{e}")
            return e, False
