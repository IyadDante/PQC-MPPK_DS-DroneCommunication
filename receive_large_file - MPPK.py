import socket
import hashlib
import struct
import time
import psutil
from verify import verify_signature  # Use existing MPPK verification logic

# Constants
OUTPUT_FILE = "received_large_file_MPPK.bin"
HOST = "0.0.0.0"
PORT = 12345
BUFFER_SIZE = 1024 * 1024  # 1MB chunks

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        print(f"Connected by {addr}")

        start_time = time.time()  # Start timing
        cpu_usages = []

        # Step 1: Receive file hash and signature
        file_hash_length = struct.unpack("!I", conn.recv(4))[0]
        file_hash = conn.recv(file_hash_length).decode()
        signature_length = struct.unpack("!I", conn.recv(4))[0]
        signature = conn.recv(signature_length).decode()
        print(f"Received file hash: {file_hash} and signature: {signature}")

        # Step 2: Receive the file in chunks
        received_file_data = b""
        while True:
            chunk_size_data = conn.recv(4)
            if not chunk_size_data:
                break

            chunk_size = struct.unpack("!I", chunk_size_data)[0]
            if chunk_size == 0:  # End marker
                break

            chunk = conn.recv(chunk_size)
            received_file_data += chunk
            cpu_usages.append(psutil.cpu_percent(interval=0.1))
            print(f"Received chunk of size {len(chunk)} bytes.")

        # Step 3: Verify hash and signature
        reconstructed_hash = hashlib.sha256(received_file_data).hexdigest()
        is_valid = verify_signature(reconstructed_hash, signature)  # From verify.py

        if is_valid and reconstructed_hash == file_hash:
            with open(OUTPUT_FILE, "wb") as f:
                f.write(received_file_data)
            print("File integrity and MPPK signature verified. File saved.")
        else:
            print("Verification failed: Hash or MPPK signature mismatch!")

        end_time = time.time()
        print(f"Time taken: {end_time - start_time:.2f} seconds.")
        print(f"Average CPU usage: {sum(cpu_usages) / len(cpu_usages):.2f}%")

except Exception as e:
    print(f"An error occurred: {e}")
