import requests
import json


def calculate_top_ten_ints(interfaces):
    interface_volume_dict = {}
    print(json.dumps(interfaces, indent=2))
    for interface in interfaces["interface"]:
        total_bytes = int(interface["statistics"]["in-octets"]) + \
                          int(interface["statistics"]["out-octets"])
        name = {}
        interface_volume_dict[interface["name"]] = total_bytes

    print(json.dumps(interface_volume_dict, indent=2))
    print(sorted(interface_volume_dict.items(),
          key=lambda x: x[1], reverse=True))

#Funciton uses restconf to get the interface stats
#Returns interfacce stats json object
#Accepts host as parameter


def get_interface_stats(host):
    api_url = "https://" + host + "/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces"
    credentials = ("developer", "C1sco12345")
    print(api_url)
    headers = {"Content-type": "application/yang-data+json",
               "Accept": "application/yang-data+json"}
    try:
        response = requests.get(url=api_url, headers=headers,
                                auth=credentials, verify=False)
        interfaces_json = response.json()
        return interfaces_json

    except:
        print("Error: " + str(response.status_code) + response.text)


def main():
    print("Please enter host: ")
    host = input()
    requests.packages.urllib3.disable_warnings()
    response = get_interface_stats(host)
    calculate_top_ten_ints(response["Cisco-IOS-XE-interfaces-oper:interfaces"])


if __name__ == "__main__":
    main()
