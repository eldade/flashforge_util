import socket_utils
import socket

def get_local_ip():
    try:
        # Create a dummy socket to connect to an external site
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Connect to a public DNS server (Google's in this case)
            s.connect(("8.8.8.8", 80))
            # Get the socket's own address
            ip = s.getsockname()[0]
            return ip
    except Exception as e:
        print(f"Error: {e}")
        return None

def discover_printer():
    local_ip = get_local_ip()
    # Convert the local IP address to its hexadecimal representation
    hex_ip = ''.join([f'{int(x):02x}' for x in local_ip.split('.')])

    # The message to send - Your IP in hex followed by '46500000'
    message = bytes.fromhex(hex_ip + '46500000')

    # Standard UDP broadcast address
    broadcast_ip = "255.255.255.255"
    broadcast_port = 19000

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Enable broadcasting mode
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Set a longer timeout for the socket
    # TODO: Might want to set a shorter timeout and retry sending the broadcast packet every once in a while, in case it is dropped
    sock.settimeout(10)

    try:
        # Send the message
        sock.sendto(message, (broadcast_ip, broadcast_port))
        print("Sent discovery packet, waiting for response...")

        # Listen for a response
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                if data:
                    # Decode the printer name and clean up the string
                    # TODO: Add support for discovering multiple printers, this will just return the first one found
                    printer_name = data.decode('utf-8', errors='ignore')
                    printer_name = printer_name.split('\x00', 1)[0]
                    # Return the printer name and IP address
                    return printer_name, addr[0]
            except socket.timeout:
                print("No response received.")
                return None, None
    finally:
        sock.close()

