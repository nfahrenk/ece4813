#!flask/bin/python
from __future__ import print_function
from flask import Flask, jsonify, request, render_template, redirect
import requests
from urllib import urlencode
import datetime
from av_detec import AV_DETEC_OPTIONS
app = Flask(__name__, static_url_path="")

BASE_URL = "https://6fjd5bdqz3.execute-api.us-east-2.amazonaws.com/prod"

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/malware', methods=['GET'])
def list_malware():
    malware = requests.get(BASE_URL + "/malware?" + urlencode({key: val for key,val in request.args.items() if val}))
    # pdb.set_trace()
    return render_template('listMalware.html', malware=malware.json()['results'], 
                            av_detec_options=AV_DETEC_OPTIONS,
                            next_page=malware.json()['next_page'],
                            prev_page=malware.json()['prev_page'])

@app.route('/malware/add', methods=['GET','POST'])
def add_malware():
    if request.method == 'GET':
        return render_template('addMalware.html')
    else:
        #List of malware displayed after new malware has been added
        requests.post(BASE_URL + "/malware/add")
        list_malware()

@app.route('/map', methods=['GET'])
def map_malware():
    response = requests.get(BASE_URL + "/map").json()
    return render_template('dashboard.html', **response)
        
@app.route('/', methods=['GET'])
def check_malware():
    response = requests.get(BASE_URL + "/check").json()
    malware = requests.get(BASE_URL + "/malware?" + urlencode({"from_ingest_date": datetime.datetime.now() - datetime.timedelta(days=7)}))
    return render_template('index.html', has_ip=response["ip_exists"], ip_address=response["source_ip"], malware=malware.json()['results'])

@app.route('/malware/<string:id>', methods=['GET'])
def view_malware(id):
    response = requests.get(BASE_URL + "/malware/" + str(id)).json()
    return render_template('viewMalware.html', **response)

@app.route('/malware/<string:id>/edit', methods=['GET', 'POST'])
def edit_malware(id):
    if request.method == "GET":
        response = requests.get(BASE_URL + "/malware/" + str(id)).json()
        return render_template('editMalware.html', **response)
    else:
        headers = {'Content-Type': 'application/json'}
        print('fuckkkk')
        print(request.form)
        response = requests.post(BASE_URL + "/edit/" + str(id), headers=headers, json=request.form).json()
        print(response)
        return redirect("/malware/" + str(id) + "/edit")

@app.route('/malware/<string:id>/delete', methods=['POST'])
def remove_malware(id):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(BASE_URL + "/delete/" + str(id), headers=headers)
    return redirect("/malware")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
