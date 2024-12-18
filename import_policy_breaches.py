"""import_policy_breaches.py: retrieve and export the policy breaches in the attack surface in a given Detectify team

The API key permissions required by this script are the following:
- API key version 3

Usage: import_policy_breaches.py [-h] -f file key
"""

import argparse
import csv
import requests
import json



API_ROOT = 'https://api.detectify.com/rest'


def export_to_csv(breaches: list, file: str) -> None:
    """Export all assets from a given Detectify team to csv

    :param all_assets: A list of dictionaries containing asset information
    :param file: The name of the file to save to
    """
    with open(f'{file}', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id','policy_id','policy_name','asset_id','asset_name','severity','active','status','status_updated_at','first_seen_at','disappeared_at']) 
        for line in breaches:
            writer.writerow([line['id'],line['policy_id'],line['policy_name'],line['asset_id'],line['asset_name'],line['severity'],line['active'],line['status'],line['status_updated_at'],line['first_seen_at'],line['disappeared_at']])



def get_policy_breaches(key):
    """Get policy breaches from Detectify.

    :param key: A Detectify API key with access to the following permissions:
        new APIv3 should be enabled
    :return: A list of all policy breaches
    """
    policy_breaches_list = []
    urlpath = f'{API_ROOT}/v3/breaches'
    while True: 
        r = requests.get(url=urlpath,
                         headers={'Authorization': key,
                                  'content-type': 'application/json'})
        policy_breaches_list += r.json()["items"]
        if "next" in r.json()["pagination"]:
            urlpath = r.json()["pagination"]["next"]
        else:
            return policy_breaches_list




def main():


    parser = argparse.ArgumentParser(description='Export a list of policy breaches from Detectify')
    parser.add_argument('key', type=str, help='a valid Detectify API key')
    parser.add_argument('-f', '--file', type=str, help='save location for exported results in .csv format')
    args = parser.parse_args()
    policy_breaches = get_policy_breaches(args.key)

    if args.file:
        export_to_csv(policy_breaches, args.file)


    print("Your file is ready!")

if __name__ == '__main__':
    main()

   