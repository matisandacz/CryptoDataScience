import argparse
import requests
import json
from urllib.parse import urljoin, urlencode
import logging
import os
from enum import Enum
from datetime import datetime, timedelta, date
from tqdm import tqdm
import time


class RunMode(Enum):
    SINGLE = 1,
    BATCH = 2

def parse_iso8601(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format. Please use YYYY-MM-DD format.")


# TODO: Parameter validation
def main():

    parser = argparse.ArgumentParser(description='Crypto Data Science Application')

    subparsers = parser.add_subparsers(title='Subcommands', dest='mode')
    
    # Subparser for single mode
    parser_mode1 = subparsers.add_parser('single', help='Downloads Crypto Data from one date')
    parser_mode1.add_argument('-i', '--id', type=str, help='Coin identifier (e.g. bitcoin)', required=True)
    parser_mode1.add_argument('-d', '--date', type=parse_iso8601, help='ISO8601 date (YYYY-MM-DD)', required=True)

    # Subparser for batch mode
    parser_mode2 = subparsers.add_parser('batch', help='Downloads Crypto Data from a range of dates')
    parser_mode2.add_argument('-i', '--id', type=str, help='Coin identifier (e.g. bitcoin)', required=True)
    parser_mode2.add_argument('-s', '--start', type=parse_iso8601, help='Start ISO8601 date (YYYY-MM-DD)', required=True)
    parser_mode2.add_argument('-e', '--end', type=parse_iso8601, help='End ISO8601 date (YYYY-MM-DD)', required=True)

    args = parser.parse_args()

    if args.mode == RunMode.SINGLE.name.lower():
        print(f"Running Single mode - {args.id} - {args.date}")
        run_single_mode(args)
    elif args.mode == RunMode.BATCH.name.lower():
        print(f"Running Batch mode - {args.id} - {args.start} - {args.end}")
        run_batch_mode(args)
    else:
        parser.print_help()

# TODO: Delegate to a service.
def build_coin_history_url(coin_name, query_params):
    base_url = 'https://api.coingecko.com/api/v3/'
    endpoint = f'coins/{coin_name}/history'
    full_url = urljoin(base_url, endpoint)
    if query_params:
        query_string = urlencode(query_params)
        full_url = f'{full_url}?{query_string}'
    return full_url

# TODO: Delegate to a service.
def getTokenData(coin_name, date):

    query_parameters = {
        'date': date.strftime('%d-%m-%Y')
    }

    url = build_coin_history_url(coin_name, query_parameters)

    # Perform the HTTP Request
    logging.info(f"Performing an HTTP request to {url}")
    r = requests.get(url)

    # Raise an error if the response was an HTTP Error
    r.raise_for_status()

    return r.json()

def saveTokenData(coin_name, date, tokenData, response_path = "data/"):

    # Create a new directory if it does not exist
    if not os.path.exists(response_path):
        os.makedirs(response_path)

    # Save json
    with open(f"{response_path}/{coin_name}-{date.strftime('%Y-%m-%d')}.json", "w") as outfile:
        json.dump(tokenData, outfile)

"""
Runs this application in single mode
"""
def run_single_mode(args):

    # TODO: Convert from YYYY-MM-DD -> DD-MM-YYYY

    try:
        tokenData = getTokenData(args.id, args.date)
        saveTokenData(args.id, args.date, tokenData)
    except Exception as err:
        print(err)

    
"""
Runs this application in batch mode
"""
def run_batch_mode(args):

    delta = args.end - args.start 

    for i in tqdm(range(delta.days + 1)):
        date = args.start + timedelta(days=i)
        tokenData = getTokenData(args.id, date)
        saveTokenData(args.id, date, tokenData)

# Script will only run when executed from the command line
if __name__ == "__main__":
    main()
