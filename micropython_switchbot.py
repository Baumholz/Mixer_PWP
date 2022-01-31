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

import random
import struct

_FILE_SERVICE_UUID = bluetooth.UUID(0x1234)
_CONTROL_CHARACTERISTIC_UUID = bluetooth.UUID(0x1235)


_COMMAND_SEND = const(0)
_COMMAND_RECV = const(1)  # Not yet implemented.
_COMMAND_LIST = const(2)
_COMMAND_SIZE = const(3)
_COMMAND_DONE = const(4)

_STATUS_OK = const(0)
_STATUS_NOT_IMPLEMENTED = const(1)
_STATUS_NOT_FOUND = const(2)

_L2CAP_PSN = const(22)
_L2CAP_MTU = const(128)
SERVICE_UUID = bluetooth.UUID("cba20d00-224d-11e6-9fb8-0002a5d5c51b")
CHAR_UUID = bluetooth.UUID("cba20002-224d-11e6-9fb8-0002a5d5c51b")
CHAR_CAPTURE_UUID = bluetooth.UUID("cba20003-224d-11e6-9fb8-0002a5d5c51b")

press = b'\x57\x01\x00'
on = b'\x57\x01\x01'
off = b'\x57\x01\x02'

async def main(d, command, timeout):
    #later switch the mac adress to the ones we are using!
    if d == 1:
        device = aioble.Device(1, "e4:6e:35:6b:62:e3")
    else:
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
            await asyncio.sleep_ms(timeout)
            print("turning on for "+str(timeout)+" milliseconds!")
            await characteristic.write(command, timeout_ms=10000)
            print("finished dispence!")

    except asyncio.TimeoutError:
        print('Timeout')


asyncio.run(main(on,5000))
