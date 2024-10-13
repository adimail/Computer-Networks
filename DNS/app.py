#             .___.__               .__.__   
# _____     __| _/|__| _____ _____  |__|  |  
# \__  \   / __ | |  |/     \\__  \ |  |  |  
#  / __ \_/ /_/ | |  |  Y Y  \/ __ \|  |  |__
# (____  /\____ | |__|__|_|  (____  /__|____/
#      \/      \/          \/     \/         
# 
#     Author: Aditya Godse (https://adimail.github.io)
#     Description: python program to perform DNS lookup
# 
# program breakdown
# - domains List: Contains the domain names to be resolved to IP addresses.
# - ip_addresses List: Contains the IP addresses to be resolved back to domain names.
# - lookup_ips(domains): Iterates over the list of domains and prints the IP addresses using socket.gethostbyname().
# - lookup_domains(ip_addresses): Iterates over the list of IP addresses and prints the associated domain names using socket.gethostbyaddr().

import socket

domains = ['adimail.github.io', 'google.com', 'hosteze.in']
ip_addresses = ['185.199.109.153', '172.217.164.110', '18.67.195.39']

def lookup_ips(domains):
    print('Domain to IP address lookup:')
    for domain in domains:
        try:
            ip = socket.gethostbyname(domain)
            print(f'{domain} -> {ip}')
        except socket.gaierror:
            print(f'DNS resolution failed for {domain}')

def lookup_domains(ip_addresses):
    print('\nIP address to Domain lookup:')
    for ip in ip_addresses:
        try:
            domain = socket.gethostbyaddr(ip)[0]
            print(f'{ip} -> {domain}')
        except socket.herror:
            print(f'Reverse DNS lookup failed for {ip}')

if __name__ == '__main__':
    lookup_ips(domains)
    lookup_domains(ip_addresses)
