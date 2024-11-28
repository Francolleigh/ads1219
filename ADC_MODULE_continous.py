#Porpuse of this script is to get developers and new developers get started with i2c hardware
#this module is a relatively high speed 24bit low noise adc 
#this scripts reads a single ended chanel 0 in a continous mode
#note that there is no license required for the script therefore no ------
#use at you own riscs
#Developed by Francolleigh Technologies
#11/28/2024

#this script assums that you are working with a respbery pi5 
#this script assums that all required libraries such smbus have been installed
#if these libraries have not been installed use "apt" or "pip" to install them


import smbus
from gpiozero import Button
from signal import pause
from gpiozero import LED
import time
import RPi.GPIO as GPIO
import io
from gpiozero import LED




# I2C setup
bus = smbus.SMBus(1)
ADS1219_I2C_ADDRESS = 0x41



# Pin number where the output will be set
GPIO_PIN = 4

# Setup the LED (output) on GPIO4
led = LED(GPIO_PIN)

# Write 0 (LOW) to GPIO pin by turning the LED off
led.on()  # Turns the GPIO pin to LOW

def set_drdy_low():
	led.on()  # Turns the GPIO pin to LOW
	#print(f"DRDY has been set to low")

# Keep the pin LOW for a while (optional)
	time.sleep(.002)


def read_adc_data():
    """Reads and processes data from the ADS1219.""" 
    try:
        # Start conversion command
       
        set_drdy_low()
        bus.write_byte(ADS1219_I2C_ADDRESS, 0x08)
        #print("Started conversion with 0x40.")
        
        # Read 3 bytes of data
        data = bus.read_i2c_block_data(ADS1219_I2C_ADDRESS, 0x10, 3)
        #print("Finished reading data from 0x40.")

        # Combine the data into a 24-bit signed result
        result = (data[0] << 16) | (data[1] << 8) | data[2]
        #print("Finished packing data into 24 bits.")

        # Handle sign extension for 24-bit value
        if result & 0x800000:  # Check if the sign bit is set
            result -= 1 << 24
        voltes = ((result / 0x7fffff) * 2.048)- 0.018

        print(f"Voltage={voltes:.3f} V")
        
    except OSError as e:
        print(f"I2C communication error: {e}")

while True:
    read_adc_data()
    time.sleep(0.5) 

