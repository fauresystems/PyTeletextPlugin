#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clue.py
MIT License (c) Faure Systems <dev at faure dot systems>

Class for a clue.
"""


class Clue:

    # __________________________________________________________________
    def __init__(self, title, fr, en):
        super().__init__()

        self.title = title
        self.fr = fr
        self.en = en
