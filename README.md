# LCD_I2C_MQTT
I Could not find a reliable way of displaying information on Sainsmart I2C LCD
from node red.   None of the public available code working.

This code utilize the publishing of lines to display on LCD on MWTT server.
Process running in background monitors the Topic and displays the relevant line.
If Node Red, MMTT server and GPIO is all on the same Raspberry Pi it creates a stable implementation.


This is my first public repo.  Apologies for mistakes.   Library to communicate to MQTT copied from: https://github.com/Tertiush/ParadoxIP150v2  library to communicate to LCD 2004 via I2C grom Sainsmart.    Just configure your display address.

Copy the LCD_I2C_MQTT.service file to /usr/lib/systemd/system   check web for details on auto loading this as service on your pi.       

