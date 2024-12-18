"""import_ports.py: retrieve and export all port information in the attack surface in a given Detectify team

The API key permissions required by this script are the following:
- API key version 3

Usage: import_ports.py [-h] -f file key
"""

import argparse
import csv
import requests
import json



API_ROOT = 'https://api.detectify.com/rest'


def export_to_csv(ports: list, file: str) -> None:
    """Export all assets from a given Detectify team to csv

    :param all_assets: A list of dictionaries containing asset information
    :param file: The name of the file to save to
    """
    with open(f'{file}', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id','team_id','asset_id','domain_name','ip_address','port','status','first_seen_at','disappeared_at']) 
        for line in ports:
            writer.writerow([line['id'],line['team_id'],line['asset_id'],line['domain_name'],line['ip_address'],line['port'],line['status'],line['first_seen_at'],line['disappeared_at']])




def get_ports(key):
    """Get ports from Detectify.

    :param key: A Detectify API key with access to the following permissions:
        new APIv3 should be enabled
    :return: A list of all ports
    """
    ports_list = []
    urlpath = f'{API_ROOT}/v3/ports'
    while True: 
        r = requests.get(url=urlpath,
                         headers={'Authorization': key,
                                  'content-type': 'application/json'})
        ports_list += r.json()["items"]
        if "next" in r.json()["pagination"]:
            urlpath = r.json()["pagination"]["next"]
        else:
            return ports_list

def main():


    parser = argparse.ArgumentParser(description='Export a list of ports from Detectify')
    parser.add_argument('key', type=str, help='a valid Detectify API key')
    parser.add_argument('-f', '--file', type=str, help='save location for exported results in .csv format')
    args = parser.parse_args()
    ports = get_ports(args.key)
    if args.file:
        export_to_csv(ports, args.file)
    print("Your file is ready!")


if __name__ == '__main__':
    main()

   