"""import_ips.py: retrieve and export IP addresses for all domains in a given Detectify team

The API key permissions required by this script are the following:
- API key version 3

Usage: import_ips.py [-h] -f file key
"""


import argparse
import csv
import requests
import json



API_ROOT = 'https://api.detectify.com/rest'

def export_to_csv(ips: list, file: str) -> None:
    """Export all assets from a given Detectify team to csv

    :param all_assets: A list of dictionaries containing asset information
    :param file: The name of the file to save to
    """
    with open(f'{file}', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id','ip_address','active','enriched','domain_name','asset_id','team_id','ip_version','first_seen_at','disappeared_at','autonomous-system-name','autonomous-system-domain','autonomous-system-number','geolocation-continent','geolocation-continent_name','geolocation-country','geolocation-country-name']) 
        for line in ips:
            writer.writerow([line['id'],line['ip_address'],line['active'],line['enriched'],line['domain_name'],line['asset_id'],line['team_id'],line['ip_version'],line['first_seen_at'],line['disappeared_at'],line['autonomous_system']['name'],line['autonomous_system']['domain'],line['autonomous_system']['number'],line['geolocation']['continent'],line['geolocation']['continent_name'],line['geolocation']['country'],line['geolocation']['country_name']])

        
def get_ips(key):
    """Get IP addresses from Detectify.

    :param key: A Detectify API key with access to the following permissions:
        new APIv3 should be enabled
    :return: A list of all IP addresses
    """
    ips_list = []
    urlpath = f'{API_ROOT}/v3/ips'
    while True: 
        r = requests.get(url=urlpath,
                         headers={'Authorization': key,
                                  'content-type': 'application/json'})
        ips_list += r.json()["items"]
        if "next" in r.json()["pagination"]:
            urlpath = r.json()["pagination"]["next"]
        else:
            return ips_list

def main():


    parser = argparse.ArgumentParser(description='Export a list of IP addresses from Detectify')
    parser.add_argument('key', type=str, help='a valid Detectify API key')
    parser.add_argument('-f', '--file', type=str, help='save location for exported results in .csv format')
    args = parser.parse_args()
    ips = get_ips(args.key)
    if args.file:
        export_to_csv(ips, args.file)
   
    print("Your file is ready!")


if __name__ == '__main__':
    main()

   