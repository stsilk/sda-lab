#!/bin/python3

import paramiko
import time
import sys
import requests
import getpass
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()

ip = input("IP address of the switch: ")
username = input("Username: ")
password = getpass.getpass()

#resetSwitch "admin" "password" "enablepass" "switch-1234"

#username = str(sys.argv[1])
#password = str(sys.argv[2])
#enable = str(sys.argv[3])
#deviceName = str(sys.argv[4])

DNA_URL = 'https://192.168.15.91'
AUTH_URL = '/dna/system/api/v1/auth/token'
DEVICES_URL = '/dna/intent/api/v1/network-device/'
EDGE_DEVICE_URL = '/dna/intent/api/v1/business/sda/edge-device'

def runCommand(command):
    remote_conn.send(command)
    time.sleep(1)
    output = remote_conn.recv(5000)
    print(output.decode("utf-8"))
    return output.decode("utf-8")

remote_conn_pre=paramiko.SSHClient()
remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_conn_pre.connect(ip, port=22, username=username,
                        password=password,
                        look_for_keys=False, allow_agent=False)
remote_conn = remote_conn_pre.invoke_shell()
output = remote_conn.recv(65535)

print("Resetting device")
output = runCommand("show run | inc crypto pki trustpoint TP-self-signed\n")
trustpoint = output.split('\r\n')[1]
print(trustpoint)

#Delete Self signed cert
runCommand("conf t\n")
runCommand("no {0}\n".format(trustpoint))
runCommand("yes\n")

#Remove pnp profile
runCommand("no pnp profile pnp-zero-touch\n")

#Remove certificate pool
runCommand("no crypto pki certificate pool\n")
runCommand("yes\n")

#Save changes
runCommand("do write\n")

#Move to enable mode
runCommand("end\n")

#delete certs
runCommand("delete /force nvram:*.cer\n")
runCommand("write erase\n")
runCommand("y\n")
runCommand("reload\n")
runCommand("yes\n")






