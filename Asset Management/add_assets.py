"""add_asset.py: add assets to a given Detectify team

The API key permissions required by this script are the following:
- Allow creating domains
- Allow uploading zone files

Usage: add_assets.py [-h] [-d [DOMAIN [DOMAIN ...]]] [-f FILE]
                     [-z [ZONEFILE [ZONEFILE ...]]]
                     key
"""

import argparse
import json
import requests

API_BASE_URL = 'https://api.detectify.com/rest'


def add_asset(domain: str, key: str) -> None:
    """Add an asset to Detectify

    :param domain: An FQDN to add to the Detectify asset inventory
    :param key: A valid Detectify API key
    """
    api_endpoint = f'/v2/assets/'
    payload = json.dumps({'name': domain.strip()})
    r = requests.post(url=f'{API_BASE_URL}{api_endpoint}',
                      headers={'X-Detectify-Key': key,
                               'content-type': 'application/json'},
                      data=payload)
    print(f'Added asset {domain.strip()} with code {r.status_code}: {r.reason}')


def upload_zone_file(zone_file: str, key: str) -> None:
    """Upload a zone file to populate domain information

    :param zone_file: A zone file including a specified $ORIGIN
    :param key: A valid Detectify API key
    """
    api_endpoint = f'/v2/zone/file/'
    r = requests.post(url=f'{API_BASE_URL}{api_endpoint}',
                      headers={'X-Detectify-Key': key,
                               'content-type': 'application/json'},
                      data=open(zone_file, 'rb'))
    print(f'Uploaded zone file {zone_file} with code {r.status_code}: {r.reason}')


def main():
    parser = argparse.ArgumentParser(description='Add assets to Detectify')
    parser.add_argument('key', type=str, help='a valid Detectify API key')
    parser.add_argument('-d', '--domain', type=str, nargs='*',
                        help='one or more domains to add to Detectify')
    parser.add_argument('-f', '--file', type=str,
                        help='a file containing a list of apex domains')
    parser.add_argument('-z', '--zonefile', type=str, nargs='*',
                        help='one or more zone files including a specified $ORIGIN')
    args = parser.parse_args()
    if not (args.domain or args.file or args.zonefile):
        parser.error('No domains specified. Use at least one of flag -d, -f, or -z.')

    if args.domain:
        for domain in args.domain:
            add_asset(domain, args.key)

    if args.file:
        with open(args.file, 'r') as infile:
            for domain in infile.read().splitlines():
                add_asset(domain, args.key)

    if args.zonefile:
        for zone_file in args.zonefile:
            upload_zone_file(zone_file, args.key)


if __name__ == '__main__':
    main()
