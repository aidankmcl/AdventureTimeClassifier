"""
Handling the scraping for each 
Adventure Time episode's transcript
"""

import requests
import re

from bs4 import BeautifulSoup
import unicodedata

class Scraper:
    "First honest stab at using classes on my own time"

    def __init__(self):
        print "getting started"
        self.base_url = 'http://adventuretime.wikia.com'
        # urls = self.get_urls()
        print self.get_lines('http://adventuretime.wikia.com/wiki/Slumber_Party_Panic/Transcript')

    # # Main beef
    def get_urls(self):
        page = requests.get(self.base_url+'/wiki/Category:Transcripts').content
        soup = BeautifulSoup(page, 'lxml')
        links = soup.find_all('a')
        urls = [self.base_url+link.get('href') for link in links 
            if link.get('href') != None and '/Transcript' in link.get('href')] # Is a list comp this big a gross thing?
        return urls

    def get_lines(self, url):
        page = requests.get(url).content
        soup = BeautifulSoup(page, 'lxml')
        lines = [self.strip(line.text) for line in soup.find_all('dd') if ':' in line.text and line.text != None]
        return lines

    # # Helpers
    def ununicode(self, unicode_string):
        return unicodedata.normalize('NFKD', unicode_string).encode('ascii','ignore')

    def index_character(self, text, character):
        return [i for i, letter in enumerate(text) if letter == character]

    def strip(self, line):
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
        start = self.index_character(line, '[')
        end = self.index_character(line, ']')
        for cut_start, cut_end in zip(start, end): # goes through and cuts out actions
            line = ''.join([line[:cut_start], line[cut_end+1:]]) # chunk by chunk
        line = line.translate(None, '("")\n~') # translate to None strips all occurences of characters, and it's faster than re!
        return line


if __name__ == '__main__':
    Scraper()