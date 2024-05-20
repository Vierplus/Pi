import asyncio
from asyncua import Server, ua


async def update_values(temperature_var, humidity_var):
    new_temperature = await temperature_var.get_value() + 1.0  # Simulate updating the temperature
    new_humidity = await humidity_var.get_value() + 1.0  # Simulate updating the humidity

    await temperature_var.write_value(new_temperature)
    await humidity_var.write_value(new_humidity)

    print(f"Updated Temperature to {new_temperature} and Humidity to {new_humidity}")


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
    uri = "http://example.com/Messestand"  # Use a generic, stable URI
    idx = await server.register_namespace(uri)

    # Add an object to the address space
    messestand = await server.nodes.objects.add_object(idx, "Messestand")
    temperature = await messestand.add_variable(idx, "Temperature", 0.0)
    humidity = await messestand.add_variable(idx, "Humidity", 0.0)
    await temperature.set_writable()
    await humidity.set_writable()

    print("Starting OPC UA server at " + url)

    # Serve clients and update values periodically
    async with server:
        print("OPC UA server is running and waiting for requests...")
        while True:
            await update_values(temperature, humidity)  # Update the values
            await asyncio.sleep(5)  # Adjust the sleep duration as needed


async def start_opc_ua_server():
    await opc_ua_server()
