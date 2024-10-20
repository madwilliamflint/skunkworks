import os
import re
import subprocess
import ipaddress

# Function to scan the network using Nmap
def scan_network():
    devices = []
    result = subprocess.run(['nmap', '-sn', '192.168.1.0/24'], capture_output=True, text=True)
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

# Function to detect secondary router
def detect_secondary_router(devices):
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

# Main function
def main():
    devices = scan_network()
    routers = detect_secondary_router(devices)
    if routers:
        print("Potential secondary routers detected:")
        for ip, mac in routers:
            print(f"IP: {ip}, MAC: {mac}")
    else:
        print("No secondary routers detected.")

if __name__ == "__main__":
    main()
