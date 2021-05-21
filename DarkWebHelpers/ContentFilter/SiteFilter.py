from DarkWebHelpers.db.DB_Handler import SQL_Manger

db = SQL_Manger()
phrases = db.LoadForbiddenPhrases()


class SiteBanned(object):
    def __repr__(self):
        return "A site Filter to avoid porn content"

    def __init__(self, site_url: str) -> None:
        self.site = site_url
        self.ForbiddenSite = phrases
        self.State = None

    def __len__(self):
        return len(self.ForbiddenSite)

    def __CheckUrl(self):
        for keyword in self.ForbiddenSite:
            if self.site.lower().count(keyword):
                self.State = True
                break
        else:
            self.State = False

    def IsForbidden(self):
        self.__CheckUrl()
        return self.State
