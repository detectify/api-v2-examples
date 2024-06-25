"""bulk_update_SM_settings_from_list.py: update the Surface Monitoring settings for a given list of domains

The API key permissions required by this script are the following:
- Allow listing domains
- Allow updating domains

Usage: bulk_update_SM_settings_from_list.py [-h] domain_file key
"""

import argparse
import json
import requests

API_BASE_URL = 'https://api.detectify.com/rest'


def update_surface_monitoring_settings(domain: dict, key: str) -> None:
    """Update the Surface Monitoring settings for a given domain

    :param domain: A dictionary containing an asset name and token
    :param key: A valid Detectify API key
    """
    api_endpoint = f'/v2/domains/{domain["token"]}/settings/'

    # Change these settings as desired
    # Current schema always available at https://developer.detectify.com/#operation/updateAssetSettings
    payload = {"brute_force": True,
               "custom_headers": {},
               "enable_active_tls_assessments": True,
               "enable_certificate_assessments": True,
               "enable_passive_tls_assessments": True,
               "enable_tls_discovery": True,
               "fingerprinting": True,
               "include_discovered_ports_in_surface_monitoring": True,
               "monitoring": True,
               "requests_per_second": 0,
               "scrape": True,
               "ssl_audit": True,
               "stateless_tests": True,
               "subdomain_takeover_tests": True}
    r = requests.put(url=f'{API_BASE_URL}{api_endpoint}',
                     headers={'X-Detectify-Key': key,
                              'content-type': 'application/json'},
                     data=json.dumps(payload))
    print(f'Updated settings for asset {domain["name"]} with response code {r.status_code}: {r.reason}')


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


def domains_to_tokens(domains: list, key: str) -> list:
    """Associate each provided root domain with its token

    :param domains: A list of domains provided by the user
    :param key: A valid Detectify API key
    :return: A filtered list of dictionaries containing asset names and tokens
    """
    all_assets = get_root_assets(key)
    tokens = []
    for asset in all_assets:
        if asset['name'] in domains:
            tokens.append({'name': asset['name'], 'token': asset['token']})
    return tokens


def main():
    parser = argparse.ArgumentParser(description='update the Surface Monitoring settings for a given list of domains')
    parser.add_argument('domain_file', type=str, help='a file containing a list of apex domains')
    parser.add_argument('key', type=str, help='a valid Detectify API key')
    args = parser.parse_args()

    with open(args.domain_file) as file:
        domains = domains_to_tokens(file.read().splitlines(), args.key)

    for domain in domains:
        update_surface_monitoring_settings(domain, args.key)


if __name__ == '__main__':
    main()
