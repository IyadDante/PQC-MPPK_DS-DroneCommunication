import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct
import time
import psutil

# File and connection parameters
OUTPUT_FILE = "received_large_file_AES.bin"
HOST = "0.0.0.0"
PORT = 12345
BUFFER_SIZE = 1024 * 1024  # 1MB chunks

# AES parameters
KEY = b"thisisaverysecurekey1234"  # 32 bytes key

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        print(f"Connected by {addr}")

        # Receive IV from sender
        iv_length = struct.unpack("!I", conn.recv(4))[0]  # Receive IV length
        iv = conn.recv(iv_length)  # Receive IV itself

        # Initialize AES cipher
        cipher = Cipher(algorithms.AES(KEY), modes.GCM(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        start_time = time.time()  # Start timing
        cpu_usages = []  # Track CPU usage

        with open(OUTPUT_FILE, "wb") as f:
            while True:
                # Receive chunk size
                chunk_size_data = conn.recv(4)
                if not chunk_size_data:
                    break

                chunk_size = struct.unpack("!I", chunk_size_data)[0]
                if chunk_size == 0:
                    break

                # Receive and decrypt the chunk
                chunk = conn.recv(chunk_size)
                if len(chunk) != chunk_size:
                    print(f"Received incomplete or corrupted chunk of size {len(chunk)} bytes.")
                    break

                decrypted_chunk = decryptor.update(chunk)
                f.write(decrypted_chunk)
                cpu_usages.append(psutil.cpu_percent(interval=0.1))  # Record CPU usage
                print(f"Received and decrypted chunk of size {len(chunk)} bytes.")

            # Finalize decryption and verify tag
            final_decrypted = decryptor.finalize()
            f.write(final_decrypted)

            # Receive and verify tag
            tag_length = struct.unpack("!I", conn.recv(4))[0]
            tag = conn.recv(tag_length)
            decryptor.finalize_with_tag(tag)

        end_time = time.time()  # End timing

        print(f"File transfer completed in {end_time - start_time:.2f} seconds.")
        if cpu_usages:
            print(f"Average CPU usage during transfer: {sum(cpu_usages) / len(cpu_usages):.2f}%")

except Exception as e:
    print(f"An error occurred: {e}")
