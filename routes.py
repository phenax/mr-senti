
import json
import os
from flask import render_template, make_response

def initialize_routes(app):

	@app.route('/')
	def hello():
		return render_template('index.html', foo = 'bar')

	@app.route('/api/analyse', methods= [ 'GET' ])
	def api_route():

		jsonResponse = json.dumps({
			'hello': 'world'
		})

		response= make_response(jsonResponse, 200)
		response.headers['Content-Type'] = 'application/json'

		return response
