import os
import shutil
import threading
from random import randrange
from urllib.parse import urlparse

import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from stem import Signal
from stem.control import Controller

from DarkWebHelpers import app

config = app.AppConfigurations()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TorService:
    def __init__(self):
        # self.CheckTor()
        pass

    @staticmethod
    def CheckTor():
        com = os.system('systemctl is-active tor')
        if int(com) == 0:
            pass
        else:
            exit('Tor is off')

    @staticmethod
    def RenewIP():
        with Controller.from_port(port=config.TOR_Control_PORT) as controller:
            controller.authenticate('password')
            controller.signal(Signal.NEWNYM)

    @property
    def proxies(self):
        return {
            'http': f'socks5h://127.0.0.1:{config.TOR_Data_PORT}',
            'https': f'socks5h://127.0.0.1:{config.TOR_Data_PORT}'
        }


class TorRequest(object):
    ContentHolder = None

    def __init__(self):
        self.sate = None
        self.session = requests.Session()
        self.content = None

    @staticmethod
    def download(url, MAIN_DIR):
        config.debug("Image {}".format(url))
        session = requests.Session()
        scheme, netloc, path, _, _, _ = urlparse(url)
        extension = path.split('.')[-1]
        if extension == '/webscreen':
            extension = 'png'

        config.debug(path)
        try:

            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

            req = session.get(url, stream=True, headers=headers, proxies=TorService().proxies)

            if req.status_code == 200:
                # req.raw.decode_content = True
                dir_path = os.path.join(MAIN_DIR, urlparse(url).netloc)
                config.debug(dir_path)
                config.debug(os.path.exists(dir_path))
                if not os.path.exists(dir_path):
                    os.makedirs(str(os.path.join(dir_path)))
                else:
                    pass

                with open(
                        os.path.join(os.path.join(dir_path), f'{randrange(1000000)}.{extension}'), "wb") as image:
                    shutil.copyfileobj(req.raw, image)
                    image.close()
                    # for chunk in req.iter_content(chunk_size=4084):
                    #     if chunk:  # filter out keep-alive new chunks
                    #         image.write(chunk)

                    config.debug('Image successfully Downloaded:\nSaved in: {}, Total Threads: {} '.format(dir_path,
                                                                                                           threading.active_count()))

            else:
                pass
        except BaseException as e:
            config.debug(e)

    def CreateRequest(self, url):
        try:
            if urlparse(url).scheme:
                pass
            else: 
                url = "http://{}".format(url)
            config.debug("Request Sent")
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            self.session.mount('http://', adapter)
            self.session.mount('https://', adapter)
            self.session.trust_env = False
            req = self.session.get(url=url, headers=headers, timeout=10, proxies=TorService().proxies)
            if req.status_code == 200:
                config.debug(req.status_code)
                self.ContentHolder = req.text
                self.sate = True
            else:
                config.debug("Request To {} Responded Back {}--{}".format(url, req.status_code, req.reason))
                self.session.close()
                self.sate = False

        except requests.exceptions.ConnectTimeout as e:
            config.debug(e)
            self.session.close()

        except BaseException as e:
            config.debug(e)
            TorService().RenewIP()
            self.session.close()
        finally:
            return self.sate
