import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import time

# Load public key
with open("public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

# File to send
FILE_PATH = "large_file.bin"
HOST = "10.0.0.202"  # Receiver's IP
PORT = 12345
PLAINTEXT_SIZE = 190  # Max plaintext size for 2048-bit RSA with OAEP
ENCRYPTED_SIZE = 256  # Fixed ciphertext size for 2048-bit RSA

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to receiver.")

        with open(FILE_PATH, "rb") as f:
            chunk = f.read(PLAINTEXT_SIZE)
            while chunk:
                encrypted_chunk = public_key.encrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                s.sendall(encrypted_chunk)
                chunk = f.read(PLAINTEXT_SIZE)  # Read the next plaintext chunk

        print("File sent successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
