
import sys
import os
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report


vectorizer= TfidfVectorizer(
	min_df = 5,
	max_df = .8,
	sublinear_tf = True,
	use_idf = True
)


