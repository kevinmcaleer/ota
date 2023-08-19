import network
import urequests
import os
import json
import machine
from time import sleep

class OTAUpdater:

    def __init__(self, ssid, password, repo_url):
        self.ssid = ssid
        self.password = password
        self.repo_url = repo_url
        self.version_url = repo_url + 'main/version.json'
        self.firmware_url = repo_url + 'main/test.py'

        # get the current version (stored in version.json)
        if 'version.json' in os.listdir():    
            with open('version.json') as f:
                self.current_version = json.load(f)['version']
            print(f"Current device firmware version is '{self.current_version}'")

        else:
            self.current_version = 0
            # save the current version
            with open('version.json', 'w') as f:
                json.dump({'version': self.current_version}, f)
            
    def connect_wifi(self):
        # Connect to Wi-Fi

        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(self.ssid, self.password)
        while not sta_if.isconnected():
            print('.', end="")
            sleep(0.25)
        print(f'Connected to WiFi, IP is: {sta_if.ifconfig()[0]}')
        
    def fetch_latest_code(self):
        # Fetch the latest
        
        response = urequests.get(self.firmware_url)
        print(f'Fetched latest firmware code, status: {response.status_code}, -  {response.text}')
        data = response.text
            
        self.latest_code = data

    def save_code(self):
        # Save the fetched code and update the version file to latest version.
        with open('latest_code.py', 'w') as f:
            f.write(self.latest_code)
        
        self.current_version = self.latest_version

        # save the current version
        with open('version.json', 'w') as f:
            json.dump({'version': self.current_version}, f)
        
        self.latest_code = None

    def update_and_reset(self):
        # Handle OTA update and reset.
        print('Updating device...', end='')
        os.rename('latest_code.py', 'main.py')  # Overwrite the old code.
        print('Restarting device...')
        machine.reset()  # Reset the device to run the new code.
        
    def check_for_updates(self):
        # If there's a newer version on GitHub than what's running, update.
        
        self.connect_wifi()
        print('Checking for latest version...')
        response = urequests.get(self.version_url)
        
        data = json.loads(response.text)
       
        # Turn list to dict using dictionary comprehension
        my_dict = {data[i]: data[i + 1] for i in range(0, len(data), 2)}
        
        self.latest_version = my_dict['version']  # This would be base64 encoded.
        print(f'latest version is: {self.latest_version}')
        
        newer_version_available = True if self.current_version < self.latest_version else False
        print(f'Newer version available: {newer_version_available}')    
        return newer_version_available
    
    def download_and_install_update_if_available(self):
        if self.check_for_updates():
            self.fetch_latest_code()
            self.save_code()
            self.update_and_reset()
        else:
            print('No new updates available.')