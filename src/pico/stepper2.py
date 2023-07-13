from machine import Pin, ADC
import utime
import time

step = Pin(17)
direction = Pin(16, Pin.OUT)

# To control speed just modify the amount/value of nop[dely amount 0-31].
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def move():
    wrap_target()
    set(pins, 1)   [31]
    nop()          [31]
    nop()          [31]
    set(pins, 0)   [31]
    nop()          [31]
    nop()          [31]
    wrap()

"""Instantiate a state machine with the move
program, at 100000Hz, with set base to step pin."""
motor = rp2.StateMachine(0, move, freq=10000, set_base=step)

# Set direction
direction.value(1)

# Start your motor!
motor.active(1)

# wait 5 seconds
time.sleep(5)

# Stop your motor!
motor.active(0)