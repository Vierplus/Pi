import asyncio

async def process_message(message):
    # Placeholder for your custom logic
    # Process the message and generate a response
    response = f"Processed: {message}"  # Example response
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
