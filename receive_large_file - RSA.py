import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import logging

# Load private key
with open("private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

HOST = "0.0.0.0"
PORT = 12345
OUTPUT_FILE = "received_file_RSA.bin"

# Configure logging
logging.basicConfig(
    filename="receiver - RSA.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    logging.info(f"Server listening on {HOST}:{PORT}")

    conn, addr = s.accept()
    logging.info(f"Connected by {addr}")

    with open(OUTPUT_FILE, "wb") as f:
        while chunk := conn.recv(512):  # Adjust based on encryption chunk size
            decrypted_chunk = private_key.decrypt(
                chunk,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            f.write(decrypted_chunk)

    logging.info("File received and decrypted.")
