#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PluginSettingsDialog.py
MIT License (c) Faure Systems <dev at faure dot systems>

Dialog to configure clue language and kick efects.
"""

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QSettings, QSize
from PyQt5.QtWidgets import (QDialog, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QRadioButton, QLabel, QPushButton, QSizePolicy, QGroupBox)
from PyQt5.QtGui import QIcon


class PluginSettingsDialog(QDialog):
    languageChanged = pyqtSignal()
    messageToTeletext = pyqtSignal(str)

    # __________________________________________________________________
    def __init__(self, logger):

        super(PluginSettingsDialog, self).__init__()

        self._logger = logger

        self.setAttribute(Qt.WA_AlwaysStackOnTop)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle(self.tr("Settings"))
        self.setWindowIcon(QIcon('./settings.svg'))
        self.buildUi()

    # __________________________________________________________________
    def buildUi(self):

        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        lang_box = QGroupBox(self.tr("Clues language"))
        lang_box_layout = QVBoxLayout(lang_box)
        main_layout.addWidget(lang_box)

        eng_button = QRadioButton(self.tr("English"))
        fre_button = QRadioButton(self.tr("French"))
        lang_box_layout.addWidget(eng_button)
        lang_box_layout.addWidget(fre_button)

        settings = QSettings("settings.ini", QSettings.IniFormat);
        settings.setIniCodec("UTF-8");
        settings.beginGroup("Cues")
        lang = settings.value("language", "fr")
        settings.endGroup()

        if lang == "fr":
            fre_button.setChecked(True)
        else:
            eng_button.setChecked(True)

        close_button = QPushButton(self.tr("Close"))
        close_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        eng_button.pressed.connect(self.setCuesInEnglish)
        fre_button.pressed.connect(self.setCuesInFrench)
        close_button.pressed.connect(self.accept)

    # __________________________________________________________________
    @pyqtSlot()
    def effectGarland(self):

        self.messageToTeletext.emit("effet:guirlande")
        self.close()

    # __________________________________________________________________
    @pyqtSlot()
    def setCuesInEnglish(self):

        self._logger.info(self.tr("Settings : set cues in English"))

        settings = QSettings("settings.ini", QSettings.IniFormat);
        settings.setIniCodec("UTF-8");
        settings.beginGroup("Cues")
        settings.setValue("language", "en")
        settings.endGroup()
        settings.sync()

        self.languageChanged.emit()

    # __________________________________________________________________
    @pyqtSlot()
    def setCuesInFrench(self):

        self._logger.info(self.tr("Settings : set cues in French"))

        settings = QSettings("settings.ini", QSettings.IniFormat);
        settings.setIniCodec("UTF-8");
        settings.beginGroup("Cues")
        settings.setValue("language", "fr")
        settings.endGroup()
        settings.sync()

        self.languageChanged.emit()
