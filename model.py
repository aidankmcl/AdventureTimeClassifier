
from random import shuffle

from wrangle import Wrangler

from sklearn import metrics
from sklearn.externals import joblib
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression as LR
from sklearn.svm import LinearSVC as SVC
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


if __name__ == "__main__":
    win = Wrangler(400, percent_train=1.0, max_lines=400)

    train_text = win.train
    train_labels = win.labels
    test_text = win.test
    test_labels = win.test_labels

    shuffle_temp = [(text, label) for text, label in zip(train_text, train_labels)]
    shuffle(shuffle_temp)
    shuffled_train_text = [text for (text, label) in shuffle_temp]
    shuffled_train_labels = [label for (text, label) in shuffle_temp]

    good_min = []
    good_max = []
    best_raw_acc = [0]
    predictions = {}
    real = {}

    '0.5286 min_df=74 max_df=80 with SVC'
    '~0.35 min_df=35 max_df=180 with LR'
    # vect = TfidfVectorizer(min_df=74, max_df=80, ngram_range=(1, 3))
    vect = TfidfVectorizer(min_df=35, max_df=180, ngram_range=(1, 3))
    trainX = vect.fit_transform(shuffled_train_text)

    # model = SVC()
    model = LR()
    model.fit(trainX, shuffled_train_labels)

    joblib.dump(model, 'pickle/model.pkl')

    # test_vect = vect.transform(test_text)

    # pr_test_vect = model.predict(test_vect)
    # raw_acc = metrics.accuracy_score(test_labels, pr_test_vect)
