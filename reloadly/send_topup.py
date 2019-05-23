#!/usr/bin/env python3
import sys
import argparse
import yaml
import requests
import json

parser = argparse.ArgumentParser(description = 'Sends a reloadly topup')
parser.add_argument('phoneNumber', type=str)
parser.add_argument('amount', type=int)
args = parser.parse_args()

config = None
with open('config.yaml', 'r') as stream:
    config = yaml.safe_load(stream)

print("Authenticating")
print()

url = 'https://auth.reloadly.com/oauth/token'
headers = {'content-type': 'application/json'}
body = {'client_id': config['client_id'], 'client_secret': config['client_secret'], 'grant_type':'client_credentials','audience':'https://topups.reloadly.com'}

r = requests.post(url, headers=headers, json=body)

if(r.status_code == 200):
    print("Successfully received access token")
    print()
else:
    print("access token failure. exiting")
    sys.exit(1)

token = json.loads(r.content)['access_token']

#now form the topup body
headers = {'accept': 'application/com.reloadly.topups-v1+json', 'Authorization':'Bearer ' + token}

#get the list of suppored countries
r = requests.get('https://topups.reloadly.com/countries', headers=headers)

country_list = json.loads(r.content)
receiving_country = None
for country in country_list:
    for country_code in country['callingCodes']:
        if args.phoneNumber[0] == '+':
            if country_code == args.phoneNumber[:len(country_code)]:
                receiving_country = country
                break
        else:
            if country_code[1:] == args.phoneNumber[:len(country_code)-1]:
                receiving_country = country
                break

    if(receiving_country != None):
        break

if(receiving_country == None):
    print("Did not find valid country for phone number")
    sys.exit(1)

print("Auto detected country code " + receiving_country['isoName'])
print()

#now detect the operator of the number in that country
url = 'https://topups.reloadly.com/operators/auto-detect/phone/' + args.phoneNumber + '/country-code/' + receiving_country['isoName'] + '?&includeBundles=true'
r = requests.get(url, headers=headers)

operator_id = None
operator_name = None
if r.status_code == 200:
    operator_id = json.loads(r.content)['operatorId']
    operator_name = json.loads(r.content)['name']

if(operator_id == None):
    print('Failed to get operator ID. Exiting')
    sys.exit(1)

print('Auto detected operator ' + operator_name + ' with ID ' + str(operator_id))
print()

print('Sending topup')
body = {
  "recipientPhone": {
    "countryCode": receiving_country['isoName'],
    "number": args.phoneNumber
  },
  "senderPhone": {
    "countryCode": "US",
    "number": "+19379029186" 
  },
  "operatorId": operator_id,
  "amount": args.amount,
  "customIdentifier": "test transaction by Josh Adkins" 
}

r = requests.post('https://topups.reloadly.com/topups',headers=headers,json=body)

print(r)
print(r.content)
