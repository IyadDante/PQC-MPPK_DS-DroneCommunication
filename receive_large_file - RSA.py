import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

# Load private key
with open("private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# File to save
OUTPUT_FILE = "received_large_file_RSA.bin"
HOST = "0.0.0.0"
PORT = 12345
BUFFER_SIZE = 256  # Encrypted chunk size for 2048-bit RSA key

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        print(f"Connected by {addr}")

        with open(OUTPUT_FILE, "wb") as f:
            while True:
                chunk = conn.recv(BUFFER_SIZE)
                if not chunk:
                    break

                print(f"Received encrypted chunk of size {len(chunk)} bytes")

                # Ensure the chunk is the correct size before decrypting
                if len(chunk) != BUFFER_SIZE:
                    print("Received incomplete or corrupted chunk.")
                    break

                decrypted_chunk = private_key.decrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                f.write(decrypted_chunk.strip())  # Remove padding after decryption

        print(f"File received and saved to {OUTPUT_FILE}.")

except Exception as e:
    print(f"An error occurred: {e}")
