# Initialize SPI communication
import RPi.GPIO as GPIO
import spidev
from time import sleep
bus=0
device=0
spi = spidev.SpiDev()
spi.open(bus, device)
spi.xfer2([(0x0A << 1) & 0x7E, 0x80])
sleep(30)
spi.close()