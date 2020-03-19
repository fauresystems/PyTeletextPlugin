#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PluginDialog.py
MIT License (c) Marie Faure <dev at faure dot systems>

Dialog to control TeletextProps app running on Raspberry.
"""

import os, re

from PluginSettingsDialog import PluginSettingsDialog
from AppletDialog import AppletDialog
from Clue import Clue
from LedWidget import LedWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QSize, QPoint, QSettings
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QFrame,
                             QPlainTextEdit, QPushButton, QSizePolicy, QComboBox, QLabel)


class TvScreenLabel(QLabel):

    # __________________________________________________________________
    def __init__(self, text, hint=None):
        super().__init__(text)

        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.black)
        palette.setColor(QPalette.WindowText, Qt.white)

        self.setAutoFillBackground(True)
        self.setPalette(palette)

        self.setStyleSheet("font-size:20px")

        self.hint = hint

    # __________________________________________________________________
    def heightForWidth(self, w):
        return w * 9 / 16

    # __________________________________________________________________
    def sizeHint(self):
        # return QSize(160, 90)
        # ↕return QSize(320, 180)
        if self.hint:
            hint = self.hint
        else:
            hint = self.size()

        return hint


class PluginDialog(AppletDialog):
    aboutToClose = pyqtSignal()
    messageToTeletext = pyqtSignal(str)
    switchLed = pyqtSignal(str, str)

    # __________________________________________________________________
    def __init__(self, title, icon, logger):
        super().__init__(title, icon, logger)

        # always on top sometimes doesn't work
        self.setAttribute(Qt.WA_AlwaysStackOnTop)
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint | Qt.WindowStaysOnTopHint)

    # __________________________________________________________________
    def _buildUi(self):
        self._clues = {}
        self._selectionComboBox = None
        self.loadLanguage()
        self.loadClueAlbum('clue-album.ini')

        if self._clues:
            self._selectionComboBox = QComboBox()
            self._selectionComboBox.addItem(self.tr("Load clue..."), None)
            for k in self._clues:
                clue = self._clues[k]
                self._selectionComboBox.addItem(clue.title, k)

        self._options = {}
        if os.path.isfile('definitions.ini'):
            definitions = QSettings('definitions.ini', QSettings.IniFormat)
            for group in definitions.childGroups():
                definitions.beginGroup(group)
                if group == "options":
                    for key in definitions.childKeys():
                        self._options[key] = definitions.value(key)
                definitions.endGroup()

        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        self._led = LedWidget(self.tr("Raspberry Teletext"), QSize(40, 20))
        self._led.setRedAsBold(True)
        self._led.setRedAsRed(True)
        self._led.switchOn('gray')

        settings_button = QPushButton()
        settings_button.setIcon(QIcon("./settings.svg"))
        settings_button.setFlat(True)
        settings_button.setToolTip(self.tr("Effects and language"))
        settings_button.setIconSize(QSize(16, 16))
        settings_button.setFixedSize(QSize(24, 24))

        header_layout = QHBoxLayout()
        header_layout.addWidget(self._led)
        header_layout.addWidget(settings_button, Qt.AlignRight)
        main_layout.addLayout(header_layout)

        stop_button = QPushButton()
        stop_button.setIcon(QIcon("./cancel.svg"))
        stop_button.setFlat(True)
        stop_button.setToolTip(self.tr("Clear TV screen"))
        stop_button.setIconSize(QSize(16, 16))
        stop_button.setFixedSize(QSize(24, 24))

        if 'tv-screen-width' in self._options and 'tv-screen-height' in self._options:
            hint = QSize(int(self._options['tv-screen-width']), int(self._options['tv-screen-height']))
            # self._tvScreen = TvScreenLabel(self.tr("<div align=center>Display on TV</div>"), hint)
            self._tvScreen = TvScreenLabel('', hint)
            policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        else:
            # self._tvScreen = TvScreenLabel(self.tr("<div align=center>Display on TV</div>"))
            self._tvScreen = TvScreenLabel('')
            policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy.setHeightForWidth(True)
        self._tvScreen.setSizePolicy(policy)

        display_layout = QHBoxLayout()
        display_layout.addWidget(self._tvScreen)
        display_layout.addStretch()
        display_layout.addWidget(stop_button, Qt.AlignRight)
        main_layout.addLayout(display_layout)

        if self._selectionComboBox:
            main_layout.addWidget(self._selectionComboBox)

        self._editor = QPlainTextEdit()
        self._editor.setFrameShape(QFrame.NoFrame)
        self._editor.setCursorWidth(8)
        main_layout.addWidget(self._editor)

        clear_button = QPushButton(self.tr("Erase draft"))
        clear_button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

        send_button = QPushButton(self.tr("Display on TV"))
        send_button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

        button_layout = QHBoxLayout()
        button_layout.addWidget(send_button)
        button_layout.addWidget(clear_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        settings_button.pressed.connect(self.settings)
        stop_button.pressed.connect(self.stop)
        clear_button.pressed.connect(self.erase)
        send_button.pressed.connect(self.send)
        self.switchLed.connect(self._led.switchOn)
        if self._selectionComboBox:
            self._selectionComboBox.activated.connect(self.selectClue)

        self._editor.setFocusPolicy(Qt.StrongFocus)
        self._editor.setFocus(Qt.OtherFocusReason)

    # __________________________________________________________________
    @pyqtSlot(str)
    def teletextDisplayMessage(self, message):
        if message == "-":
            message = ""
        message = message.replace('\n', '<br>')
        self._tvScreen.setText('<div style="text-align:center">' + message + '</div>')

    # __________________________________________________________________
    @pyqtSlot(str)
    def teletextMessage(self, message):
        if message.startswith("DISCONNECTED"):
            self._tvScreen.setText("")
            self._led.switchOn('yellow')
        else:
            if self._led.color() != 'green':
                self._led.switchOn('green')

    # __________________________________________________________________
    def closeEvent(self, e):
        self.aboutToClose.emit()

    # __________________________________________________________________
    @pyqtSlot()
    def erase(self):
        self._selectionComboBox.setCurrentIndex(0)
        self._editor.clear()

    # __________________________________________________________________
    def loadClueAlbum(self, filename):
        # keys with ',' are read as list and will be joined back
        if os.path.isfile(filename):
            album = QSettings(filename, QSettings.IniFormat)
            album.setIniCodec("UTF-8");
            for group in album.childGroups():
                album.beginGroup(group)
                key = group
                if not 'fr' in album.childKeys():
                    self._logger.warning(
                        "{} [{}] : {}".format(self.tr("Clue"), group, self.tr("ignored because 'fr' is missing")))
                    continue
                if not 'en' in album.childKeys():
                    self._logger.warning(
                        "{} [{}] : {}".format(self.tr("Clue"), group, self.tr("ignored because 'en' is missing")))
                    continue
                try:
                    title = album.value('fr')
                    if '|' in title:
                        fr = re.compile(r'\s*\|\s*').split(title)
                    else:
                        fr = (title, '')
                    text = album.value('en')
                    if '|' in text:
                        en = re.compile(r'\s*\|\s*').split(text)
                    else:
                        en = (text, '')
                    self._clues[key] = Clue(title, fr, en)
                except:
                    self._logger.warning("{} {}".format(self.tr("Failed to load clue : "), key))
                album.endGroup()

    # __________________________________________________________________
    @pyqtSlot()
    def loadLanguage(self):
        settings = QSettings("settings.ini", QSettings.IniFormat);
        settings.setIniCodec("UTF-8");
        settings.beginGroup("Cues")
        self._language = settings.value("language", "fr")
        settings.endGroup()

        if self._selectionComboBox:
            self.selectClue(self._selectionComboBox.currentIndex())

    # __________________________________________________________________
    @pyqtSlot('int')
    def selectClue(self, index):
        try:
            k = self._selectionComboBox.itemData(index)
            if k:
                self._editor.clear()
                clue = self._clues[k]
                if self._language == "fr":
                    text1, text2 = clue.fr
                else:
                    text1, text2 = clue.en
                if text2:
                    self._editor.insertPlainText(text1 + '\n' + text2)
                else:
                    self._editor.insertPlainText(text1)
                self._editor.setFocus(Qt.OtherFocusReason)
        except:
            self._logger.warning("{} {}".format(self.tr("Failed to select clue : index"), index))

    # __________________________________________________________________
    @pyqtSlot()
    def send(self):
        message = self._editor.toPlainText().strip()
        if len(message):
            self.messageToTeletext.emit("afficher:" + message)
        self._selectionComboBox.setCurrentIndex(0)
        self._editor.clear()

    # __________________________________________________________________
    @pyqtSlot(str)
    def setLanguage(self, lang):
        self._logger.info(self.tr("Request received : language in ") + lang)

        if lang in ["en", "fr"]:
            self._language = lang

            settings = QSettings("settings.ini", QSettings.IniFormat);
            settings.setIniCodec("UTF-8");
            settings.beginGroup("Cues")
            settings.setValue("language", self._language)
            settings.endGroup()
            settings.sync()

            if self._selectionComboBox:
                self.selectClue(self._selectionComboBox.currentIndex())

    # __________________________________________________________________
    @pyqtSlot()
    def settings(self):
        dlg = PluginSettingsDialog(self._logger)
        dlg.setModal(True)
        dlg.move(self.pos() + QPoint(20, 20))
        dlg.languageChanged.connect(self.loadLanguage)
        dlg.messageToTeletext.connect(self.messageToTeletext)
        dlg.exec()

    # __________________________________________________________________
    @pyqtSlot()
    def stop(self):
        self.messageToTeletext.emit("effacer")
