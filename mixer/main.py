from time import sleep_ms, sleep
import math
from rotary_irq_esp import RotaryIRQ
from machine import Pin
import json
from wot_client import api
import uasyncio
import ure
import _thread
import utime
import time

def handle_interrupt(pin):
    global val_power_old
    value = pin.value()
    print(value,val_power_old)
    #if val_power_old == value:
    #    return
    if value:
        api.publish_property_value("status", True)
        print("INTERRUPT_TRUE")
    else:
        api.publish_property_value("status", False)
        print("INTERRUPT_FALSE")
    val_power_old = value

OnOff = Pin(26, Pin.IN, Pin.PULL_UP)
OnOff.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=handle_interrupt)

LED_MIX = Pin(25, Pin.OUT)
api.init()
length = 0

LED_ROTTARY_ONE = Pin(33, Pin.OUT)
LED_ROTTARY_TWO = Pin(32, Pin.OUT)
LED_ROTTARY_THREE = Pin(5, Pin.OUT)
LED_ROTTARY_FOUR = Pin(17, Pin.OUT)

print(api.get_device_id())        

def get_rotaryvalue(v):
    return math.floor(v/5)

r = RotaryIRQ(pin_num_clk=16, 
              pin_num_dt=4, 
              min_val=0, 
              max_val=19, 
              reverse=False, 
              range_mode=RotaryIRQ.RANGE_WRAP)
              
val_rot_old = get_rotaryvalue(r.value())
val_power_old = 0

#AP-MODE
def web_page(length):
  
  html = """<html><head><title>Mixer AP Mode</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}
  .button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  }</style></head><body> <h1>Mixer AP Mode</h1> 
  <h2>Mixer Configuration</h2>
  <form enctype="multipart/form-data" method="get">
    <label>Mixing time in secounds</label><br/>
    <input type="number" id="length" name="length" step="any" value='""" + str(length) + """'><br><br>
    <input class="button" type="submit" value="Send">
  </form>
  </body></html>"""

  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind socket with portnumber and IP Address ('' for localhost)
s.bind(('', 80))
s.listen(5)
s.setblocking(False)

def mix(duration):
    LED_MIX.on()
    print("start mix")
    while not OnOff.value():
        time.sleep(0.5)
    api.publish_property_value("status", True)
    timer(duration)
    #_thread.start_new_thread(timer(duration),())
    
    
def timer(duration):
    unexpected = False
    totalduration = duration
    while duration > 0:
        current_time = utime.time()
        while OnOff.value():
            unexpected = True
            tmp = utime.time()
            delta = tmp - current_time
            current_time = tmp
            duration -= delta
            print("U_TIME: " + str(utime.time()))
            print("TIME: " + str(duration))
            time.sleep(0.1)
            if duration <= 0:
                LED_MIX.off()
        if totalduration != duration and unexpected and duration > 0:
            unexpected = False
            print("unexpectedturnoff")
            api.publish_event("unexpectedturnoff", True)
        time.sleep(0.3)
        

def ap(callback):
    while True:
        try:
            print("bin in ap")
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            request = str(request)
            print('Content = %s' % request)
            
            length = ure.search(r"/?length=(.*?) HTTP", request)
            print("legnth:",length)
            if length != None:
                length = length.group(1)
                if length:
                    mix(float(length))
            print(length)
            
            response = web_page(length)
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
        except OSError:
            val = callback()
            if val != 1 or val != 2:
                return    
            time.sleep(0.5)
  
def onoff(val_power_new):
    global val_power_old
    print(val_power_old)
    if val_power_old != val_power_new:
        val_power_old = val_power_new
        if val_power_new == 0:
            api.publish_property_value("status", True)
        else:
            api.publish_property_value("status", False)


def example_on_action_handler(topic, msg):
    print('I am the example on_action_handler!', topic, msg)
    mix(float(msg))
    
    
api.set_on_action_handler(example_on_action_handler)

def turn_leds_on(count):
    if count == 0:
        LED_ROTTARY_ONE.on()
        LED_ROTTARY_TWO.off()
        LED_ROTTARY_THREE.off()
        LED_ROTTARY_FOUR.off()
    elif count == 1:
        LED_ROTTARY_ONE.on()
        LED_ROTTARY_TWO.on()
        LED_ROTTARY_THREE.off()
        LED_ROTTARY_FOUR.off()
    elif count == 2:
        LED_ROTTARY_ONE.on()
        LED_ROTTARY_TWO.on()
        LED_ROTTARY_THREE.on()
        LED_ROTTARY_FOUR.off()
    elif count == 3:
        LED_ROTTARY_ONE.on()
        LED_ROTTARY_TWO.on()
        LED_ROTTARY_THREE.on()
        LED_ROTTARY_FOUR.on()

def rotated():
    global val_rot_old, r
    val_rot_new = get_rotaryvalue(r.value())
    print("VAL_OLD:",val_rot_old)
    print("VAL_NEW:",val_rot_new)
    if val_rot_old != val_rot_new:
        turn_leds_on(val_rot_new)
        val_rot_old = val_rot_new
        print('result =', val_rot_new)
        api.set_access_mode(val_rot_new)
        api.publish_property_value("access_mode",val_rot_new)
    return val_rot_new

LED_ROTTARY_ONE.on()
while True:
    r.add_listener(rotated)
    val_rot_new = get_rotaryvalue(r.value())
    print(val_rot_new)           
    #TODO: add the code to switch the mode and run the different functions        
    if val_rot_new == 1 or val_rot_new == 2:
        ap(rotated)                    
    sleep_ms(1000)