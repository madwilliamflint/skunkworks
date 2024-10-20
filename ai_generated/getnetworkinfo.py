import os
import re
import socket
from scapy.all import ARP, Ether, srp
import ipaddress

def get_network_info():
    # Get the output from ipconfig
    output = os.popen('ipconfig').read()

    # Extract the IP address and subnet mask using regex
    ip_pattern = re.compile(r'IPv4 Address.*: ([\d.]+)')
    subnet_pattern = re.compile(r'Subnet Mask.*: ([\d.]+)')
    ip_address = ip_pattern.search(output).group(1)
    subnet_mask = subnet_pattern.search(output).group(1)
    return ip_address, subnet_mask

def calculate_network_range(ip_address, subnet_mask):
    # Convert IP address and subnet mask to IPv4Network
    network = ipaddress.IPv4Network(f'{ip_address}/{subnet_mask}', strict=False)
    return str(network)

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

# Get network information
ip_address, subnet_mask = get_network_info()
network_range = calculate_network_range(ip_address, subnet_mask)

# Scan the network
devices = scan_network(network_range)

# Print the results
if not devices:
    print("No devices found. Check the network range or permissions.")
else:
    print("IP Address\tMAC Address\tHost Name")
    print("----------------------------------------")
    for device in devices:
        print(f"{device['IP']}\t{device['MAC']}\t{device.get('HostName', 'Unknown')}")
