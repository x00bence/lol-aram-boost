import subprocess
import re
import urllib3
import requests

if __name__ == '__main__':
    try:        
        print('$ lol-aram-boost | x00bence\n')

        # Batch command to get the client process
        command = "WMIC PROCESS WHERE name='LeagueClientUx.exe' GET commandline"

        # Execute the command
        output = subprocess.Popen(command, stdout=subprocess.PIPE,
                                shell=True).stdout.read().decode('utf-8')

        # Extract needed args
        port = re.findall(r'"--app-port=(.*?)"', output)[0]
        password = re.findall(r'"--remoting-auth-token=(.*?)"', output)[0]

        # Disables the annoying certificate error
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Set up session
        session = requests.session()
        session.verify = False

        print('[*] Connected to League; Enter to boost lobby, ^C to exit.')

        # Loop
        while True:
            input()
            session.post('https://127.0.0.1:%s/lol-login/v1/session/invoke?destination=lcdsServiceProxy&method=call&args=["","teambuilder-draft","activateBattleBoostV1",""]' %
                    port, data={}, auth=requests.auth.HTTPBasicAuth('riot', password))
            print('[+] Boosted the lobby!')
    except KeyboardInterrupt:
        exit()

