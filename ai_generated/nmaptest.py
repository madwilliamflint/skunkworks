import subprocess
import re
import json
from datetime import datetime
import os

# File to save MAC addresses and manufacturers
mac_list_file = "mac_list.json"

def log(message):
    print(message)  # Placeholder for future logging functionality

def generate_human_readable(dt=None):
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def parse_human_readable(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

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

# Function to scan the network using Nmap
def scan_network(network="10.131.37.0/24"):
    log(f"Scanning network: {network}")
    devices = []
    result = subprocess.run(['nmap', '-A', network], capture_output=True, text=True)
    lines = result.stdout.splitlines()

    ip_mac_pairs = {}
    current_ip = None
    current_mac = None

    for line in lines:
        if "Nmap scan report for" in line:
            current_ip = re.search(r'for (.+)', line)
            if current_ip:
                current_ip = current_ip.group(1)
                ip_mac_pairs[current_ip] = {"MAC": None, "Manufacturer": None, "Latency": None, "OS": None, "Ports": [], "FirstSeen": generate_human_readable(), "MostRecentlySeen": generate_human_readable()}
        elif "MAC Address" in line:
            current_mac_match = re.search(r'([0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}) \((.+)\)', line)
            if current_mac_match and current_ip:
                current_mac = current_mac_match.group(1)
                manufacturer = current_mac_match.group(3).strip() if current_mac_match.group(3) else "Unknown"
                ip_mac_pairs[current_ip]["MAC"] = current_mac
                ip_mac_pairs[current_ip]["Manufacturer"] = manufacturer
        elif "Host is up" in line:
            latency = re.search(r'\(([^)]+)\)', line)
            if latency and current_ip:
                latency_value = latency.group(1).strip()
                if "latency" in latency_value:
                    latency_value = latency_value.replace("latency", "").strip()
                ip_mac_pairs[current_ip]["Latency"] = latency_value
        elif "OS details" in line:
            os_match = re.search(r'OS details: (.+)', line)
            if os_match and current_ip:
                os_details = os_match.group(1).strip()
                ip_mac_pairs[current_ip]["OS"] = os_details
        elif re.match(r'\d+/tcp', line):
            if current_ip:
                ip_mac_pairs[current_ip]["Ports"].append(line.strip())
    
    return ip_mac_pairs

# Main function to load, scan, and save data
def main():
    mac_list = load_mac_list()
    devices = scan_network()

    current_time = generate_human_readable()

    for ip, info in devices.items():
        mac = info["MAC"]
        if mac not in mac_list:
            vendor = get_mac_vendor_macvendors(mac)
            if vendor == "Unknown":
                vendor = get_mac_vendor_maclookup(mac)
            info["Manufacturer"] = vendor
            info["FirstSeen"] = current_time
            info["MostRecentlySeen"] = current_time
            mac_list[mac] = info
        else:
            mac_list[mac]["MostRecentlySeen"] = current_time

    save_mac_list(mac_list)

    # Print the results
    print(f"{'IP Address':<15} {'MAC Address':<17} {'Host Name':<40} {'Manufacturer':<25} {'Latency':<10} {'OS':<20} {'Ports':<20} {'First Seen':<20} {'Most Recently Seen'}")
    print("-" * 150)
    for mac, info in mac_list.items():
        print(f"{info.get('IP', 'Unknown'):<15} {mac:<17} {info.get('HostName', 'Unknown')[:40]:<40} {info.get('Manufacturer', 'Unknown'):<25} {info.get('Latency', 'Unknown'):<10} {info.get('OS', 'Unknown'):<20} {', '.join(info.get('Ports', [])):<20} {info.get('FirstSeen', 'Unknown'):<20} {info.get('MostRecentlySeen', 'Unknown')}")
        
if __name__ == "__main__":
    main()
