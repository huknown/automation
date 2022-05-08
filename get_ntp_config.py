import requests
import socket


def main():

    #Parameters for url request
    creds = ("developer", "C1sco12345")
    headers = {"Accept": "application/yang-data+json"}

    #Open the output.txt file and prepare it for write
    with open("ntp_output.txt", "w") as outputfile:
        #Add some table titles in file for context
        outputfile.write("ROUTER:    NTP_SERVER\n")
        outputfile.write("====================\n")
        #OPen the hosts file and read hosts
        with open("hosts-file", "r") as hosts:
            #Loop through each host and get ntp using restconf
            for line in hosts:
                print(line.strip())
                api_url = "https://" + line.strip() + \
                    "/restconf/data/Cisco-IOS-XE-native:native/ntp"
                try:
                    response = requests.get(
                        url=api_url, headers=headers, auth=creds, verify=False)
                    #print(response.json())
                    ntp_obj = response.json()
                    ntp_list = ntp_obj["Cisco-IOS-XE-native:ntp"]["Cisco-IOS-XE-ntp:server"]["server-list"]
                    #print(ntp_list)
                    for ntp in ntp_list:
                       outputfile.write(line.strip(
                       ) + ":    "
                           + ntp["ip-address"] + "\n")

                except requests.exceptions.RequestException as e:
                    #exit the script and throw relevant error
                    print(f"Error encountered {e}")
                    SystemExit(e)
                #write ntp and router to file as needed


if __name__ == "__main__":
    main()
