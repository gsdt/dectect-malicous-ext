

from pymongo import MongoClient
from config import MONGO_CONECTION
import json
from flask import Flask, request, Response, send_from_directory, abort, render_template
from flask_cors import CORS
from flask import jsonify
from urllib.parse import urlparse
import time
from ml import Detector
import os
os.environ["PYSPARK_PYTHON"] = "/usr/bin/python3"
os.environ["PYSPARK_DRIVER_PYTHON"] = "/usr/bin/python3"

app = Flask(__name__, template_folder='templates')
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
            "result": {
                "label": label,
                "source": source
            }
        }
    )


@app.route('/api/check', methods=['POST'])
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
        print('Checking domain:', domain)
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
@app.route('/api/exclude', methods=['POST'])
def request_exclude_url():
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
@app.route('/api/report', methods=['POST'])
def request_report_url():
    userEmail = request.form["user_email"]
    url = request.form["url_report"]
    label = request.form["label"]
    userName = request.form["user_name"]
    content_report = request.form["content_report"]
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

    print(data)

    collection_reported.insert_many(data)
    response_data = {
        "result": {
            "status": "Report success, thanks your reported !",
        }
    }

    return jsonify(response_data)

# for exclude url to black or white list
@app.route('/api/add', methods=['POST'])
def add_to_database():
    url = request.form["url"]
    label = request.form["label"]

    o = urlparse(url)
    domain = o.netloc

    print("Adding to db:")
    print("URL:", url)
    print("domain:", domain)

    result = result = collection.find_one({"url": domain})
    if result != None:
        return jsonify({
            "result": {
                "status": "this domain already in db."
            }
        })
    data = [
        {
            "url": url,
            "label": label
        },
        {
            "url": domain,
            "label": label
        }
    ]
    collection.insert_many(data)
    return jsonify({
        "result": {
            "status": "success."
        }
    })


@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get('id')
    try:
        return send_from_directory('/home/chodx/remote1/2019-06-27', filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/list', methods=['GET'])
def list_pcap_file():
    result = ''
    files = os.listdir('/home/chodx/remote1/2019-06-27')
    print(files)
    for f in files:
        result += f'<a href="download?id={f}">{f}</a><br>'
    return result

@app.route('/admin/reports', methods=['GET'])
def list_reports():
    code = request.args.get('code')
    if code != "chodx2019@2020":
        abort(400)
    report_list = []
    for document in collection_reported.find():
        report_list += [document]
    
    return render_template('list.html', reports=report_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
