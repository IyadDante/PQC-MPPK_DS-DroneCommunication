import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import time
import psutil
import struct

# File and connection parameters
FILE_PATH = "large_file.bin"
HOST = "10.0.0.202"  # Receiver's IP
PORT = 12345
BUFFER_SIZE = 1024 * 1024  # 1MB chunks

# AES parameters
KEY = b"thisisaverysecurekey1234"  # 32 bytes key
IV = os.urandom(16)  # Random 16 bytes Initialization Vector (IV)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to receiver.")

        # Send IV to the receiver
        s.sendall(struct.pack("!I", len(IV)))  # Send IV length
        s.sendall(IV)  # Send IV itself

        # Initialize AES cipher
        cipher = Cipher(algorithms.AES(KEY), modes.GCM(IV), backend=default_backend())
        encryptor = cipher.encryptor()

        start_time = time.time()  # Start timing
        cpu_usages = []  # Track CPU usage

        with open(FILE_PATH, "rb") as f:
            chunk = f.read(BUFFER_SIZE)
            while chunk:
                encrypted_chunk = encryptor.update(chunk)
                s.sendall(struct.pack("!I", len(encrypted_chunk)))  # Send chunk length
                s.sendall(encrypted_chunk)  # Send encrypted chunk
                cpu_usages.append(psutil.cpu_percent(interval=0.1))  # Record CPU usage
                print(f"Sent encrypted chunk of size {len(encrypted_chunk)} bytes.")
                chunk = f.read(BUFFER_SIZE)  # Read the next chunk

        # Finalize encryption and send the last block and tag
        encrypted_final = encryptor.finalize()
        s.sendall(struct.pack("!I", len(encrypted_final)))
        s.sendall(encrypted_final)
        tag = encryptor.tag
        s.sendall(struct.pack("!I", len(tag)))
        s.sendall(tag)

        end_time = time.time()  # End timing

        print(f"File sent successfully in {end_time - start_time:.2f} seconds.")
        if cpu_usages:
            print(f"Average CPU usage during transfer: {sum(cpu_usages) / len(cpu_usages):.2f}%")

except Exception as e:
    print(f"An error occurred: {e}")
