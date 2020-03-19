#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PluginApplet.py
MIT License (c) Marie Faure <dev at faure dot systems>

PluginApplet application extends MqttApplet.
"""

from constants import *
from MqttApplet import MqttApplet
from PluginDialog import PluginDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class PluginApplet(MqttApplet):
    teletextDisplayMessageReceived = pyqtSignal(str)
    propsMessageReceived = pyqtSignal(str)
    languageReceived = pyqtSignal(str)

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):
        super().__init__(argv, client, debugging_mqtt)

        self.setApplicationDisplayName(APPDISPLAYNAME)

        # on_message per topic callbacks
        try:
            mqtt_sub_teletext = self._definitions['mqtt-sub-props']
            self._mqttClient.message_callback_add(mqtt_sub_teletext, self.mqttOnMessageFromProps)
        except Exception as e:
            self._logger.error(self.tr("Teletext sub topic definition is missing"))
            self._logger.debug(e)

        try:
            mqtt_sub_language = self._definitions['mqtt-sub-control-scenario']
            self._mqttClient.message_callback_add(mqtt_sub_language, self.mqttOnLanguage)
        except Exception as e:
            self._logger.error(self.tr("Language sub topic definition is missing"))
            self._logger.debug(e)

        try:
            mqtt_sub_display = self._definitions['mqtt-sub-display']
            self._mqttClient.message_callback_add(mqtt_sub_display, self.mqttOnDisplayMessageFromTeletextProps)
        except Exception as e:
            self._logger.error(self.tr("Display sub topic definition is missing"))
            self._logger.debug(e)

        # on_message default callback
        self._mqttClient.on_message = self.mqttOnMessage

        self._PluginDialog = PluginDialog(self.tr("Teletext"), './teletext-on.svg', self._logger)
        self._PluginDialog.aboutToClose.connect(self.exitOnClose)
        self.teletextDisplayMessageReceived.connect(self._PluginDialog.teletextDisplayMessage)
        self.propsMessageReceived.connect(self._PluginDialog.teletextMessage)
        self.languageReceived.connect(self._PluginDialog.setLanguage)
        self._PluginDialog.messageToTeletext.connect(self.publishMessageToTeletext)
        self._PluginDialog.show()

    # __________________________________________________________________
    @pyqtSlot()
    def exitOnClose(self):
        self._logger.info(self.tr("exitOnClose "))
        self.quit()

    # __________________________________________________________________
    def mqttOnDisplayMessageFromTeletextProps(self, client, userdata, msg):
        message = None
        try:
            message = msg.payload.decode(encoding="utf-8", errors="strict")
        except:
            pass

        if message:
            self._logger.info(
                self.tr("Display message received from Teletext props : '") + message + self.tr("' in ") + msg.topic)
            self.teletextDisplayMessageReceived.emit(message)
        else:
            self._logger.warning(
                "{0} {1}".format(self.tr("Decoding MQTT display message from Teletext props failed on"), msg.topic))

    # __________________________________________________________________
    def mqttOnLanguage(self, client, userdata, msg):
        message = None
        try:
            message = msg.payload.decode(encoding="utf-8", errors="strict")
        except:
            pass

        if message:
            self._logger.info(self.tr("Message (language) received : '") + message + self.tr("' in ") + msg.topic)
            if message == "anglais":
                self.languageReceived.emit("en")
            elif message in ["français", "enfants"]:
                self.languageReceived.emit("fr")
            else:
                self._logger.warning(
                    "{0} {1}".format(self.tr("MQTT message (language) ignored (not supported) :"), message))
        else:
            self._logger.warning("{0} {1}".format(self.tr("MQTT message (language) decoding failed on"), msg.topic))

    # __________________________________________________________________
    def mqttOnMessage(self, client, userdata, msg):
        message = None
        try:
            message = msg.payload.decode(encoding="utf-8", errors="strict")
        except:
            pass

        if message:
            self._logger.info(self.tr("Message received : '") + message + self.tr("' in ") + msg.topic)
        ##self.messageReceived.emit(msg.topic, message)
        else:
            self._logger.warning("{0} {1}".format(self.tr("MQTT message decoding failed on"), msg.topic))

    # __________________________________________________________________
    def mqttOnMessageFromProps(self, client, userdata, msg):
        message = None
        try:
            message = msg.payload.decode(encoding="utf-8", errors="strict")
        except:
            pass

        if message:
            self._logger.info(
                self.tr("Message received from Teletext props : '") + message + self.tr("' in ") + msg.topic)
            self.propsMessageReceived.emit(message)
        else:
            self._logger.warning(
                "{0} {1}".format(self.tr("Decoding MQTT message from Teletext props failed on"), msg.topic))

    # __________________________________________________________________
    @pyqtSlot(str)
    def publishMessageToTeletext(self, message):
        if self._definitions['mqtt-pub-props']:
            self.publishMessage(self._definitions['mqtt-pub-props'], message)
        else:
            self._logger.warning(
                "{0} : {1}".format(self.tr("TeletextPlugin inbox is not defined, message ignored"), message))
