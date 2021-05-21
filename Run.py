import datetime
from pytz import timezone
import threading
from queue import Queue
from urllib.parse import urlparse
from multiprocessing import Process
from DarkWebHelpers.ContentFilter.SiteFilter import SiteBanned
from DarkWebHelpers.DataBuffer.CollectInformation import CollectInformation
from DarkWebHelpers.DataBuffer.MetaData import MetaData
from DarkWebHelpers.DataBuffer.TempDataHolder import CollectData
from DarkWebHelpers.FileHandler.FileUtility import write_json, DeleteDuplicate
from DarkWebHelpers.Scrapers.DataScraper import PhoneNumberScraping, EmailScraper, ImageLinkExtractor, BitCoinAddress
from DarkWebHelpers.TorConnectionHandler.TorProprites import TorRequest
from DarkWebHelpers.app import AppConfigurations
from DarkWebHelpers.db.DB_Handler import Code_Translator, SQL_Manger
from DarkWebHelpers.initiators.API_Engine import Query

# from DarkWebHelpers.Mail.SendMail import CreateMessage
# from DarkWebHelpers.Mail.Templates import template

config = AppConfigurations()
code = Code_Translator()
metadata = MetaData()
Collector = CollectInformation()
DownloadBuffer = []
db_manger = SQL_Manger()
keywords = db_manger.ReadWhere(Code_Translator().Unsearched)
len_data = int()
moveToDB = CollectData()


class Config(AppConfigurations):
    DEBUG = True


class ProcessTracker(SQL_Manger):
    def __init__(self):
        pass

    def ReadStatus(self):
        cur, _ = self.my_cursor()
        sql = "select isactive from proccess_state;"
        cur.execute(sql)
        result = cur.fetchone()
        return result[0]

    def MakeDecision(self):
        if self.ReadStatus() == 'running':
            return 'running'
        elif self.ReadStatus() == 'off':
            return 'off'
        else:
            return 'Unknown'

    def ChangeStatus(self, status):
        cur, commiter = self.my_cursor()
        sql = f"update proccess_state set isactive = '{status}' where id = 1"
        cur.execute(sql)
        commiter.commit()


processTracker = ProcessTracker()


def Current_SA_Time():
    d = datetime.datetime.today()
    return d.astimezone(timezone('Asia/Riyadh')).strftime("%Y-%m-%d %H:%M:%S")


def GetSiteContent(url: str) -> None:
    filter = SiteBanned(url)
    if filter.IsForbidden() or urlparse(url).netloc in config.BANNED_SITES:
        config.debug("Site [{}] is Banned".format(urlparse(url).netloc))
    else:
        config.debug(f"function running on {url}")

        req = TorRequest()
        req.CreateRequest(url=url)
        if req.sate:
            phone = PhoneNumberScraping(str(req.ContentHolder))
            phone.FindPhoneNumber(metadata=metadata, Collector=Collector)
            email = EmailScraper(metadata=metadata, Collector=Collector)
            email.FindEmails(req.ContentHolder)
            image = ImageLinkExtractor(Collector=Collector)
            image.extract(req.ContentHolder, base_url=url)
            for image_D_link in image.Links:
                DownloadBuffer.append(image_D_link)
            btc = BitCoinAddress(metadata=metadata, Collector=Collector)
            btc.FindBtcAdress(req.ContentHolder)
        else:
            config.debug("It seems sites are down")


def StartCrawler(query: str, pageID: int) -> None:
    global len_data
    Image_Downloader = TorRequest()
    # main_path = config.GetMeMainPath(query_request)
    current_page = config.GetMeCurrentPagePath(query, pageID)
    metadata.Initiates(query.strip('\r'))
    Collector.Initialize(query.strip('\r'))
    threadsBuffer = []
    DownloadThreadBuffer = []
    query_request = Query(query)
    query_request.MakeRequest(pageID)
    link_queue = Queue()
    image_queue = Queue()
    if query_request.links.__len__() > 0:
        for link in query_request.links:
            db_manger.AddLinks(urlparse(link).scheme + '://' + urlparse(link).netloc, query, Current_SA_Time(),
                               datetime.datetime.now(), datetime.datetime.now())
            link_queue.put(link)
            # GetSiteContent(link,'f')
            thread = threading.Thread(target=GetSiteContent, args=(link_queue.get(),))

            threadsBuffer.append(thread)
        for ths in threadsBuffer:
            ths.daemon = True
            ths.start()
        for thj in threadsBuffer:
            thj.join(timeout=20)

    write_json(current_page, 'statistics', Collector.ConvertIntoDict)
    write_json(current_page, 'MetaData', metadata.ConvertIntoDict)
    write_json(current_page, 'results', query_request.Result_Json)
    config.debug(Collector.ConvertIntoDict)
    config.debug(metadata.ConvertIntoDict)
    if DownloadBuffer.__len__() > 0:
        for image_link in DownloadBuffer:
            image_queue.put(image_link)
            Download_thread = threading.Thread(target=Image_Downloader.download,
                                               args=(
                                                   image_queue.get(),
                                                   current_page))  # initiate photo download thread thread
            DownloadThreadBuffer.append(Download_thread)  # Store Thread To be started later
        for thd in DownloadThreadBuffer:
            thd.daemon = True
            thd.start()
        for thdj in DownloadThreadBuffer:
            thdj.join(timeout=30)
    DownloadBuffer.clear()
    threadsBuffer.clear()
    DownloadThreadBuffer.clear()
    metadata.ClearData()
    Collector.RestCounter()


def main(k, user_id, key_id):
    Codes = Code_Translator()
    print(f" Keyword: {k}, user_id : {user_id}, key_id :{key_id}")
    # email = db_manger.GetUserEmailByID(user_id)
    # msg = CreateMessage(receiver=email, subject="Process started")
    # msg.Send(template.msg1.format(k))
    db_manger.UpdateKeywordStatus(key_id=key_id, value=int(Codes.InProcess), user_id=int(user_id))
    for i in range(1, config.PAGE_RANGE):
        StartCrawler(k, i)
        if len_data == 0:
            break

    db_manger.UpdateKeywordStatus(key_id=key_id, value=Codes.Done, user_id=int(user_id))
    # msg = CreateMessage(receiver=email, subject="Process Ended")
    # msg.Send(msg.Done.format(k))


if __name__ == '__main__':
    if processTracker.MakeDecision() == 'running':
        if keywords.__len__() == 0:
            print("Crawler was running on no keywords shutting down")
            processTracker.ChangeStatus('off')
            exit(0)
        else:

            print(f"[{datetime.datetime.utcnow()}]A process is already running shutting OFF")
            exit(0)
    elif processTracker.MakeDecision() == 'off':
        processTracker.ChangeStatus('running')
        if keywords.__len__() > 0:
            for key in keywords:
                key_id, keyword, user_id, _, _, _, _ = key
                config.debug("Running on {} {} {}".format(key_id, keyword, user_id))
                init_process = Process(target=main, args=(keyword, user_id, key_id))
                init_process.daemon = True
                init_process.start()
                init_process.join()
                init_process.terminate()
                # Invoke Loop Function
            processTracker.ChangeStatus('off')
            DeleteDuplicate()


        else:
            processTracker.ChangeStatus('off')
            exit(0)

    else:
        print("Exited with unknown status")
        exit(-1)
    moveToDB.Run()