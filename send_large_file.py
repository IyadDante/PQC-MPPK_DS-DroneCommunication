import socket
import time
import psutil
import logging

# Configure logging
logging.basicConfig(
    filename="sender.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

HOST = "10.0.0.202"  # Replace with your PC's IP
PORT = 12345
FILE_PATH = "large_file.bin"  # Ensure this points to the 200MB file

BUFFER_SIZE = 1024 * 1024  # 1MB chunks

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        logging.info("Connected to receiver.")

        start_time = time.time()  # Start timing
        cpu_usages = []  # Monitor CPU usage

        with open(FILE_PATH, "rb") as f:
            chunk = f.read(BUFFER_SIZE)
            while chunk:
                s.sendall(chunk)
                cpu_usage = psutil.cpu_percent(interval=0.1)
                cpu_usages.append(cpu_usage)
                logging.info(f"Sent {len(chunk)} bytes. CPU usage: {cpu_usage:.2f}%")
                chunk = f.read(BUFFER_SIZE)  # Read the next chunk

        end_time = time.time()  # End timing
        elapsed_time = end_time - start_time

        avg_cpu_usage = sum(cpu_usages) / len(cpu_usages) if cpu_usages else 0
        logging.info(f"File transfer completed in {elapsed_time:.2f} seconds.")
        logging.info(f"Average CPU usage during transfer: {avg_cpu_usage:.2f}%")

except Exception as e:
    logging.error(f"An error occurred: {e}")
