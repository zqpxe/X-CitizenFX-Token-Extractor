import pyshark
import threading
import asyncio
import re
import requests 
import os 
import json 

from colorama import Fore 

os.system("cls && title Fivem Token Extractor")

print(f"{Fore.RED}[!] Please Note this will extract your Fivem Tokens to the file tokens.json. Please enter your cfx token for the server{Fore.RESET}")

def is_string_valid(string):
    pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$'
    return re.match(pattern, string) is not None

def process_cfx(cfx):
    ip = is_string_valid(cfx)
    if not ip:
        if "cfx.re/join/" not in cfx:
            cfx = f"cfx.re/join/{cfx}"
        try:
            r = requests.get(f"https://{cfx}")
            if r.status_code != 200:
                print("Invalid input. Please check your CFX and try again.")
                return None
            response = r.headers.get('x-citizenfx-url', '')
            httpstrip = response.strip("https://")
            print(f"Resolved IP: {httpstrip}")
            return httpstrip
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    else:
        print(f"Input is a direct IP: {cfx}")
        return cfx

cfx_input = input("Enter the CFX (or IP): ").strip()
result = process_cfx(cfx_input)
if result:
    ip, port = result.split(':') 

fivem_servers = [
    {'ip': ip, 'port': port}, # tThe server
]

# Regex pattern to capture the X-CitizenFX-Token
token_regex = r"X-CitizenFX-Token:\s*([a-f0-9\-]{36})"

def remove_ansi_escape_codes(text):
    ansi_escape = re.compile(r'\x1b\[([0-9]{1,2})(;[0-9]{1,2})?m')
    return ansi_escape.sub('', text)  #

def clean_request_data(request_data):
    cleaned_data = remove_ansi_escape_codes(request_data) # Clean up unwanted shit 
    cleaned_data = re.sub(r'[\x00-\x1F\x7F]+', '', cleaned_data)
    cleaned_data = re.sub(r'\r\n|\n', '\n', cleaned_data).strip()
    return cleaned_data

def capture_fivem_traffic(interface, ip, port):
    asyncio.set_event_loop(asyncio.new_event_loop())  #
    print(f"Waiting for user to connect...")
    try:
        capture = pyshark.LiveCapture(
            interface=interface,
            display_filter=f'http and ip.addr == {ip} and tcp.port == {port}'
        )

        for packet in capture.sniff_continuously():
            try:

                if 'HTTP' in packet:
                    http_layer = packet['HTTP']

                    host = getattr(http_layer, 'host', None)
                    uri = getattr(http_layer, 'request_uri', None)
                    url = f"http://{host}{uri}" if host and uri else "Unknown URL"

                    request_data = str(http_layer)
                    cleaned_request_data = clean_request_data(request_data)  

                    token_match = re.search(token_regex, cleaned_request_data)
                    if token_match:
                        token = token_match.group(1)  
                        # print(f"Found Token: {token}")
                        os.system("cls")
                        print(f"{Fore.GREEN}[!]{Fore.RESET} Found 'X-CitizenFX-Token' -- Saved to tokens.json")
                        tokens = {"X-CitizenFX-Token": token}
                        with open("tokens.json", 'w') as f:
                            json.dump(tokens, f, indent=4) 
      
                        # Stop the capture once the token is found
                        capture.close()  # Stop sniffing
                        break  

            except Exception as e:
                print(f"Error processing packet: {e}")
    except Exception as e:
        print(f"Error setting up capture for {ip}:{port}: {e}")

def monitor_fivem_servers(servers, interface='eth0'):
    threads = []
    for server in servers:
        ip = server['ip']
        port = server['port']
        t = threading.Thread(target=capture_fivem_traffic, args=(interface, ip, port))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

internetProtocol = input(f"{Fore.RED}[?]{Fore.RESET} Please input your Internet Protocol (Eg. Ethernet, Wi-fi, Mullvad, CloudflareWARP) --> ")
monitor_fivem_servers(fivem_servers, interface=internetProtocol)
