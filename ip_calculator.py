#!/usr/bin/env python3
"""
Subnet Calculator - Using Python's built-in `ipaddress` standard library.
"""

import ipaddress
import sys


# ─────────────────────────────────────────────
#  Core calculation
# ─────────────────────────────────────────────

def calculate_subnet(cidr: str) -> dict:
    interface = ipaddress.ip_interface(cidr)
    network   = interface.network

    hosts = list(network.hosts())
    num_hosts = network.num_addresses

    if network.prefixlen == 32:
        first_host = last_host = str(network.network_address)
        usable = 1
    elif network.prefixlen == 31:
        first_host = str(network.network_address)
        last_host  = str(network.broadcast_address)
        usable = 2
    else:
        first_host = str(hosts[0])  if hosts else "N/A"
        last_host  = str(hosts[-1]) if hosts else "N/A"
        usable = len(hosts)

    addr = interface.ip

    def to_binary_dotted(ip_obj) -> str:
        packed = ip_obj.packed  # bytes
        return ".".join(f"{b:08b}" for b in packed)

    flags = []
    if addr.is_private:    flags.append("Private")
    if addr.is_loopback:   flags.append("Loopback")
    if addr.is_link_local: flags.append("Link-Local")
    if addr.is_multicast:  flags.append("Multicast")
    if addr.is_reserved:   flags.append("Reserved")
    if not flags:          flags.append("Public")

    return {
        "ip_address":       str(addr),
        "cidr_notation":    str(network),
        "subnet_mask":      str(network.netmask),
        "wildcard_mask":    str(network.hostmask),
        "network_address":  str(network.network_address),
        "broadcast":        str(network.broadcast_address),
        "first_host":       first_host,
        "last_host":        last_host,
        "total_hosts":      num_hosts,
        "usable_hosts":     usable,
        "prefix_length":    network.prefixlen,
        "address_type":     ", ".join(flags),
        "ip_version":       addr.version,
        # Binary
        "ip_binary":        to_binary_dotted(addr),
        "mask_binary":      to_binary_dotted(network.netmask),
        "network_binary":   to_binary_dotted(network.network_address),
    }


# ─────────────────────────────────────────────
#  Subnet splitting
# ─────────────────────────────────────────────

def split_subnet(cidr: str, new_prefix: int) -> list:
    network = ipaddress.ip_network(cidr, strict=False)
    return [str(s) for s in network.subnets(new_prefix=new_prefix)]


# ─────────────────────────────────────────────
#  Supernet summarisation
# ─────────────────────────────────────────────

def summarize_networks(cidrs: list) -> str:
    networks = [ipaddress.ip_network(c, strict=False) for c in cidrs]
    summary  = list(ipaddress.collapse_addresses(networks))
    return ", ".join(str(s) for s in summary)


# ─────────────────────────────────────────────
#  Pretty printer
# ─────────────────────────────────────────────

def print_result(r: dict):
    W = 34

    def row(label, value):
        print(f"  {label:<{W}} {value}")

    print(f"\n{'═'*60}")
    print(f"  SUBNET CALCULATION RESULTS  (IPv{r['ip_version']})")
    print(f"{'═'*60}")

    print(f"\n  ── Address Info {'─'*43}")
    row("IP Address:",        r["ip_address"])
    row("Network Address:",   r["network_address"])
    row("Broadcast Address:", r["broadcast"])
    row("Subnet Mask:",       r["subnet_mask"])
    row("Wildcard Mask:",     r["wildcard_mask"])
    row("CIDR Notation:",     r["cidr_notation"])

    print(f"\n  ── Host Range {'─'*45}")
    row("First Usable Host:", r["first_host"])
    row("Last Usable Host:",  r["last_host"])
    row("Total Addresses:",   f"{r['total_hosts']:,}")
    row("Usable Hosts:",      f"{r['usable_hosts']:,}")

    print(f"\n  ── Classification {'─'*40}")
    row("Address Type:", r["address_type"])

    print(f"\n  ── Binary Representation {'─'*33}")
    row("IP (binary):",      r["ip_binary"])
    row("Mask (binary):",    r["mask_binary"])
    row("Network (binary):", r["network_binary"])

    print(f"\n{'═'*60}\n")


# ─────────────────────────────────────────────
#  Interactive CLI
# ─────────────────────────────────────────────

BANNER = r"""
  ╔══════════════════════════════════════════════╗
  ║        S U B N E T   C A L C U L A T O R     ║
  ╚══════════════════════════════════════════════╝
"""

MENU = """  Commands:
    calc  <IP/prefix>              – Calculate subnet info
    split <IP/prefix> <new_prefix> – Split network into subnets
    super <IP/p1> <IP/p2> ...      – Summarise / find supernet
    help                           – Show this menu
    quit                           – Exit
"""


def run_cli():
    print(BANNER)
    print(MENU)
    while True:
        try:
            raw = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Bye!")
            break

        if not raw:
            continue

        parts = raw.split()
        cmd   = parts[0].lower()

        if cmd in ("quit", "exit", "q"):
            print("  Bye!")
            break

        elif cmd == "help":
            print(MENU)

        elif cmd == "calc":
            if len(parts) < 2:
                print("  Usage: calc <IP/prefix>  e.g. calc 192.168.1.0/24")
                continue
            try:
                print_result(calculate_subnet(parts[1]))
            except Exception as e:
                print(f"  Error: {e}")

        elif cmd == "split":
            if len(parts) < 3:
                print("  Usage: split <IP/prefix> <new_prefix>  e.g. split 10.0.0.0/16 18")
                continue
            try:
                subnets = split_subnet(parts[1], int(parts[2]))
                print(f"\n  Splitting {parts[1]} → /{parts[2]}  ({len(subnets)} subnets):\n")
                for i, s in enumerate(subnets):
                    r = calculate_subnet(s)
                    print(f"    [{i+1:>4}]  {s:<22}  {r['first_host']} – {r['last_host']}  ({r['usable_hosts']:,} usable)")
                    if len(subnets) > 64 and i == 63:
                        print(f"    ... and {len(subnets) - 64} more (truncated)")
                        break
                print()
            except Exception as e:
                print(f"  Error: {e}")

        elif cmd == "super":
            if len(parts) < 3:
                print("  Usage: super <IP/p> <IP/p> ...  e.g. super 10.1.0.0/24 10.1.1.0/24")
                continue
            try:
                result = summarize_networks(parts[1:])
                print(f"\n  Summary: {result}\n")
                # Show details of each summarised block
                for block in result.split(", "):
                    print_result(calculate_subnet(block))
            except Exception as e:
                print(f"  Error: {e}")

        else:
            if "/" in cmd:
                try:
                    print_result(calculate_subnet(cmd))
                    continue
                except Exception:
                    pass
            print(f"  Unknown command: '{cmd}'. Type 'help' for usage.")


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            print_result(calculate_subnet(sys.argv[1]))
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        run_cli()