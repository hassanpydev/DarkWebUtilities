from DarkWebHelpers.db.DB_Handler import SQL_Manger
from DarkWebHelpers.GetSiteContent.ContentFetcher import SiteContent
from DarkWebHelpers.PDF.PDF_Creator import Create
from DarkWebHelpers.app import AppConfigurations
config = AppConfigurations()
def Run():
    db = SQL_Manger()
    for user_data in db.ReadReminder():
        RAW_PDF_DATA = SiteContent().SendContent(user_data[1])
        email = db.GetUserEmailByID(user_id=user_data[2])
        if RAW_PDF_DATA:
            if Create():
                # db.UpdateReminder(user_data[2])
                pass
    # config.TempFileRemoval()
Run()