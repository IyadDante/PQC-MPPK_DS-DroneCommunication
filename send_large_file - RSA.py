import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import struct
import time
import psutil

# Load public key
with open("public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

# File to send
FILE_PATH = "large_file.bin"
HOST = "10.0.0.202"  # Receiver's IP
PORT = 12345
PLAINTEXT_SIZE = 190  # Max plaintext size for 2048-bit RSA with OAEP
END_MARKER = b"END_MARKER"  # Signal to mark the end of the file

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to receiver.")
        
        start_time = time.time()  # Start timing
        cpu_usages = []  # Track CPU usage

        with open(FILE_PATH, "rb") as f:
            while True:
                chunk = f.read(PLAINTEXT_SIZE)
                if not chunk:
                    break

                # Encrypt the chunk
                encrypted_chunk = public_key.encrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )

                # Send the length of the encrypted chunk followed by the chunk itself
                s.sendall(struct.pack("!I", len(encrypted_chunk)))  # Length as 4-byte integer
                s.sendall(encrypted_chunk)
                cpu_usages.append(psutil.cpu_percent(interval=0.1))  # Record CPU usage
                print(f"Sent encrypted chunk of size {len(encrypted_chunk)} bytes")

        # Send end marker
        s.sendall(struct.pack("!I", len(END_MARKER)))
        s.sendall(END_MARKER)

        end_time = time.time()  # End timing

        print(f"File sent successfully in {end_time - start_time:.2f} seconds.")
        if cpu_usages:  # Avoid division by zero if no CPU data was recorded
            print(f"Average CPU usage during transfer: {sum(cpu_usages) / len(cpu_usages):.2f}%")

except Exception as e:
    print(f"An error occurred: {e}")
