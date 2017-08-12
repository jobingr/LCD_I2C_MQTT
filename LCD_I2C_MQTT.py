#!/usr/bin/python
import ConfigParser
import lib.client as mqtt
import I2C_LCD_driver
from time import *

# Variables if ConfigParser fails
MQTT_IP = "10.0.1.195"
MQTT_port= 1883
Topic_LCD_line1 = LCD1/line1
Topic_LCD_line2 = LCD1/line2
Topic_LCD_line3 = LCD1/line3
Topic_LCD_line4 = LCD1/line4
MQTT_KeepAlive = 300                         #Seconds
MQTT_Poll_Speed = 0.1


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global Control_Partition
    global Control_NewState
    global Control_Action
    global Polling_Enabled

    print("MQTT Message: " + msg.topic+" "+str(msg.payload))
    line = int(msg.topic.split("/")[1][4])
    msg_20chars = (str(msg.payload)+"                       ")[0:19]
    print line, msg_20chars
#    mylcd = I2C_LCD_driver.lcd() 
    mylcd.lcd_display_string(msg_20chars, line)

# mylcd = I2C_LCD_driver.lcd()
# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
# client.connect("10.0.1.195", 1883, 600)
# client.loop_start()

# client.subscribe("LCD1/line1")
# client.subscribe("LCD1/line2")
# client.subscribe("LCD1/line3")
# client.subscribe("LCD1/line4")


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, 
        struct.pack('256s', ifname[:15])
    )[20:24])


if __name__ == '__main__':
    mylcd = I2C_LCD_driver.lcd()
    State_Machine = 0
    while True:
    if State_Machine == 0:  # Try to read config.ini file
        try:
            Config = ConfigParser.ConfigParser()
            Config.read("config.ini")
            MQTT_IP = Config.get("MQTT Broker","IP")
            MQTT_Port = int(Config.get("MQTT Broker","Port"))
            Topic_LCD_line1 = Config.get("MQTT Broker","Topic_LCD_line1")
            Topic_LCD_line2 = Config.get("MQTT Broker","Topic_LCD_line2")
            Topic_LCD_line3 = Config.get("MQTT Broker","Topic_LCD_line3")
            Topic_LCD_line4 = Config.get("MQTT Broker","Topic_LCD_line4")
        except Exception, e:
            print "******************* Error reading config.ini file (will use defaults): " + repr(e)
            State_Machine = 1
    elif State_Machine == 1:   #Connect to MQTT broker
        attempts = 3  # number log attempts
        try:
            print "Attempting connection to MQTT Broker: " + MQTT_IP + ":" + str(MQTT_Port)
            client = mqtt.Client()
            client.on_connect = on_connect
            client.on_message = on_message
            client.connect(MQTT_IP, MQTT_Port, MQTT_KeepAlive)
            client.loop_start()
            client.subscribe("LCD1/line1")
            client.subscribe("LCD1/line2")
            client.subscribe("LCD1/line3")
            client.subscribe("LCD1/line4")
            State_Machine = 2
        except Exception, e:
            print "MQTT connection error (" + str(attempts) + ": " + repr(e)
            time.sleep(Poll_Speed * 5)
            attempts = attempts - 1
    elif State_Machine == 2:   # Main Reporting Loop
        print "."
        sleep(MQTT_Poll_Speed)



