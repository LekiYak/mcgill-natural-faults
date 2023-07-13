from machine import Pin
import utime
 
class Stepper:
    def __init__(self, step_pin, dir_pin):
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        self.position = 0
 
    def set_speed(self, speed):
        self.delay = 1 / abs(speed)  # delay in seconds
 
    def set_direction(self, direction):
        self.dir_pin.value(direction)
 
    def move_to(self, position):
        self.set_direction(1 if position > self.position else 0)
        while self.position != position:
            self.step_pin.value(1)
            utime.sleep(self.delay + 2.5) # 1.5
            self.step_pin.value(0)
            self.position += 1 if position > self.position else -1
            print(self.position)
 
# Define the pins
step_pin = 17  # GPIO number where step pin is connected
dir_pin = 16   # GPIO number where dir pin is connected
 
# Initialize stepper
stepper = Stepper(step_pin, dir_pin)
 
def loop():
    # Move forward 2 revolutions (400 steps) at 200 steps/sec
    stepper.set_speed(10)
    stepper.move_to(500)
    utime.sleep(1)

    # Move backward 1 revolution (200 steps) at 600 steps/sec
    # stepper.set_speed(600)
    # stepper.move_to(200)
    # utime.sleep(1)

    # # Move forward 3 revolutions (600 steps) at 400 steps/sec
    # stepper.set_speed(400)
    # stepper.move_to(600)
    # utime.sleep(3)
 
if __name__ == '__main__':
    loop()