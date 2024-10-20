import socket
import fcntl
import struct

def get_network():
    interface = 'eth0'  # Change this to your network interface
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_address = socket.inet_ntoa(fcntl.ioctl(sock.fileno(), 0x8915, struct.pack('256s', bytes(interface[:15], 'utf-8')))[20:24])
    netmask = socket.inet_ntoa(fcntl.ioctl(sock.fileno(), 0x891b, struct.pack('256s', bytes(interface[:15], 'utf-8')))[20:24])

    ip_bin = struct.unpack('>I', socket.inet_aton(ip_address))[0]
    netmask_bin = struct.unpack('>I', socket.inet_aton(netmask))[0]
    network_bin = ip_bin & netmask_bin
    network_address = socket.inet_ntoa(struct.pack('>I', network_bin))

    return f"{network_address}/{bin(netmask_bin).count('1')}"

print(get_network())
