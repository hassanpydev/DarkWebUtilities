import requests
import os

from DarkWebHelpers.app import AppConfigurations
config = AppConfigurations()
class FileHandler:
    def __init__(self, path: os.path):
        if os.path.exists(path):
            self.path = path
        else:
            raise FileNotFoundError

    def Binary_File(self):
        try:
            with  open(self.path, 'rb') as f:
                assert type(f.read()) == bytes
                return f.read()
        except BaseException as e:
            config.debug(e)


class MailGunAttributes:
    API = '5c74deba1f91c91f036fb98215d85cdd-4a62b8e8-11e5f855'
    LINK = 'https://api.mailgun.net/v3/sandbox038fcc0db597430f958823237af26d2b.mailgun.org/messages'
    SENDER = 'Mailgun Sandbox <postmaster@sandbox038fcc0db597430f958823237af26d2b.mailgun.org>'


class CreateMessage(MailGunAttributes):
    def __init__(self, receiver, subject, content, file=False):
        self.receiver = receiver
        self.subject = subject
        self.content = content
        self.file = file

    def Send(self):
        req = requests.post(
            url=self.LINK,
            auth=("api", self.API),
            files=[('attachment', ('Results.txt', open('Results.txt', 'rb').read()))] if self.file else None,
            data={
                "from": self.SENDER,
                "to": [self.receiver, 'hassan@sandbox038fcc0db597430f958823237af26d2b.mailgun.org'],
                "subject": self.subject,
                "text": f"{self.content}"})
        if req.status_code == 200:
            config.debug(req.text)
        else:
            config.debug(req.text)