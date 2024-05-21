import asyncio 
from asyncua import Server, ua
from asyncua.ua import ObjectIds
import netifaces as ni
import datetime
import asyncio
import time
import adafruit_dht
import board


async def update_values(temperature_var, humidity_var, dhtDevice):
    temperature_c = dhtDevice.temperature
    humidity = dhtDevice.humidity

    # Update node values
    await temperature_var.write_value(ua.DataValue(temperature_c))
    await humidity_var.write_value(ua.DataValue(humidity))

    print("Temperature: {:.2f} C, Humidity: {:.2f}%".format(temperature_c, humidity))

async def opc_ua_server():
    # Setup the server
    server = Server()
    await server.init()

    # Define the endpoint
    url = "opc.tcp://0.0.0.0:4840"
    server.set_endpoint(url)

    # Security settings (no security)
    server.set_security_policy([ua.SecurityPolicyType.NoSecurity])

    # Namespace setup
    uri = "VierPlus"  # Use a generic, stable URI
    idx = await server.register_namespace(uri)

    # Add an object to the address space
    dev = await server.nodes.objects.add_object(idx, "Messestand")
    await (await dev.add_variable(idx, "Temperature", 0.0)).set_modelling_rule(True)
    await (await dev.add_variable(idx, "Humidity", 0.0)).set_modelling_rule(True)

    myfolder = await server.nodes.objects.add_folder(idx, "Raspi")
    mydevice = await myfolder.add_object(idx, "FBS-VierPlus", dev)

    temperature = await mydevice.get_child([f"{idx}:Temperature"])
    humidity = await mydevice.get_child([f"{idx}:Humidity"])

    await temperature.set_writable()
    await humidity.set_writable()

    
    dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    print("Starting OPC UA server at " + url)

    # Serve clients and update values periodically
    async with server:
        print("OPC UA server is running and waiting for requests...")
        while True:
            try:
                await update_values(temperature, humidity)  # Update the values
            except RuntimeError as error:
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                print(error)
                continue
            await asyncio.sleep(5)  # Adjust the sleep duration as needed


async def start_opc_ua_server():
    await opc_ua_server()
