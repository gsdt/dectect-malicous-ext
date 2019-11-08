

from pymongo import MongoClient
from config import MONGO_CONECTION
import json
from flask import Flask, request, Response
from flask_cors import CORS
from flask import jsonify
from urllib.parse import urlparse
import time
from ml import Detector
import os
os.environ["PYSPARK_PYTHON"] = "/usr/bin/python3"
os.environ["PYSPARK_DRIVER_PYTHON"] = "/usr/bin/python3"

app = Flask(__name__)
CORS(app)

client = MongoClient(MONGO_CONECTION)
db = client.Detecting_Malicious_URL_db
collection = db.formated_url
collection_reported = db.user_report_url
collection_excluded = db.user_exclude_url

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
        # search by domain
        domain = o.netloc
        result = collection.find_one({"url": domain})
        if result != None:
            is_malicous = result['label']
        else:
            is_malicous = detector.predict(url)
        print("Machine learing:", is_malicous)
        print("--- %s seconds ---" % (time.time() - start_time))
        return create_response(is_malicous, "machine_learning")
    else:
        return create_response(result['label'], 'database')

# for exclude url to black or white list
@app.route('/api/exclude/url', methods=['POST'])
def request_exclude_url():
    if request.method == 'POST':
        data = []
        userId = request.form["user_id"]
        url = request.form["url_exclude"]
        label = request.form["label"]

        o = urlparse(url)
        if o.scheme != '':
            url = url[len(o.scheme) + 3:]
        if url[-1] == "/":
            url = url[0:-1]

        data.append({
            "user_id": userId,
            "url": url.strip(),
            "label": label.strip()
        })

        collection_excluded.insert_many(data)

        response_data = {
            "result": {
                "status": "Done !",
            }
        }

        return jsonify(response_data)

# for add url to black or white list
@app.route('/api/report/url', methods=['POST'])
def request_report_url():
    if request.method == 'POST':
        userEmail = request.form["user_email"]
        url = request.form["url_report"]
        label = request.form["label"]
        userName = request.form["user_name"]
        content_report = request.form["content_report"]

        print(userEmail)
        print(url)
        print(label)
        print(userName)
        print(content_report)
        data = []

        o = urlparse(url)
        if o.scheme != '':
            url = url[len(o.scheme) + 3:]
        if url[-1] == "/":
            url = url[0:-1]
        
        data.append({
            "user_email": userEmail,
            "url": url,
            "label": label,
            "user_name": userName,
            "reason": content_report
        })

        collection_reported.insert_many(data)
        response_data = {
            "result": {
                "status": "Report success, thanks your reported !",
            }
        }

        return jsonify(response_data)
        

if __name__=='__main__':
    app.run(host='0.0.0.0', port=80)




