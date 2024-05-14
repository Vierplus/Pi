import asyncio
import socket

async def tcp_client(server_ip, server_port, message):
    reader, writer = await asyncio.open_connection(server_ip, server_port)

    print(f'Sending: {message}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

async def main():
    server_ip = '192.168.8.190'  # Server IP address
    server_port = 13000      # Server port
    message = 'Hello Server!'  # Message to send

    await tcp_client(server_ip, server_port, message)

asyncio.run(main())