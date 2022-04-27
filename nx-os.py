import xmltodict
from ncclient import manager
import json


def main():
    """
    Execution begins here
    """

    connection_params = {
        "host": "sandbox-nxos-1.cisco.com",
        "port": 830,
        "username": "admin",
        "password": "Admin_1234!",
        "hostkey_verify": False,
        "allow_agent": False,
        "look_for_keys": False,
        "device_params": {"name": "nexus"},
    }
    print("Connection established..1")
    with manager.connect(**connection_params) as this_conn:
        print("Connection established..")
        nc_filter = """
        <interfaces xmlns="http://openconfig.net/yang/interfaces">
        </interfaces>
        """
        rpc_obj = this_conn.get_config(
           source='running',
           filter=("subtree", nc_filter))
        #print(rpc_obj.xml)
        jresp = xmltodict.parse(rpc_obj.xml)
        for interface in jresp["rpc-reply"]["data"]["interfaces"]["interface"]:
            if interface["name"] == "eth1/36":
                print(json.dumps(interface, indent=2))
        #print(json.dumps(jresp, indent=2))


if __name__ == "__main__":
    main()
