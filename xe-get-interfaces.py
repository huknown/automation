import xmltodict
from ncclient import manager
import json
import logging


def main():
    """
    Execution begins here
    """

    connection_params = {
        "host": "sandbox-iosxe-recomm-1.cisco.com",
        "port": 830,
        "username": "developer",
        "password": "C1sco12345",
        "hostkey_verify": False,
        "allow_agent": False,
        "look_for_keys": False,
        "device_params": {"name": "iosxe"},
    }
    print("Connection established..1")
    #logging.basicConfig(level=logging.DEBUG)
    with manager.connect(**connection_params) as this_conn:
        print("Connection established..")
        nc_filter = """
        <interfaces xmlns="http://openconfig.net/yang/interfaces">
         <interface>
         <name>Loopback33</name>
         </interface>
        </interfaces>
        """
        rpc_obj = this_conn.get_config(
           source='running',
           filter=("subtree", nc_filter))
        print(rpc_obj.xml)
        jresp = xmltodict.parse(rpc_obj.xml)
        interface_list = []
        for interface in jresp["rpc-reply"]["data"]["interfaces"]["interface"]:
            #if interface["config"]["type"]["#text"] == "ianaift:ethernetCsmacd":
            #interface_list.append(interface)
            test = interface["name"]
            print(f"{ test }")
        #print(json.dumps(jresp, indent=2))


if __name__ == "__main__":
    main()
