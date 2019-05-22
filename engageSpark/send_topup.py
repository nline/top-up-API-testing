#!/usr/bin/env python

import argparse
import yaml
import requests
import json
import random
import string

parser = argparse.ArgumentParser(description = 'Sends an engagespark topup')
parser.add_argument('phoneNumber', type=str)
parser.add_argument('amount', type=int)
parser.add_argument('postbin', type=str)
args = parser.parse_args()

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

config = None
with open('config.yaml', 'r') as stream:
    config = yaml.safe_load(stream)

base_url = 'https://api.engagespark.com/v1/airtime-topup'

headers = {'Authorization': 'Token ' + config['api_key'], 'content-type': 'application/json'}

ref = randomString()
body = {'organizationId': str(config['organization_id']), 'maxAmount': str(args.amount), 'phoneNumber':args.phoneNumber, 'clientRef': ref, 'resultsUrl': 'https://postb.in/' + args.postbin}

r = requests.post(base_url, json=body, headers=headers)

print(r.status_code)
print(r.content)
print('Sent requests with ref:', ref, 'For callback go to:','https://postb.in/b/' + args.postbin)
