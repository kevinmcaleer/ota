from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD

firmware_url = "https://raw.githubusercontent.com/kevinmcaleer/ota_test/"

ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")
# if ota_updater.check_for_updates():
#     ota_updater.fetch_latest_code()
#     ota_updater.save_code()
#     ota_updater.update_and_reset()
# else:
#     print('done')

ota_updater.download_and_install_update_if_available()