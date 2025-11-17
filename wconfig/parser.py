import os
import subprocess
import re
import locale



def network_parse():
    operation_system = os.name
    interfaces = []
     
    if os.name == 'posix':
        output = subprocess.check_output('ifconfig', text=True)
        interfaces_raw = re.split(r'\n(?=\S)', output.strip())

        for block in interfaces_raw:
            iface = {}
    
            # Name
            name = re.match(r'^(\S+)', block)
            iface['name'] = name.group(1) if name else None
    
            # Status
            iface['status'] = 'UP' if 'UP' in block and 'RUNNING' in block else 'DOWN'
    
            # MTU
            mtu = re.search(r'mtu\s+(\d+)', block)
            iface['mtu'] = mtu.group(1) if mtu else None
    
            # IPv4
            ipv4 = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', block)
            iface['ipv4'] = ipv4.group(1) if ipv4 else None
    
            # IPv6
            ipv6 = re.search(r'inet6 ([0-9a-zA-Z:]+)', block)
            iface['ipv6'] = ipv6.group(1) if ipv6 else None
    
            # MAC
            MAC = re.search(r'ether ([0-9A-Za-z:]+)', block)
            iface['MAC'] = MAC.group(1) if MAC else None

            # Mask
            mask = re.search(r'netmask (\d+\.\d+\.\d+\.\d+)', block)
            iface['mask'] = mask.group(1) if mask else None
        
            # Packets
            iface['packets'] = {}
        
            rx_packets = re.search(r'RX packets\s+(\d+)\s+bytes\s+(\d+)', block)
            if rx_packets:
                iface['packets']['received'] = {
                'count': int(rx_packets.group(1)),
                'bytes': rx_packets.group(2)
            }
        
            tx_packets = re.search(r'TX packets\s+(\d+)\s+bytes\s+(\d+)', block)
            if tx_packets:
                iface['packets']['send'] = {
                    'count': int(tx_packets.group(1)),
                    'bytes': tx_packets.group(2)
            }
        
            interfaces.append(iface)
        return interfaces
    else:
        encoding = locale.getpreferredencoding()
        output = subprocess.check_output('ipconfig', text=True, encoding=encoding, errors='replace')
        interfaces_raw = re.split(r'(?m)(?=^.*(?:Адаптер|Adapter))', output, flags=re.IGNORECASE)
        interfaces = []

        for block in interfaces_raw:
            iface = {}

            # Name
            name = re.search(r'^\s*(?:Адаптер|Adapter)\s*(.*?):\s*$', block, re.MULTILINE)
            iface['name'] = name.group(1) if name else None

            # Status
            status = re.search(r'(?:Состояние среды|Media State)', block, re.IGNORECASE)
            if not status: 
                iface['status'] = 'UP'
            else:
                iface['status'] = 'DOWN'
                iface['ipv4'] = None
                iface['ipv6'] = None
                iface['mask'] = None
            
                interfaces.append(iface)
                continue

            # IPv4
            ipv4 = re.search(r'IPv4.*?:\s*(\d+\.\d+\.\d+\.\d+)', block)
            iface['ipv4'] = ipv4.group(1) if ipv4 else None

            # IPv6
            ipv6 = re.search(r'IPv6.*?:\s*([0-9A-Za-z:]+)', block)
            iface['ipv6'] = ipv6.group(1) if ipv6 else None

            # Mask
            mask = re.search(r'(?:Маска подсети|Subnet Mask|mask).*?:\s*(\d+\.\d+\.\d+\.\d+)', block, re.IGNORECASE)
            iface['mask'] = mask.group(1) if mask else None

            
            interfaces.append(iface)
        return interfaces
