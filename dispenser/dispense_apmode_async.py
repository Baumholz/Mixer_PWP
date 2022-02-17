#followed guide from https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/
#this file in boot.py
#get the micropython socket api
try:
  import usocket as socket
except:
  import socket

#for connecting to the LED pin
from machine import Pin
#to connect to the wifi
import network

#this turns off the esp debug messages, not necessary!
import esp
esp.osdebug(None)

#save flash memory by collecting unused memory
import gc
gc.collect()

import ure
import uasyncio as asyncio
from micropython_switchbot import run_ble

        
#function to create the webpage
def web_page(length):
  html = """<html><head><title>Dispenser AP Mode</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}
  .button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}
  .button3{background-image: linear-gradient(#e7bd3b, #4286f4); }</style></head><body> <h1>Dispenser AP Mode</h1> 
  <h2>Dispense Configuration</h2>
  <form enctype="multipart/form-data" method="get">
    <label>Dispense length in s</label><br/>
    <input type="number" id="length" name="length" step="any" value='""" + str(length) + """'><br><br>
    <input class="button" type="submit">
  </form>
  </body></html>"""
  return html

#create the webserver from the esp that the client connects to
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind the web server to a port, 80 for default
s.bind(('', 80))
#accept a maximum of 5 connections
s.listen(5)
s.setblocking(False)
async def ap_mode(callback):
    print("in ap mode")
    length = 0
    while True:
      try:
          print("on")
          conn, addr = s.accept()
          print('Got a connection from %s' % str(addr))
          request = conn.recv(1024)
          request = str(request)
          print('Content = %s' % request)
          request = str(request)
          length = ure.search(r"/?length=(.*?) HTTP", request)
          if length != None:
            length = length.group(1)
            on = b'\x57\x01\x01'
            try:
                asyncio.run(run_ble(on,float(length)*1000, callback))
            except:
                print("no number, try again")
          response = web_page(length)
          conn.send('HTTP/1.1 200 OK\n')
          conn.send('Content-Type: text/html\n')
          conn.send('Connection: close\n\n')
          conn.sendall(response)
          conn.close()
      except OSError:
          """If socket not set"""
          await asyncio.sleep_ms(500)

    



