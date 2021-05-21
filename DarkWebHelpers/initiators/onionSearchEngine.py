import requests
from bs4 import BeautifulSoup

from DarkWebHelpers.app import AppConfigurations

config = AppConfigurations()


class ResultManger(list):
    """A class to manipulate results and remove duplication from list
        self.RemoveDuplicate delete repeated values from list depending on the link key"""

    def __repr__(self):
        return "Result Manager"

    def RemoveDuplicate(self) -> list:
        clean_data = []  # Unique data are saved here
        checksum = []  # save links here to ensure not to save redundant data
        for value in self:
            if value.get('link') in checksum:
                pass
            else:
                clean_data.append(value)
                checksum.append(value.get('link'))
        return clean_data


class RequestDispatcher:
    @staticmethod
    def MakeRequest(target: str, json=False, headers=None):
        if headers is None:
            headers = dict()
        try:
            req = requests.get(target, headers=headers)
            if req.status_code == 200:
                if json:
                    return req.json()
                return req.text
        except BaseException as e:

            config.debug(e)


class OnionScraper:
    def __init__(self, sourcePage):
        self.sourcePage = sourcePage
        self.links = []
        self.data = ResultManger()

    @staticmethod
    def GetlinksAndTitlesAndDescription(obj: list, data_type: str = 'description') -> list:
        """ :param data_type: a value refers to if the operation is for links, titles or description
            :type obj: a 'a' tag
        """
        temp_list = list()
        if data_type == 'links':
            for link in obj:
                links_soup = BeautifulSoup(str(link), 'html.parser')
                link_to_process = str(links_soup.find('a').get_attribute_list('href')[0])
                if link_to_process.startswith('url.php?'):
                    temp_list.append(link_to_process.split('=')[1])

            return list(set(temp_list))
        elif data_type == 'titles':
            for var in obj:
                temp_list.append(var)
        elif data_type == 'description':
            for var in obj:
                if var.text:
                    temp_list.append(str(var.text).strip().strip('\n').strip('\xa0|'))
                else:
                    temp_list.append('Unavailable')
        return temp_list

    def ExtractData(self, html_code) -> None:
        """:type html_code: string
           extract titles and links from html code
        """

        soup = BeautifulSoup(html_code, 'html.parser')
        link = soup.find_all('html')[0].find('body').findAll('table')[1].find_all('tr')[0].find_all('td')[
            1].find_all('a')
        title = soup.find_all('html')[0].find('body').findAll('table')[1].find_all('tr')[0].find_all('td')[
            1].find_all('b')
        if all([link, title]):
            total_links = self.GetlinksAndTitlesAndDescription(link, data_type='links')
            total_titles = self.GetlinksAndTitlesAndDescription(title, data_type='titles')
            description = soup.find_all('html')[0].find('body').findAll('table')[1].find_all('tr')[0].find_all('td')[
                1].find_all('br')
            total_descriptions = self.GetlinksAndTitlesAndDescription(description, data_type='description')
            if any([total_titles.__len__() == 0 or total_links.__len__() == 0]):
                pass
            else:
                for index, value in enumerate(total_links):
                    if value:
                        self.data.append(
                            dict(title=total_titles[index].text, link=value, description=total_descriptions[index]))
                    self.links.append(value)
                    if config.DEBUG:
                        print(value, total_titles[index].text, total_descriptions[index])
        else:
            pass


class OnionSearchEngine(RequestDispatcher, OnionScraper):

    def __init__(self, query: str, page_number: int):
        super().__init__(RequestDispatcher)
        """

        :type page_number: int
        :type query: str
        """

        self.query = query.strip('\r')
        self.page_number = page_number
        self.FinalData = {}
        self.OnionSearchEngine = 'https://onionsearchengine.com/search.php?search={}&submit=Search&page={}'.format(
            self.query, self.page_number)

    def Remove_duplicate(self, data: list):
        return self.data

    @property
    def Links(self) -> list:
        return list(set(self.links))

    @property
    def Result_Json(self):
        inner_dict = {'total': 10 * 24, 'per_page': self.links.__len__(), 'current_page': self.page_number,
                      'last_page': 24, 'from': 1,
                      'to': 24, 'data': self.data.RemoveDuplicate()}
        self.FinalData.update({self.query: dict()})
        self.FinalData.get(self.query).update({f'PageNum{self.page_number}': inner_dict})
        return self.FinalData

    def Search(self):
        try:
            html_code = self.MakeRequest(target=self.OnionSearchEngine)
            self.ExtractData(html_code)
        except IndexError as e:
            print(["ERROR SCRAPING ONION NO RESULTS"], e)
        except BaseException as e:
            print(["ERROR SCRAPING ONION"], e)
