import urllib.parse
import time
import requests
import hashlib
import hmac
import base64
from app import app, config
from flask import render_template, redirect, url_for, flash

api_url = 'https://api.kraken.com'
api_key = config.api
api_sec = config.api_sec

def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


def kraken_request(url_path, data, api_key, api_sec):
    headers = {"API-Key": api_key, "API-Sign": get_kraken_signature(url_path, data, api_sec)}
    resp = requests.post((api_url + url_path), headers=headers, data=data)
    return resp


balances = kraken_request("/0/private/Balance", {
    "nonce": str(int(1000*time.time()))
}, api_key, api_sec)
USDC_bal = balances.json()['result']['USDC']
USD_bal = balances.json()['result']['ZUSD']

@app.route('/')
def index():
    return render_template('index.html')