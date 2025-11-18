from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box
from .parser import network_parse
import subprocess

console = Console(width=180)



def format_bytes(val):
    val = float(val)
    for unit in ['B','KB','MB','GB','TB']:
        if val < 1024:
            return f"{val} {unit}"
        val = round((val/1024),2)


def display_posix(interfaces):
    for iface in interfaces:
        name = str(iface.get("name") or "-")
        status = str(iface.get('status') or "-")
        mtu = str(iface.get('mtu') or '-')
        ipv4 = str(iface.get('ipv4') or "-")
        ipv6 = str(iface.get('ipv6') or "-")
        mask = str(iface.get('mask') or "-")
        mac = str(iface.get('MAC') or "-")
        rx_count = iface['packets']['received']['count']
        rx_bytes = iface['packets']['received']['bytes']
        tx_count = iface['packets']['send']['count']
        tx_bytes = iface['packets']['send']['bytes']

        values = [
            f"Status : {status}",
            f"MTU    : {mtu}",
            f"IPv4   : {ipv4}",
            f"IPv6   : {ipv6}",
            f"Mask   : {mask}",
            f"MAC    : {mac}",
            f"RX     : {rx_count} ({format_bytes(rx_bytes)})",
            f"TX     : {tx_count} ({format_bytes(tx_bytes)})"
        ]
        max_len = max(len(name)+ 8, max(len(v) for v in values))

        side_len = (max_len - len(name) - 2) // 2
        top_line = "╭" + "─"*side_len + f" {name} " + "─"*(max_len - len(name) - 2 - side_len) + "╮"
        console.print(f"[bold #66cccc]{top_line}[/bold #66cccc]")


        table = Table(box=None, show_header=False, expand=False)


        status_color = "bold green" if status.upper() == "UP" else "bold red"
        table.add_row(
            Text("Status : ", style=status_color) + Text(status, style=status_color)
        )

        mtu_text =  Text("MTU    : ", style="white") + Text(mtu, style= "bold #024961")
        table.add_row(mtu_text)

        ipv4_text = Text("IPv4   : ", style="white") + Text(ipv4, style= "bold #006688")
        table.add_row(ipv4_text)

  
        ipv6_text = Text("IPv6   : ", style="white") + Text(ipv6, style="bold #00aaff")
        table.add_row(ipv6_text)


        mask_text = Text("Mask   : ", style="white") + Text(mask, style="bold bright_cyan")
        table.add_row(mask_text)


        mac_text = Text("MAC    : ", style="white") + Text(mac, style="bold cyan")
        table.add_row(mac_text)

 
        rx_text = Text("RX     : ", style="white") + Text(f"{rx_count} ({format_bytes(rx_bytes)})", style="bold bright_blue")
        table.add_row(rx_text)


        tx_text = Text("TX     : ", style="white") + Text(f"{tx_count} ({format_bytes(tx_bytes)})", style="bold bright_blue")
        table.add_row(tx_text)

        console.print(table)


        bottom_line = "╰" + "─"*max_len + "╯"
        console.print(f"[bold #338888]{bottom_line}[/bold #338888]\n")

def display_win(interfaces):
    for iface in interfaces:
        name = str(iface.get('name') or '-')
        status = str(iface.get('status') or '-')
        ipv4 = str(iface.get('ipv4') or '-')
        ipv6 = str(iface.get('ipv6') or '-')
        mask = str(iface.get('mask') or '-')

        values = [
            f"Status : {status}",
            f"IPv4   : {ipv4}",
            f"IPv6   : {ipv6}",
            f"Mask   : {mask}"
        ]

        max_len = max(len(name)+ 8, max(len(v) for v in values))

        side_len = (max_len - len(name) - 2) // 2
        top_line = "╭" + "─"*side_len + f" {name} " + "─"*(max_len - len(name) - 2 - side_len) + "╮"
        console.print(f"[bold #66cccc]{top_line}[/bold #66cccc]")

        table = Table(box=None, show_header=False, expand=False)

        status_color = "bold green" if status.upper() == "UP" else "bold red"
        table.add_row(
            Text("Status : ", style=status_color) + Text(status, style=status_color)
        )


        ipv4_text = Text("IPv4   : ", style="white") + Text(ipv4, style= "bold #006688")
        table.add_row(ipv4_text)

  
        ipv6_text = Text("IPv6   : ", style="white") + Text(ipv6, style="bold #00aaff")
        table.add_row(ipv6_text)


        mask_text = Text("Mask   : ", style="white") + Text(mask, style="bold bright_cyan")
        table.add_row(mask_text)

        console.print(table)

        bottom_line = "╰" + "─"*max_len + "╯"
        console.print(f"[bold #338888]{bottom_line}[/bold #338888]\n")

def display(name: str):
    interfaces = network_parse()
    console.clear()

    if name == 'posix':
        display_posix(interfaces=interfaces)
    else:
        display_win(interfaces=interfaces)

    

