import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

# Load public key
with open("public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

# File to send
FILE_PATH = "large_file.bin"
HOST = "10.0.0.202"  # Receiver's IP
PORT = 12345
PLAINTEXT_SIZE = 190  # Max plaintext size for 2048-bit RSA with OAEP
END_MARKER = b"END"  # Marker to signal end of transmission

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to receiver.")

        with open(FILE_PATH, "rb") as f:
            while True:
                chunk = f.read(PLAINTEXT_SIZE)
                if not chunk:
                    break

                # Pad the last chunk if smaller than PLAINTEXT_SIZE
                if len(chunk) < PLAINTEXT_SIZE:
                    chunk += b" " * (PLAINTEXT_SIZE - len(chunk))

                encrypted_chunk = public_key.encrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                print(f"Sending encrypted chunk of size {len(encrypted_chunk)} bytes")
                s.sendall(encrypted_chunk)

        # Send the end marker
        s.sendall(END_MARKER)
        print("File sent successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
