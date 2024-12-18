"""import_technologies.py: retrieve and export the Surface Monitoring settings for all domains in a given Detectify team

The API key permissions required by this script are the following:
- API key version 3

Usage: import_technologies.py [-h] key
"""

import argparse
import csv
import requests
import json



API_ROOT = 'https://api.detectify.com/rest'


def export_to_csv(techs: list, file: str) -> None:
    """Export all assets from a given Detectify team to csv

    :param all_assets: A list of dictionaries containing asset information
    :param file: The name of the file to save to
    """
    with open(f'{file}', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id','team_id','asset_id','domain_name','service_protocol','port','name','version','categories','active','first_seen_at','disappeared_at']) 
        for line in techs:
            writer.writerow([line['id'],line['team_id'],line['asset_id'],line['domain_name'],line['service_protocol'],line['port'],line['name'],line['version'],line['categories'],line['active'],line['first_seen_at'],line['disappeared_at']])




def get_technologies(key):
    """Get technologies from Detectify.

    :param key: A Detectify API key with access to the following permissions:
        new APIv3 should be enabled
    :return: A list of all technologies
    """
    techs_list = []
    urlpath = f'{API_ROOT}/v3/technologies'
    while True: 
        r = requests.get(url=urlpath,
                         headers={'Authorization': key,
                                  'content-type': 'application/json'})
        techs_list += r.json()["items"]
        if "next" in r.json()["pagination"]:
            urlpath = r.json()["pagination"]["next"]
        else:
            return techs_list

def main():


    parser = argparse.ArgumentParser(description='Export a list of technologies from Detectify')
    parser.add_argument('key', type=str, help='a valid Detectify API key')
    parser.add_argument('-f', '--file', type=str, help='save location for exported results in .csv format')
    args = parser.parse_args()
    techs = get_technologies(args.key)
    if args.file:
        export_to_csv(techs, args.file)

    print("Your file is ready!")


if __name__ == '__main__':
    main()

   