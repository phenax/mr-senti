
import json
import os
from flask import render_template, make_response, request
from libs.MrSenti import MrSenti



# MrSenti instance
senti= MrSenti()

# Load the dataset into memory
senti.load_dataset()

# Load the classifer if saved
model_exists= senti.load_model('no_test_prefix')

# If the model doesnt exist(wasnt saved)
if(not model_exists):
	senti.train()  # Train the classifier
	senti.save()   # Save the classifier


def initialize_routes(app):
	"""Initialize the routes for the app
	
	Arguments:
		app {Flask} --  Flask app instance
	"""

	@app.route('/api/analyse', methods= [ 'GET' ])
	def api_route():

		inputStr = request.args.get('text')

		labels = senti.test_probability([ inputStr ])
		label = senti.test([ inputStr ], False)

		json_response = json.dumps({
			'input': inputStr,
			'label': label[0],# 'neg' if labels[0] < .5 else 'pos',
			'probabilities': {
				'pos': labels[0],
				'neg': 1 - labels[0],
			}
		})

		response= make_response(json_response, 200)
		response.headers['Content-Type'] = 'application/json'

		return response


	@app.route('/')
	def hello():
		return render_template('index.html')

