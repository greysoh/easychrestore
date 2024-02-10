from simple_term_menu import TerminalMenu

import urllib.request
from json import loads

from dl import download

print("""                                                                                                    
,------.                        ,-----.,--.     ,------.                ,--.                        
|  .---' ,--,--. ,---.,--. ,--.'  .--./|  ,---. |  .--. ' ,---.  ,---.,-'  '-. ,---. ,--.--. ,---.  
|  `--, ' ,-.  |(  .-' \  '  / |  |    |  .-.  ||  '--'.'| .-. :(  .-''-.  .-'| .-. ||  .--'| .-. : 
|  `---.\ '-'  |.-'  `) \   '  '  '--'\|  | |  ||  |\  \ \   --..-'  `) |  |  ' '-' '|  |   \   --. 
`------' `--`--'`----'.-'  /    `-----'`--' `--'`--' '--' `----'`----'  `--'   `---' `--'    `----' 
                      `---'                                                                         
      
EasyChRestore by @greysoh - Make ChromeOS flashing great again!
""")

print("Stage 1: Fetching JSON files...")

# Mainstream chromeOS
raw_chromeos_request = urllib.request.Request(
    url = "https://dl.google.com/dl/edgedl/chromeos/recovery/recovery2.json",
    data = None,

    headers = {
        # Chrome latest useragent (from 2/10/24)
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
)

raw_chromeos_listing = urllib.request.urlopen(raw_chromeos_request).read()
chromeos_listing = loads(raw_chromeos_listing)

# "Cloudready" chromeOS
raw_chromeos_cloudready_request = urllib.request.Request(
    url = "https://dl.google.com/dl/edgedl/chromeos/recovery/cloudready_recovery2.json",
    data = None,

    headers = {
        # Chrome latest useragent (from 2/10/24)
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
)

raw_chromeos_cloudready_listing = urllib.request.urlopen(raw_chromeos_cloudready_request).read()
chromeos_listing += loads(raw_chromeos_cloudready_listing)

print("Stage 2: Generating list of items...")

# TODO: There has to be a better way to do this, but this does work.
dataset = set()

for entry in chromeos_listing:
    dataset.add(entry["manufacturer"])

dataset = list(dataset)

vendor_devices = []
vendor_device_channel = []

vendor_device_selection_data = set()
vendor_device_channel_data = set()

print("Stage 3: Loading UI...")

terminal_menu = TerminalMenu(dataset, title="Choose a manufacturer\n")
manufacturer_index = terminal_menu.show()

vendor_devices = [x for x in chromeos_listing if x["manufacturer"] == dataset[manufacturer_index]]

for device in vendor_devices:
    vendor_device_selection_data.add(device["name"])

vendor_device_selection_data = list(vendor_device_selection_data)

terminal_menu = TerminalMenu(vendor_device_selection_data, title="Choose a device\n")
device_index = terminal_menu.show()

vendor_device_channel = [x for x in vendor_devices if x["name"] == vendor_device_selection_data[device_index]]
for device_channel in vendor_device_channel:
    vendor_device_channel_data.add(f"{device_channel['channel']} (ver: {device_channel['chrome_version']})")

terminal_menu = TerminalMenu(vendor_device_channel_data, title="Choose a channel\n")
release_channel_index = terminal_menu.show()

device = vendor_device_channel[release_channel_index]

print("Downloading file...")
download(device["url"], ".")