import socket

def check_port(ip, ports):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1) # Timeout de 1 minuto

    result = sock.connect_ex((ip, ports))
    sock.close()

    if result == 0:
        return True
    else:
        return False
    
banner = r"""
    ╔══════════════════════════════════╗
    ║           WELCOME!!!             ║
    ║     SCAN NETWORK - DISCOVER,     ║
    ║        WHAT PORT IS OPENED.      ║
    ╚══════════════════════════════════╝
"""

information = """
    This utility allows you to scan a target IP for common open ports.
    Use isolate one or more IP to scan
    Option 1: Scan a single IP for common ports (22, 80, 443, 3389).
    Option 2: Scan a range of ports through the file.
    Use 'exit', 'quit', or 'q' to exit the program.
"""

def main():
    print(banner)
    print(information)

    while True:
        target_ip = input("Enter the option number (1 or 2) | (To leave, type 'exit', 'quit', or 'q') : ")

        if target_ip == "1":
            ip = input("Enter the target IP address: ")
            common_ports = [22, 80, 443, 3389]
            print(f"Scanning {ip} for common ports...")
            
            for port in common_ports:
                if check_port(ip, port):
                    print(f"[+] Port {port} is open")
                else:
                    print(f"[-] Port {port} is closed")

        elif target_ip == "2":
            file_path = input("Enter the path to the file containing IP addresses: ")
            try:
                with open(file_path, 'r') as file:
                    ips = file.read().splitlines()
                    for ip in ips:
                        print(f"Scanning {ip} for common ports...")
                        common_ports = [22, 80, 443, 3389]
                        for port in common_ports:
                            if check_port(ip, port):
                                print(f"[+] Port {port} is open on {ip}")
                            else:
                                print(f"[-] Port {port} is closed on {ip}")
            except FileNotFoundError:
                print("File not found. Please check the path and try again.")
        elif target_ip in ["exit", "quit", "q"]:
            print("Good Bye!")
            break
        else:
            print("Invalid option. Please enter 1 or 2. Use 'exit', 'quit', or 'q' to exit the program.")
    


if __name__ == "__main__":
    main()