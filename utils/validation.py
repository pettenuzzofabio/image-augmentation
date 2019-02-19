#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division

import os
import sys
from os.path import isfile

import constants


def is_valid_file(file_path):
    _name, extension = os.path.splitext(file_path)
    return isfile(file_path) and extension.lower() in constants.IMAGE_EXTENSIONS


def validate_path(path):
    if not os.path.exists(path):
        print("The path " + path + " is not valid.")
        sys.exit()


def normalize_output_path(path):
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except:
            print("The path " + path + " is not a valid directory.")
            sys.exit()

    return os.path.abspath(path)
