import datetime
import json

import requests

"""
Requires a valid API Token
Refer to the Cloudflare Wiki to see how you can get yours one.
Double-Check you have the correct permissions for DNS entries.
"""


token = "<API-TOKEN>"
base_url = "https://api.cloudflare.com/client/v4"
headers = {"Content-Type":"application/json",
           "Authorization":f"Bearer {token}",
           }

zone_list = []

def get_zones(headers):
    print("[*] Fetching Zones...")
    zones_request = requests.get(f"{base_url}/zones", headers=headers)
    zones_json = json.loads(zones_request.text)

    for zone_result in zones_json['result']:
        zone_list.append((zone_result['name'],zone_result['id']))

    zone_index = 0
    for zone in zone_list:
        print(f"[*] [{zone_index}] Found Zone: {zone[0]} - {zone[1]}")
        zone_index +=1
    choice = int(input("[*] Purge DNS-Records for which zone? 0/1/2 etc..]\n"))

    while choice > zone_index-1:
        print("[!] Please pick the correct entry marked by the number [0]/[1]...")
        choice = int(input("[*] Purge DNS-Records for which zone?\n"))

    get_dns_records(zone_list[choice])

def get_dns_records(zone_entry):
    dns_records = []
    print(f"[*] Fetching DNS-Records for: {zone_entry[0]} - {zone_entry[1]}")
    page_index = 1
    while True:

        dns_records_request = requests.get(f"{base_url}/zones/{zone_entry[1]}/dns_records?page={page_index}", headers=headers)
        dns_records_json = json.loads(dns_records_request.text)

        if len(dns_records_json['result']) == 0:
            print("[*] Reached last page...")
            choice = input("[*] Print records? [y/n]\n")
            if choice.lower() in ["y", "yes"]:
                for record in dns_records:
                    print(f"[*] Record: {record[0]} - {record[1]}")
            else:
                print("[*] Omitting Print...")
            break;
        else:
            for dns_record in dns_records_json['result']:
                dns_records.append((dns_record['name'],dns_record['id']))

            print(f"[*] Found Total: {len(dns_records)} DNS Records")

            print("[*] Checking Next Page...")
            page_index += 1
    choice = input(("[*] Do you want to keep a DNS Record? [y/n]\n"))
    if choice.lower() in ["y","yes"]:
        keep_records = input("[*] Please provide Record-Names comma separated. e.G. www.domain.com,mail.domain.com\n")
        user_keep_record_list = keep_records.split(",")

        keep_record_list = []
        for keep_record in user_keep_record_list:
            record_found = False
            for record in dns_records:
                if record[0] == keep_record:
                    keep_record_list.append(record)
                    dns_records.remove(record)
                    record_found = True
                    break;
            if not record_found:
                print(f"[!] Record {keep_record} not found in Record-List...Omitting")
        print("\n")
        print("[*] Keeping records\n")
        for record in keep_record_list:
            print(f"[*] {record[0]} - {record[1]}")


        print("[*] Entering Danger-Mode...")
        delete_dns_records(dns_records,zone_entry)

def delete_dns_records(dns_records,zone_entry):
    print("\n")
    print("[!] DANGER-ZONE: Deleting Records. Continue at your own risk\n")
    print(f"[!] {len(dns_records)} Records will be deleted.")
    final_choice = input(f"[!] Do you want to delete {len(dns_records)} records from your zone: {zone_entry[0]}? [y/n]\n")
    if final_choice.lower() in ["y","Y"]:
        print(f"[*] Safety-Measure: Exporting Current BIND config...")
        export_bind_config_request = requests.get(f"{base_url}/zones/{zone_entry[1]}/dns_records/export",headers=headers)
        with open(f"./{datetime.datetime.now()}_{zone_entry[0]}_dns_record_export.txt","w") as file:
            file.write(export_bind_config_request.text)
            print(f"[*] Wrote export to: ./{zone_entry[0]}_dns_record_export.txt")
            file.close

        print(f"[!] Deleting {len(dns_records)} Records")
        deleted_records = []
        for record in dns_records:
            delete_dns_record_request = requests.delete(f"{base_url}/zones/{zone_entry[1]}/dns_records/{record[1]}",headers=headers)
            deleted_record_json = json.loads(delete_dns_record_request.text)
            deleted_records.append(deleted_record_json['result']['id'])
            print(f"[*] Deleted: {deleted_record_json['result']['id']}")
    else:
        print("[*] Exiting...")
        exit(0)
get_zones(headers)