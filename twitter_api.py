import tweepy
import configparser
import requests
import socket
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini')


api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

headers = {'accept': 'application/json',
           'X-Shopper-Id': '554531765',
           'Content-Type': 'application/json',
           'Authorization': 'sso-key %s:%s' % (
               config['godaddy']['api_key'], config['godaddy']['api_key_secret'])}
params = {
    'domain': 'amir-portfolio.com',
    'checkType': 'FULL',
    'forTransfer': 'false',
}

available_url = 'https://api.godaddy.com/v1/domains/available'
purchase_url = 'https://api.godaddy.com/v1/domains/purchase'

data = {
    "consent": {
        "agreedAt": datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "agreedBy": socket.gethostbyname(socket.gethostname()),
        "agreementKeys": [
            "DNRA"
        ]
    },
    "contactAdmin": {
        "addressMailing": {
            "address1": "2155 E Warner Rd",
            "address2": "string",
            "city": "Tempe",
            "country": "US",
            "postalCode": "85284",
            "state": "Arizona"
        },
        "email": "user@example.com",
        "fax": "+1.4806242598",
        "jobTitle": "developer",
        "nameFirst": "Registration ",
        "nameLast": "Private",
        "nameMiddle": "",
        "organization": "Domains By Proxy, LLC",
        "phone": "+1.4806242599"
    },
    "contactBilling": {
        "addressMailing": {
            "address1": "1051 summit ave N",
            "address2": "",
            "city": "madison",
            "country": "US",
            "postalCode": "57042",
            "state": "SD"
        },
        "email": "amirnuri@icloud.com",
        "fax": "",
        "jobTitle": "developer",
        "nameFirst": "amir",
        "nameLast": "kemal",
        "nameMiddle": "",
        "organization": "DSU",
        "phone": "+1.2028077946"
    },
    "contactRegistrant": {
        "addressMailing": {
            "address1": "DomainsByProxy.com",
            "address2": "2155 E Warner Rd",
            "city": "Tempe",
            "country": "US",
            "postalCode": "85284",
            "state": "Arizona"
        },
        "email": "user@example.com",
        "fax": "+1.4806242598",
        "jobTitle": "developer",
        "nameFirst": "Registration ",
        "nameLast": "Private",
        "nameMiddle": "",
        "organization": "Domains By Proxy, LLC",
        "phone": "+1.4806242599"
    },
    "contactTech": {
        "addressMailing": {
            "address1": "DomainsByProxy.com",
            "address2": "2155 E Warner Rd",
            "city": "Tempe",
            "country": "US",
            "postalCode": "85284",
            "state": "Arizona"
        },
        "email": "user@example.com",
        "fax": "+1.4806242598",
        "jobTitle": "developer",
        "nameFirst": "Registration ",
        "nameLast": "Private",
        "nameMiddle": "",
        "organization": "Domains By Proxy, LLC",
        "phone": "+1.4806242599"
    },
    "domain": "",
    "nameServers": [
        "ns1.vultr.com",
        "ns2.vultr.com"
    ],
    "period": 1,
    "privacy": False,
    "renewAuto": False
}
price_max = 6.99
auth = tweepy.OAuth1UserHandler(
    api_key,
    api_key_secret,
    access_token,
    access_token_secret
)


api = tweepy.API(auth)

tweets = api.user_timeline()

for tweet in tweets:
    for url in tweet.entities['urls']:
        check_url = url['display_url']
        params["domain"] = check_url
        response = requests.get(
            available_url, params=params, headers=headers)
        if response.json()['available']:
            domain_price = (response.json()['price'])/1000000
            if domain_price < price_max:
                print(check_url, '-->', domain_price)
                data["domain"] = check_url
                response = requests.post(
                    purchase_url,  headers=headers, json=data)
                print(response.json())
