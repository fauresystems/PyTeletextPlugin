# Teletext plugin for Room 2.0
***Send MQTT messages to Raspberry connected props running TeletextProps.***

*TeletextPlugin* is pure python applet written as Room 2.0 plugin, nevertheless it can be run as standalone Escape Room application.


## MqttApplet base class
*TeletextApplet* extends *MqttApplet*, the base class for Room Control plugins.
 
*MqttApplet* is a PyQt5 GUI application with paho MQTT.

We have choosen MQTT QoS 1 as default (see *constants.py*).

MQTT topics are defined in *definitions.ini*.

You might not modify this file.


## TeletextApplet
*Teletext plugin* is a PyQt5 GUI application extending *MqttApplet*.

*Teletext plugin* expects to monitor a Raspberry connected props running *TeletextProps* which MQTT topics are given in `definitions.ini`:

```python
mqtt-pub-teletext = Room/Demoniak/Props/Raspberry Teletext/inbox
mqtt-sub-teletext = Room/Demoniak/Props/Raspberry Teletext/outbox
mqtt-sub-room-language = Room/Demoniak/Control/game:scenario
mqtt-sub-display = Room/Demoniak/Props/Raspberry Teletext/display
```

Use *Teletext plugin* as a model to create your own Room 2.0 plugin.


## Installation
Download `TeletextPlugin-master.zip` from this GitHub repository and unflate it in Room/Plugins directory in Room 2.0 software installation folder.

Edit `definitions.ini` to set MQTT topics for your Escape Room and `constants.py`:
```python
MQTT_DISPLAY_TOPIC = "Room/Demoniak/Props/Raspberry Teletext/display"
``` 


## Author

**Marie FAURE** (Oct 1th, 2019)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/fauresystems?tab=repositories" target="_blank">fauresystems</a>
* web: <a href="https://www.live-escape.net/" target="_blank">Live Escape Grenoble</a>