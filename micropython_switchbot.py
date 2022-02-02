# MIT license; Copyright (c) 2021 Jim Mussared

# This is a WIP client for l2cap_file_server.py. See that file for more
# information.
#https://github.com/micropython/micropython-lib/blob/master/micropython/bluetooth/aioble/multitests/ble_write_capture.py
#https://github.com/OpenWonderLabs/python-host/blob/master/switchbot_py3.py

import sys

sys.path.append("")

from micropython import const

import uasyncio as asyncio
import aioble
import bluetooth

SERVICE_UUID = bluetooth.UUID("cba20d00-224d-11e6-9fb8-0002a5d5c51b")
CHAR_UUID = bluetooth.UUID("cba20002-224d-11e6-9fb8-0002a5d5c51b")
CHAR_CAPTURE_UUID = bluetooth.UUID("cba20003-224d-11e6-9fb8-0002a5d5c51b")

press = b'\x57\x01\x00'
on = b'\x57\x01\x01'
off = b'\x57\x01\x02'

import tsl2591
n = 12
p = 25 
tsl = tsl2591.Tsl2591("test")

def get_light():
    full, ir = tsl.get_full_luminosity()  # read raw values (full spectrum and ir spectrum)
    lux = tsl.calculate_lux(full, ir)  # convert raw values to lux
    print (lux, full, ir)
    return lux

async def run_ble(command, timeout, callback):
    #later switch the mac adress to the ones we are using!
    device = aioble.Device(1, "e4:6e:35:6b:62:e3")

    try:
        async with await device.connect(timeout_ms=10000) as connection:
            print(connection)
            print("services")
            service = await connection.service(SERVICE_UUID)
            print("service", service)
            characteristic = await service.characteristic(CHAR_UUID)
            characteristic_capture = await service.characteristic(CHAR_CAPTURE_UUID)
            print("characteristic", characteristic.uuid, characteristic_capture.uuid)
            await characteristic.write(command, timeout_ms=10000)
            callback("status", True)
            await asyncio.sleep_ms(int(timeout))
            print("turning on for "+str(timeout)+" milliseconds!")
            await characteristic.write(command, timeout_ms=10000)
            callback("status", False)
            print("finished dispence!")

    except asyncio.TimeoutError:
        print('Timeout')
        
def run_on_api(timeout, callback):
    import urequests
    import time
    authToken = '6a80dc7e7efeb93ade60f8bbac144c32760c6f93ffcc22c589bfe2697f0bfda2703bd2b03d466f28c3e9473b43937896'
    deviceID1='E46E356B62E3'
    headers={"Authorization":authToken, "Connection":"close"}
    body = """{"command":"turnOn"}"""
    response = urequests.post("https://api.switch-bot.com/v1.0/devices/" + deviceID1 + "/commands", data=body, headers=headers)
    response = response.json()
    if response["statusCode"] == 100:
        print("Dispensor is on")
        callback("status", True)
    time.sleep(timeout)
    body = """{"command":"turnOn"}"""
    response = urequests.post("https://api.switch-bot.com/v1.0/devices/" + deviceID1 + "/commands", data=body, headers=headers)
    response = response.json()
    if response["statusCode"] == 100:
        print("Dispensor is off")
        callback("status", False)
    lightvalue = get_light()
    if lightvalue > 10:
        print("Device is empty")
        callback("level","False")
        callback("emptyingredient","True")
    else:
        print("Device still has things in it")
        callback("level","True")

#asyncio.run(run_ble(on,5000))

