import requests
import json

url = "https://x.x.x.x:p/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet" #x.x.x.x ip, p port

payload={}

headers = {
  'Content-type': 'application/yang-data+json ',
  'Accept': 'application/yang-data+json'
}

basic = requests.auth.HTTPBasicAuth('admin', 'hackathon')
response = requests.get(url, headers=headers, auth=basic, verify=False, data=payload)

print(response.text)

dict_output = json.loads(response.text)

with open("output/posta_1.txt", "w") as outfile:
    outfile.write(str(dict_output))

import netmiko

device_info = {
    'device_type': "cisco_ios",
    'ip': "10.54.109.105",
    'username': "admin",
    'password': "hackathon"
}

ssh_session = netmiko.ConnectHandler(**device_info)
result = ssh_session.send_command("show runn | i username")
#ssh_session.disconnect()

with open("output/output1.txt", "w") as outfile:
    outfile.write(result)

cfg_list = [
        "username cisco18 privilege 15 secret 0 cisco"
]
cfg_output = ssh_session.send_config_set(cfg_list)
ssh_session.save_config()
print(cfg_output)

ssh_session.disconnect()

device_info['username'] = "cisco18"
device_info['password'] = "cisco"

ssh_session = netmiko.ConnectHandler(**device_info)
result = ssh_session.send_command("show users")

print(result)

with open("output/output2.txt", "w") as outfile:
    outfile.write(result)

ssh_session.disconnect()
