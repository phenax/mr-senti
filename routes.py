
import json
import os
from flask import render_template, make_response, request
from libs.MrSenti import MrSenti

senti= MrSenti()

senti.load_dataset()

modelExists= senti.load_model('no_test_prefix')

if(not modelExists):
	senti.train()
	senti.save()

def initialize_routes(app):

	@app.route('/')
	def hello():
		return render_template('index.html', foo = 'bar')

	@app.route('/api/analyse', methods= [ 'GET' ])
	def api_route():

		inputStr= request.args.get('text')

		label= senti.test([ inputStr ], False)

		jsonResponse= {
			'input': inputStr,
			'label': label[0]
		}

		jsonResponseString = json.dumps(jsonResponse)

		response= make_response(jsonResponseString, 200)
		response.headers['Content-Type'] = 'application/json'

		return response
