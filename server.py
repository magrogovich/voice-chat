import socket
import sounddevice as sd
import numpy as np

def audio_callback(indata, frames, time, status):
    # This function is called whenever new audio data is received
    if status:
        print(status, flush=True)

    # Send the audio data to all connected clients
    for client_socket in clients:
        client_socket.sendall(indata.tobytes())

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(5)

    print("Server is listening for incoming connections...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr} established.")

        # Add the new client socket to the list
        clients.append(client_socket)

        # Start a new thread for each client to handle audio communication
        audio_stream = sd.InputStream(callback=audio_callback)
        audio_stream.start()

        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
            except ConnectionResetError:
                # Handle disconnection
                break

        # Remove the disconnected client from the list
        clients.remove(client_socket)
        audio_stream.stop()
        client_socket.close()

if __name__ == "__main__":
    clients = []  # List to store connected client sockets
    start_server()
