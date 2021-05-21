import os


class AppConfigurations:
    MAILGUN_API = '64125c2f853be51e315b6ac5d13395f6-e5da0167-7dcab27f'
    MAILGUN_DOMAIN = 'rasidg.com'
    MAILGUN_URL = "https://api.mailgun.net/v3/rasidg.com/messages"
    BANNED_SITES = ['galitsin.ilovecpqmnkzei2ezalbb2zowkdmis4pxz3jp4fgmiqm7vjofrikscad.onion',
       'slavesqd5edenkv6.onion',"video-bbs.pedolnkdbfuaraczdyks5pte6vhdobiapvbefdifp4cwxgyf6ec4czid.onion",
       "incest-mom-and-son.pedolnklqy6jeshhpzk4yyjpwwkdk6qqgyhj4c4nzlzh2myumkfoihid.onion",
       "child-sample-vid.pedolnkdbfuaraczdyks5pte6vhdobiapvbefdifp4cwxgyf6ec4czid.onion",
       "free-bibcam.pedolnklqy6jeshhpzk4yyjpwwkdk6qqgyhj4c4nzlzh2myumkfoihid.onion"]
    TOR_Data_PORT = 9050
    TOR_Control_PORT = 9051
    TOR_ADDRESS = '127.0.0.1'
    MAIN_DIR = r"/DarkWebUtilities/keywords"
    TOR_AUTH = 'hassan1998'
    DATABASE_USER = 'abosaif'
    DATABASE_PASS = 'abosaif123'
    DATABASE_ADDRESS = '127.0.0.1'
    DATABASE_NAME = 'darkweb'
    PAGE_RANGE = 25
    DEBUG =  False
    LASTSEEN_MAX_THREADS = 50
    PATH_TO_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    HTML_FILE = r"/tmp/htmltemp.html"
    PDF_FILE = ""
    THREADING_SLEEP_TIME = 5
    PDF_FILE_PATH = r'C:\Users\PC\Desktop\DarkWebUtilities\temp_files\temp.pdf'

    def TempFileRemoval(self):
        if os.path.exists(self.PDF_FILE_PATH):
            os.remove(self.PDF_FILE_PATH)
        if os.path.exists(self.HTML_FILE):
            os.remove(self.HTML_FILE)

    def debug(self, data):
        if self.DEBUG:
            print("[Debugger]: ", data)
        else:
            pass

    def GetMeMainPath(self, keyword: str):
        path = os.path.join(self.MAIN_DIR, keyword.strip())
        if os.path.exists(path):
            pass
        else:
            os.makedirs(path)
        return path

    def GetMeCurrentPagePath(self, keyword, page_number):
        path = os.path.join(self.GetMeMainPath(keyword), 'pagen{}'.format(page_number))
        if os.path.exists(path):
            pass
        else:
            os.makedirs(path)

        return path
