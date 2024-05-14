from asyncua import ua, Server
from asyncua.ua import ObjectIds
import netifaces as ni
import datetime
import asyncio
import time
import adafruit_dht
import board

async def main():
    server = Server()
    await server.init()
    
    # Get the IP address
    IPV4_Address = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    url = "opc.tcp://" + IPV4_Address + ":4840"
    server.set_endpoint(url)

    server.set_security_policy(
        [
            ua.SecurityPolicyType.NoSecurity
        ])

    # OPC UA Namespace
    name = "OPCUA_Musterplatine"
    addspace = await server.register_namespace(name)

    dev = await server.nodes.base_object_type.add_object_type(addspace, "FBS-Platine")
    await (await dev.add_variable(addspace, "Temperature", 0.0)).set_modelling_rule(True)
    await (await dev.add_variable(addspace, "Humidity", 0.0)).set_modelling_rule(True)

    myfolder = await server.nodes.objects.add_folder(addspace, "Raspi")
    mydevice = await myfolder.add_object(addspace, "FBS-Platine", dev)

    temperature_node = await mydevice.get_child([f"{addspace}:Temperature"])
    humidity_node = await mydevice.get_child([f"{addspace}:Humidity"])

    await temperature_node.set_writable()
    await humidity_node.set_writable()

    dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

    async with server:
        print("Server started at", url)

        while True:
            try:
                temperature_c = dhtDevice.temperature
                humidity = dhtDevice.humidity

                # Update node values
                await temperature_node.write_value(ua.DataValue(temperature_c))
                await humidity_node.write_value(ua.DataValue(humidity))

                print("Temperature: {:.2f} C, Humidity: {:.2f}%".format(temperature_c, humidity))
            except RuntimeError as error:
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                print(error)
                continue

            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())