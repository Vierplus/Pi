from asyncua import ua, Server
from asyncua.ua import ObjectIds
import netifaces as ni
import datetime
import asyncio
import datetime

#GPIOs konfigurieren
#import RPi.GPIO as GPIO
import time
import os

# Zählweise der Pins auf GPIO-Nummern festlegen
#GPIO.setmode(GPIO.BCM);

# Warnmeldungen ausschalten
#GPIO.setwarnings(False);

# Konstanten definieren
luefterPIN = 13

# GPIO Eingänge definieren
#GPIO.setup(luefterPIN, GPIO.OUT)
#GPIO.output(luefterPIN, GPIO.LOW)

# PWM-Channel initialisieren
#pwm1 = GPIO.PWM(luefterPIN, 100)
#pwm1.start(100.0)

#def setFanDuty(sfd = 0.0): # Setzt den Dutycycle (in % von 0.0-100.0) für den Lüfter
#    pwm1.ChangeDutyCycle(sfd)
#    return
        
#def startFan(): # Setzt den Lüfter für 1s Anlaufzeit auf 100%
#    fanOutput = 100.0
#    setFanDuty(fanOutput)
#    print("Anlaufzeit: 1s")
#    time.sleep(1)
#    return

async def main():
    server=Server()
    await server.init()
    #Get the ip address
    IPV4_Address = ni.ifaddresses('en0')[ni.AF_INET][0]['addr']
    url="opc.tcp://"+IPV4_Address+":4840"
    server.set_endpoint(url)

    server.set_security_policy(
        [
            ua.SecurityPolicyType.NoSecurity
        ])

    #OPCUA Namensraum festleben
    name="OPCUA_Musterplatine"
    addspace= await server.register_namespace(name)

    dev = await server.nodes.base_object_type.add_object_type(addspace, "FBS-Platine")
    await (await dev.add_variable(addspace, "sensor", 1.0)).set_modelling_rule(True)
    await (await dev.add_variable(addspace, "luefter", 0)).set_modelling_rule(True)
    await (await dev.add_variable(addspace, "time", datetime.datetime.utcnow())).set_modelling_rule(True)

    # First a folder to organise our nodes
    myfolder = await server.nodes.objects.add_folder(addspace, "Raspi")

    # instanciate one instance of our device
    mydevice = await myfolder.add_object(addspace, "FBS-Platine", dev)

    # get proxy to child-elements
    sensor = await mydevice.get_child(
        [f"{addspace}:sensor"]
    )
    luefter = await mydevice.get_child(
        [f"{addspace}:luefter"]
    )
    time = await mydevice.get_child(
        [f"{addspace}:time"]
    )

    await luefter.set_writable()

    #OPCUA-Server starten
    async with server:
        print("Server startet auf {}",format(url))

        while True:
            now = datetime.datetime.now()
            await asyncio.sleep(2)
            print("Zeit: ", now)


if __name__ == "__main__":
    asyncio.run(main())