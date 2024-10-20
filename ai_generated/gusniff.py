import os
import re
import socket
from scapy.all import ARP, Ether, srp
import ipaddress
import json
import requests
import subprocess
from datetime import datetime

class NetworkScanner:
    def __init__(self, mac_list_file="mac_list.json"):
        self.mac_list_file = mac_list_file
        self.mac_list = self.load_mac_list()
        
    def generate_human_readable(self,dt=None):
        # Use current time if no datetime object is given
        if dt is None:
            dt = datetime.now()
            # Convert datetime object to human-readable string format
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def parse_human_readable(self,date_str):
        # Convert human-readable string format to datetime object
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")        

    def log(self, message):
        print(message)  # Placeholder for future logging functionality

    def get_mac_vendor_macvendors(self, mac_address):
        url = "https://api.macvendors.com/"
        response = requests.get(url + mac_address)
        if response.status_code == 200:
            return response.text
        else:
            return "Unknown"

    def get_mac_vendor_maclookup(self, mac_address):
        url = "https://api.maclookup.app/v2/lookup"
        payload = {"mac": mac_address}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('vendor', 'Unknown')
        else:
            return "Unknown"

    def load_mac_list(self):
        if os.path.exists(self.mac_list_file):
            with open(self.mac_list_file, "r") as file:
                data = json.load(file)
                # Set default value for PossibleRouter
                for mac, info in data.items():
                    if 'PossibleRouter' not in info:
                        info['PossibleRouter'] = 'No'
                return data
        else:
            return {}

    def save_mac_list(self):
        with open(self.mac_list_file, "w") as file:
            json.dump(self.mac_list, file, indent=4)

    def get_network_info(self):
        output = os.popen('ipconfig').read()
        ip_pattern = re.compile(r'IPv4 Address.*: ([\d.]+)')
        subnet_pattern = re.compile(r'Subnet Mask.*: ([\d.]+)')
        ip_address = ip_pattern.search(output).group(1)
        subnet_mask = subnet_pattern.search(output).group(1)
        return ip_address, subnet_mask

    def calculate_network_range(self, ip_address, subnet_mask):
        network = ipaddress.IPv4Network(f'{ip_address}/{subnet_mask}', strict=False)
        return str(network)

    def scan_network(self, network):
        self.log(f"Scanning network: {network}")
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

    def get_subnet_mask(self, ip_address):
        try:
            return str(ipaddress.IPv4Network(ip_address, strict=False).netmask)
        except ValueError:
            return None

    def detect_secondary_routers(self, devices):
        subnet_masks = {}
        for ip, mac in devices:
            subnet_mask = self.get_subnet_mask(ip)
            if subnet_mask:
                if subnet_mask not in subnet_masks:
                    subnet_masks[subnet_mask] = []
                subnet_masks[subnet_mask].append((ip, mac))
        routers = []
        for subnet_mask, devices in subnet_masks.items():
            if len(devices) > 1:
                routers.extend(devices)
        return routers

    def update_mac_list(self, devices, secondary_routers):
        for ip, mac in devices:
            if mac not in self.mac_list:
                vendor = self.get_mac_vendor_macvendors(mac)
                if vendor == "Unknown":
                    vendor = self.get_mac_vendor_maclookup(mac)
                is_router = 'Yes' if (ip, mac) in secondary_routers else 'No'
                hostname = socket.gethostbyaddr(ip)[0] if 'Unknown' else 'Unknown'
                self.mac_list[mac] = {
                    "IP": ip,
                    "HostName": hostname,
                    "Vendor": vendor,
                    "PossibleRouter": is_router
                }
        self.save_mac_list()


    def print_table(self, data, fields=None):
            # Determine the fields to output
        if fields is None:
            fields = list(data[0].keys())
        else:
            if all(isinstance(field, int) for field in fields):
                # Convert ordinal positions to field names
                fields = [list(data[0].keys())[i] for i in fields]
    
        # Calculate the width of each column
        column_widths = {field: max(len(field), max(len(str(row[field])) for row in data)) for field in fields}

        # Print the header
        header = " | ".join(f"{field:{column_widths[field]}}" for field in fields)
        print(header)
        print("-" * len(header))

        # Print each row
        for row in data:
            print(" | ".join(f"{str(row[field]):{column_widths[field]}}" for field in fields))
        
    def _print_table(self,data, fields=None):
        # Determine the fields to output
        if fields is None:
            #print(data)
            fields = list(data[0].keys())

        # Calculate the width of each column
        column_widths = {field: max(len(field), max(len(str(row[field])) for row in data)) for field in fields}
        
        # Print the header
        header = " | ".join(f"{field:{column_widths[field]}}" for field in fields)
        print(header)
        print("-" * len(header))

        # Print each row
        for row in data:
            print(" | ".join(f"{str(row[field]):{column_widths[field]}}" for field in fields))



    def print_table(self,data, fields=None, placeholder="N/A"):
        # Get all possible fields
        all_fields = set()
        for record in data:
            all_fields.update(record.keys())
    
        all_fields = list(all_fields)

        # Determine the fields to output
        if fields is None:
            fields = all_fields
        else:
            if all(isinstance(field, int) for field in fields):
                # Convert ordinal positions to field names
                fields = [all_fields[i] for i in fields]

        # Calculate the width of each column
        column_widths = {field: max(len(field), max(len(str(row.get(field, placeholder))) for row in data)) for field in fields}

        # Print the header
        header = " | ".join(f"{field:{column_widths[field]}}" for field in fields)
        print(header)
        print("-" * len(header))

        # Print each row
        for row in data:
            print(" | ".join(f"{str(row.get(field, placeholder)):{column_widths[field]}}" for field in fields))

    def print_results(self):
        print(json.dumps(self.mac_list,sort_keys=True,indent=4))
#        self.print_table(list(self.mac_list.values()))

    def run(self):
        ip_address, subnet_mask = self.get_network_info()
        network_range = self.calculate_network_range(ip_address, subnet_mask)
        # Scan the network
        devices = self.scan_network(network_range)
        for device in devices:
            print(device)
        
        
    def old_run(self):
        # Get network information
        ip_address, subnet_mask = self.get_network_info()
        network_range = self.calculate_network_range(ip_address, subnet_mask)

        # Scan the network
        devices = self.scan_network(network_range)

        # Detect secondary routers
        # secondary_routers = self.detect_secondary_routers(devices)

        # Update MAC list with new devices
        for ip, mac in devices:
            print("Processing mac [{0}]".format(mac))
            if mac not in self.mac_list:
                vendor = self.get_mac_vendor_macvendors(mac)
                if vendor == "Unknown":
                    vendor = self.get_mac_vendor_maclookup(mac)
                    
                is_router = "No"
                # is_router = 'Yes' if (ip, mac) in secondary_routers else 'No'

                
                hostname = 'Unknown'
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except socket.herror as e:
                    print("Error looking up hostname for [{0}]. : {1}".format(ip,str(e)))

                print("Adding data for mac [{0}]".format(mac))
                self.mac_list[mac] = {
                    "MAC": mac,
                    "IP": ip,
                    "HostName": hostname,
                    "Vendor": vendor,
                    "PossibleRouter": is_router,
                    "SeenFirst": self.generate_human_readable()
                }

            self.mac_list[mac]["SeenMostRecent"] = self.generate_human_readable()

        # Save updated MAC list
        #        self.save_mac_list(self.mac_list)
        self.save_mac_list()

        # Print the results
        self.print_results()


if __name__ == '__main__':
    app = NetworkScanner()
    # For display testing, I don't need to scan the network every damned iteration.
    app.run()
    #app.print_results()
    
