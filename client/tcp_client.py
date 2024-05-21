import asyncio

async def tcp_client(host, port):
    reader, writer = await asyncio.open_connection(host, port)

    writer.write("A".encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()}')

    print('Closing the connection')
    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    host = '100.84.218.109'  # Replace with your server's IP address
    port = 8888         # Replace with your server's port

    asyncio.run(tcp_client(host, port))