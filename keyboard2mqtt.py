#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import json
import logging
import os
import sys

import evdev

import paho.mqtt.client as paho
import paho.mqtt.publish as publish


version_tuple = (0, 0, 1)
version = version_string = __version__ = '%d.%d.%d' % version_tuple
__author__ = 'clach04'

log = logging.getLogger(__name__)
logging.basicConfig()  # TODO include function name/line numbers in log
log.setLevel(level=logging.DEBUG)  # Debug hack!

log.info('Python %s on %s', sys.version, sys.platform)

DEFAULT_USB_DEVICE_LIST = [
    (0x16c0, 0x27db), # YARONGTECH USB RFID Card Reader
]
def find_usb_device(usb_search_list=None):
    usb_search_list = usb_search_list or DEFAULT_USB_DEVICE_LIST
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if (device.info.vendor, device.info.product) in usb_search_list:
            return device
    return None


ERROR_CHARACTER = '?'
VALUE_UP = 0
VALUE_DOWN = 1

CHARMAP = {
        evdev.ecodes.KEY_1: ['1', '!'],
        evdev.ecodes.KEY_2: ['2', '@'],
        evdev.ecodes.KEY_3: ['3', '#'],
        evdev.ecodes.KEY_4: ['4', '$'],
        evdev.ecodes.KEY_5: ['5', '%'],
        evdev.ecodes.KEY_6: ['6', '^'],
        evdev.ecodes.KEY_7: ['7', '&'],
        evdev.ecodes.KEY_8: ['8', '*'],
        evdev.ecodes.KEY_9: ['9', '('],
        evdev.ecodes.KEY_0: ['0', ')'],
        evdev.ecodes.KEY_MINUS: ['-', '_'],
        evdev.ecodes.KEY_EQUAL: ['=', '+'],
        evdev.ecodes.KEY_TAB: ['\t', '\t'],
        evdev.ecodes.KEY_Q: ['q', 'Q'],
        evdev.ecodes.KEY_W: ['w', 'W'],
        evdev.ecodes.KEY_E: ['e', 'E'],
        evdev.ecodes.KEY_R: ['r', 'R'],
        evdev.ecodes.KEY_T: ['t', 'T'],
        evdev.ecodes.KEY_Y: ['y', 'Y'],
        evdev.ecodes.KEY_U: ['u', 'U'],
        evdev.ecodes.KEY_I: ['i', 'I'],
        evdev.ecodes.KEY_O: ['o', 'O'],
        evdev.ecodes.KEY_P: ['p', 'P'],
        evdev.ecodes.KEY_LEFTBRACE: ['[', '{'],
        evdev.ecodes.KEY_RIGHTBRACE: [']', '}'],
        evdev.ecodes.KEY_A: ['a', 'A'],
        evdev.ecodes.KEY_S: ['s', 'S'],
        evdev.ecodes.KEY_D: ['d', 'D'],
        evdev.ecodes.KEY_F: ['f', 'F'],
        evdev.ecodes.KEY_G: ['g', 'G'],
        evdev.ecodes.KEY_H: ['h', 'H'],
        evdev.ecodes.KEY_J: ['j', 'J'],
        evdev.ecodes.KEY_K: ['k', 'K'],
        evdev.ecodes.KEY_L: ['l', 'L'],
        evdev.ecodes.KEY_SEMICOLON: [';', ':'],
        evdev.ecodes.KEY_APOSTROPHE: ['\'', '"'],
        evdev.ecodes.KEY_BACKSLASH: ['\\', '|'],
        evdev.ecodes.KEY_Z: ['z', 'Z'],
        evdev.ecodes.KEY_X: ['x', 'X'],
        evdev.ecodes.KEY_C: ['c', 'C'],
        evdev.ecodes.KEY_V: ['v', 'V'],
        evdev.ecodes.KEY_B: ['b', 'B'],
        evdev.ecodes.KEY_N: ['n', 'N'],
        evdev.ecodes.KEY_M: ['m', 'M'],
        evdev.ecodes.KEY_COMMA: [',', '<'],
        evdev.ecodes.KEY_DOT: ['.', '>'],
        evdev.ecodes.KEY_SLASH: ['/', '?'],
        evdev.ecodes.KEY_SPACE: [' ', ' '],
}

def keyboard_reader_evdev(dev):
    barcode_string_output = ''
    # barcode can have a 'shift' character; this switches the character set
    # from the lower to upper case variant for the next character only.
    shift_active = False
    for event in dev.read_loop():

        #print('categorize:', evdev.categorize(event))
        #print('typeof:', type(event.code))
        #print("event.code:", event.code)
        #print("event.type:", event.type)
        #print("event.value:", event.value)
        #print("event:", event)

        if event.code == evdev.ecodes.KEY_ENTER and event.value == VALUE_DOWN:
            #print('KEY_ENTER -> return')
            # all barcodes end with a carriage return
            return barcode_string_output
        elif event.code == evdev.ecodes.KEY_LEFTSHIFT or event.code == evdev.ecodes.KEY_RIGHTSHIFT:
            #print('SHIFT')
            shift_active = event.value == VALUE_DOWN
        elif event.value == VALUE_DOWN:
            ch = CHARMAP.get(event.code, ERROR_CHARACTER)[1 if shift_active else 0]
            #print('ch:', ch)
            # if the charcode isn't recognized, use ?
            barcode_string_output += ch

def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('Python %r on %r' % (sys.version, sys.platform))

    try:
        config_filename = argv[1]
    except IndexError:
        config_filename = os.environ.get('KEYBOARD2MQTT_CONFIG_FILE', 'config.json')
    if os.path.exists(config_filename):
        log.info('Using config file %r', config_filename)
        with open(config_filename, 'rb') as f:  # TODO use codec/encoding
            data = f.read()
            data = data.decode('utf-8')
            config = json.loads(data)
            del(data)
    else:
        log.warning('Missing config file %r, using defaults', config_filename)
        config = {}

    default_config = {
        'debug': False,
        'mqtt_broker': 'localhost',
        'mqtt_port': 1883,
        'mqtt_topic': 'tag_keyboard_reader',
    }
    default_config.update(config)
    config = default_config
    print(json.dumps(config, indent=4))
    if config['debug']:
        log.setLevel(level=logging.DEBUG)
    else:
        log.setLevel(level=logging.INFO)
    log.debug('hello')
    log.info('hello')

    # list all devices
    for path in evdev.list_devices():
        #log.info('device path %r' % path)
        tmp_dev = evdev.InputDevice(path)
        log.info('device path %r %r %r %r %r ' % (path, tmp_dev.info, tmp_dev.path, tmp_dev.name, tmp_dev.phys))

    dev = find_usb_device()  # TODO pick up device id from config file
    log.info('Found device path %r' % dev)

    dev.grab()

    try:
        while True:
            read_string = keyboard_reader_evdev(dev)
            print(read_string)  # TODO mqtt publish (or a callback mechanism rather than mqtt specific)
    except KeyboardInterrupt:
        logging.debug('Keyboard interrupt')
    except Exception as err:
        logging.error(err)
    finally:
        dev.ungrab()

    """
    # initial payload trivial, just the keypresses with terminator (newline) removed
    # no announcements, no timestamps, so client details
    mqqt_message = 'payload goes here'
    result =  publish.single(config['mqtt_topic'], mqqt_message, hostname=config['mqtt_broker'], port=config['mqtt_port'])
    log.debug('mqqt publish result %r', result)  # returns None on success, on failure exception
    """

    return 0


if __name__ == "__main__":
    sys.exit(main())
