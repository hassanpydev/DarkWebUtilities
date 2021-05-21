import argparse
import sys

from DarkWebHelpers.GetSiteContent.ContentFetcher import SiteContent

args = argparse.ArgumentParser()
args.add_argument('-l', type=str, required=True)
parser = args.parse_args()
if parser.l:
    content = SiteContent()
    if content.SendContent(url=parser.l):
        sys.stdout.write(content.SendContent(url=parser.l))
    else:
        sys.stdout.write(str(404))
else:
    sys.stderr.write("You must specify a Link!")
