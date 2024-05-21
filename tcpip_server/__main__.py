import asyncio
import socket
import cv2

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

async def capture_hex():
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

    # Get the RGB value of the center pixel
    center_pixel = rgb_frame[120, 160]

    # Convert the RGB value to a hex value
    hex_value = rgb_to_hex(center_pixel)
    print(f"Hex value of center pixel: {hex_value}")

    # Return the hex value
    return hex_value

async def process_message(message):
    hex_value = await capture_hex()
    if hex_value is not None:
        response = f"Processed hex value: {hex_value}"
    else:
        response = "Failed to capture frame and get hex value."
    return response

async def handle_client(reader, writer):
    try:
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')

        print(f"Received {message} from {addr}")

        # Add your custom logic here
        response_message = await process_message(message)

        # Send response
        writer.write(response_message.encode())
        await writer.drain()

        print(f"Sent response to {addr}")

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        print("Closing the connection")
        writer.close()
        await writer.wait_closed()

async def tcp_server(host, port):
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f"TCP server running on {addr}")

    async with server:
        await server.serve_forever()

async def start_tcp_ip_server():
    await tcp_server('0.0.0.0', 8888)

# If you want to run the server in the main event loop
if __name__ == "__main__":
    asyncio.run(start_tcp_ip_server())
