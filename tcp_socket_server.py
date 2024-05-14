import socket
import cv2

def capture_rgb():
    # Initialize the USB camera
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return None

    # Capture a frame from the camera
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Error: Unable to capture frame.")
        return None

    # Resize the frame to the desired dimensions
    frame = cv2.resize(frame, (320, 240))

    # Release the camera
    cap.release()

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Return the RGB frame
    return rgb_frame

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
                    rgb_frame = capture_rgb()
                    if rgb_frame is not None:
                        client_socket.sendall(rgb_frame.tobytes())
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close the connection
            client_socket.close()

if __name__ == "__main__":
    main()
