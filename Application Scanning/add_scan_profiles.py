"""add_scan_profiles.py: create one or more scan profiles in a given Detectify team

This version of the script DOES NOT avoid creating duplicate scan profiles. Please check your list of domains before
running this script!

The API key permissions required by this script are the following:
- Allow creating scan profiles
- Allow listing domains

Usage: add_scan_profiles.py [-h] [-d [DOMAIN [DOMAIN ...]]] [-f FILE] key
"""

import argparse
import json
import requests

API_BASE_URL = 'https://api.detectify.com/rest'


def create_scan_profile(assets: dict, asset_name: str, key: str) -> None:
    """Create an Application Scan profile for a given domain

    :param assets: A dictionary of assets and tokens
    :param asset_name: The name of the asset associated with the given token
    :param key: A valid Detectify API key
    """
    api_endpoint = '/v2/profiles/'
    asset_token = get_root_asset_token(assets, asset_name)
    if not asset_token:
        return  # If asset_token is not found, skip
    payload = json.dumps({'asset_token': asset_token,
                          'endpoint': asset_name})
    r = requests.post(url=f'{API_BASE_URL}{api_endpoint}',
                      headers={'X-Detectify-Key': key,
                               'content-type': 'application/json'},
                      data=payload)
    print(f'Added scan profile for {asset_name} with code {r.status_code}: {r.reason}')


def get_root_asset_token(assets: dict, asset_name: str) -> str:
    """Look up the asset token associated with the root asset given a domain in Detectify

    :param assets: A dictionary of assets and tokens
    :param asset_name: The name of the asset to look up the root asset token for
    :return: A root asset token
    """
    # For each named root asset, check to see if it is a substring of the provided asset name, and return the first
    try:
        return assets[[root_asset for root_asset in assets if root_asset in asset_name][0]]
    except IndexError:
        print(f'{asset_name} is not associated with any assets. Skipping.')


def get_assets(key: str) -> dict:
    """Get the full list of apex domains and subdomains from Detectify for later filtering

    :param key: A valid Detectify API key
    :return: A dictionary of assets and tokens
    """
    print('Querying assets. . .')
    all_assets = {}
    marker = ''
    has_more = True
    while has_more:
        api_endpoint = f'/v2/assets/'
        r = requests.get(url=f'{API_BASE_URL}{api_endpoint}?marker={marker}',
                         headers={'X-Detectify-Key': key,
                                  'content-type': 'application/json'})
        for asset in r.json()['assets']:
            all_assets[asset['name']] = asset['token']
        try:
            marker = r.json()['next_marker']
        except KeyError:  # next_marker may not exist when has_more is False
            pass
        has_more = r.json()['has_more']
    return all_assets


def main():
    parser = argparse.ArgumentParser(description='Create Application Scan profiles in Detectify')
    parser.add_argument('key', type=str, help='a valid Detectify API key')
    parser.add_argument('-d', '--domain', type=str, nargs='*',
                        help='one or more domains for Application Scan')
    parser.add_argument('-f', '--file', type=str,
                        help='a file containing a list of domains')
    args = parser.parse_args()
    if not (args.domain or args.file):
        parser.error('No domains specified. Use at least one of flag -d or -f.')
    assets = get_assets(args.key)   # Must get full list of assets to convert names to tokens
    print(f'Retrieved {len(assets)} assets')

    if args.domain:
        for domain in args.domain:
            create_scan_profile(assets, domain, args.key)

    if args.file:
        with open(args.domain_file) as domains_to_delete:
            for domain in domains_to_delete.read().splitlines():
                create_scan_profile(assets, domain, args.key)


if __name__ == '__main__':
    main()
