from ip_calculator import run_cli
from network_scan import main as network_scan_main

def calculator():
    run_cli()

def port_scan():
    network_scan_main()

def ping_ips():
    print("Ping various IPs")


banner = r"""
    ╔══════════════════════════════════╗
    ║           WELCOME!!!             ║
    ║     SIMPLE   UTILITY   MENU      ║ 
    ║        FOR INFRASTRUCTURE        ║ 
    ╚══════════════════════════════════╝ 
""" 
instructions = """
    1. Subnet calculator: Calculate subnet information based on IP and CIDR.
    2. Scan port: Check if common ports are open on a target IP.
    3. Ping range of IPs: Ping a range of IP addresses to check their availability.
    0. Exit: Exit the program.
    Use '?' to display this menu again.
"""

def main_menu():
    print(banner)
    print(instructions)

    while True:
        choice = input("Enter your choice (0-3): ")

        if choice == "1":
            calculator()
        elif choice == "2":
            port_scan()
        elif choice == "3":
            ping_ips()
        elif choice == "?":
            print(instructions)
        elif choice == "0":
            print("Good Bye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main_menu()
            