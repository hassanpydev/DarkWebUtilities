import os
import shutil
import threading
from random import randrange
from urllib.parse import urlparse, urljoin

import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from DarkWebHelpers.DataBuffer.CollectInformation import CollectInformation
from DarkWebHelpers.DataBuffer.MetaData import MetaData
from DarkWebHelpers.TorConnectionHandler.TorProprites import TorService, headers

WorkSpace_Path = None
tor = TorService()
Collector = CollectInformation()
Collector.Initialize()
metadata = MetaData()
metadata.Initiates()


class ImageDownloader(object):
    def __init__(self, url, base_url):
        self.url = url
        self.base = base_url
        self.path = os.path.join(self.base, WorkSpace_Path)
        self.extension = None
        self.FormatUrl = None
        self.Path()
        self.download()

    def Path(self):
        scheme, netloc, path, _, _, _ = urlparse(self.url)
        self.extension = path.split('.')[-1]
        # print(urlparse(self.url))
        if netloc:
            if not scheme:
                "Check if the url is complete then call download method"
                self.FormatUrl = urljoin('https://', self.url)
            else:
                self.FormatUrl = self.url
        else:
            self.FormatUrl = urljoin('https://' + self.base, self.url)

    def download(self):
        session = requests.Session()
        try:

            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

            req = session.get(self.FormatUrl, stream=True, headers=headers, proxies=tor.proxies)

            if req.status_code == 200:
                # req.raw.decode_content = True
                if not os.path.exists(os.path.join(WorkSpace_Path, self.base)):
                    os.makedirs(str(os.path.join(WorkSpace_Path, self.base)))

                with open(
                        os.path.join(os.path.join(WorkSpace_Path, self.base),
                                     f'{randrange(1000000)}.{self.extension}'),
                        "wb") as image:
                    shutil.copyfileobj(req.raw, image)
                    Collector.NumOfPhotos += 1
                    image.close()
                    # for chunk in req.iter_content(chunk_size=4084):
                    #     if chunk:  # filter out keep-alive new chunks
                    #         image.write(chunk)

                    print('Image successfully Downloaded:\nSaved in: {}, Total Threads: {} '.format(WorkSpace_Path,
                                                                                                    threading.active_count()))

            else:
                req.close()
        except urllib3.exceptions.SSLError:
            session.close()
            pass
        except (
                requests.exceptions.ConnectionError, requests.exceptions.ProxyError,
                requests.exceptions.StreamConsumedError,
                requests.exceptions.HTTPError):
            pass
        except RuntimeError:
            pass
        except urllib3.exceptions.MaxRetryError:
            session.close()
            pass
        except requests.exceptions.ChunkedEncodingError:
            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

            req = session.get(self.FormatUrl, stream=True, headers=headers, proxies=tor.proxies)

            if req.status_code == 200:
                # req.raw.decode_
                # content = True
                if not os.path.exists(os.path.join(WorkSpace_Path, self.base)):
                    os.makedirs(str(os.path.join(WorkSpace_Path, self.base)))

                with open(
                        os.path.join(os.path.join(WorkSpace_Path, self.base),
                                     f'{randrange(1000000)}.{self.extension}'),
                        "wb") as image:
                    shutil.copyfileobj(req.raw, image)
                    Collector.NumOfPhotos += 1
                    image.close()
                    # for chunk in req.iter_content(chunk_size=4084):
                    #     if chunk:  # filter out keep-alive new chunks
                    #         image.write(chunk)

                    print('Image successfully Downloaded:\nSaved in: {}, Total Threads: {} '.format(WorkSpace_Path,
                                                                                                    threading.active_count()))
            req.close()
        except urllib3.exceptions.SSLError:
            session.close()
            pass
        except (
                requests.exceptions.ConnectionError, requests.exceptions.ProxyError,
                requests.exceptions.StreamConsumedError,
                requests.exceptions.HTTPError):
            session.close()
        except RuntimeError as e:
            print(e, 431)
            pass
        except urllib3.exceptions.MaxRetryError:
            session.close()
            pass
        except (ConnectionResetError, ConnectionRefusedError, ConnectionAbortedError):
            session.close()
            pass
        except FileExistsError:
            session.close()
            ...

        except FileExistsError as e:
            session.close()
            print(e)
        except PermissionError as e:
            pass
        except FileNotFoundError:
            pass
        except requests.exceptions.InvalidSchema as e:
            session.close()
            pass
        except ConnectionError as e:
            session.close()
            tor.RenewIP()
            pass
        except IsADirectoryError:
            pass
        except BaseException as e:
            session.close()
            tor.RenewIP()
            try:
                session = requests.Session()
                retry = Retry(connect=3, backoff_factor=0.5)
                adapter = HTTPAdapter(max_retries=retry)
                session.mount('http://', adapter)
                session.mount('https://', adapter)

                req = session.get(self.FormatUrl, stream=True, headers=headers, proxies=tor.proxies)

                if req.status_code == 200:
                    # req.raw.decode_content = True
                    if not os.path.exists(os.path.join(WorkSpace_Path, self.base)):
                        os.makedirs(str(os.path.join(WorkSpace_Path, self.base)))

                    with open(
                            os.path.join(os.path.join(WorkSpace_Path, self.base),
                                         f'{randrange(1000000)}.{self.extension}'),
                            "wb") as image:
                        shutil.copyfileobj(req.raw, image)
                        Collector.NumOfPhotos += 1
                        image.close()
                        # for chunk in req.iter_content(chunk_size=1192):
                        #     if chunk:  # filter out keep-alive new chunks
                        #         image.write(chunk)

                        print(
                            'Image successfully Downloaded:\nSaved in: {}, Total Threads: {} '.format(WorkSpace_Path,
                                                                                                      threading.active_count()))
                req.close()
            except requests.exceptions.InvalidSchema as e:
                session.close()
            except (requests.exceptions.ConnectionError, requests.exceptions.ProxyError,
                    requests.exceptions.StreamConsumedError, requests.exceptions.HTTPError):
                session.close()
            except RuntimeError as e:
                print(e, 496)
            except FileExistsError:
                session.close()
            except urllib3.exceptions.SSLError:
                session.close()
            except urllib3.exceptions.MaxRetryError:
                session.close()
            except IsADirectoryError:
                session.close()

            except FileExistsError as e:
                print(e)
                session.close()
            except PermissionError as e:
                session.close()
            except FileNotFoundError:
                session.close()
                pass
            except ConnectionError as e:
                tor.RenewIP()
                session.close()
                pass
