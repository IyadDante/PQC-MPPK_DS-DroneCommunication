import socket
import time
import psutil
import hashlib
import json
from sign import sign_message  # Import the MPPK signing function

HOST = "10.0.0.202"  # Replace with the receiver's IP
PORT = 12345
FILE_PATH = "large_file.bin"
SIGNATURE_PATH = "file_signature.json"

BUFFER_SIZE = 1024 * 1024  # 1MB chunks

# Step 1: Hash and Sign the File
with open(FILE_PATH, "rb") as f:
    file_data = f.read()

hash_object = hashlib.sha256(file_data)  # Hash the file
signature = sign_message(hash_object.hexdigest())  # Sign the hash
with open(SIGNATURE_PATH, "w") as sig_file:
    json.dump(signature, sig_file)  # Save signature to a file

print("File signed. Signature saved.")

# Step 2: Send the File and Signature
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to receiver.")

    # Send the file
    with open(FILE_PATH, "rb") as f:
        chunk = f.read(BUFFER_SIZE)
        while chunk:
            s.sendall(chunk)
            print(f"Sent {len(chunk)} bytes...")
            chunk = f.read(BUFFER_SIZE)

    # Send the signature file
    with open(SIGNATURE_PATH, "rb") as sig_file:
        signature_data = sig_file.read()
        s.sendall(signature_data)
        print(f"Sent signature file ({len(signature_data)} bytes).")

print("File and signature transfer completed.")
