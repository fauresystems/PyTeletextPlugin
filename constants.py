#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
constants.py

Contains all the Room Control applet constants.
"""

# __________________________________________________________________
# Required by MqttApplet
APPNAME = "Room 2.0"  # the Room Control application
APPLET = "TeletextPlugin"

MQTT_DEFAULT_HOST = 'localhost'
MQTT_DEFAULT_PORT = 1883
MQTT_DEFAULT_QoS = 1

TRANSLATOR_FR = "Teletext.fr_FR.qm"  # mandatory, can be ""

# __________________________________________________________________
# Required by TeletextApplet
APPDISPLAYNAME = "Room 2.0"  # the Room Control application
