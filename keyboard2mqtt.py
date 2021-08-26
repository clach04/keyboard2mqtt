#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import json
import logging
import os
import sys

import paho.mqtt.client as paho
import paho.mqtt.publish as publish


version_tuple = (0, 0, 1)
version = version_string = __version__ = '%d.%d.%d' % version_tuple
__author__ = 'clach04'

log = logging.getLogger(__name__)
logging.basicConfig()  # TODO include function name/line numbers in log
log.setLevel(level=logging.DEBUG)  # Debug hack!

log.info('Python %s on %s', sys.version, sys.platform)


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

    # initial payload trivial, just the keypresses with terminator (newline) removed
    # no announcements, no timestamps, so client details
    mqqt_message = 'payload goes here'
    result =  publish.single(config['mqtt_topic'], mqqt_message, hostname=config['mqtt_broker'], port=config['mqtt_port'])
    log.debug('mqqt publish result %r', result)  # returns None on success, on failure exception

    return 0


if __name__ == "__main__":
    sys.exit(main())
