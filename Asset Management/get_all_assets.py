"""get_all_assets.py: fetch all assets within a given Detectify team and optionally write to a file

The API key permissions required by this script are the following:
- Allow listing domains

Usage: get_all_assets.py [-h] [-f FILE] key
"""

import argparse
import csv
import requests

API_BASE_URL = 'https://api.detectify.com/rest'


def export_to_csv(all_assets: list, file: str) -> None:
    """Export all assets from a given Detectify team to csv

    :param all_assets: A list of dictionaries containing asset information
    :param file: The name of the file to save to
    """
    with open(f'{file}', 'w+', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([[x['name']] for x in all_assets])


def get_assets(key: str) -> list:
    """Get the full list of apex domains and subdomains from Detectify

    :param key: A valid Detectify API key
    :return: A list of dictionaries containing asset information
    """
    print('Querying assets. . .')
    all_assets = []
    marker = ''
    has_more = True
    while has_more:
        api_endpoint = f'/v2/assets/'
        r = requests.get(url=f'{API_BASE_URL}{api_endpoint}?marker={marker}&include_subdomains=true',
                         headers={'X-Detectify-Key': key,
                                  'content-type': 'application/json'})
        all_assets += r.json()['assets']
        try:
            marker = r.json()['next_marker']
        except KeyError:  # next_marker may not exist when has_more is False
            pass
        has_more = r.json()['has_more']
    return all_assets


def main():
    parser = argparse.ArgumentParser(description='get a count for all subdomains discovered so far in a team')
    parser.add_argument('key', type=str, help='a valid Detectify API key')
    parser.add_argument('-f', '--file', type=str, help='save location for exported results in .csv format')
    args = parser.parse_args()

    all_assets = get_assets(args.key)
    
    if args.file:
        export_to_csv(all_assets, args.file)


if __name__ == '__main__':
    main()
