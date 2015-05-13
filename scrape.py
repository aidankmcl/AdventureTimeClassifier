"""
Handling the scraping for each 
Adventure Time episode's transcript
"""

import requests
import re
import unicodedata

from bs4 import BeautifulSoup


# # Helpers # #
def ununicode(unicode_string):
    "For handling intermittent Korean"
    return unicodedata.normalize('NFKD', unicode_string).encode('ascii', 'ignore')


def index_character(text, character):
    "This is for getting all indices rather than just the first encounter"
    return [i for i, letter in enumerate(text) if letter == character]


def filter_repeats(links):
    seen = set()
    seen_add = seen.add
    return [link for link in links if not (link in seen or seen_add(link))]


def clean(line):
    """
    There are 2 tricky bits about cleaning up the transcripts
    which are:
        1. Lady Rainicorn's speech is Korean and
        needs to be encoded as ascii while the translation is
        Surrounded by ("quotes and parenthesis")
        2. Character [actions inside brackets] are
        sprinkled throughout, and we don't want those.
    I'm first cutting out [actions] and then stripping
    quotation marks and parenthesis for ("translated text").
    """

    line = ununicode(line)
    starts = index_character(line, '[')
    ends = index_character(line, ']')
    # Goes through and preserves errthang outside [actions].
    for placeholder_start, placeholder_end in zip(starts, ends):
        start = line.find('[') # Have to follow the updated indices in instances of multiple [action] \n
        end = line.find(']')   # statements. I feel this isn't the most elegant but it is scraping after all.
        line = ''.join([line[0:start], line[end+1:]]) # chunk by chunk baby

    # Translating to 'None' strips all occurences of undesired characters, and it's faster than re!
    line = line.translate(None, '("")\n~\t\r')
    return line


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

    def get_lines_from_url(self, url):
        "This accesses all the <dd> tags (which contain script lines). Luh u bs4"

        page = requests.get(url).content
        soup = BeautifulSoup(page, 'lxml')
        title = soup.find('div', 'header-container').find('h1').text.split('/')[0]
        # clean works the stripping magic. It's all about the stripping
        lines = []
        for line in soup.find_all('dd'):  # was a nasty 1 line list comp
            if ':' in line.text and line.text is not None:
                lines.append(ununicode(line.text).replace('\n', ''))
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
        with open('episodes/'+str(index)+'::'+title, 'w') as episode_file:
            [episode_file.write(line+'\n') for line in episode_line_list]


if __name__ == '__main__':
    AT = Scraper()
    urls = AT.get_urls()
    for index, url in enumerate(urls):
        title, lines = AT.get_lines_from_url(url+'/Transcript')
        AT.write_lines_by_episode(index, title, lines)
