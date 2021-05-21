from datetime import datetime

import mysql.connector

from DarkWebHelpers.app import AppConfigurations

"""
SELECT id, keyword, emails ,phones , videos ,btc , btc_count ,
 email_count,video_count,phone_count ,image_count ,total_phone_contact , total_email_contact , total_contact ,
   total_marketing , user_id
   FROM contact_data;
"""

"SELECT * FROM contact_data;\n"

"SELECT * FROM contact_data where keyword='database' and user_id=1;\n"

"""SELECT id, keyword, emails ,phones , videos ,btc , btc_count ,
 email_count,video_count,phone_count ,image_count ,total_phone_contact , total_email_contact , total_contact ,
   total_marketing , user_id
   FROM contact_data where keyword='database' and user_id=1;
"""

"""
UPDATE contact_data SET image_count=100 WHERE keyword='database' && user_id=1
"""

"""
UPDATE contact_data SET image_count=100 , total_phone_contact=10 WHERE keyword='database' && user_id=1

"""


class Code_Translator:
    @property
    def Unsearched(self) -> int:
        """
        attribute to distinguish the state of keyword stat
        @return int :
        """
        return 0

    @property
    def Done(self) -> int:
        return 1

    @property
    def InProcess(self) -> int:
        return 2


config = AppConfigurations()


