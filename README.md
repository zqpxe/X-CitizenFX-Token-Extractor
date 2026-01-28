# X-CitizenFX-Token-Extractor

Extract your `X-CitizenFX-Token` quickly and easily.

## Description

This script allows you to retrieve your FiveM `X-CitizenFX-Token` automatically. It saves the token to a file, without displaying it in the console.

## Installation

Install the required Python libraries:

```bash
pip install pyshark colorama
```

## Usage

Run the script with:

```bash
python ExtractFivemTokens.py
```

Follow these steps:

1. Find a FiveM server you can connect to.
2. Copy the server’s CFX code and paste it into the script when prompted.
3. Specify your Internet protocol:
   * **No VPN:** Use `Wi-Fi` or `Ethernet`.
   * **With VPN:** Hover over the network icon in your taskbar to see the VPN name (e.g., `CloudflareWARP`, `Mullvad`) and enter it.
4. Join the server. Your token will be automatically saved to a file.

## Disclaimer

* Your token is saved to a file and **will not** be printed in the console.
* Use responsibly. Do not share your token
  
## Why did I publish this
* 95% of the FiveM community probably have no need use this tool. I developed this a year ago while experimenting with how the client communicates with servers and stuff like that.

