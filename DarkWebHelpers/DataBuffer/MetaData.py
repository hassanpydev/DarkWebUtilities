class MetaData:

    def __init__(self):
        self.emails = []
        self.Videos = []
        self.Phones = []
        self.btc = []
        self.keyword = None

    def Initiates(self, keyword):
        """

        @type keyword: str that the search operation is running on
        """
        self.keyword = keyword

    @property
    def ConvertIntoDict(self) -> dict:
        """

        @return:
        """
        return {self.keyword: {'Emails': list(set(self.emails)),
                               "Videos": list(set(self.Videos)),
                               "Phones": list(set(self.Phones)),
                               "btc": list(set(self.btc))}}

    def ClearData(self):
        self.emails.clear()
        self.Videos.clear()
        self.Phones.clear()
        self.btc.clear()
