# from DarkWebHelpers.app import AppConfigurations
# config = AppConfigurations()
class CollectInformation:
    """[Class to holds data about search results]
    """

    def __init__(self):
        self.NumOfVideos = int()
        self.NumOfPhotos = int()
        self.NumOfEmails = int()
        self.PhoneNumbers = int()
        self.NUmOfBTC = int()
        self.keyword = None

    def Initialize(self, keyword) -> None:
        """[This functions holds the keywords]

        Args:
            keyword ([str]): [A keyword the used to search for in the Darkweb]
        """
        self.keyword = keyword

    @property
    def ConvertIntoDict(self):
        """[summary]

        Returns:
            [dict]: [returns a dict that contains a metadata about the search operation]
        """
        return {self.keyword: {
            'NumberOVideos': self.NumOfVideos,
            'NumberOfImages': self.NumOfPhotos,
            'NumberOfEmails': self.NumOfEmails,
            'NumberOfPhones': self.PhoneNumbers,
            'NumberOfBTC': self.NUmOfBTC
        }}

    def RestCounter(self):
        self.NumOfVideos = 0
        self.NumOfPhotos = 0
        self.NumOfEmails = 0
        self.PhoneNumbers = 0
        self.NUmOfBTC = 0
