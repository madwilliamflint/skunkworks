import subprocess
import re

def working_scan_network(network="10.131.37.0/24"):
    print(f"Scanning network: {network}")
    devices = []
    result = subprocess.run(['nmap', '-sn', network], capture_output=True, text=True)
    lines = result.stdout.splitlines()

    ip_mac_pairs = {}
    current_ip = None

    for line in lines:
        print(line)  # Log every line of the Nmap output
        if "Nmap scan report for" in line:
            current_ip = re.search(r'for (.+)', line)
            if current_ip:
                current_ip = current_ip.group(1)
                ip_mac_pairs[current_ip] = {"MAC": None, "Manufacturer": None, "Latency": None}
                print(f"Found IP: {current_ip}")
        elif "MAC Address" in line:
            current_mac_match = re.search(r'([0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}) \((.+)\)', line)
            if current_mac_match and current_ip:
                current_mac = current_mac_match.group(1)
                manufacturer = current_mac_match.group(3).strip() if current_mac_match.group(3) else "Unknown"
                ip_mac_pairs[current_ip]["MAC"] = current_mac
                ip_mac_pairs[current_ip]["Manufacturer"] = manufacturer
                print(f"Found MAC: {current_mac}, Manufacturer: {manufacturer}")
        elif "Host is up" in line:
            latency = re.search(r'\(([^)]+)\)', line)
            if latency and current_ip:
                latency_value = latency.group(1).strip()
                if "latency" in latency_value:
                    latency_value = latency_value.replace("latency", "").strip()
                ip_mac_pairs[current_ip]["Latency"] = latency_value
                print(f"Latency: {latency_value}")

    # Print all devices found
    for ip, info in ip_mac_pairs.items():
        print(f"IP: {ip}, MAC: {info['MAC']}, Manufacturer: {info['Manufacturer']}, Latency: {info['Latency']}")
    
    return ip_mac_pairs

# Example usage
devices = scan_network()
for ip, info in devices.items():
    print(f"IP: {ip}, MAC: {info['MAC']}, Manufacturer: {info['Manufacturer']}, Latency: {info['Latency']}")
