import threading
from time import sleep

from DarkWebHelpers.DataTracker.LastSeen import Scanner
from DarkWebHelpers.app import AppConfigurations
from DarkWebHelpers.db.DB_Handler import SQL_Manger

config = AppConfigurations()
def Run():
    db = SQL_Manger()
    for row in db.ReadLinks:
        scanner = Scanner(row)
        thread = threading.Thread(target=scanner.Threader)
        thread.setDaemon(True)
        thread.start()
        while threading.active_count() >= config.LASTSEEN_MAX_THREADS:
            config.debug(threading.active_count())
            sleep(config.THREADING_SLEEP_TIME)

Run()
