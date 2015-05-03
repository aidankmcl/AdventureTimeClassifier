from model import vect

from sklearn.externals import joblib

MODEL = joblib.load('pickle/model.pkl')
text = vect.transform([""])
print MODEL.predict(text)

