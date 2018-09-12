#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from enum import Enum
import random
import time

BLACK		= 0
LIGHT_BLACK	= 50
DARK_GRAY	= 100
GRAY		= 150
LIGHT_GRAY	= 200
DARK_WHITE	= 250
WHITE		= 255

class Enhancement(Enum):
	brightness	= 0
	contrast	= 1
	sharpness	= 2

	@staticmethod
	def get_random_enhancement():
		return random.choice(list(Enhancement))

class Channels(Enum):
	bgr	= 0
	hsv	= 1
	hls	= 2

	@staticmethod
	def get_random():
		return random.choice(list(Channels))
