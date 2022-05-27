import requests


def get_interfaces(host):
    url = "http://66.129.234.213:41001/rpc/get-interface-information"
    headers = {"Content-Type": "application/xml", "Accept": "application/json"}
    creds = ("jcluser", "Juniper!1")

    try:
        resp = requests.get(url=url, auth=creds, headers=headers, verify=False)
        interfaces = resp.json()
        return interfaces
    except:
        print("Error: " + str(resp.status_code) + resp.text)


def main():
    #Askfor host to get interfaces from
    print(f"Please enter the host to fetch data from:\n")
    host = input()
    process_host = get_interfaces(host)
    requests.packages.urllib3.disable_warnings()
    print(f"Host | Interface Name | IP | Type")
    for interface in process_host["interface-information"][0]["physical-interface"]:
        #print Host, Interface name, IP, Type,
        #print(interface)
        name = interface["name"][0]["data"]
        if "link-level-type" in interface:
            link_type = interface["link-level-type"][0]["data"]
        else:
            link_type = "N/A"
        print(f"{host} | {name} | {link_type}")


if __name__ == "__main__":
    main()
