import socket
import time
import psutil
import hashlib
import json
from verify import V  # Import the verification function

HOST = "0.0.0.0"
PORT = 12345
OUTPUT_FILE = "received_large_file.bin"
SIGNATURE_FILE = "received_file_signature.json"
PUBLIC_KEY_FILE = "public_key.json"

BUFFER_SIZE = 1024 * 1024  # 1MB chunks

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")

    conn, addr = s.accept()
    print(f"Connected by {addr}")

    # Step 1: Receive the file
    with open(OUTPUT_FILE, "wb") as f:
        while chunk := conn.recv(BUFFER_SIZE):
            f.write(chunk)
            print(f"Received {len(chunk)} bytes...")

    # Step 2: Receive the signature
    with open(SIGNATURE_FILE, "wb") as sig_file:
        while chunk := conn.recv(BUFFER_SIZE):
            sig_file.write(chunk)
            print(f"Received {len(chunk)} bytes (signature file)...")

print("File and signature received.")

# Step 3: Verify the File
with open(OUTPUT_FILE, "rb") as f:
    file_data = f.read()

hash_object = hashlib.sha256(file_data)  # Hash the received file
mu = hash_object.hexdigest()

with open(SIGNATURE_FILE, "r") as sig_file:
    signature = json.load(sig_file)

with open(PUBLIC_KEY_FILE, "r") as pub_file:
    public_key = json.load(pub_file)

# Verify the signature
result = V(public_key, int(mu, 16), signature, m=2, n=2, lambda_=1, ell=[1, 1], p=19)
if result['left'] == result['right']:
    print("File verification: VALID")
else:
    print("File verification: INVALID")
