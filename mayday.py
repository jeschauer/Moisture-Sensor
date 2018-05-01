#!/usr/bin/python

# Start by importing the libraries we want to use

import RPi.GPIO as GPIO # This is the GPIO library we need to use the GPIO pins on the Raspberry Pi
import time # This is the time library, we need this so we can use the sleep function
from twilio.rest import Client
import os

# Your Account SID from twilio.com/console
account_sid = os.environ["account_sid"]
# Your Auth Token from twilio.com/console
auth_token  = os.environ["auth_token"]
# From Phone Number
from_phone_nbr = os.environ["from_phone"]
#To Phone number
to_phone_nbr = os.environ["to_phone"]

client = Client(account_sid, auth_token)

last_message = ""

def send_message(body):
    global last_message
    if body != last_message:
        message = client.messages.create(
            to=to_phone_nbr, 
            from_=from_phone_nbr,
            body=body)
        print("SMS SENT")
        last_message = body

send_message("Mayday is up and running.")

# Set our GPIO numbering to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin that we have our digital output from our sensor connected to
channel_high = 17
# Set the GPIO pin to an input
GPIO.setup(channel_high, GPIO.IN)

# This is our callback function, this function will be called every time there is a change on the specified GPIO channel, in this example we are using 17

def callback_high(channel):
    high_input = GPIO.input(channel)
    if high_input == 1:
        print "PANIC"
        send_message("PANIC!")
    else:
        print "Stop Panicking"
        send_message("Stop Panicking")


# This line tells our script to keep an eye on our gpio pin and let us know when the pin goes HIGH or LOW
GPIO.add_event_detect(channel_high, GPIO.BOTH, bouncetime=1)
# This line asigns a function to the GPIO pin so that when the above line tells us there is a change on the pin, run this function
GPIO.add_event_callback(channel_high, callback_high)

# Define the GPIO pin that we have our digital output from our sensor connected to
channel_low = 22
# Set the GPIO pin to an input
GPIO.setup(channel_low, GPIO.IN)

# This is our callback function, this function will be called every time there is a change on the specified GPIO channel, in this example we are using 17

def callback_low(channel):
#    print GPIO.input(channel_low)
    if GPIO.input(channel):
        print "COME HOME"
        send_message("Water Level is High in Sump Pump")
    else:
        print "All is well"
        send_message("Water Level has receeded within tolerance")


# This line tells our script to keep an eye on our gpio pin and let us know when the pin goes HIGH or LOW
GPIO.add_event_detect(channel_low, GPIO.BOTH, bouncetime=1)
# This line asigns a function to the GPIO pin so that when the above line tells us there is a change on the pin, run this function
GPIO.add_event_callback(channel_low, callback_low)




# This is an infinte loop to keep our script running
while True:
	# This line simply tells our script to wait 0.1 of a second, this is so the script doesnt hog all of the CPU
	time.sleep(0.1)

