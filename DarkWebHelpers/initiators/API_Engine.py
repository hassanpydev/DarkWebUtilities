import requests

from DarkWebHelpers.TorConnectionHandler.TorProprites import headers
from DarkWebHelpers.app import AppConfigurations
from DarkWebHelpers.initiators.onionSearchEngine import OnionSearchEngine

config = AppConfigurations()


def isOnionAvailable() -> bool:
    try:
        req = requests.get('https://onionsearchengine.com/')

        # return False if req.status_code != 200 else True
        if req.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        return False


class Query:
    def __init__(self, query, deepScan=True):
        self.deepScan = deepScan
        self.query = query.strip('\r')
        self.links = []
        self.data = {}

    def dorkSearch(self):
        return ' AND '.join('"{}"'.format(text) for text in self.query.split())

    @property
    def Links(self) -> list:
        return list(set(self.links)) # remove duplicate

    @property
    def Result_Json(self):
        return self.data

    def MakeRequest(self, page_number):


        self.data.update({self.query: dict()})
        try:
            if isOnionAvailable():
                onion = OnionSearchEngine(query=self.query, page_number=page_number)
                onion.Search()
                self.links.extend(onion.Links)
                self.data = onion.Result_Json
            # else:
            #     print("Performing API Search")
            #     if self.deepScan:
            #         api_url = f"https://darksearch.io/api/search?query={self.dorkSearch()}&page={page_number}"
            #         # print(api_url)
            #     else:
            #         api_url = f"https://darksearch.io/api/search?query='{self.query}'&page={page_number}"
            #         # print(api_url)
            #     req = requests.get(api_url, headers=headers)
            # 
            #     for link in req.json()['data']:
            #         self.links.append(link.get('link'))
            # 
            #     self.data.get(self.query).update({'PageNum{}'.format(page_number): req.json()})
            #     config.debug(page_number)
        except requests.exceptions.ConnectionError:
            pass
        except BaseException as e:
            # print(req.text)
            config.debug("Connecting To API Error")
            config.debug(e)
