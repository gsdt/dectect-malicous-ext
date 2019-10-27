from pymongo import MongoClient
from config import MONGO_CONECTION
import json
from flask import Flask, request, Response
from flask_cors import CORS
from flask import jsonify
from urlparse  import urlparse
import machine_learning

app = Flask(__name__)
CORS(app)

client = MongoClient(MONGO_CONECTION)
db = client.Detecting_Malicious_URL_db
collection = db.formated_url

@app.route('/api/check', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def check_request_url():
    if request.method == 'GET': #waiting
        return "GET"
    elif request.method == 'POST':
        url = request.form["url"]

        o = urlparse(url)
        if o.scheme != '':
            url = url[len(o.scheme) + 3:]
        if url[-1] == "/":
            url = url[0:-1]

        label = ""
        result = collection.find_one({"url": url})
        print(url)
        print(result)
        if result == None:
            response_data = {
                "result": {
                    "label": machine_learning.detect(1, url),
                    "source": "machine_learning"
                }
            }
            return jsonify(response_data)
        else:
            response_data = {
                "result": {
                    "label": result["label"],
                    "scource": "databse"
                }
            }
            return jsonify(response_data)
        
    elif request.method == 'PATCH': #waiting
        return "PATCH"

    elif request.method == 'PUT': #waiting
        return "PUT"

    elif request.method == 'DELETE': #waiting
        return "ECHO: DELETE"

@app.route('/api/exclude/url', methods = ['POST']) #waiting for exclude url to black or white list
def request_exclude_url():
    if request.method == 'POST':
        return "ECHO: POST"

@app.route('/api/import/url', methods = [ 'PUT']) #waiting for add url to black or white list
def request_import_url():
    if request.method == 'PUT':
        return "ECHO: PUT"

if __name__=='__main__':
    app.run(host='0.0.0.0', port=80)




