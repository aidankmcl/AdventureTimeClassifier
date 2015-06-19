import os
import math

import numpy as np
from collections import Counter


def index_character(text, character):
    "This is for getting all indices rather than just the first encounter"
    return [i for i, letter in enumerate(text) if letter == character]


def count_lines(fname):
        counter = 0
        with open(fname, 'r') as f:
            for line in f:
                counter += 1
        return counter


def get_tops(dirname):
        tops = []
        for root, _, files in os.walk(dirname):
            for f in files:
                if count_lines(os.path.join(root, f)) > self.min_lines:
                    tops.append(f)
        return tops


def line_cut(line, index):
    return line.split(':')[index].strip()


def clean(line):
    """
    There are 2 cases to address here
        1. Lady Rainicorn's speech is Korean and
        needs to be encoded as ascii while the translation is
        Surrounded by ("quotes and parenthesis")
        2. Character [actions inside brackets] are
        sprinkled throughout, and we don't want those.
    I'm first cutting out [actions] and then stripping
    quotation marks and parenthesis for ("translated text").
    """

    line = line.encode('ascii')
    # Goes through and preserves errthang outside [actions].
    counter = 0
    while ']' in line:
        line = ''.join([line[:line.find('[')], line[line.find(']')+1:]])
        counter+=1
        if counter == 5:
            line = line.translate(None, '[]')
            break

    # Translating to 'None' strips all occurences of undesired characters,
    # and it's faster than re!
    line = line.translate(None, '("")\n~\t\r')
    return line


def sort_num(episode_name):
    return int(episode_name.split('::')[0])


class Episode:
    """
    Returns information about a specified epsiode by its ID
    """

    def __init__(self, episode=False):
        self.episode_list = sorted(os.listdir('episodes/'), key=sort_num)
        self.req_ep = episode
        self.lines = []
        self.characters = []

        if type(episode) == int and episode < len(self.episode_list):
            self.lines = self.get_lines(episode)
            self.characters = self.get_characters()
        else:
            pass

    def get_lines(self, ep_index, data_dir='episodes/'):
        episode = self.episode_list[ep_index]
        with open(data_dir+episode, 'r') as f:
            return [clean(line) for line in f]

    def get_characters(self):
        characters = set()
        [characters.add(line_cut(line, 0)) for line in self.lines]
        return list(characters)

    def get_character_lines(self, character):
        if character in self.characters:
            return [line_cut(line, 1) for line in self.lines if line_cut(line, 0) == character]
        else:
            return []

    def get_keyword_mentions(self, keyword, character=None):
        if character in self.characters:
            return [line for line in self.lines if keyword in line_cut(line, 1) and character in line_cut(line, 0)]
        else:
            return [line for line in self.lines if keyword in line_cut(line, 1)]


class Character:

    def __init__(self, name, episode=None):
        self.episode_list = sorted(os.listdir('episodes/'), key=sort_num)
        self.lines = []

        if type(episode) == int and episode < len(self.episode_list):
            self.episode = Episode(episode)
            self.lines = self.episode.get_character_lines(name)
            return
        else:
            pass

        for i, ep in enumerate(self.episode_list):
            lines = Episode(i).get_character_lines(name)
            self.lines.append(lines)

    def mentions(self, keyword):
        mentions = []
        for episode_chunk in self.lines:
            [mentions.append(line) for line in episode_chunk if keyword in line]
        return mentions
