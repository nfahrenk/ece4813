#!flask/bin/python
from __future__ import print_function
from flask import Flask, jsonify, request, render_template
from environment import MACHINE
import requests
from urllib import urlencode
import pdb
app = Flask(__name__, static_url_path="")

BASE_URL = "https://6fjd5bdqz3.execute-api.us-east-2.amazonaws.com/prod"
FILE_TYPE_OPTIONS = [
    'elf'
]
AV_DETEC_OPTIONS = [
    'Unix.Trojan.Mirai-5607483-0',
    'Win.Trojan.L-43',
    'Unix.Trojan.Mirai-5932143-0',
    'Unix.Trojan.Mirai-1',
    'Unix.Trojan.Spike-6301360-0',
    'Unix.Trojan.SSHScan-6335682-0',
    'Unix.Trojan.Gafgyt-111',
    'Unix.Trojan.DDoS_XOR-1',
    'Legacy.Trojan.Agent-1388639',
    'Unix.Trojan.Mirai-5678467-0',
    'Unix.Trojan.Flooder-353',
    'Unix.Trojan.Agent-37008',
    'Unix.Exploit.CVE_2016_5195-2',
]
DOMAINS_OPTIONS = [
    's3.wio2lo1n3.pw;xmr.crypto-pool.fr',
    's3.wio2lo1n3.pw'
]
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
                            file_type_options=FILE_TYPE_OPTIONS,
                            domains_options=DOMAINS_OPTIONS,
                            next_page=malware.json()['next_page'],
                            prev_page=malware.json()['prev_page'])

@app.route('/addMalware', methods=['GET','POST'])
def add_malware():
    if request.method == 'GET':
        return render_template('addMalware.html')
    else:
        #List of malware displayed after new malware has been added
        list_malware()

if __name__ == '__main__':
    if MACHINE == 'local':
        app.run(debug=True, port=5000)
    else:
        app.run(host='0.0.0.0', port=80)
    
