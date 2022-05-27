import requests
import json


def get_interfaces(host):
    #define variables for use in api call
    headers = {"Content-Type": "application/xml", "Accept": "application/json"}
    auth = ("jcluser", "Juniper!1")
    url = "http://" + host + "/rpc/get-interface-information/terse"

    try:
        resp = requests.get(url=url, headers=headers, auth=auth, verify=False)
        interface_obj = resp.json()
        return interface_obj
    #should NOTE proper request exception handling below
    except requests.exceptions.RequestException as e:
        print("Error:" + str(e) + resp.text)
        raise SystemExit(e)


def out_to_console(resp_dict, host):
    device = host.split(":")[1]
    with open("junos_interface.csv", "a") as output:
        for physical_int in resp_dict["interface-information"][0]["physical-interface"]:
            physical_int_name = physical_int["name"][0]["data"]
            #print(f"{physical_int_name}\n")
            if "logical-interface" in physical_int:
                for sub_int in physical_int["logical-interface"]:
                    sub_int_name = sub_int["name"][0]["data"]
                    sub_int_oper = sub_int["oper-status"][0]["data"]
                    sub_int_ip = "undefined"
                    if "address-family" in sub_int:
                        for address_fam in sub_int["address-family"]:
                            if address_fam["address-family-name"][0]["data"] == "inet":
                                if "interface-address" in address_fam:
                                    sub_int_ip = sub_int["address-family"][0]["interface-address"][0]["ifa-local"][0]["data"]

                #if sub_int["address-family"][0]["interface-address"][0]["ifa-local"][0]["data"]:
                #    sub_int_ip = sub_int["address-family"][0]["interface-address"][0]["ifa-local"][0]["data"]
                #else:
                #    sub_int_ip = "undefined"
                    output.write(
                        f"{device},{sub_int_name},{sub_int_oper},{sub_int_ip}\n")


def main():
    #Ask user for device ip
    hosts = ["66.129.234.214:33004", "66.129.234.214:33007",
             "66.129.234.214:33010", "66.129.234.214:33013"]
    requests.packages.urllib3.disable_warnings()
    for host in hosts:
        print(f"Connecting to host: {host}\n")
        dict_resp = get_interfaces(host)
        print(f"Processing details to print to file")
        out_to_console(dict_resp, host)


if __name__ == "__main__":
    main()
