
import sys
import os
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.externals import joblib



class MrSenti:


	def __init__(self):
		
		self.testing_set = []
		self.training_set = []

		self.testing_labels = []
		self.training_labels = []

		self.vectorizer= TfidfVectorizer(
			min_df = 5,
			max_df = .8,
			sublinear_tf = True,
			use_idf = True
		)

		self.classifier = svm.SVC()


	def load_model(self, model_name = 'mr-senti'):

		try:
			classifier= joblib.load(os.path.join('model', model_name + '.pkl'))
		except FileNotFoundError:
			return False

		self.classifier= classifier

		return True


	def save(self, model_name = 'mr-senti'):

		joblib.dump(self.classifier, os.path.join('model', model_name + '.pkl'))


	def load_dataset(self, root = 'datasets', classes = [ 'pos', 'neg' ]):

		for senti_class in classes:

			dirname = os.path.join(root, senti_class)

			for filename in os.listdir(dirname):

				with open(os.path.join(dirname, filename)) as file:

					content = file.read()

					if filename.startswith('cv9'):
						# Testing data
						self.testing_set.append(content)
						self.testing_labels.append(senti_class)
					else:
						# Training data
						self.training_set.append(content)
						self.training_labels.append(senti_class)

		self._vectorize(self.vectorizer)


	def _vectorize(self, vectorizer = None):

		vectorizer = vectorizer if vectorizer else self.vectorizer;

		self.training_set_vector = vectorizer.fit_transform(self.training_set)

		self.testing_set_vector = vectorizer.transform(self.testing_set)


	def train(self):

		print('Training');

		return self.classifier.fit(self.training_set_vector, self.training_labels)


	def test(self, dataset = None):

		dataset = dataset if dataset else self.testing_set_vector;

		return self.classifier.predict(dataset)





senti= MrSenti()

senti.load_dataset()

wasLoadedModel= senti.load_model()

if(not wasLoadedModel):
	senti.train()

prediction = senti.test()

print(classification_report(senti.testing_labels, prediction))

if(not wasLoadedModel):
	senti.save()



