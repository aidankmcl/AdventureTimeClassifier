import os
import math

import numpy as np
from collections import Counter


class Wrangler:
    """
    For doing whatever pre-processing that needs to happen
    before fun data sciencey things
    """

    def __init__(self, min_lines, percent_train=0.8, max_lines=1000):
        self.data = 'raw-data/'
        self.min_lines = min_lines
        self.max_lines = max_lines
        self.percent_train = percent_train
        self.tops = self.get_tops()
        self.label_dict = self.label_matching()
        self.characters = ' '.join([name.split('.')[0] for name in self.tops])

        self.train = []
        self.labels = []
        self.test = []
        self.test_labels = []

        print self.characters
        self.get_data(self.tops)

    def count_lines(self, fname):
        counter = 0
        with open(fname, 'r') as f:
           for line in f:
               counter += 1
        return counter

    def get_tops(self, dirname=self.data):
        tops = []
        for root, _, files in os.walk(dirname):
            for f in files:
                if self.count_lines(os.path.join(root, f)) > self.min_lines:
                    tops.append(f)
        return tops

    def get_file_lines(self, fname, data_dir=self.data):
        key_label = self.label_dict[fname]
        total_lines = self.count_lines(data_dir+fname)
        train_end = math.floor(total_lines*self.percent_train)

        iterations = int(math.floor(self.max_lines/train_end))

        if train_end > self.max_lines:
            train_end = self.max_lines

        with open(data_dir+fname, 'r') as f:
            for i, line in enumerate(f):
                for num in range(iterations+1):
                    if i < train_end:
                        self.train.append(line.translate(None, '\n'))
                        self.labels.append(key_label)
                    else:
                        self.test.append(line)
                        self.test_labels.append(key_label)

    def label_matching(self):
        converter = {name: i for i, name in enumerate(self.tops)}
        return converter

    def get_data(self, names):
        "Runs train"

        for name in names:
            self.get_file_lines(name)
