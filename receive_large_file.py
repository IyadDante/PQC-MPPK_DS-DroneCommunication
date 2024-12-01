import socket

HOST = "0.0.0.0"
PORT = 12345
OUTPUT_FILE = "received_large_file.bin"

BUFFER_SIZE = 1024 * 1024  # 1MB chunks

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    
    with open(OUTPUT_FILE, "wb") as f:
        while chunk := conn.recv(BUFFER_SIZE):
            f.write(chunk)
            print(f"Received {len(chunk)} bytes...")
    
    print("File transfer completed.")
