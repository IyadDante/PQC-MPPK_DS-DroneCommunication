import socket
import hashlib
import struct
import time
import psutil
from sign import sign_message  # Use existing MPPK signing implementation

# Constants
FILE_PATH = "large_file.bin"  # File to send
HOST = "10.0.0.202"           # Receiver's IP
PORT = 12345
BUFFER_SIZE = 1024 * 1024     # 1MB chunks

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to receiver.")

        start_time = time.time()  # Start timing
        cpu_usages = []

        # Step 1: Hash the file content
        with open(FILE_PATH, "rb") as f:
            file_data = f.read()
        file_hash = hashlib.sha256(file_data).hexdigest()

        # Step 2: Generate MPPK Digital Signature
        signature = sign_message(file_hash)  # From sign.py

        # Send file hash and signature
        s.sendall(struct.pack("!I", len(file_hash)))
        s.sendall(file_hash.encode())
        s.sendall(struct.pack("!I", len(str(signature))))
        s.sendall(str(signature).encode())
        print(f"Sent file hash and MPPK signature: {file_hash}, {signature}")

        # Step 3: Send file in chunks
        with open(FILE_PATH, "rb") as f:
            chunk = f.read(BUFFER_SIZE)
            while chunk:
                s.sendall(struct.pack("!I", len(chunk)))  # Send chunk size
                s.sendall(chunk)  # Send chunk
                cpu_usages.append(psutil.cpu_percent(interval=0.1))
                print(f"Sent chunk of size {len(chunk)} bytes.")
                chunk = f.read(BUFFER_SIZE)

        # Send end marker to indicate completion
        s.sendall(struct.pack("!I", 0))  # Zero length
        print("File sent successfully.")

        end_time = time.time()
        print(f"Time taken: {end_time - start_time:.2f} seconds.")
        print(f"Average CPU usage: {sum(cpu_usages) / len(cpu_usages):.2f}%")

except Exception as e:
    print(f"An error occurred: {e}")
