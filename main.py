

from pymongo import MongoClient
from config import MONGO_CONECTION
import json
from flask import Flask, request, Response
from flask_cors import CORS
from flask import jsonify
from urllib.parse import urlparse
import time
from ml import Detector

app = Flask(__name__)
CORS(app)

client = MongoClient(MONGO_CONECTION)
db = client.Detecting_Malicious_URL_db
collection = db.formated_url

detector = Detector()

def create_response(label, source):
    return jsonify(
        {
            "result" : {
                "label": label,
                "source": source
            }
        }
    )

@app.route('/api/check', methods = ['POST'])
def check_request_url():
    org_url = request.form["url"]
    url = org_url

    o = urlparse(url)
    if o.scheme != '':
        url = url[len(o.scheme) + 3:]
    if url[-1] == "/":
        url = url[0:-1]

    label = ""
    result = collection.find_one({"url": url})
    print("Process: ", url)
    print("From database:", result)
    if result == None:
        start_time = time.time()
        is_malicous = detector.predict(url)
        print("Machine learing:", is_malicous)
        print("--- %s seconds ---" % (time.time() - start_time))
        return create_response(is_malicous, "machine_learning")
    else:
        return create_response(result['label'], 'database')

@app.route('/api/exclude/url', methods = ['POST']) # waiting for exclude url to black or white list
def request_exclude_url():
    if request.method == 'POST':
        return "ECHO: POST"

@app.route('/api/import/url', methods = [ 'PUT']) # waiting for add url to black or white list
def request_import_url():
    if request.method == 'PUT':
        return "ECHO: PUT"

if __name__=='__main__':
    app.run(host='0.0.0.0', port=80)