class SQL_Manger:
    def __init__(self):
        pass

    def AddLinks(self, link: str, keyword, LastSeen, created_at, updated_at):
        """Must update the table to accept user id to avoid data leak """
        try:
            config.debug("Inserting......")
            cur, commiter = self.my_cursor()
            sql = "INSERT INTO links ( link, keyword, LastSeen, created_at, updated_at) VALUES ( %s , %s, %s, %s, %s)"
            values = (link, keyword, LastSeen, created_at, updated_at)
            cur.execute(sql, values)
            commiter.commit()
        except BaseException as e:
            config.debug(e)

    @staticmethod
    def my_cursor():
        try:
            connector = mysql.connector.connect(host=config.DATABASE_ADDRESS, database=config.DATABASE_NAME,
                                                user=config.DATABASE_USER,
                                                password=config.DATABASE_PASS)
            return connector.cursor(), connector
        except mysql.connector.errors.InterfaceError as e:
            config.debug(e)
            exit(code=-1)

    def UpdateReminder(self, user_id):
        print(user_id)
        cur, commiter = self.my_cursor()
        sql = "UPDATE remind_mes SET done = '1' WHERE user_id = {} ".format(int(user_id))
        cur.execute(sql)
        commiter.commit()
    def ReadReminder(self):
        cur, commiter = self.my_cursor()
        sql = "SELECT * FROM remind_mes where done = 0 "
        cur.execute(sql)
        result = cur.fetchall()
        return result

    def GetUserEmailByID(self, user_id):
        cur, commiter = self.my_cursor()
        sql = "SELECT email FROM users where id = {}".format(user_id)
        cur.execute(sql)
        result = cur.fetchone()
        return result[0]

    def ReadWhere(self, value: int) -> tuple:
        """

        :rtype: tuple
        """
        cur, commiter = self.my_cursor()
        """

        @rtype: tuple
        """
        try:
            sql = f"SELECT * FROM keyword WHERE searched ='{value}'"
            cur.execute(sql)
            result = cur.fetchall()
            if True:
                config.debug("Data has been Fetched! Total: {}".format(len(result)))
            commiter.close()
            return result

        except BaseException as e:
            config.debug("Error while Reading\n {}".format(e))
    def Fill(self,phrase):
        try:
            cur, commiter = self.my_cursor()
            sql = "insert into filters (phrase) values ( '{}' )".format(phrase)
            # values = (phrase)
            cur.execute(sql)
            commiter.commit()

        except BaseException as e:
            print(e)

    def CheckIfKeyWordExist(self, keyword, user_id):
        try:
            cur, commiter = self.my_cursor()
            sql = f"select keyword from contact_data where keyword = '{keyword}' and user_id = {user_id}"
            cur.execute(sql)
            results = cur.fetchall()
            if len(results) > 0:
                return True
            else:
                return False

        except BaseException as e:
            print(e)
    def GetEmailByUser_id(self,user_id):
        try:
            cur, commiter = self.my_cursor()
            sql = "select email from users where id = {}".format(user_id)
            result = cur.fetchone()
            return result
        except BaseException as e:
            print(e)

    def DeleteOldContact_data(self, keyword,  user_id):
        try:
            cur, commiter = self.my_cursor()
            # sql = 'UPDATE contact_data SET emails = "{}" and phones = "{}" and videos = "{}" and btc = "{}" and btc_count = {} ' \
            #       ' and email_count = {} and video_count = {} and phone_count = {} and image_count = {} and link_count = {} ' \
            #       ' and updated_at = "{}" where keyword = "{}" and user_id = {}'.format(emails, phones, videos, btc,
            #                                                                        btc_count, email_count,
            #                                                                        video_count, phone_count,
            #                                                                        image_count, link_count,
            #                                                                        datetime.now(), keyword, user_id)
            sql = 'delete from contact_data where keyword = "{}" and user_id = {}'.format(keyword,user_id)
            print(sql)
            cur.execute(sql)
            commiter.commit()
        except BaseException as e:
            print(e)

    def InsertTotalResults(self, keyword, emails, phones, videos, btc, btc_count, email_count, video_count, phone_count,
                           image_count, link_count, total_phone_contact, total_email_contact, total_contact,
                           total_marketing, user_id, created_at, updated_at, keyword_id):
        try:
            cur, commiter = self.my_cursor()
            sql = "insert into contact_data (keyword, emails, phones, videos, btc, btc_count, email_count, video_count,phone_count, image_count,link_count, total_phone_contact, total_email_contact, total_contact, total_marketing, user_id,created_at, updated_at,keyword_id) " \
                  "VALUES ( %s , %s, %s, %s, %s, %s , %s, %s, %s, %s, %s , %s, %s, %s, %s, %s , %s, %s, %s)"
            values = (
                keyword, emails, phones, videos, btc, btc_count, email_count, video_count, phone_count, image_count,
                link_count, total_phone_contact, total_email_contact, total_contact, total_marketing, user_id,
                created_at,
                updated_at, keyword_id)
            cur.execute(sql, tuple(values))
            commiter.commit()

        except BaseException as e:
            config.debug(e)

    def ReadBTC(self):
        addresses = []
        cur, commiter = self.my_cursor()
        cur.execute("SELECT btc,keyword,user_id FROM contact_data")
        my_result = cur.fetchall()

        return my_result

    def UpdateBTC(self, total_received, total_sent, balance, unconfirmed_balance, final_balance, n_tx, unconfirmed_n_tx,
                  final_n_tx, address, user_id):
        cur, commiter = self.my_cursor()
        date = datetime.utcnow()
        config.debug("Date Of updating is: {}".format(date))
        sql = "UPDATE bitcoins SET total_received = '{}' and total_sent = '{}' and balance = '{}' and unconfirmed_balance = '{}'," \
              "final_balance = '{}' and n_tx = '{}' and unconfirmed_n_tx = '{}'and final_n_tx = '{}' and updated_at = '{}' where address = '{}'" \
              " and user_id = '{}' " \
            .format(total_received, total_sent, balance, unconfirmed_balance, final_balance, n_tx, unconfirmed_n_tx,
                    final_n_tx, date, address, user_id)
        update_date = "UPDATE bitcoins SET updated_at = '{}' where address = '{}' and user_id = '{}'".format(date,
                                                                                                             address,
                                                                                                             user_id)
        cur.execute(sql)
        cur.execute(update_date)
        commiter.commit()

    def InsertBTC(self, keyword, address, total_received, total_sent, balance, unconfirmed_balance, final_balance, n_tx,
                  unconfirmed_n_tx,
                  final_n_tx, user_id):
        cur, commiter = self.my_cursor()
        sql = "INSERT INTO bitcoins (keyword, address, total_received, total_sent, balance," \
              " unconfirmed_balance, final_balance, n_tx, unconfirmed_n_tx, final_n_tx, user_id, " \
              "created_at, updated_at) VALUES (%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s)"
        values = (keyword, address, total_received, total_sent, balance, unconfirmed_balance,
                  final_balance, n_tx, unconfirmed_n_tx, final_n_tx, user_id, datetime.utcnow(), datetime.utcnow())
        cur.execute(sql, values)
        commiter.commit()

    @property
    def ReadLinks(self):
        cur, commiter = self.my_cursor()
        cur.execute("SELECT * FROM links")
        my_result = cur.fetchall()
        # self.connector.close()
        return my_result

    def DoseBTCExist(self, address):
        cur, commiter = self.my_cursor()
        cur.execute("SELECT * from bitcoins where address = '{}' ".format(address))
        results = cur.fetchall()
        if results:
            return True
        else:
            return False

    # def ReadWhere(self, value: int) -> tuple:
    #     """
    #
    #     @rtype: tuple
    #     """
    #     try:
    #         cur, commiter = self.my_cursor()
    #         sql = f"SELECT * FROM keyword WHERE searched ='{value}'"
    #         cur.execute(sql)
    #         result = cur.fetchall()
    #         if True:
    #             print("Data has been Fetched! Total: {}".format(len(result)))
    #         commiter.close()
    #         return result
    #
    #     except BaseException as e:
    #         print("Error while Reading\n", e)
    def UpdateKeywordStatus(self, key_id, value, user_id):
        try:
            cur, commiter = self.my_cursor()
            sql = f'UPDATE keyword SET searched = {value} WHERE id = {key_id} and user_id = {user_id}'
            cur.execute(sql)
            commiter.commit()
            config.debug("Status has been changed")
        except BaseException as e:
            config.debug("Error while Updating a row\n {}".format(e))
    def LoadForbiddenPhrases(self):
        try:
            ForbiddenPhrases = []
            cur, commiter = self.my_cursor()
            cur.execute("SELECT phrase FROM filters")
            myresult = cur.fetchall()
            for phrase in myresult:
                ForbiddenPhrases.append(phrase[0])
            return set(ForbiddenPhrases)
        except BaseException as e:
            print(e)
    def UpdateLinks(self, id, lastStat, updated_at=None):
        try:
            cur, commiter = self.my_cursor()
            lastseen_sql = "UPDATE links SET LastSeen = '{}' WHERE id = '{}'".format(lastStat, id)
            # date_sql = "UPDATE links SET updated_at = '{}' WHERE id = '{}'".format(updated_at, id)
            cur.execute(lastseen_sql)
            # self.my_cursor.execute(date_sql)
            commiter.commit()
            # self.connector.close()
            config.debug("Record Updated successfully".title())
            if updated_at:
                date_sql = "UPDATE links SET LastSeen = '{}' WHERE id = '{}'".format(lastStat, id)
                cur.execute(date_sql)
                commiter.commit()
                # self.connector.close()
                config.debug("Record Updated successfully".title())
        except BaseException as e:
            config.debug(e)

