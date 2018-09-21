#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from enum import Enum
import random

### CONSTANTS MEANT TO BE EDITED ###

N_FILES_OUTPUT                      = 10
IMAGE_EXTENSIONS                    = [".jpg", ".jpeg", ".png"]
FILES_INPUT_PATH                    = "./input/"
FILES_OUTPUT_PATH                   = "./output/"
# Probability that each transformation
PROBABILITY_TRANSFORMATION_GETS_APPLIED  = 1.0

class CounterMaxTransformations:
    SALT_PEPPER_NOISE   = 0
    SPECKLE_NOISE       = 0
    GAUSS_NOISE         = 0
    BLUR                = 0
    SHADOW              = 0
    ENHANCEMENTS        = 0
    SHADE_COLORS        = 0

    # The following transformations
    # alter pixel coordinates
    SHEAR               = 1
    SKEW                = 0
    WARP                = 0
    ROTATION            = 0

MIN_BLUR 				= 1
MAX_BLUR 				= 3
MIN_GAUSS_NOISE 		= 1
MAX_GAUSS_NOISE 		= 100
MIN_SALT_PEPPER_NOISE 	= 0.0001
MAX_SALTPEPPER_NOISE 	= 0.001
MIN_SPECKLE_NOISE 		= 0.01
MAX_SPECKLE_NOISE 		= 0.3
# By default s&p and speckle noise
# is followed by blurring
ADD_BLUR_AFTER_SP_AND_SPECKLE_NOISE = True

### PAY ATTENTION BEFORE EDITING THE FOLLOWING CONSTANTS ###

BLACK       = 0
LIGHT_BLACK = 50
DARK_GRAY   = 100
GRAY        = 150
LIGHT_GRAY  = 200
DARK_WHITE  = 250
WHITE       = 255


class Enhancement(Enum):
    brightness  = 0
    contrast    = 1
    sharpness   = 2

    @staticmethod
    def get_random():
        return random.choice(list(Enhancement))


class Channels(Enum):
    bgr = 0
    hsv = 1
    hls = 2

    @staticmethod
    def get_random():
        return random.choice(list(Channels))