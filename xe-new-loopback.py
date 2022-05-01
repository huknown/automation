import xmltodict
import yaml
from lxml.etree import fromstring
from ncclient import manager
import json
from pprint import pprint
import xml.dom.minidom
from ncclient.operations import RaiseMode


def update_intf(this_conn, this_file):
    with open(this_file, "r") as opened_file:
        intfs_to_update = []
        config_State = yaml.safe_load(opened_file)
        #print(config_State)

        for name, intfs_params in config_State["interfaces"].items():
            intfs_to_update.append(
                {
                    "name": name,
                    "config": {
                        "name": name,
                        "type": {
                            "@xmlns:ianaift": "urn:ietf:params:xml:ns:yang:iana-if-type",
                            "#text": "ianaift:softwareLoopback"
                        },
                        "description": intfs_params["description"],
                        "enabled": "false"
                    },
                    "subinterfaces": {
                        "subinterface": {
                            "index": "0",
                            "config": {
                               "index": "0",
                               "description": intfs_params["description"],
                               "enabled": "false"
                            },
                            "ipv4": {
                                "@xmlns": "http://openconfig.net/yang/interfaces/ip",
                                "addresses": {
                                    "address": {
                                        "ip": intfs_params["ipv4"]["ip"],
                                        "config": {
                                            "ip": intfs_params["ipv4"]["ip"],
                                            "prefix-length": intfs_params["ipv4"]["prefix"]
                                        }
                                    }
                                }
                            }
                        }
                    }
                    }
            )
        config_dict = {
           "config": {
              "interfaces": {
                  "@xmlns": "http://openconfig.net/yang/interfaces",
                  "interface": intfs_to_update,
              }
           }
        }
        #pprint(config_dict)
        xpayload = xmltodict.unparse(config_dict)
        print(xml.dom.minidom.parseString(xpayload).toprettyxml())
        with this_conn.locked(target="running"):
            this_conn.raise_mode = RaiseMode.NONE
            config_resp = this_conn.edit_config(
                target="running", config=xpayload)
            #val_resp = this_conn.validate(source="running")
            this_conn.raise_mode = RaiseMode.ALL
        if config_resp.ok:  # and val_resp.ok:
            print("Interface commited to running configs")
        else:
            print("Its time for ASR come back later")
            print(f"RPC editconfig error: \n {config_resp.error}")
            #print(f"RPC validation error: \n {val_resp.error}")
            #this_conn.discard_changes()
            print("WAAHHH")
    return config_resp


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
    print("Script Started!!")
    with manager.connect(**connection_params) as this_conn:
        print("Connection established..to device")
        config_resp = update_intf(this_conn, "interface_template.yaml")

        #rpc_obj = this_conn.get_config(
        #   source='candidate')
        #print(rpc_obj.xml)


if __name__ == "__main__":
    main()
