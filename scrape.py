"""
Handling the scraping for each
Adventure Time episode's transcript
"""

import requests
import re
from unidecode import unidecode

from bs4 import BeautifulSoup


class Scraper:
    "There's magic in these words"

    def __init__(self):
        print "Mathematical!"
        self.base_url = 'http://adventuretime.wikia.com'
        self.urls = []

    # # Main # #
    def get_urls(self):
        "Runs through and grabs all the URLs from the table of contents"

        page = requests.get(self.base_url+'/wiki/List_of_episodes').content
        soup = BeautifulSoup(page, 'lxml')
        links = []
        rows = soup.find_all('tr', {'style': 'text-align: center; background: #f2f2f2'})
        for episode_row in rows:
            tail = episode_row.find_all('td')[1].find('a')['href']
            self.urls.append(self.base_url+tail)

        return self.urls

    def get_lines_from_ep_url(self, url):
        "This accesses all the script lines. Luh u bs4"

        page = requests.get(url+'/Transcript').content
        soup = BeautifulSoup(page, 'lxml')
        title = soup.find('div', 'header-container').find('h1').text.split('/')[0]

        if self.urls.index(url) > 187:
            raw_lines = soup.find(id='mw-content-text').find_all('p')
        else:  # the page structure changes here for some reason
            raw_lines = soup.find_all('dd')

        lines = []
        for line in raw_lines:  # used to be a nasty 1 line list comp
            if ':' in line.text and line.text is not None:
                lines.append(unidecode(line.text).replace('\n', ''))
        return (title, lines)

    def chunk_to_dict(self, episode_chunk):
        """
        Takes a list of lines that make up an episode and returns a
        dictionary that maps character name to lines.

        The structure coming in is an episode worth of
            ["<name>: <sentence>", "<name>: <sentence>", ...]  
        and we're spitting out
            {<name>: [<sentence>, ...], <name>: [sentence, ...]}
        """
        names = {}
        for line in episode:
            if ':' not in line or line == ['']:
                continue
            line = line.split(':', 1)
            name, script = line[0].strip().translate(None, ".'"), line[1].strip(' ')
            if '&' in name or 'and' in name:
                continue
            if '/' in name:
                name = name[0:name.find('/')]
            if name == "Pen":
                name = "Finn"
            if name == "Lich":
                name = "The Lich"
            if re.search('[a-zA-Z]', script) != None:
                names.setdefault(name, []).append(script)

        return names

    def write_lines_by_character(self, episode_dict):
        for name in ep_dict.keys():
            with open('raw-data/'+name+'.txt', 'a') as Ooo:
                Ooo.write('\n'.join(ep_dict[name]))

    def write_lines_by_episode(self, index, title, episode_line_list):
        with open('episodes1/'+str(index)+'::'+title, 'w') as episode_file:
            [episode_file.write(line+'\n') for line in episode_line_list]


if __name__ == '__main__':
    AT = Scraper()
    urls = AT.get_urls()
    for index, url in enumerate(urls):
        print index, url
        title, lines = AT.get_lines_from_ep_url(url)
        AT.write_lines_by_episode(index, title, lines)
