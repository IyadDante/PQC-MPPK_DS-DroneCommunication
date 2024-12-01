import socket
import time
import psutil
import logging

# Configure logging
logging.basicConfig(
    filename="receiver.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

HOST = "0.0.0.0"
PORT = 12345
OUTPUT_FILE = "received_large_file.bin"

BUFFER_SIZE = 1024 * 1024  # 1MB chunks

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logging.info(f"Server listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        logging.info(f"Connected by {addr}")

        start_time = time.time()  # Start timing
        cpu_usages = []  # Monitor CPU usage

        with open(OUTPUT_FILE, "wb") as f:
            while chunk := conn.recv(BUFFER_SIZE):
                f.write(chunk)
                cpu_usage = psutil.cpu_percent(interval=0.1)
                cpu_usages.append(cpu_usage)
                logging.info(f"Received {len(chunk)} bytes. CPU usage: {cpu_usage:.2f}%")

        end_time = time.time()  # End timing
        elapsed_time = end_time - start_time

        avg_cpu_usage = sum(cpu_usages) / len(cpu_usages) if cpu_usages else 0
        logging.info(f"File transfer completed in {elapsed_time:.2f} seconds.")
        logging.info(f"Average CPU usage during transfer: {avg_cpu_usage:.2f}%")

except Exception as e:
    logging.error(f"An error occurred: {e}")
