from DarkWebHelpers.TorConnectionHandler.TorProprites import TorRequest
from DarkWebHelpers.app import AppConfigurations
from bs4 import BeautifulSoup
import os

config = AppConfigurations()




class SiteContent:

    def Remove_ExternalLinks(self):
        FixedHeader = """
    <div class="branding">
          <h1 style="color:red;text-align: center" class="branding-heading">
            <span class="visually-hidden">
             External Links Have Been Omitted Due To Security Reasons!
            </span>
          </h1>
         </div>"""
        new_html = ''
        new_html += FixedHeader
        for line in open(config.HTML_FILE, 'rb').readlines():
            line.strip()
            if line.decode().count('</a>'):
                # config.debug("A tag Found")
                new_html += str(line.decode()).replace('</a>', '')
                new_html += str(line.decode()).replace('<a', '')
            if line.decode().count('href'):
                # config.debug("A tag Found")
                new_html += str(line.decode()).replace('href', 'None')
            else:
                new_html += line.decode()
        return new_html

    def SendContent(self, url):
        req = TorRequest()

        req.CreateRequest(url)
        if req.sate:
            soup = BeautifulSoup(req.ContentHolder, "html.parser")
            with open(config.HTML_FILE, 'wb') as f:
                f.write(soup.prettify().encode())
                f.close()
            if True:
                return self.Remove_ExternalLinks()
        else:
            return False


# os.remove(config.HTML_FILE)
