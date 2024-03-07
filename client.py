import socket
import sounddevice as sd
import numpy as np

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


def start_client():
    global server_socket

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(('localhost', 12345))

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
    start_client()
