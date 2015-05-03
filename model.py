
from random import shuffle

from wrangle import Wrangler

from sklearn import metrics
from sklearn.externals import joblib
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression as LR
from sklearn.svm import LinearSVC as SVC
from sklearn.feature_extraction.text import TfidfVectorizer


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
