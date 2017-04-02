
import json
import os
from flask import render_template, make_response, request
from libs.MrSenti import MrSenti

senti= MrSenti()

senti.load_dataset()

wasLoadedModel= senti.load_model()

if(not wasLoadedModel):
	senti.train()

def initialize_routes(app):

	@app.route('/')
	def hello():
		return render_template('index.html', foo = 'bar')

	@app.route('/api/analyse', methods= [ 'GET' ])
	def api_route():

		inputStr= request.args.get('text')

		label= senti.test([ inputStr ], False)

		jsonResponse= {
			'hello': 'world',
			'input': inputStr,
			'output': label[0]
		}

		jsonResponseString = json.dumps(jsonResponse)

		response= make_response(jsonResponseString, 200)
		response.headers['Content-Type'] = 'application/json'

		return response
