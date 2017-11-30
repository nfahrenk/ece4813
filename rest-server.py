#!flask/bin/python
from __future__ import print_function
from flask import Flask, jsonify
from environment import MACHINE

app = Flask(__name__, static_url_path="")

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

if __name__ == '__main__':
    if MACHINE == 'local':
        app.run(debug=True, port=5000)
    else:
        app.run(host='0.0.0.0', port=80)
    
