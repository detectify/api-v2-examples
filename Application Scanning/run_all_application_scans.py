"""run_all_application_scans.py: trigger scans on all Application Scan profiles in a given Detectify team

This script triggers IMMEDIATE Application Scans. Please ensure you have permission to start scans before running this
script!

The API key permissions required by this script are the following:
- Allow listing scan profiles
- Allow starting scan

Usage: run_all_application_scans.py [-h] key
"""

import argparse
import requests

API_BASE_URL = 'https://api.detectify.com/rest'


def start_application_scan(profile: dict, key: str) -> None:
    """Trigger an immediate scan on a given Application Scan profile

    :param profile: A dictionary containing the necessary identifiers for an Application Scan profile
    :param key: A valid Detectify API key
    """
    api_endpoint = f'/v2/scans/{profile["token"]}/'
    r = requests.post(url=f'{API_BASE_URL}{api_endpoint}',
                      headers={'X-Detectify-Key': key,
                               'content-type': 'application/json'})
    print(f'Starting scan on {profile["endpoint"]} with code {r.status_code}: {r.reason}')


def get_scan_profiles(key: str) -> list:
    """Get the full set of scan profiles from a given Detectify team

    :param key: A valid Detectify API key
    :return: A list of dictionaries containing identifiers for all Application Scan profiles
    """
    print('Querying list of scan profiles...')
    api_endpoint = f'/v2/profiles/'
    r = requests.get(url=f'{API_BASE_URL}{api_endpoint}',
                     headers={'X-Detectify-Key': key,
                              'content-type': 'application/json'})
    return r.json()


def main():
    parser = argparse.ArgumentParser(description='Run all application scan profiles')
    parser.add_argument('key', type=str, help='a valid Detectify API key')
    args = parser.parse_args()

    scan_profiles = get_scan_profiles(args.key)

    for profile in scan_profiles:
        start_application_scan(profile, args.key)


if __name__ == '__main__':
    main()
