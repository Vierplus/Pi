from asyncua import Client
import asyncio

url = "opc.tcp://10.62.255.16:4840/freeopcua/server/"
namespace = "OPCUA_Musterplatine"

async def main():
    client = Client(url=url,timeout=10)
    await client.connect()

    nsidx = await client.get_namespace_index(namespace)
    print(f"Namespace Index for '{namespace}': {nsidx}")

    var = await client.nodes.root.get_child(
    ["0:Objects", f"{nsidx}:Raspi", f"{nsidx}:FBS-Platine", f"{nsidx}:luefter"]
    )

    async with client:
        print("Client startet auf {}",format(url))
        
        while True:
            act_fanspeed = await var.read_value()
            print("FAN Speed: ", act_fanspeed)
            fanspeed = input("Enter FAN Speed from 0-100:")
            await var.write_value(int(fanspeed))


if __name__ == "__main__":
    asyncio.run(main())