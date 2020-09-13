import subprocess
import re
import os
import requests
import urllib3
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Disables the annoying warning

# Get's the League Client port and password by parsing the lockfile
def get_lcu(): 
    command = "WMIC PROCESS WHERE name='LeagueClientUx.exe' GET commandline" # Shell command on Windows machines to get the League Client process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output = process.stdout.read().decode('utf-8')
    installDir = re.findall(r'"--install-directory=(.*?)"', output)[0] # Find the installation directory using regex
    lockfilePath = os.path.join(installDir, 'lockfile') # Get the lockfile

    if os.path.isfile(lockfilePath) is False: # If no lockfile is found, we error out
        raise Exception('Lockfile could not be found.') 

    lockfileContents = open(lockfilePath).read().split(':') # Split the lockfile
    
    # Lockfile parts that we need
    options = dict()
    options['port'] = lockfileContents[2]
    options['password'] = lockfileContents[3]

    return options

options = get_lcu()
print('Connected to League...')

# Makes a request to the League Client API, which in turn enables the ARAM Skin Boost
def make_request(): 
    session = requests.session()
    session.verify = False # Disable verification for the SSL certificate
    session.post('https://127.0.0.1:%s/lol-champ-select/v1/team-boost/purchase' % options['port'], data={}, auth=HTTPBasicAuth('riot', options['password']))

make_request()
print('Boosted the lobby!')
