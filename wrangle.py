import os
import math

import numpy as np
from collections import Counter

from sklearn import metrics
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression as LR
from sklearn.feature_extraction.text import TfidfVectorizer

class Wrangler:
    """
    For doing whatever pre-processing that needs to happen
    before feeding to Passage
    """

    def __init__(self, min_lines, percent_train=0.8, max_lines=1000):
        self.data = 'raw-data/'
        self.min_lines = min_lines
        self.max_lines = max_lines
        self.percent_train = percent_train
        self.tops = self.get_tops()
        self.label_dict = self.label_matching()

        self.train = []
        self.labels = []
        self.test = []
        self.test_labels = []

    def count_lines(self, fname):
        counter = 0
        with open(fname, 'r') as f:
           for line in f:
               counter += 1
        return counter

    def get_tops(self, dirname='raw-data/'):
        tops = []
        for root, _, files in os.walk(dirname):
            for f in files:
                if self.count_lines(os.path.join(root, f)) > self.min_lines:
                    tops.append(f)
        return tops

    def get_file_lines(self, fname, data_dir='raw-data/'):
        key_label = self.label_dict[fname]
        total_lines = self.count_lines(data_dir+fname)
        train_end = math.floor(total_lines*self.percent_train)
        if train_end > self.max_lines:
            train_end = self.max_lines
        
        with open(data_dir+fname, 'r') as f:
            for i, line in enumerate(f):
                if i < train_end:
                    self.train.append(line.translate(None, '\n'))
                    self.labels.append(key_label)
                else:
                    self.test.append(line)
                    self.test_labels.append(key_label)



    def label_matching(self):
        converter = {name: i for i,name in enumerate(self.tops)}
        return converter

    def get_data(self, names):
        "Runs train"

        for name in names:
            self.get_file_lines(name)



if __name__ == '__main__':
    win = Wrangler(500, percent_train=1.0, max_lines=500)
    
    print win.tops
    print len(win.tops)

    win.get_data(win.tops)

    train_text = win.train
    train_labels = win.labels
    test_text = win.test
    test_labels = win.test_labels

    vect = TfidfVectorizer(min_df=10, ngram_range=(1, 2))
    trainX = vect.fit_transform(train_text)

    model = LR()
    model.fit(trainX, train_labels)

    test_vect = vect.transform(test_text)

    pr_test_vect = model.predict(test_vect)
    print 'predictions = ', Counter(pr_test_vect)
    print 'real = ', Counter(test_labels)
    print metrics.accuracy_score(test_labels, pr_test_vect)
    print model.predict(vect.transform("You wouldn't know what to do with it Gunter"))




