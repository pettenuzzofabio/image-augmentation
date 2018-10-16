#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from random import randint

import constants
import noise
import numpy as np
import shadow_polygon as polygon
import shadow_single as single


def add_n_random_shadows(image, n_shadow  = 4, blur_scale = 1.0):
	intensity = np.random.uniform(constants.MIN_SHADOW, constants.MAX_SHADOW)
	return add_n_shadows(image, n_shadow, intensity, blur_scale)

def add_n_shadows(image, n_shadow = 4, intensity = 0.5, blur_scale = 1.0):
	for i in range(n_shadow ):
		blur_width = noise.get_blur_given_intensity(intensity, blur_scale)

		choice = np.random.uniform(0, 4)
		if choice < 1:
			image = polygon.add_n_triangles_shadow(image, intensity, blur_width)
		elif choice < 2:
			image = polygon.add_n_triangles_light(image, intensity, blur_width)
		elif choice < 3:
			image = single.add_single_light(image, intensity, blur_width)
		else:
			image = single.add_single_shadow(image, intensity, blur_width)

	return image