import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import logging

# Load private key
with open("private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# File to save
OUTPUT_FILE = "received_large_file_RSA.bin"
HOST = "0.0.0.0"
PORT = 12345
BUFFER_SIZE = 256  # Encrypted chunk size for 2048-bit RSA key

# Configure logging
logging.basicConfig(
    filename="receiver - RSA.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logging.info(f"Server listening on {HOST}:{PORT}")
        print(f"Server listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        logging.info(f"Connected by {addr}")
        print(f"Connected by {addr}")

        with open(OUTPUT_FILE, "wb") as f:
            chunk = conn.recv(BUFFER_SIZE)
            while chunk:
                decrypted_chunk = private_key.decrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                f.write(decrypted_chunk)
                chunk = conn.recv(BUFFER_SIZE)

        logging.info(f"File received and saved to {OUTPUT_FILE}.")
        print(f"File received and saved to {OUTPUT_FILE}.")

except Exception as e:
    logging.error(f"An error occurred: {e}")
    print(f"An error occurred: {e}")
