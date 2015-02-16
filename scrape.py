"""
Handling the scraping for each 
Adventure Time episode's transcript
"""

import requests
import re
import unicodedata

from bs4 import BeautifulSoup

class Scraper:
    "There's magic in these words"

    def __init__(self):
        print "Mathematical!"
        self.base_url = 'http://adventuretime.wikia.com'

    # # Main beef # #
    def get_urls(self):
        "Runs through and grabs all the URLs from the table of contents"

        page = requests.get(self.base_url+'/wiki/Category:Transcripts').content
        soup = BeautifulSoup(page, 'lxml')
        links = soup.find_all('a')
        # goes through every href and only gets links with '/Transcript'
        urls = [self.base_url+link.get('href') for link in links # grooosss but whatevs for now
            if link.get('href') != None and '/Transcript' in link.get('href')]
        urls.sort()
        return self.filter_repeats(urls)

    def get_lines(self, url):
        "This accesses all the <dd> tags (which contain script lines). Luh u bs4"

        page = requests.get(url).content
        soup = BeautifulSoup(page, 'lxml')
        # self.clean works the stripping magic. It's all about the stripping
        lines = [self.clean(line.text) for line in soup.find_all('dd') if ':' in line.text and line.text != None]
        return lines

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
            if name == "Pen": name = "Finn"
            if name == "Lich": name = "The Lich"
            if re.search('[a-zA-Z]', script) != None:
                names.setdefault(name, []).append(script)

        return names

    def write_episode(self, episode_dict):
        "For writing lines out to files corresponding to speaker."

        for name in ep_dict.keys():
            with open('raw-data/'+name+'.txt', 'a') as Ooo:
                Ooo.write('\n'.join(ep_dict[name]))
        return


    # # Helpers # #
    def ununicode(self, unicode_string):
        "So Python doesn't get mad at Lady Rainicorn"
        return unicodedata.normalize('NFKD', unicode_string).encode('ascii','ignore')

    def index_character(self, text, character):
        "This is for getting all indices rather than just the first encounter"
        return [i for i, letter in enumerate(text) if letter == character]

    def filter_repeats(self, links):
        seen = set()
        seen_add = seen.add
        return [ link for link in links if not (link in seen or seen_add(link))]

    def clean(self, line):
        """
        There are 2 tricky bits about cleaning up the transcripts
        which are:
            1. Lady Rainicorn's speech is Korean and
            needs to be encoded as ascii while the translation is 
            Surrounded by ("quotes and parenthesis")
            2. Character [actions inside block parens] are
            sprinkled throughout, and we don't want those.
        I'm first cutting out [actions] and then stripping 
        quotation marks and parenthesis for ("translated text").
        """

        line = self.ununicode(line)
        starts = self.index_character(line, '[')
        ends = self.index_character(line, ']')
        # Goes through and preserves errthang outside [actions].
        for placeholder_start, placeholder_end in zip(starts, ends): 
            start = line.find('[') # Have to follow the updated indices in instances of multiple [action] \n
            end = line.find(']')   # statements. I feel this isn't the most elegant but it is scraping after all.
            line = ''.join([line[0:start], line[end+1:]]) # chunk by chunk baby
        
        # Translating to 'None' strips all occurences of undesired characters, and it's way faster than re!
        line = line.translate(None, '("")\n~\t\r')
        return line


if __name__ == '__main__':
    AT = Scraper()

    urls = AT.get_urls()
    for i, url in enumerate(urls):
        episode = AT.get_lines(url)
        ep_dict = AT.chunk_to_dict(episode)
        AT.write_episode(ep_dict)
        print i, url

    print 'Slamacow!'
