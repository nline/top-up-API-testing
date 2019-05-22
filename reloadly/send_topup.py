#!/usr/bin/env python

import argparse
import yaml
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

parser = argparse.ArgumentParser(description = 'Sends a reloadly topup')
parser.add_argument('phone-number', type=str)
parser.add_argument('amount', type=int)
args = parser.parse_args()

config = None
with open('config.yaml', 'r') as stream:
    config = yaml.safe_load(stream)

print("Authenticating with ID:", config['client_id'], "secret:", config['client_secret'])

#get an access token
auth = HTTPBasicAuth(config['client_id'], config['client_secret'])
client = BackendApplicationClient(client_id=config['client_id'])
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url='https://topups.reloadly.com/token', client_id=config['client_id'], client_secret=config['client_secret'], auth=auth)

print("Got token:", token)
