import socket
import picamera
import io

def capture_rgb():
    # Initialize the camera
    with picamera.PiCamera() as camera:
        # Capture an image into a stream
        stream = io.BytesIO()
        camera.capture(stream, format='rgb')
        # Return the RGB value
        return stream.getvalue()

def main():
    # Set up the socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8888))  # Bind to all available interfaces on port 8888
    server_socket.listen(1)  # Listen for incoming connections (only 1 at a time)

    print("Server started, waiting for connections...")

    while True:
        # Accept incoming connection
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} established.")

        try:
            while True:
                # Receive data from the client
                data = client_socket.recv(1024)
                if not data:
                    break  # No more data, close connection

                if data.decode() == 'get_rgb':
                    # Send RGB data to client
                    rgb_value = capture_rgb()
                    client_socket.sendall(rgb_value)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close the connection
            client_socket.close()

if __name__ == "__main__":
    main()