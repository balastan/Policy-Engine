import base64
import os

from flask import Flask
from flask import request
import json
import requests

import logging
import sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

app = Flask(__name__)

opa_url = os.environ.get("OPA_ADDR", "http://localhost:8181")
policy_path = os.environ.get("POLICY_PATH", "/v1/data/httpapi/authz")

def check_auth(url, method, url_as_array, token):
	resource = url_as_array[0]
	object_id = url_as_array[1]

	logging.info(resource)
	logging.info(object_id)

	ability = "SHOW"
	if method != "GET":
		ability = "MANAGE"

	input_dict = {"input": {
		"resource": resource,
		"object": object_id,
		"path": url_as_array,
		"ability": ability,
		"method": method,
	}}

	if token is not None:
		input_dict["input"]["token"] = token

	logging.info("Checking auth...")
	logging.info(json.dumps(input_dict, indent=2))
	try:
		rsp = requests.post(url, data=json.dumps(input_dict))
	except Exception as err:
		logging.info(err)
		return {}
	j = rsp.json()
	if rsp.status_code >= 300:
		# logging.info("Error checking auth, got status %s and message: %s" % (j.status_code, j.text))
		return {}
	logging.info("Auth response:")
	logging.info(json.dumps(j, indent=2))
	return j

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def root(path):
	user_encoded = request.headers.get('Authorization', "Bearer ")
	logging.info(request.headers)
	logging.info( user_encoded )
	if user_encoded:
		token = user_encoded.split("Bearer ")[1]
	url = opa_url + policy_path
	path_as_array = path.split("/")
	j = check_auth(url, request.method, path_as_array, token).get("result", {})
	if j.get("allow", False) == True:
		return json.dumps({"allow": "true"}, indent=2)
	return json.dumps({"allow": "false"}, indent=2)

if __name__ == "__main__":
	app.run()