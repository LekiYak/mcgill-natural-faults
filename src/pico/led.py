from machine import Pin
import utime

led = Pin(25, Pin.OUT)

led.value(1)
utime.sleep(0.2)
led.value(0)
utime.sleep(0.1)
led.value(1)
utime.sleep(0.2)
led.value(0)