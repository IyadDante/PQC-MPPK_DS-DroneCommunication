import socket
import time
import psutil

HOST = "10.0.0.202"  # Replace with your PC's IP
PORT = 12345
FILE_PATH = "large_file.bin"  # Path to the large file

BUFFER_SIZE = 1024 * 1024  # 1MB chunks

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to receiver.")
    
    start_time = time.time()  # Start timing

    # Monitor CPU usage during the transfer
    cpu_usages = []

    with open(FILE_PATH, "rb") as f:
        chunk = f.read(BUFFER_SIZE)
        while chunk:
            s.sendall(chunk)
            cpu_usages.append(psutil.cpu_percent(interval=0.1))  # Track CPU usage
            print(f"Sent {len(chunk)} bytes...")
            chunk = f.read(BUFFER_SIZE)  # Read the next chunk

    end_time = time.time()  # End timing

    print(f"File transfer completed in {end_time - start_time:.2f} seconds.")
    if cpu_usages:  # Avoid division by zero if no CPU data was recorded
        print(f"Average CPU usage during transfer: {sum(cpu_usages) / len(cpu_usages):.2f}%")
