# keyboard2mqtt

RFID tag reader and 1D/2D barcode reader to MQTT - or any device that emulates a HID USB Keyboard with newline as the terminator.

In theory any (real) keyboard could be captured, not just a device that emulates a keyboard.

## Getting Started

NOTE needs a working MQTT broker, mosquitto is a good basic one to try:

    sudo apt update
    sudo apt install -y mosquitto mosquitto-clients
    sudo systemctl enable mosquitto.service

If installing/working with a source checkout issue:

    pip install -r requirements.txt

### TODO

  * service (see https://github.com/clach04/pirest#pirest-service)
  * udev permissions/rules (see https://github.com/clach04/pyusb-keyboard-alike/commits/yarongtech)
  * https://json5.org/ support - be easier to support hex digits for USB ids in config file, consider
      * https://github.com/dpranke/pyjson5
      * https://github.com/spyoungtech/json-five -- supports preserving comments (not needed for keyboard2mqtt, but cool :))
  * USB id (list) specified in (json5) config, see above
  * document known working devices


## Credits

  * Based on https://gist.github.com/clach04/9bc0ccc80edd28253af959c45b959490 which is in turn based on
  * https://gist.github.com/michalfapso/1755e8a35bb83720c2559ce8ffde5f85 - easier to maintain code, which is in turn inspired by
  * https://github.com/julzhk/usb_barcode_scanner which is in turn inspired by
  * https://www.piddlerintheroot.com/barcode-scanner/ / https://www.raspberrypi.org/forums/viewtopic.php?f=45&t=55100 from 'brechmos'
