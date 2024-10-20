import os
import re
import socket
from scapy.all import ARP, Ether, srp
import ipaddress
import json
import requests
import subprocess

# File to save MAC addresses and manufacturers
mac_list_file = "mac_list.json"

def log(message):
    print(message)  # Placeholder for future logging functionality

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

# Function to scan the network using Nmap
def scan_network(network):
    log(f"Scanning network: {network}")
    devices = []
    result = subprocess.run(['nmap', '-sn', network], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    current_ip = None
    current_mac = None
    for line in lines:
        if "Nmap scan report for" in line:
            current_ip = re.search(r'for ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', line)
            if current_ip:
                current_ip = current_ip.group(1)
        elif "MAC Address" in line:
            current_mac = re.search(r'([0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5})', line)
            if current_mac:
                current_mac = current_mac.group(0)
        if current_ip and current_mac:
            devices.append((current_ip, current_mac))
            current_ip = None
            current_mac = None
    return devices

# Function to get subnet mask of a device
def get_subnet_mask(ip_address):
    try:
        return str(ipaddress.IPv4Network(ip_address, strict=False).netmask)
    except ValueError:
        return None

# Function to detect secondary routers
def detect_secondary_routers(devices):
    subnet_masks = {}
    for ip, mac in devices:
        subnet_mask = get_subnet_mask(ip)
        if subnet_mask:
            if subnet_mask not in subnet_masks:
                subnet_masks[subnet_mask] = []
            subnet_masks[subnet_mask].append((ip, mac))
    routers = []
    for subnet_mask, devices in subnet_masks.items():
        if len(devices) > 1:
            routers.extend(devices)
    return routers

# Load existing MAC list
mac_list = load_mac_list()

# Get network information
ip_address, subnet_mask = get_network_info()
network_range = calculate_network_range(ip_address, subnet_mask)

# Scan the network
devices = scan_network(network_range)

# Detect secondary routers
secondary_routers = detect_secondary_routers(devices)

# Update MAC list with new devices
for ip, mac in devices:
    if mac not in mac_list:
        vendor = get_mac_vendor_macvendors(mac)
        if vendor == "Unknown":
            vendor = get_mac_vendor_maclookup(mac)
        is_router = 'Yes' if (ip, mac) in secondary_routers else 'No'
        hostname = socket.gethostbyaddr(ip)[0] if 'Unknown' else 'Unknown'
        mac_list[mac] = {
            "IP": ip,
            "HostName": hostname,
            "Vendor": vendor,
            "PossibleRouter": is_router
        }

# Save updated MAC list
save_mac_list(mac_list)

# Print the results
print(f"{'IP Address':<15} {'MAC Address':<17} {'Host Name':<40} {'Manufacturer':<25} {'Possible Router'}")
print("-" * 120)
for mac, info in mac_list.items():
    print(f"{info['IP']:<15} {mac:<17} {info.get('HostName', 'Unknown')[:40]:<40} {info['Vendor']:<25} {info['PossibleRouter']}")
