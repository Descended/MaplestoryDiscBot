import mysql.connector

from src.settings import Config


class DatabaseHandler:
    """
        Static class that handles all requests/calls to Database
    """

    @staticmethod
    def get_character_stats(character_name):
        try:
            con = mysql.connector.connect(host=Config.DATABASE_HOST, user=Config.DATABASE_USER,
                                          password=Config.DATABASE_PASS, database=Config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM characters WHERE name = '{character_name}'")
            rows = cursor.fetchall()
            con.disconnect()
            return rows, True
        except Exception as e:
            print(e)
            return e, False

    @staticmethod
    def get_character_look(character_id, hair, face, skin):
        con = mysql.connector.connect(host=Config.DATABASE_HOST, user=Config.DATABASE_USER,
                                      password=Config.DATABASE_PASS, database=Config.DATABASE_NAME)
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            f"SELECT * FROM inventoryitems WHERE characterid = '{character_id}' AND inventorytype = '-1'")  # -1 = equipped
        rows = cursor.fetchall()
        itemId = [face, hair]
        for item in rows:  # saves all equipped items in a list
            item_id = item["itemid"]
            itemId.append(item_id)
        con.disconnect()
        url = f"https://maplestory.io/api/{Config.REGION}/{Config.VERSION}/Character/200{skin}/{str(itemId)[1:-1]}/stand1/1".replace(
            " ", "")  # gets the character img
        return url.replace(" ", "")  # removes whitespaces

    @staticmethod
    def get_guild_name(guild_id):
        if guild_id == 0:  # Guildless
            return "None"
        con = mysql.connector.connect(host=Config.DATABASE_HOST, user=Config.DATABASE_USER,
                                      password=Config.DATABASE_PASS, database=Config.DATABASE_NAME)
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            f"SELECT name FROM guilds WHERE guildid = '{guild_id}'")  # gets the guild name through the guild id
        rows = cursor.fetchall()
        guild_name = rows[0]["name"]
        con.disconnect()
        return guild_name

    @staticmethod
    def get_guild_info(name):
        try:
            con = mysql.connector.connect(host=Config.DATABASE_HOST, user=Config.DATABASE_USER,
                                          password=Config.DATABASE_PASS, database=Config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM guilds WHERE name = '{name}'")
            rows = cursor.fetchall()
            con.disconnect()
            return rows, True
        except Exception as e:
            print(e)
            return e, False

    @staticmethod
    def get_alliance_name(alliance_id):
        if alliance_id == 0:
            return "None"
        else:
            con = mysql.connector.connect(host=Config.DATABASE_HOST, user=Config.DATABASE_USER,
                                          password=Config.DATABASE_PASS, database=Config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(f"SELECT name FROM alliance WHERE id = '{alliance_id}'")
            rows = cursor.fetchall()
            alliance_name = rows[0]['name']
            con.disconnect()
            return alliance_name

    @staticmethod
    def get_character_name(id):
        con = mysql.connector.connect(host=Config.DATABASE_HOST, user=Config.DATABASE_USER,
                                      password=Config.DATABASE_PASS, database=Config.DATABASE_NAME)
        cursor = con.cursor(dictionary=True)
        cursor.execute(f"SELECT name FROM characters WHERE id = '{id}'")
        rows = cursor.fetchall()
        character_name = rows[0]['name']
        con.disconnect()
        return character_name

    @staticmethod
    def get_account_id(character_name):
        try:
            con = mysql.connector.connect(host=Config.DATABASE_HOST, user=Config.DATABASE_USER,
                                          password=Config.DATABASE_PASS, database=Config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(f"SELECT accountid from characters WHERE name = '{character_name}'")
            rows = cursor.fetchall()
            if len(rows) == 0:  # checks if character exists
                return False
            account_id = rows[0]['accountid']
            con.disconnect()
            return account_id
        except Exception as e:
            print(e)
            return e

    @staticmethod
    def unban_account(name):
        try:
            id = DatabaseHandler.get_account_id(name)
            if not id:  # checks if id is false which means the character was not found
                return f"Couldn't find {name}"
            con = mysql.connector.connect(host=Config.DATABASE_HOST, user=Config.DATABASE_USER,
                                          password=Config.DATABASE_PASS, database=Config.DATABASE_NAME)
            cursor = con.cursor()
            cursor.execute(f"UPDATE accounts SET banned = -1 WHERE id = '{id}'")
            cursor.execute(f"DELETE FROM macbans WHERE aid = '{id}'")  # aid = account_id
            cursor.execute(f"DELETE FROM ipbans WHERE aid = '{id}'")
            con.commit()
            con.disconnect()
            return f"Successfully unbanned {name}"
        except Exception as e:
            print(e)
            return e

    @staticmethod
    def get_rankings(category):
        """
        Given a SQL Column (i.e. mesos, nx), order it Descending (Greatest to Least) and return the list
        category: string
        Return: dict, boolean
        """
        try:
            con = mysql.connector.connect(host=Config.DATABASE_HOST, user=Config.DATABASE_USER,
                                          password=Config.DATABASE_PASS, database=Config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(f"SELECT name, {category}, job FROM characters WHERE gm <= 0 ORDER BY level DESC")
            rows = cursor.fetchall()
            con.disconnect()
            return rows, True
        except Exception as e:
            print(e)
            return e, False

    @staticmethod
    def get_vp(id):
        try:
            con = mysql.connector.connect(host=Config.DATABASE_HOST, user=Config.DATABASE_USER,
                                          password=Config.DATABASE_PASS, database=Config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(f"SELECT votepoints from accounts WHERE id = '{id}'")
            rows = cursor.fetchall()
            con.disconnect()
            vp = rows[0]["votepoints"]
            return vp
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def give_vp(name, amount):
        try:
            id = DatabaseHandler.get_account_id(name)
            if not id:
                return f"Character {name} not found"
            vp = DatabaseHandler.get_vp(id)
            con = mysql.connector.connect(host=Config.DATABASE_HOST, user=Config.DATABASE_USER,
                                          password=Config.DATABASE_PASS, database=Config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            total = amount + vp
            cursor.execute(f"UPDATE accounts SET votepoints = {total} where id = '{id}'")
            con.commit()
            con.disconnect()
            return f"Successfully gave {amount} votepoints to {name}"
        except Exception as e:
            print(e)
            return Config.DATABASE_OFFLINE_MESSAGE

    @staticmethod
    def get_gm_level(name):
        try:
            con = mysql.connector.connect(host=Config.DATABASE_HOST, user=Config.DATABASE_USER,
                                          password=Config.DATABASE_PASS, database=Config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(
                f"SELECT gm from characters WHERE name = '{name}'")
            # selects gm level, most sources only have it so the characters are gm and not the accounts change this if ur source has account wide gm
            rows = cursor.fetchall()
            if len(rows) == 0:  # checks if character exists
                return False
            level = rows[0]["gm"]  # like mentioned above change this if the name is different
            con.disconnect()
            return level
        except Exception as e:
            print(e)

    @staticmethod
    def set_gm_level(name, level):
        try:
            lvl = DatabaseHandler.get_gm_level(name)
            if lvl is False:
                return f"Character {name} not found"
            if lvl == level:
                return f"{name} is already GM level: {level}"
            con = mysql.connector.connect(host=Config.DATABASE_HOST, user=Config.DATABASE_USER,
                                          password=Config.DATABASE_PASS, database=Config.DATABASE_NAME)
            cursor = con.cursor(dictionary=True)
            cursor.execute(f"UPDATE characters SET gm = {level} where name = '{name}'")
            # updates gm level, most sources only have it so the characters are gm and not the accounts change this if ur source has account wide gm
            con.commit()  # commits all changes to the database
            con.disconnect()
            return f"Successfully gave GM level {level} to: {name}"
        except Exception as e:
            print(e)
            return Config.DATABASE_OFFLINE_MESSAGE