# class UpdateDB:
#     def __init__(self):
#         self.mydb = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="root",
#             database="darkweb"
#         )
#         self.mycursor = self.mydb.cursor()
#
#     def Commiter(self, sql):
#         self.mycursor.execute(sql)
#         self.mydb.commit()
#         self.mydb.close()
#
#     def InsertNew(self, keyword, userid, page):
#         try:
#             sql = "INSERT INTO keyword ( key_name, user_id, searched ) VALUES ( %s, %s, %s)"
#             values = (keyword, userid, page, 1)
#             self.mycursor.execute(sql, values)
#             self.mydb.commit()
#             self.mydb.close()
#             config.debug("Keyword has been added: {} {}".format(keyword, page))
#         except BaseException as e:
#             config.debug("Error while Inserting\n {}".format(e))
#
# def DropWhere(self, k, v):
#     try:
#         sql = "DELETE FROM keyword WHERE {} = '{}'".format(k, v)
#         self.Commiter(sql)
#         print("Keyword: {} has been deleted".format(v))
#     except BaseException as e:
#         print("Error while Dropping a row\n", e)

# def ReadWhere(self, value: int) -> tuple:
#     """
#
#     @rtype: tuple
#     """
#     try:
#         sql = f"SELECT * FROM keyword WHERE searched ='{value}'"
#         self.mycursor.execute(sql)
#         result = self.mycursor.fetchall()
#         if True:
#             print("Data has been Fetched! Total: {}".format(len(result)))
#         self.mydb.close()
#         return result
#
#     except BaseException as e:
#         print("Error while Reading\n", e)

