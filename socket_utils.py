import socket

BUFFER_SIZE = 65536
TIMEOUT_SECONDS = 10

def send_bytes(printer_adress, message_data):
    """Sends and receives data"""

    printer_socket = socket.socket()
    printer_socket.settimeout(TIMEOUT_SECONDS)
    printer_socket.connect((printer_adress['ip'], printer_adress['port']))

    return printer_socket.send(message_data.encode())

def send_and_receive(printer_adress, message_data):
    """Sends and receives data"""

    printer_socket = socket.socket()
    printer_socket.settimeout(TIMEOUT_SECONDS)
    printer_socket.connect((printer_adress['ip'], printer_adress['port']))

    sent = printer_socket.sendall(message_data)

    data = printer_socket.recv(BUFFER_SIZE)
    printer_socket.close()

    return data

def send_data_with_progress(sock, data):
    # Size of each chunk to send
    chunk_size = 1024  # 1 KB chunks, adjust as needed

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
        print(f"Progress: {progress:.2f}%")

    print("Data transfer complete.")