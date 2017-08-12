#!/usr/bin/python
import lib.client as mqtt
import I2C_LCD_driver
from time import *

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global Control_Partition
    global Control_NewState
    global Control_Action
    global Polling_Enabled
#    global mylcd


    print("MQTT Message: " + msg.topic+" "+str(msg.payload))
    line = int(msg.topic.split("/")[1][4])
    msg_20chars = (str(msg.payload)+"                       ")[0:19]
    print line, msg_20chars
#    mylcd = I2C_LCD_driver.lcd() 
    mylcd.lcd_display_string(msg_20chars, line)

mylcd = I2C_LCD_driver.lcd()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("10.0.1.195", 1883, 600)
client.loop_start()

client.subscribe("LCD1/line1")
client.subscribe("LCD1/line2")
client.subscribe("LCD1/line3")
client.subscribe("LCD1/line4")


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, 
        struct.pack('256s', ifname[:15])
    )[20:24])

#mylcd.lcd_display_string("IP Address:", 1) 

#mylcd.lcd_display_string(get_ip_address('eth0'), 2)

#for i in range(1000):
while True:
    print "."
    sleep(1)

