import time
import math
from rotary_irq_esp import RotaryIRQ
import wot_client.api as apiX
import sys
from dispense_apmode import ap_mode
from micropython_switchbot import run_on_api

sys.path.reverse()
apiX.init()
class Action:
    def __init__(self, mode):
        self.set_mode(mode)
        
    def set_mode(self, new_mode):
        self.mode = new_mode
        print("mode: ", self.mode)
        apiX.set_access_mode(new_mode) 

    def run_dispenser(self, duration):
        if self.mode == 1:
            #create ap and control
            ap_mode(apiX.publish_event)
        elif self.mode == 2:
            #create ap and control
            ap_mode(apiX.publish_event)
        elif self.mode == 3:
            #internet
            print("in 3")
            #run_on_api(duration, apiX.publish_event)
        
default_mode = 3
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


apiX.set_access_mode(default_mode)
def example_on_action_handler(topic, msg):
    print('I am the example on_action_handler!', topic, msg)
    # set msg to duration not mode!!! 
    run_on_api(int(msg), apiX.publish_event)

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
            apiX.publish_event("mode",str(val_new))
            a.set_mode(val_new)
            print(val_new)
            print(val_old)
            if val_old == 1 or val_old==2:
                print("going into the ap mode")
                ap_mode(apiX.publish_event)
            #TODO: add the code to switch the mode and run the different functions
        time.sleep_ms(5000)
rotary_send()



