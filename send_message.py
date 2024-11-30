import socket
from sign import sign_message  # Import the signing function
import json

# Telemetry data to send
telemetry_data = {
    "location": "45.4215, -75.6972",
    "altitude": "120m",
    "speed": "25km/h",
    "battery": "85%"
}
message = json.dumps(telemetry_data)

# Sign the message
signed_message = sign_message(message)

# Send the signed message
HOST = "10.0.0.202"  # Your PC's IPv4 address
PORT = 12345         # Ensure the port matches the receiver script

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(json.dumps({"message": message, "signature": signed_message}).encode())
    print("Signed telemetry data sent.")
