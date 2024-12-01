import socket
import time

HOST = "0.0.0.0"
PORT = 12345
OUTPUT_FILE = "received_large_file.bin"

BUFFER_SIZE = 1024 * 1024  # 1MB chunks

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    
    start_time = time.time()  # Start timing

    with open(OUTPUT_FILE, "wb") as f:
        while chunk := conn.recv(BUFFER_SIZE):
            f.write(chunk)
            print(f"Received {len(chunk)} bytes...")

    end_time = time.time()  # End timing

    print(f"File transfer completed in {end_time - start_time:.2f} seconds.")
