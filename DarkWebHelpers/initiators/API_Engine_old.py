import requests

from DarkWebHelpers.TorConnectionHandler.TorProprites import headers
from DarkWebHelpers.app import AppConfigurations

config = AppConfigurations()


class Query:
    def __init__(self, query, deepScan=False):
        self.deepScan = deepScan
        self.query = query.strip('\r').replace(' ', '%20')
        self.links = []
        self.data = {}

    def dorkSearch(self):
        return ' AND '.join('"{}"'.format(text) for text in self.query.split())

    @property
    def Links(self) -> list:
        return self.links

    @property
    def Result_Json(self):
        return self.data

    def MakeRequest(self, pagen):
        try:
            self.data.update({self.query: dict()})
            if self.deepScan:
                api_url = f"https://darksearch.io/api/search?query={self.dorkSearch()}&page={pagen}"
                #print(api_url)
            else:
                api_url = f"https://darksearch.io/api/search?query='{self.query}'&page={pagen}"
                #print(api_url)
            req = requests.get(api_url, headers=headers)

            for link in req.json()['data']:
                self.links.append(link.get('link'))

            self.data.get(self.query).update({'PageNum{}'.format(pagen): req.json()})
            config.debug(pagen)
        except requests.exceptions.ConnectionError:
            pass
        except BaseException as e:
            # print(req.text)
            config.debug("Connecting To API Error")
            config.debug(e)
