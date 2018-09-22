#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import errno
import math
import os
import random

import colors
import colors
import constants
import cv2
import distort
import noise
import numpy as np
import rotation
import shadow
from skimage import img_as_ubyte
from skimage import transform as tf


functions_list = []

def get_n_augmented_images(image, n_transformations):
	images_list = []
	for i in range(0, n_transformations, 1):
		images_list.append(get_augmented_image(image))
	return images_list

def get_augmented_image(image):
	if not functions_list :
		__init_functions_list()

	for function in functions_list:
		if (np.random.uniform() <= constants.PROBABILITY_TRANSFORMATION_GETS_APPLIED):
			image = function(image)
	return image

def write_images(full_name, images_list, output_path):
	name, extension = os.path.splitext(full_name)
	prefix = output_path + "\\" + name

	i = 0
	for image in images_list:
		output_name = prefix + str(i) + extension
		try:
			cv2.imwrite(output_name, image)
		except:
			try:
				os.makedirs(output_path)
				cv2.imwrite(output_name, image)
			except:
				raise
		i += 1

def __init_functions_list():
	__append_function_n_times(noise.add_random_saltpepper_noise, constants.MaxTransformations.SALT_PEPPER_NOISE)
	__append_function_n_times(noise.get_random_speckle_noise, 	 constants.MaxTransformations.SPECKLE_NOISE)
	__append_function_n_times(noise.add_random_gauss_noise, 	 constants.MaxTransformations.GAUSS_NOISE)
	__append_function_n_times(noise.add_random_blur, 			 constants.MaxTransformations.BLUR)
	__append_function_n_times(shadow.add_n_random_shadows, 		 constants.MaxTransformations.SHADOW)
	__append_function_n_times(colors.get_enhanced_image, 		 constants.MaxTransformations.ENHANCEMENTS)
	__append_function_n_times(colors.random_color_shade, 		 constants.MaxTransformations.SHADE_COLORS)
	__append_function_n_times(distort.get_random_shear, 		 constants.MaxTransformations.SHEAR)
	__append_function_n_times(distort.get_random_skew, 			 constants.MaxTransformations.SKEW)
	__append_function_n_times(distort.get_random_warp, 			 constants.MaxTransformations.WARP)
	__append_function_n_times(rotation.get_random_rotation,		 constants.MaxTransformations.ROTATION)

def __append_function_n_times(function, n):
	for i in range(0, n):
		functions_list.append(function)