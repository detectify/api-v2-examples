"""delete_assets.py: delete specified root assets from a given Detectify team

The API key permissions required by this script are the following:
- Allow deleting domains
- Allow listing domains

Usage: delete_assets.py [-h] [-d [DOMAIN [DOMAIN ...]]] [-f FILE] key
"""

import argparse
import requests

API_BASE_URL = 'https://api.detectify.com/rest'


def delete_asset(asset_token: str, asset_name: str, key: str) -> None:
    """Delete a given Detectify asset

    :param asset_token: The internal UUID used to identify individual assets
    :param asset_name: The name of the asset associated with the given token
    :param key: A valid Detectify API key
    """
    try:
        api_endpoint = f'/v2/assets/{asset_token}/'
        r = requests.delete(url=f'{API_BASE_URL}{api_endpoint}',
                            headers={'X-Detectify-Key': key,
                                     'content-type': 'application/json'})
        print(f'deleted asset {asset_name} with code {r.status_code}: {r.reason}')
    except KeyError:
        print(f'Asset {asset_name} not found, skipping')
        pass


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
        r = requests.get(url=f'{API_BASE_URL}{api_endpoint}?marker={marker}&include_subdomains=true',
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
    parser = argparse.ArgumentParser(description='Delete assets from Detectify')
    parser.add_argument('key', type=str, help='a valid Detectify API key')
    parser.add_argument('-d', '--domain', type=str, nargs='*',
                        help='one or more domains to add to Detectify')
    parser.add_argument('-f', '--file', type=str,
                        help='a file containing a list of apex domains')
    args = parser.parse_args()
    if not (args.domain or args.file):
        parser.error('No domains specified. Use at least one of flag -d or -f.')
    assets = get_assets(args.key)   # Must get full list of assets to convert names to tokens
    print(f'Retrieved {len(assets)} assets')

    if args.domain:
        for domain in args.domain:
            delete_asset(assets[domain], domain, args.key)

    if args.file:
        with open(args.file) as domains_to_delete:
            for domain in domains_to_delete.read().splitlines():
                delete_asset(assets[domain], domain, args.key)


if __name__ == '__main__':
    main()
