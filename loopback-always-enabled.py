import os
import time
import requests
import json

while True:
    response = os.system("ping -c 1 " + '10.54.109.105' + ">/dev/null 2>&1")
    if response != 0:
        print("No hay conectividad a 10.54.109.105...")
        time.sleep(15)
        continue


    url = "https://x.x.x.x:p/restconf/data/ietf-interfaces:interfaces/interface=Loopback18"

    payload={}

    headers = {
        'Content-type': 'application/yang-data+json ',
        'Accept': 'application/yang-data+json'
    }

    basic = requests.auth.HTTPBasicAuth('admin', 'hackathon')
    response = requests.get(url, headers=headers, auth=basic, verify=False, data=payload)

    enable = response.json()['ietf-interfaces:interface']['enabled']
    if not enable:
        print("Interfaz Loopback18 DOWN(" + (str(enable) + ")"))
    else:
        print("Interfaz Loopback18 UP(" + (str(enable) + ")"))

    if not enable:
        url = "https://x.x.x.x:p/restconf/data/ietf-interfaces:interfaces/interface=Loopback18"

        payload='''{
  "ietf-interfaces:interface": { "name": "Loopback18",
    "type": "iana-if-type:softwareLoopback",
    "enabled": true,
    "ietf-ip:ipv4": {
      "address": [
        {
          "ip": "x.x.x.x",
          "netmask": "255.255.255.255"
        }
      ]
    },
    "ietf-ip:ipv6": {
    }
  }
}'''
        headers = {
            'Content-type': 'application/yang-data+json ',
            'Accept': 'application/yang-data+json'
        }
        basic = requests.auth.HTTPBasicAuth('admin', 'hackathon')
        response = requests.put(url, headers=headers, auth=basic, verify=False, data=payload)
        #print("Se levanto la inerfaz! " + str(response.json()))
    time.sleep(15)
