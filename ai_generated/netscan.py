from scapy.all import ARP, Ether, srp
import socket

def get_mac(ip):
    try:
        # Send an ARP request to get the MAC address
        ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, verbose=False)
        for _, rcv in ans:
            return rcv[Ether].src
    except Exception as e:
        print(f"Error getting MAC address for {ip}: {e}")
        return None

def scan_network(network):
    try:
        print(f"Scanning network: {network}")
        # Create an ARP request packet
        arp = ARP(pdst=network)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp

        # Send the packet and get the response
        result = srp(packet, timeout=2, verbose=False)[0]

        # Parse the response
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
    except Exception as e:
        print(f"Error scanning network: {e}")
        return []

# Change this to your network range
network = "192.168.1.0/24"
devices = scan_network(network)

if not devices:
    print("No devices found. Check the network range or permissions.")
else:
    print("IP Address\tMAC Address\tHost Name")
    print("----------------------------------------")
    for device in devices:
        print(f"{device['IP']}\t{device['MAC']}\t{device.get('HostName', 'Unknown')}")
