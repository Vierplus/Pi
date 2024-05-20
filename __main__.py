import asyncio
from tcpip_server.__main__ import start_tcp_ip_server as tcp_server_main
from opcua_server.__main__ import start_opc_ua_server as opc_ua_server_main

async def main():
    # Run both servers concurrently
    await asyncio.gather(
        tcp_server_main(),
        opc_ua_server_main()
    )

if __name__ == '__main__':
    asyncio.run(main())
