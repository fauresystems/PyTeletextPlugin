# Teletext plugin for Room
***Send MQTT messages to Raspberry connected props running TeletextProps.***

***Teletext plugin*** is a pure python applet written as a **Room** plugin, but it still can be run as a standalone Escape Room application.

![](screenshot.png)

You will find <a href="https://xcape.io/public/documentation/en/room/AddapluginPyTeletextPlugin.html" target="_blank">detailed installation help in the Room manual</a>.


## Installation
Download `PyTeletextPlugin-master.zip` from this GitHub repository and unflate it in Room/Plugins directory in **Room** software installation folder.

Edit `definitions.ini` to set MQTT topics for your Escape Room:
```python
[mqtt]
; mqtt-sub-* topics are subscribed by MqttApplet
mqtt-pub-teletext = Room/My room/Props/Raspberry Teletext/inbox
mqtt-sub-teletext = Room/My room/Props/Raspberry Teletext/outbox
mqtt-sub-room-language = Room/Demoniak/Control/game:scenario
mqtt-sub-display = Room/My room/Props/Raspberry Teletext/display
``` 


## Usage
Start `teletext.py` script in `rc.local`:

```bash
usage: python3 teletext.py [-h] [-s SERVER] [-p PORT] [-d] [-l LOGGER]

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        change MQTT server host
  -p PORT, --port PORT  change MQTT server port
  -d, --debug           set DEBUG log level
  -l LOGGER, --logger LOGGER
                        use logging config file
```

To switch MQTT broker, kill the program and start again with new arguments.


## TeletextApplet
*Teletext plugin* is a PyQt5 GUI application extending *MqttApplet*.

*Teletext plugin* expects to monitor a Raspberry connected props running the [Teletext Props](https://github.com/fauresystems/TeletextProps) .

You can use *Teletext plugin* as a template  to create your own **Room** plugin.

About `create-teletextplugin-no-venv-tgz.bat`:
* install <a href="https://www.7-zip.org/" target="_blank">7-Zip</a> on your Windows desktop
* run `create-teletextplugin-no-venv-tgz.bat` to archive your work without *python venv*
* run `create-teletextplugin-tgz.bat` to archive your work with *venv*

#### IDE for hacking `TeletextApplet.py`:
> You can open a PyCharm Professional project to hack the code remotely, thanks to `.idea` folder. Or if you prefer, you can hack the code with <a href="https://eric-ide.python-projects.org/" target="_blank">Eric6 IDE</a>. 


## MqttApplet base class
*TeletextApplet* extends *MqttApplet*, the base class for Room Control plugins.
 
*MqttApplet* is a PyQt5 GUI application with paho MQTT.

#### Notes about MQTT QoS:
>*Python script hangs* have been reported when `paho-mqtt` is running asynchronously with QoS 2 on a network with significant packet loss (particularly Wifi networks).

We have choosen MQTT QoS 1 as default (see *constants.py*).

MQTT topics are defined in *definitions.ini*.

You might not modify `MqttApplet.py` file.


## Author

**Marie FAURE** (Oct 9th, 2019)
* company: FAURE SYSTEMS SAS
* mail: *dev at faure dot systems*
* github: <a href="https://github.com/fauresystems?tab=repositories" target="_blank">fauresystems</a>
* web: <a href="https://faure.systems/" target="_blank">Faure Systems</a>