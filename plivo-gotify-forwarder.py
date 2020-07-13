#!/usr/bin/env python3
'''plivo to gotify forwarder'''

PORT = 1622
GOTIFY_URL_TEMPLATE = 'http://127.0.0.1:1621/message?token={}'

from datetime import datetime
import sys

import requests

from flask import Flask, request, make_response
app = Flask(__name__)
app.secret_key = r'CHANGE ME'

def bad_request():
    return make_response(('Bad request :(', 400, {}))

# ROUTES

@app.route('/test')
def test():
    return 'OK'

@app.route('/<secret>', methods=['GET', 'POST'])
def incoming_sms(secret):

    try:
        sender = request.values['From'].strip()
        beacon = request.values['To'].strip()
        text = request.values['Text'].strip()
    except:
        print("[DEBUG] incoming sms was malformed")
        return bad_request()

    print("[DEBUG] from {}".format(sender))
    print('[DEBUG]   "{}"'.format(text))

    now = datetime.utcnow()
    r = requests.post(GOTIFY_URL_TEMPLATE.format(secret), data=dict(
        title='US SMS received',
        priority=8,
        message=sender + now.strftime(' on %a %d %b at %H:%M Z: ') + text,
    ))

    return 'OK'

if __name__ == '__main__':

    if app.secret_key == r'CHANGE ME':
        print("Please set the secret key to some long random arbitrary string!")
        sys.exit(2)

    app.run(host='0.0.0.0', port=PORT)
