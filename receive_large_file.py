import socket

HOST = "0.0.0.0"  # Listen on all available interfaces
PORT = 12345       # Same port as in send_message.py

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        data = conn.recv(1024)
        if data:
            print("Received data:", data.decode())
