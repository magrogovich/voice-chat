import socket
import sounddevice as sd
import numpy as np
import sys

def audio_callback(outdata, frames, time, status):
    # This function is called whenever the audio device needs more data to play
    if status:
        print(status, flush=True)

    # Receive audio data from the server and play it
    try:
        data = server_socket.recv(frames * 2 * 2)  # frames * 2 channels * 2 bytes per sample
        if len(data) == frames * 2 * 2:
            outdata[:] = np.frombuffer(data, dtype=np.int16).reshape((frames, 2))
        else:
            print("Incomplete audio data received.")
    except ConnectionResetError:
        print("Connection to the server lost.")
        exit()

def start_client(server_ip):
    global server_socket

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server_socket.connect((server_ip, 3000))
    except socket.error as e:
        print(f"Error connecting to the server: {e}")
        exit()

    # Start a new thread for audio communication
    audio_stream = sd.OutputStream(callback=audio_callback)
    audio_stream.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Client disconnected.")
        server_socket.close()
        audio_stream.stop()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py <server_ip>")
        sys.exit(1)

    server_ip = sys.argv[1]
    start_client(server_ip)
