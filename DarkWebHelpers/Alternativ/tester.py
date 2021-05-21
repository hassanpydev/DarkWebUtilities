import csv
import time
from multiprocessing import Pool, cpu_count, current_process, freeze_support
from urllib.parse import quote, unquote, parse_qs, urlparse

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from DarkWebHelpers.TorConnectionHandler.TorProprites import headers, TorService
ENGINES = {
    "ahmia": "http://msydqstlz2kzerdg.onion",
    "darksearchio": "http://darksearch.io",
    "onionland": "http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion",
    "notevil": "http://hss3uro2hsxfogfq.onion",
    "darksearchenginer": "http://7pwy57iklvt6lyhe.onion",
    "phobos": "http://phobosxilamwcg75xt22id7aywkzol6q6rfl2flipcqoc4e4ahima5id.onion",
    "onionsearchserver": "http://oss7wrm7xvoub77o.onion",
    "torgle": "http://submarhglcl66nz6.onion/",
    "torgle1": "http://torgle5fj664v7pf.onion",
    "onionsearchengine": "http://onionf4j3fwqpeo5.onion",
    "tordex": "http://tordex7iie7z2wcg.onion",
    "tor66": "http://tor66sezptuu2nta.onion",
    "tormax": "http://tormaxunodsbvtgo.onion",
    "haystack": "http://haystakvxad7wbk5.onion",
    "multivac": "http://multivacigqzqqon.onion",
    "evosearch": "http://evo7no6twwwrm63c.onion",
    "deeplink": "http://deeplinkdeatbml7.onion",
}

desktop_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) '
    'AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
]

supported_engines = ENGINES

def get_parameter(url, parameter_name):
    parsed = urlparse.urlparse(url)
    return parse_qs(parsed.query)[parameter_name][0]

def clear(toclear):
    str = toclear.replace("\n", " ")
    str = ' '.join(str.split())
    return str

def link_finder(engine_str, data_obj):
    global filename
    name = ""
    link = ""
    csv_file = None
    found_links = []

    csv_file = open('filename', 'a', newline='')

    def add_link():
        found_links.append({"engine": engine_str, "name": name, "link": link})
        field_delim = ","
        csv_writer = csv.writer(csv_file, delimiter=field_delim, quoting=csv.QUOTE_ALL)
        fields = {"engine": engine_str, "name": name, "link": link}
        line_to_write = []
        line_to_write.append(fields['engine'])
        line_to_write.append(fields['name'])
        line_to_write.append(fields['link'])
        csv_writer.writerow(line_to_write)

    if engine_str == "ahmia":
        for r in data_obj.select('li.result h4'):
            name = clear(r.get_text())
            link = r.find('a')['href'].split('redirect_url=')[1]
            add_link()

    if engine_str == "darksearchenginer":
        for r in data_obj.select('.table-responsive a'):
            name = clear(r.get_text())
            link = clear(r['href'])
            add_link()

    if engine_str == "darksearchio":
        for r in data_obj:
            name = clear(r["title"])
            link = clear(r["link"])
            add_link()

    if engine_str == "deeplink":
        for tr in data_obj.find_all('tr'):
            cels = tr.find_all('td')
            if cels is not None and len(cels) == 4:
                name = clear(cels[1].get_text())
                link = clear(cels[0].find('a')['href'])
                add_link()

    if engine_str == "evosearch":
        for r in data_obj.select("#results .title a"):
            name = clear(r.get_text())
            link = get_parameter(r['href'], 'url')
            add_link()



    if engine_str == "haystack":
        for r in data_obj.select(".result b a"):
            name = clear(r.get_text())
            link = get_parameter(r['href'], 'url')
            add_link()

    if engine_str == "multivac":
        for r in data_obj.select("dl dt a"):
            if r['href'] != "":
                name = clear(r.get_text())
                link = clear(r['href'])
                add_link()
            else:
                break

    if engine_str == "notevil":
        for r in data_obj.find_all("p"):
            r=r.find("a")
            name = clear(r.get_text())
            link = unquote(r["href"]).split('./r2d.php?url=')[1].split('&')[0]
            add_link()


    if engine_str == "onionland":
        for r in data_obj.select('.result-block .title a'):
            if not r['href'].startswith('/ads/'):
                name = clear(r.get_text())
                link = unquote(unquote(get_parameter(r['href'], 'l')))
                add_link()

    if engine_str == "onionsearchengine":
        for r in data_obj.select("table a b"):
            name = clear(r.get_text())
            link = get_parameter(r.parent['href'], 'u')
            add_link()

    if engine_str == "onionsearchserver":
        for r in data_obj.select('.osscmnrdr.ossfieldrdr1 a'):
            name = clear(r.get_text())
            link = clear(r['href'])
            add_link()

    if engine_str == "phobos":
        for r in data_obj.select('.serp .titles'):
            name = clear(r.get_text())
            link = clear(r['href'])
            add_link()

    if engine_str == "tor66":
        for i in data_obj.find('hr').find_all_next('b'):
            if i.find('a'):
                name = clear(i.find('a').get_text())
                link = clear(i.find('a')['href'])
                add_link()


    if engine_str == "tordex":
        for r in data_obj.select('.container h5 a'):
            name = clear(r.get_text())
            link = clear(r['href'])
            add_link()

    if engine_str == "torgle":
        for i in data_obj.find_all('ul', attrs={"id": "page"}):
            for j in i.find_all('a'):
                if str(j.get_text()).startswith("http"):
                    link = clear(j.get_text())
                else:
                    name = clear(j.get_text())
            add_link()

    if engine_str == "torgle1":
        for r in data_obj.select("#results a.title"):
            name = clear(r.get_text())
            link = clear(r['href'])
            add_link()

    if engine_str == "tormax":
        for r in data_obj.find_all("section",attrs={"id":"search-results"})[0].find_all("article"):
            name = clear(r.find('a',attrs={"class":"title"}).get_text())
            link = clear(r.find('div',attrs={"class":"url"}).get_text())
            add_link()




    return found_links

def get_tqdm_desc(e_name, pos):
    return "%20s (#%d)" % (e_name, pos)


def get_proc_pos():
    return (current_process()._identity[0]) - 1


def notevil(searchstr):
    results = []
    notevil_url1 = supported_engines['notevil'] + "/index.php?q={}"
    notevil_url2 = supported_engines['notevil'] + "/index.php?q={}&hostLimit=20&start={}&numRows={}&template=0"
    max_nb_page = 20

    # Do not use requests.Session() here (by experience less results would be got)
    req = requests.get(notevil_url1.format(quote(searchstr)), proxies=TorService().proxies, headers=headers)
    soup = BeautifulSoup(req.text, 'html5lib')

    page_number = 1
    last_div = soup.find("div", attrs={"style": "text-align:center"}).find("div", attrs={"style": "text-align:center"})
    if last_div is not None:
        for i in last_div.find_all("a"):
            page_number = int(i.get_text())
        if page_number > max_nb_page:
            page_number = max_nb_page

    pos = get_proc_pos()
    with tqdm(total=page_number, initial=0, desc=get_tqdm_desc("not Evil", pos), position=pos) as progress_bar:
        num_rows = 20
        results = link_finder("notevil", soup)
        progress_bar.update()

        for n in range(2, page_number + 1):
            start = (int(n - 1) * num_rows)
            req = requests.get(notevil_url2.format(quote(searchstr), start, num_rows),
                               proxies=TorService().proxies,
                               headers=headers)
            soup = BeautifulSoup(req.text, 'html5lib')
            results = results + link_finder("notevil", soup)
            progress_bar.update()
            time.sleep(1)

    return results
notevil('isis')