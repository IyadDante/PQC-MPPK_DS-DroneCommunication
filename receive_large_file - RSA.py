import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import struct

# Load private key
with open("private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# File to save
OUTPUT_FILE = "received_large_file_RSA.bin"
HOST = "0.0.0.0"
PORT = 12345
END_MARKER = b"END_MARKER"

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        print(f"Connected by {addr}")

        with open(OUTPUT_FILE, "wb") as f:
            while True:
                # Receive the length of the incoming chunk
                chunk_size_data = conn.recv(4)  # 4 bytes for chunk size
                if not chunk_size_data:
                    break

                chunk_size = struct.unpack("!I", chunk_size_data)[0]

                # Receive the actual chunk
                chunk = conn.recv(chunk_size)
                if chunk == END_MARKER:
                    print("End of file marker received.")
                    break

                if len(chunk) != chunk_size:
                    print(f"Received incomplete or corrupted chunk of size {len(chunk)} bytes.")
                    break

                # Decrypt and write the chunk
                decrypted_chunk = private_key.decrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                f.write(decrypted_chunk)

        print(f"File received and saved to {OUTPUT_FILE}.")

except Exception as e:
    print(f"An error occurred: {e}")
