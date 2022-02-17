import machine, neopixel
def init_lights():
    n = 12
    p = 25 

    np = neopixel.NeoPixel(machine.Pin(p), n)
    np[0] = (255, 0, 0)
    np[3] = (125, 204, 223)
    np[7] = (120, 153, 23)
    np[10] = (255, 0, 153) 
    np.write() 

    


