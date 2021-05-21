import datetime
from pytz import timezone

from DarkWebHelpers.TorConnectionHandler.TorProprites import TorRequest
from DarkWebHelpers.app import AppConfigurations
from DarkWebHelpers.db.DB_Handler import SQL_Manger

config = AppConfigurations()

lastseen = TorRequest()


class Scanner:
    def __init__(self, row):
        self.row = row

    @staticmethod
    def convert():
        # mins, sec = divmod(seconds, 60)
        # hour, min = divmod(mins, 60)
        # m, s = divmod(seconds.total_seconds(), 60)
        # if int(round(m // 60)) > 24:
        #     difference = "{}d".format(int(round(m // 60)) /12)
        #     print(difference)
        #     return difference
        # else:
        #     difference = "{}h:{}m".format(int(round(m // 60)), int(round(m % 60)))
        d = datetime.datetime.today()
        return d.astimezone(timezone('Asia/Riyadh')).strftime("%Y-%m-%d %H:%M:%S")

    def Threader(self):
        # config.debug(self.row)
        try:
            db = SQL_Manger()

            if lastseen.CreateRequest(self.row[1]):
                if self.row[5]:
                    db.UpdateLinks(self.row[0], self.convert(), datetime.datetime.now())
        except BaseException as e:
            config.debug('error===> {}'.format(e))

# ('id', 'int(10) unsigned', 'NO', 'PRI', None, 'auto_increment')
# ('link', 'varchar(255)', 'NO', '', None, '')
# ('keyword', 'varchar(255)', 'NO', '', None, '')
# ('LastSeen', 'varchar(255)', 'NO', '', None, '')
# ('created_at', 'timestamp', 'YES', '', None, '')
# ('updated_at', 'timestamp', 'YES', '', None, '')
