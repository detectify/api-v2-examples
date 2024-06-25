"""get_SM_settings.py: retrieve and export the Surface Monitoring settings for all domains in a given Detectify team

The API key permissions required by this script are the following:
- Allow listing domains

Usage: get_SM_settings.py [-h] key file
"""

import argparse
import csv
import requests

API_BASE_URL = 'https://api.detectify.com/rest'


def export_to_csv(asset_settings: list, file: str) -> None:
    """Export all asset settings from a given Detectify team to csv

    :param asset_settings: A list of dictionaries containing asset names and setting information
    :param file: The name of the file to save to
    """
    with open(f'{file}', 'w+', newline='') as f:
        writer = csv.writer(f)
        header_row = ['name'] + [x for x in asset_settings[0]['settings']]
        writer.writerow(header_row)

        for asset in asset_settings:
            row = [asset['name']] + list(asset['settings'].values())
            writer.writerow(row)


def get_asset_settings(key: str, token: str) -> dict:
    """Get the Surface Monitoring settings for a given Detectify asset

    :param key: A valid Detectify API key
    :param token: A valid asset token for a root asset
    :return: A dictionary containing all asset settings
    """
    api_endpoint = f'/v2/domains/{token}/settings/'
    r = requests.get(url=f'{API_BASE_URL}{api_endpoint}',
                     headers={'X-Detectify-Key': key,
                              'content-type': 'application/json'})
    return r.json()


def get_root_assets(key: str) -> list:
    """Get the full list of apex domains from Detectify

    :param key: A valid Detectify API key
    :return: A list of dictionaries containing asset information
    """
    marker = ''
    has_more = True
    assets = []
    while has_more:
        api_endpoint = '/v2/assets/'
        r = requests.get(url=f'{API_BASE_URL}{api_endpoint}?marker={marker}',
                         headers={'X-Detectify-Key': key,
                                  'content-type': 'application/json'})
        try:
            marker = r.json()['next_marker']
        except KeyError:  # next_marker may not exist when has_more is False
            pass
        has_more = r.json()['has_more']
        assets += r.json()['assets']
    return assets


def main():
    parser = argparse.ArgumentParser(description='export the Surface Monitoring settings for a given list of domains')
    parser.add_argument('key', type=str, help='a valid Detectify API key')
    parser.add_argument('file', type=str, help='save location for exported results in .csv format')
    args = parser.parse_args()

    root_assets = get_root_assets(args.key)
    print(f'Retrieved {len(root_assets)} assets')
    asset_settings = []

    for asset in root_assets:
        asset_settings.append({'name': asset['name'],
                               'settings': get_asset_settings(args.key, asset['token'])})

    export_to_csv(asset_settings, args.file)


if __name__ == '__main__':
    main()
