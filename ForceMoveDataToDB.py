import datetime
import json
import os
from collections import Counter

from DarkWebHelpers.app import AppConfigurations
from DarkWebHelpers.db.DB_Handler import SQL_Manger, Code_Translator

config = AppConfigurations()


class CalculateData:
    def __init__(self, phones: int, site_numbers: int, emails: int, btc: int):
        self.phones = phones
        self.total_site_numbers = site_numbers
        self.emails = emails
        self.TotalContactingByPhone = None
        self.TotalContactingByEmail = None
        self.btc = btc
        self.TotalMarketingByBTC = None
        self.TotalContacting = None

    def Get_Total_Contacting_By_Phone(self):
        return self.phones / self.total_site_numbers * 100.00

    def Get_Total_Contacting_By_Email(self):
        return self.emails / self.total_site_numbers * 100.00

    def Get_Total_Contacting(self):
        return self.Get_Total_Contacting_By_Phone() + self.Get_Total_Contacting_By_Email()

    def Get_Total_btc_deals(self):
        return self.btc / self.total_site_numbers * 100.00


class FacilitateData:
    def __init__(self, metadata: dict = None, statistics: dict = None):
        self.statistics = statistics
        self.metadata = metadata

    @property
    def Total_BTC_numbers(self):
        return self.statistics.get('NumberOfBTC')

    @property
    def Total_Images_numbers(self):
        return self.statistics.get('NumberOfImages')

    @property
    def Total_Emails_numbers(self):
        return self.statistics.get('NumberOfEmails')

    @property
    def Total_Phones_numbers(self):
        return self.statistics.get('NumberOfPhones')

    @property
    def Total_Videos_numbers(self):
        return self.statistics.get('NumberOVideos')

    @property
    def list_of_emails(self):
        return list(set(self.metadata.get('Emails')))

    @property
    def list_of_Videos(self):
        return list(set(self.metadata.get('Videos')))

    @property
    def list_of_Phones(self):
        return list(set(self.metadata.get('Phones')))

    @property
    def list_of_btc(self):
        return list(set(self.metadata.get('btc')))


class CollectData:
    def __init__(self):
        self.keyword = None
        self.statistics = None
        self.metadata = None
        self.user_id = None
        self.totalLinks = int()
        self.key_id = None

    def initialize(self, key, key_id, user_id):

        self.keyword = key.strip().strip('\r')
        self.key_id = key_id  # keywrord id
        self.user_id = user_id
        self.totalLinks = int()
        self.statistics = {self.keyword: {
            "NumberOVideos": 1,
            "NumberOfImages": 1,
            "NumberOfEmails": 1,
            "NumberOfPhones": 1,
            "NumberOfBTC": 1
        }}

        self.metadata = {self.keyword: {"Emails": list(),
                                        "Videos": list(),
                                        "Phones": list(),
                                        "btc": list()}}

    def Update_Metadata(self, dictionary):
        if self.keyword:
            self.metadata.get(self.keyword)
            self.metadata.get(self.keyword)['btc'].extend(list(set(dictionary['btc'])))
            self.metadata.get(self.keyword)['Emails'].extend(list(set(dictionary['Emails'])))
            self.metadata.get(self.keyword)['Phones'].extend(list(set(dictionary['Phones'])))
            self.metadata.get(self.keyword)['Videos'].extend(list(set(dictionary['Videos'])))
        else:
            raise ValueError("Keyword must be specified before updating Metadata")

    def Update_statistics(self, dictionary):
        processed_data = Counter(self.statistics.get(self.keyword)) + Counter(dictionary)
        if processed_data:
            self.statistics = dict({self.keyword: dict(processed_data)})

    def TransferData(self):
        result = FacilitateData(statistics=self.statistics.get(self.keyword), metadata=self.metadata.get(self.keyword))
        # math = CalculateData(result.Total_Phones_numbers, 200, result.Total_Emails_numbers, result.Total_BTC_numbers)
        contact_data = SQL_Manger()
        if contact_data.CheckIfKeyWordExist(self.keyword, self.user_id):
            contact_data.DeleteOldContact_data(keyword=self.keyword, user_id=self.user_id)
            config.debug("Old data Has Been Deleted Data")
            contact_data.InsertTotalResults(self.keyword, str(result.list_of_emails), str(result.list_of_Phones),
                                            str(result.list_of_Videos), str(result.list_of_btc),
                                            result.Total_BTC_numbers - 1,
                                            result.Total_Emails_numbers - 1, result.Total_Videos_numbers - 1,
                                            result.Total_Phones_numbers - 1, result.Total_Images_numbers - 1,
                                            self.totalLinks, 0, 0,
                                            0, 0, self.user_id, datetime.datetime.utcnow(), datetime.datetime.utcnow(),
                                            self.key_id)
        else:
            contact_data.InsertTotalResults(self.keyword, str(result.list_of_emails), str(result.list_of_Phones),
                                            str(result.list_of_Videos), str(result.list_of_btc),
                                            result.Total_BTC_numbers - 1,
                                            result.Total_Emails_numbers - 1, result.Total_Videos_numbers - 1,
                                            result.Total_Phones_numbers - 1, result.Total_Images_numbers - 1,
                                            480, 0, 0,
                                            0, 0, self.user_id, datetime.datetime.utcnow(), datetime.datetime.utcnow(),
                                            self.key_id)

            config.debug("Data Has Been Transferred")

    def Print_Data(self):
        print("Statistics: ", self.statistics)
        print("Metadata: ", self.metadata)
        print("Total Links: ", self.totalLinks)

    def LoadJson(self, filepath):
        try:
            with open(filepath, '+r') as f:
                loader = json.load(f)
                config.debug(loader)
                if filepath.endswith('statistics.json'):
                    self.Update_statistics(loader.get(self.keyword))
                elif filepath.endswith('results.json'):
                    self.Update_Links(loader.get(self.keyword))
                else:
                    self.Update_Metadata(loader.get(self.keyword))
        except BaseException as e:
            config.debug(e)

    def SearchDirectory(self):
        for root, folder, files in os.walk(
                config.GetMeMainPath(self.keyword)):
            for file in files:
                if file.endswith('.json'):
                    self.LoadJson(os.path.join(root, file))

    def Update_Links(self, directory):
        offset = list(directory.keys())[0]
        self.totalLinks += len(directory.get(offset)['data'])


db = SQL_Manger()
DataHolder = CollectData()
keywords = db.ReadWhere(Code_Translator().Done)
for key_id, keyword, user_id, _, _, _, _ in keywords:
    print("Data Found:", key_id, keyword, user_id)
    DataHolder.initialize(keyword, key_id, user_id)
    DataHolder.SearchDirectory()
    DataHolder.TransferData()
    db.UpdateKeywordStatus(user_id=user_id, key_id=key_id, value=Code_Translator().Done)
