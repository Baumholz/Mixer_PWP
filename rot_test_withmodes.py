import time
import math
from rotary_irq_esp import RotaryIRQ
import wot_client.api as apiX
import sys
import uasyncio as asyncio
from ble import turnon_ble
sys.path.reverse()

class Action:
    def __init__(self, mode):
        self.mode = mode

    def run_dispenser(self, duration):
        if self.mode == 0:
            #do nothing
            pass
        elif self.mode == 1:
            #create ap and control
            pass
        elif self.mode == 2:
            #create ap and control
            pass
        elif self.mode == 3:
            #internet
            #bluetooth function aufrufen
            #time.sleep(duration)
            #bluetooth function aufrufen
            pass

a = Action(3)

def init():
    r = RotaryIRQ(pin_num_clk=13, 
                  pin_num_dt=12, 
                  min_val=0, 
                  max_val=19, 
                  reverse=False, 
                  range_mode=RotaryIRQ.RANGE_WRAP)
                  
    val_old = math.floor(r.value()/5)
    return r, val_old

apiX.init()
apiX.set_access_mode(3)
def example_on_action_handler(topic, msg):
    print('I am the example on_action_handler!', topic, msg)
    #msg = duration
    #a.run_dispenser(msg)
    press = b'\x57\x01\x00'
    on = b'\x57\x01\x01'
    off = b'\x57\x01\x02'
    asyncio.run(turnon_ble(1,on,msg*1000))

apiX.set_on_action_handler(example_on_action_handler)

print("done with set on")
print("done with first part")

def rotary_send():
    r, val_old = init()
    while True:
        print("ready to publish event")
        val_new = math.floor(r.value()/5)
        
        if val_old != val_new:
            val_old = val_new
            print('result =', val_new)
            apiX.publish_event("mode","test"+str(val_new))
            apiX.set_access_mode(val_new)
            #TODO: add the code to switch the mode and run the different functions
        time.sleep_ms(5000)
rotary_send()

