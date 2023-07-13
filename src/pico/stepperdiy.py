from machine import Pin
import utime
 

step_pin = 17  # GPIO number where step pin is connected
dir_pin = 16   # GPIO number where dir pin is connected

# Step motor
for i in range(0, 50):
    step = Pin(step_pin, Pin.OUT)
    step.value(1)
    utime.sleep(0.1)
    step.value(0)
    utime.sleep(0.1)