import os
import re
import socket
from scapy.all import ARP, Ether, srp
import ipaddress
import json
import requests

# File to save MAC addresses and manufacturers
mac_list_file = "mac_list.json"

# Function to get MAC vendor information from MACVendors.com
def get_mac_vendor_macvendors(mac_address):
    url = "https://api.macvendors.com/"
    response = requests.get(url + mac_address)
    if response.status_code == 200:
        return response.text
    else:
        return "Unknown"

# Function to get MAC vendor information from MACLookup.app
def get_mac_vendor_maclookup(mac_address):
    url = "https://api.maclookup.app/v2/lookup"
    payload = {"mac": mac_address}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('vendor', 'Unknown')
    else:
        return "Unknown"

# Function to load saved MAC addresses with manufacturers
def load_mac_list():
    if os.path.exists(mac_list_file):
        with open(mac_list_file, "r") as file:
            return json.load(file)
    else:
        return {}

# Function to save MAC addresses with manufacturers
def save_mac_list(mac_list):
    with open(mac_list_file, "w") as file:
        json.dump(mac_list, file, indent=4)

# Function to get network information
def get_network_info():
    output = os.popen('ipconfig').read()
    ip_pattern = re.compile(r'IPv4 Address.*: ([\d.]+)')
    subnet_pattern = re.compile(r'Subnet Mask.*: ([\d.]+)')
    ip_address = ip_pattern.search(output).group(1)
    subnet_mask = subnet_pattern.search(output).group(1)
    return ip_address, subnet_mask

# Function to calculate network range
def calculate_network_range(ip_address, subnet_mask):
    network = ipaddress.IPv4Network(f'{ip_address}/{subnet_mask}', strict=False)
    return str(network)

# Function to scan network
def scan_network(network):
    print(f"Scanning network: {network}")
    arp = ARP(pdst=network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=2, verbose=False)[0]
    devices = []

    for sent, received in result:
        ip = received.psrc
        mac = received.hwsrc
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            hostname = None
        devices.append({"IP": ip, "MAC": mac, "HostName": hostname})

    return devices

# Load existing MAC list
mac_list = load_mac_list()

# Get network information
ip_address, subnet_mask = get_network_info()
network_range = calculate_network_range(ip_address, subnet_mask)

# Scan the network
devices = scan_network(network_range)

# Update MAC list with new devices
for device in devices:
    mac = device["MAC"]
    if mac not in mac_list:
        vendor = get_mac_vendor_macvendors(mac)
        if vendor == "Unknown":
            vendor = get_mac_vendor_maclookup(mac)
        mac_list[mac] = {
            "IP": device["IP"],
            "HostName": device["HostName"],
            "Vendor": vendor
        }

# Save updated MAC list
save_mac_list(mac_list)

# Print the results
print(f"{'IP Address':<15} {'MAC Address':<17} {'Host Name':<40} {'Manufacturer'}")
print("-" * 95)
for mac, info in mac_list.items():
    print(f"{info['IP']:<15} {mac:<17} {info.get('HostName', 'Unknown')[:40]:<40} {info['Vendor']}")
