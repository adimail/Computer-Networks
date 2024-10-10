#             .___.__               .__.__   
# _____     __| _/|__| _____ _____  |__|  |  
# \__  \   / __ | |  |/     \\__  \ |  |  |  
#  / __ \_/ /_/ | |  |  Y Y  \/ __ \|  |  |__
# (____  /\____ | |__|__|_|  (____  /__|____/
#      \/      \/          \/     \/         
# 
#     Author: Aditya Godse (https://adimail.github.io)
#     Description: A program to demonstrate Sub-netting and find subnet masks
# 
# Following script uses the `ipaddress` python module to demonstrate subnetting
# we divide an IP address into smaller pieces called subnets
# It takes an IP address and splits it into provided subnet size (eg. /24 to /26)
# The program then prints useful information about each subnet, including:
#   - Network Address: The first address in the subnet (not usable by devices).
#   - Broadcast Address: The last address in the subnet (not usable by devices).
#   - Subnet Mask: This helps determine the size of each subnet.
#   - Usable IP Range: The range of IP addresses that devices can actually use.
#   - Total Hosts: The number of devices that can be connected to the subnet.

# FAQs
#  1. why 192.168.1.0?
#   192.168.1.0 is part of a private IP range that is widely used in home and small office networks
#  ----------
#  2. what is /24?
#   /24 in an IP address refers to the subnet mask or the network prefix, which defines how many bits are used to define the network portion
#   An IPv4 address consists of 32 bits, written in 4 sections of 8 bits (called octets), like this:
#   192.168.1.0
#   Each section (octet) is represented in decimal but can be translated into binary. For example:
#   192 is 11000000 in binary, 168 is 10101000 in binary etc
#   So, the IP address 192.168.1.0 in binary would look like: 11000000.10101000.00000001.00000000
#   The /24 notation is called CIDR notation (Classless Inter-Domain Routing), and it tells us how many bits from the left are used for the network portion of the IP address.
#   /24 means that the first 24 bits are reserved for the network, and the remaining 8 bits are used for the host portion (devices in that network).
#   The network mask for /24 is 255.255.255.0, which looks like this in binary:
#   11111111.11111111.11111111.00000000
#   Network portion: The first 24 bits (192.168.1) represent the network.
#   Host portion: The remaining 8 bits (the last octet) are available for hosts, i.e., devices on this network.
#  ----------
#  3. how to calculate usable IP range?
#   `subnet.network_address` gives us the network address and `subnet.broadcast_address` gives us the broadcast address
#   subness address and broadcast address are the first and last addresses in the network
#   so the avaliable hosts IPs are in range between them


import ipaddress

def subnetting(network, new_prefix):
    try:
        ip_network = ipaddress.ip_network(network, strict=False)
    except ValueError as e:
        print(f"Error: {e}")
        return

    subnets = list(ip_network.subnets(new_prefix=new_prefix))
    
    print(f"Original Network: {ip_network}")
    print(f"Subnetting into {len(subnets)} subnets (new prefix: /{new_prefix})\n")
    
    for i, subnet in enumerate(subnets):
        print(f"Subnet {i+1}:")
        print(f"  Network Address: {subnet.network_address}")
        print(f"  Broadcast Address: {subnet.broadcast_address}")
        print(f"  Subnet Mask: {subnet.netmask}")
        print(f"  Usable Host IP Range: {subnet.network_address + 1} - {subnet.broadcast_address - 1}")
        print(f"  Total Hosts: {subnet.num_addresses - 2}\n")

if __name__ == "__main__":
    # Example: Start with a /24 network and split it into subnets
    network = "192.168.1.0/24"
    
    # Define prefix length
    # 26 means we split the /24 network into /26 subnets
    new_prefix = 26
    
    subnetting(network, new_prefix)
