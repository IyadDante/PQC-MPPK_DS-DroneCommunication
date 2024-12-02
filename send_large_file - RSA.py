import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import time
import logging

# Load public key
with open("public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# File to send
FILE_PATH = "large_file.bin"
HOST = "10.0.0.202"  # Receiver's IP
PORT = 12345
BUFFER_SIZE = 1024  # RSA limits chunk size

# Configure logging
logging.basicConfig(
    filename="sender - RSA.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        logging.info("Connected to receiver.")

        start_time = time.time()

        with open(FILE_PATH, "rb") as f:
            chunk = f.read(BUFFER_SIZE - 42)  # Subtract padding overhead
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
                chunk = f.read(BUFFER_SIZE - 42)  # Read the next chunk

        elapsed_time = time.time() - start_time
        logging.info(f"File sent in {elapsed_time:.2f} seconds.")
        print(f"File sent in {elapsed_time:.2f} seconds.")

except Exception as e:
    logging.error(f"An error occurred: {e}")
    print(f"An error occurred: {e}")
