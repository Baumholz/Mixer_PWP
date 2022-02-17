import time
import math
from rotary_irq_esp import RotaryIRQ
import wot_client.api as apiX
import sys
from dispense_apmode_async import ap_mode
from micropython_switchbot import run_on_api
from light import init_lights
import uasyncio as asyncio

sys.path.reverse()
apiX.init()
init_lights()

class Action:
    def __init__(self, mode):
        self.set_mode(mode)
        
    def set_mode(self, new_mode):
        self.mode = new_mode
        print("mode: ", self.mode)
        apiX.set_access_mode(new_mode) 
        
default_mode = 0
a = Action(default_mode)

def init():
    r = RotaryIRQ(pin_num_clk=27, 
                  pin_num_dt=26, 
                  min_val=0, 
                  max_val=19, 
                  reverse=False, 
                  range_mode=RotaryIRQ.RANGE_WRAP)
                  
    val_old = math.floor(r.value()/5)
    return r, val_old


def example_on_action_handler(topic, msg):
    run_on_api(int(msg), apiX.publish_event)

apiX.set_on_action_handler(example_on_action_handler)

r, val_old = init()

val_old = r.value()
def rotated():
    """check if rotary value changed"""
    global val_old
    val_new = math.floor(r.value()/5) 
    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)
        a.set_mode(val_new)
        apiX.publish_event("access_mode", str(val_new))
        return True
    return False

async def check_modes(task):
    """Kill ap mode if value changed"""
    print(a.mode)
    if rotated() and task:
        task.cancel()  
    await asyncio.sleep_ms(1_000)

async def main():
    """
    Start tasks in parallel
    """
    task = None
    if a.mode == 1 or a.mode == 2:
        task = asyncio.create_task(ap_mode(apiX.publish_event))
    asyncio.create_task(check_modes(task))
    await asyncio.sleep_ms(10_000)
    
def rotary_send():
    while True:
        print("ready to publish event")
        r.add_listener(rotated) 
        asyncio.run(main())
        time.sleep_ms(5000) 


rotary_send()





