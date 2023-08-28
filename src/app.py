import argparse
from distutils.debug import DEBUG
import requests
import json
from urllib.parse import urljoin, urlencode
from dateutil.parser import parse as parse_iso8601
import logging

logging.getLogger().setLevel(level="INFO")

parser = argparse.ArgumentParser(description='Download Crypto Data')
parser.add_argument('-i', '--id', type=str, help='Coin identifier (e.g. bitcoin)', required=True)
parser.add_argument('-d', '--date', type=str, help='ISO8601 date (e.g. 2017-12-30)', required=True)
args = parser.parse_args()

base_url = 'https://api.coingecko.com/api/v3/'

def build_coin_history_url(coin_name, query_params):
    endpoint = f'coins/{coin_name}/history'
    full_url = urljoin(base_url, endpoint)
    if query_params:
        query_string = urlencode(query_params)
        full_url = f'{full_url}?{query_string}'
    return full_url

coin_name = args.id
query_parameters = {
    'date': args.date
}

url = build_coin_history_url(coin_name, query_parameters)

try:

    # Perform the HTTP Request
    logging.info(f"Performing an HTTP request to {url}")
    r = requests.get(url)
    logging.info(f"Status code was {r.status_code}")
    # Raise an error if the response was an HTTP Error
    
    r.raise_for_status()

    # Creates the file if it doesnt exist, and save json
    with open("response.json", "w") as outfile:
        json.dump(r.json(), outfile)

except Exception as err:
    logging.error(err)
