
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.externals import joblib



# MrSenti class
class MrSenti:
	"""A wrapper class for sentimental analysis with sklearn 
	
	Perform sentiment analysis on a set of strings
	"""


	def __init__(self):
		
		self.testing_set = []
		self.training_set = []

		self.testing_labels = []
		self.training_labels = []

		# Text vectorizer
		self.vectorizer= TfidfVectorizer(
			min_df = 5,
			max_df = .8,
			sublinear_tf = True,
			use_idf = True
		)

		# Classifier instance
		self.classifier = svm.SVC()


	def load_model(self, model_name = 'mr-senti'):
		"""Load a model(classifier) if it exists
		
		Loads a model(classifier) from ./models and returns operation status
		
		Keyword Arguments:
			model_name {str} -- Model name (default: {'mr-senti'})
		
		Returns:
			bool -- Operation status(True if the model was loaded)
		"""

		try:
			classifier= joblib.load(os.path.join('model', model_name + '.pkl'))
		except FileNotFoundError:
			return False

		self.classifier= classifier

		return True


	def save(self, model_name = 'mr-senti'):
		"""Save a model(classifier)
		
		Saves a model inside ./models
		
		Keyword Arguments:
			model_name {str} --  Name of the classifier/model (default: {'mr-senti'})
		"""

		joblib.dump(self.classifier, os.path.join('model', model_name + '.pkl'))


	def load_dataset(self, testPrefix = 'cv9', root = 'datasets', classes = [ 'pos', 'neg' ]):
		"""Load a dataset
		
		Loads a dataset from the filesystem into memory
		
		Keyword Arguments:
			root {str} -- Dataset directory relative to project root (default: {'datasets'})
			classes {list} -- Classes for the classifier to learn about (default: {[ 'pos', 'neg' ]})
		"""

		for senti_class in classes:

			dirname = os.path.join(root, senti_class)

			for filename in os.listdir(dirname):

				with open(os.path.join(dirname, filename)) as file:

					content = file.read()

					if filename.startswith(testPrefix):
						# Testing data
						self.testing_set.append(content)
						self.testing_labels.append(senti_class)
					else:
						# Training data
						self.training_set.append(content)
						self.training_labels.append(senti_class)

		self._vectorize(self.vectorizer)


	def _vectorize(self, vectorizer = None):
		"""Vectorize the training and testing set
		
		Keyword Arguments:
			vectorizer {TfidfVectorizer} -- Vectorizer instance (default: {None})
		"""

		vectorizer = vectorizer if vectorizer else self.vectorizer;

		self.training_set_vector = vectorizer.fit_transform(self.training_set)

		self.testing_set_vector = vectorizer.transform(self.testing_set)


	def vectorize(self, dataset):
		"""Vectorize a dataset
		
		Arguments:
			dataset {List} -- List to vectorize
		
		Returns:
			Vector -- Transformed list
		"""
		return self.vectorizer.transform(dataset)



	def train(self):
		"""Train the classifier
		"""
		return self.classifier.fit(self.training_set_vector, self.training_labels)


	def test(self, dataset = None, debug = True, labels = None):
		"""Test the classifier with some data
		
		Keyword Arguments:
			dataset {List} -- Dataset (default: {None})
			debug {bool} -- Debug mode (default: {True})
			labels {List} -- List of labels (default: {None})
		
		Returns:
			List -- The predictions made by the classifier
		"""

		dataset = self.vectorize(dataset) if (dataset != None) else self.testing_set_vector;
		labels = labels if (labels != None) else self.testing_labels;

		prediction = self.classifier.predict(dataset)

		if(debug):
			print(classification_report(labels, prediction))

		return prediction

