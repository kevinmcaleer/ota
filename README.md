# MicroPython Over-the-Air updater

---

This library enables you to update your MicroPython projects over the air, at start-up

---

To use this code:
1. add the `ota.py` to your MicroPython device

1. create a file named `WIFI_CONFIG.py`, which contains two variables: `SSID` and `PASSWORD`:

    ```python
    SSID = "my wifi hotspot name"
    PASSWORD = "wifi password"
    ```

1. Add this to your main program code:

    ```python
    from ota import OTAUpdater
    from WIFI_CONFIG import SSID, PASSWORD

    firmware_url = "https://raw.githubusercontent.com/<username>/<repo_name>/"

    ```

    where `<username>` is your github username and `<repo_name>` is the name of the repository to check for updates.

1. Add this to your main program code:

    ```python
    ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "test.py")
    ota_updater.download_and_install_update_if_available()

    ```

    ---

The `OTAUpdater` will connect to github over wifi using your provided wifi credentials, check what the most up-to-date version of the firmware is, compare this to a local file present on the device named `version.json`, which contains the version number of the current on device firmware.

If the local file is not present it will create one with a version number of `0`. If the Github verison is newer it will download the latest file and overwrite the file on the device with the same name, then restart the MicroPython board.
