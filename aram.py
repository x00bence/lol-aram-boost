import subprocess
import re
import os
import urllib3
import requests

# Disables the annoying error
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

command = "WMIC PROCESS WHERE name='LeagueClientUx.exe' GET commandline"

output = subprocess.Popen(command, stdout=subprocess.PIPE,
                          shell=True).stdout.read().decode('utf-8')

port = re.findall(r'"--app-port=(.*?)"', output)[0]
password = re.findall(r'"--remoting-auth-token=(.*?)"', output)[0]

print('Connected to League ...')

session = requests.session()
session.verify = False

session.post('https://127.0.0.1:%s/lol-champ-select/v1/team-boost/purchase' %
             port, data={}, auth=requests.auth.HTTPBasicAuth('riot', password))

print('Boosted the lobby!')

input("Press any key to continue . . .")
