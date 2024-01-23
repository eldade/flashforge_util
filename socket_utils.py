import socket

BUFFER_SIZE = 4096
TIMEOUT_SECONDS = 10

def send_bytes(socket, message_data):
    """Sends and receives data"""

    return socket.send(message_data.encode())

def connect(printer_address):
    printer_socket = socket.socket()
    printer_socket.settimeout(TIMEOUT_SECONDS)
    printer_socket.connect((printer_address['ip'], printer_address['port']))
    printer_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    return printer_socket
def send_and_receive(printer_socket, message_data):
    """Sends and receives data"""

    sent = printer_socket.sendall(message_data)

    data = printer_socket.recv(BUFFER_SIZE)

    return data

def send_data_with_progress(sock, data):
    # Size of each chunk to send
    chunk_size = BUFFER_SIZE  # 1 KB chunks, adjust as needed

    # Get the total size of the data for progress calculation
    total_size = len(data)
    bytes_sent = 0

    # Send the data in chunks
    while bytes_sent < total_size:
        # Determine the size of the next chunk
        end_index = min(bytes_sent + chunk_size, total_size)

        # Send the chunk
        sock.sendall(data[bytes_sent:end_index])
        bytes_sent = end_index

        # Calculate and print the progress
        progress = (bytes_sent / total_size) * 100
        print("\033[K", end='\r')  # Clear the line
        print(f"Progress: {progress:.2f}%", end='')

    print("\nData transfer complete.")