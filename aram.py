import subprocess
import re
import os
import requests
from requests.auth import HTTPBasicAuth


def get_lcu(): 
    command = "WMIC PROCESS WHERE name='LeagueClientUx.exe' GET commandline"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output = process.stdout.read().decode('utf-8')
    installDir = re.findall(r'"--install-directory=(.*?)"', output)[0]
    lockfilePath = os.path.join(installDir, 'lockfile')

    if os.path.isfile(lockfilePath) is False:
        raise Exception('Lockfile could not be found.') 

    lockfileContents = open(lockfilePath).read().split(':')
    
    options = dict()
    options['port'] = lockfileContents[2]
    options['password'] = lockfileContents[3]

    return options

options = get_lcu()
print('Connected to League...')

def make_request(): 
    session = requests.session()
    session.verify = False
    session.post('https://127.0.0.1:%s/lol-champ-select/v1/team-boost/purchase' % options['port'], data={}, auth=HTTPBasicAuth('riot', options['password']))

make_request()
print('Boosted the lobby!')
