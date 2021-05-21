import os
import re
import urllib
from urllib.parse import urlparse, urljoin

import phonenumbers
from bs4 import BeautifulSoup
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

from DarkWebHelpers.DataTracker.BitCoinTracker import Validate
from DarkWebHelpers.app import AppConfigurations

config = AppConfigurations()


class ImageLinkExtractor:
    """A photos scraper based on HTML tag"""

    def __init__(self, Collector):
        self.links = []
        self.Collector = Collector

    @staticmethod
    def Path(base_url: str, url: str):
        scheme, netloc, path, _, _, _ = urlparse(url)
        bscheme, bnetloc, bpath, _, _, _ = urlparse(base_url)
        # print("Base scheme is:",bscheme,bnetloc)
        base = os.path.join(bscheme + '://', bnetloc)

        # print(base)
        if not scheme:
            # print("Scheme was not found:")
            # print(urljoin(base,url))
            return urljoin(base, url)
        else:
            # print("Scheme was Found!!")
            # print(url)
            return url

    def __GetPageSource(self, src, base_url):

        try:
            # r = requests.get(url, proxies=proxies)
            # print(r.status_code, r.reason)

            soup = BeautifulSoup(src, 'html.parser')
            Images = soup.findAll('img')
            # Collector.NumOfPhotos += len ( Images )
            for img in Images:
                # print(img['src'])

                if urllib.parse.unquote((img['src'])).lower().count('icon') or urllib.parse.unquote((img['src'])).count(
                        'base64'):
                    # print(f"Avoid an ICON\n\t{img['src']}")
                    pass
                else:
                    self.links.append(self.Path(base_url=base_url, url=img['src']))
            self.Collector.NumOfPhotos += len(list(set(self.links)))
        except BaseException as e:
            config.debug(e)

    @property
    def Links(self):
        return self.links

    def extract(self, src, base_url):
        self.__GetPageSource(src, base_url)


class PhoneNumberScraping:
    """A phone numbers scraper based on regex pattern"""

    def __init__(self, sourcecode):
        self.pattern = r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
        self.sourcecode = sourcecode
        self.PhoneNumbers = list()

    def FindPhoneNumber(self, metadata, Collector) -> None:
        """This function requires a metadata and collector for registering data"""
        for phone in re.finditer(self.pattern, str(self.sourcecode)):
            try:
                if carrier._is_mobile(number_type(phonenumbers.parse(phone.group(), None))):
                    config.debug("Phone Number Found: {}".format(phone.group()))
                    self.PhoneNumbers.append(phone.group())
                    metadata.Phones.append(phone.group())
            except phonenumbers.phonenumberutil.NumberParseException:
                pass
        set(self.PhoneNumbers)
        Collector.PhoneNumbers += len(self.PhoneNumbers)


class VideoLinkExtractor:
    "A Video scraper based on HTML tag"

    def __init__(self, metadata, Collector):
        self.metadata = metadata
        self.TotalVideos = int()
        self.Collector = Collector

    def __GetPageSource(self, sourcePage):
        """ A private method that commence the extraction process
        """
        try:
            soup = BeautifulSoup(sourcePage, 'html.parser')
            iframes = soup.findAll('iframe')
            for iframe in iframes:
                config.debug("Video Found: {}".format(iframe['src']))
                self.metadata.Videos.append(iframe['src'])
            # VideoDownloader(vid['src'],self.base).save()
            # pass
            videos = soup.findAll("video")
            for video in videos:
                config.debug("Video Found: {}".format(video['src']))
                self.metadata.Videos.append(video['src'])
            self.Collector.NumOfVideos += len(videos) + len(iframes)
            set(self.Collector.Videos)
        except BaseException as e:
            config.debug(e)

    def extract(self, sourcePage):
        """Initiates the extraction process
        """
        self.__GetPageSource(sourcePage)

    # @property
    # def Statistics(self) :
    #     """An attribute to holds the Statistics

    #     Returns:
    #         [dict]: [dict that holds the results of the extraction process]
    #     """
    #     return {'TotalVideos' : self.TotalVideos , 'Videos' : self.TotalVideos}


class BitCoinAddress:
    """A Bitcoin Wallet address scraper based on regex pattern"""

    def __init__(self, metadata, Collector):
        self.metadata = metadata
        self.Collector = Collector
        self.pattern = u"[13][a-km-zA-HJ-NP-Z1-9]{25,34}\s"
        self.pattern2 = u"^[13][a-km-zA-HJ-NP-Z0-9]{26,33}$"
        self.btcAddresss = list()

    def FindBtcAdress(self, sourcePage) -> None:
        for btc in re.finditer(self.pattern, str(sourcePage)):

            validator = Validate(btc.group())
            if validator.V():
                config.debug("BTC Address Found: {}".format(btc.group()))
                self.btcAddresss.append(btc.group())
                self.metadata.btc.append(btc.group())
        for btc in re.finditer(self.pattern2, str(sourcePage)):

            validator = Validate(btc.group())
            if validator.V():
                config.debug("BTC Address Found: {}".format(btc.group()))
                self.btcAddresss.append(btc.group())
                self.metadata.btc.append(btc.group())
        set(self.btcAddresss)
        self.Collector.NUmOfBTC += len(self.btcAddresss)

class EmailScraper(object):
    "An email scraper based on regex pattern"

    def __init__(self, metadata, Collector) -> None:
        self.metadata = metadata
        self.Collector = Collector

        self.regexFirst = u"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        self.regexSecond = u"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
        self.Emails = list()

    def FindEmails(self, sourcePage) -> None:
        for email in re.finditer(self.regexFirst, str(sourcePage)):
            if email.group().count('.js') or email.group().count('.png') or email.group().count('html') or email.group().count('image'):
                pass
            else:
                self.Emails.append(email.group())
                self.metadata.emails.append(email.group())
                config.debug("Email Found: {}".format(email.group()))

        for email in re.finditer(self.regexSecond, str(sourcePage)):
            if email.group().count('.js') or email.group().count('.png') or email.group().count('html') or email.group().count('image'):
                pass
            else:
                config.debug("Email Found: {}".format(email.group()))
                self.Emails.append(email.group())
                self.metadata.emails.append(email.group())

        self.Collector.NumOfEmails += len(list(set(self.Emails)))

