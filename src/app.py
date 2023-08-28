import argparse
import requests
import json

#python app.py --help
# TODO: Verify date is formatted as expected. Fail early.
parser = argparse.ArgumentParser(description='Download Crypto Data')
parser.add_argument('-i', '--id', type=str, help='Coin identifier (e.g. bitcoin)', required=True)
parser.add_argument('-d', '--date', type=str, help='ISO8601 date (e.g. 2017-12-30)', required=True)
args = parser.parse_args()

"""

endpoint = /coins/{id}/history?date=dd-mm-yyyy

id va en path
el date es una variable

An example endpoint would be :
"""

# TODO como se llama cada parte?

url = url library?

# Make API request
r = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/history?date=30-12-2017')

# Creates the file if it doesnt exist, and save json
with open("response.json", "w") as outfile:
    json.dump(r.json(), outfile)