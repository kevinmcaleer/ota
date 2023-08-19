from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD

firmware_url = "https://raw.githubusercontent.com/kevinmcaleer/ota_test/"

ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")

ota_updater.download_and_install_update_if_available()