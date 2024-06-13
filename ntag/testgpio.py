import RPi.GPIO as GPIO
from time import sleep
import sys
pin_rst=7
pin_mode=10
GPIO.setmode(pin_mode)
GPIO.setup(pin_rst, GPIO.OUT)
GPIO.output(pin_rst, 0)
sleep(50)
GPIO.cleanup()
