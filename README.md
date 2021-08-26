# keyboard2mqtt

RFID tag reader and 1D/2D barcode reader to MQTT - or any device that emulates a HID USB Keyboard with newline as the terminator.

## Getting Started

NOTE needs a working MQTT broker, mosquitto is a good basic one to try:

    sudo apt update
    sudo apt install -y mosquitto mosquitto-clients
    sudo systemctl enable mosquitto.service

If installing/working with a source checkout issue:

    pip install -r requirements.txt

TODO service and udev permissions/rules


## Credits

  * Based on https://gist.github.com/clach04/9bc0ccc80edd28253af959c45b959490 which is in turn based on
  * https://gist.github.com/michalfapso/1755e8a35bb83720c2559ce8ffde5f85 - easier to maintain code, which is in turn inspired by
  * https://github.com/julzhk/usb_barcode_scanner which is in turn inspired by
  * https://www.piddlerintheroot.com/barcode-scanner/ / https://www.raspberrypi.org/forums/viewtopic.php?f=45&t=55100 from 'brechmos'
