#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import errno
import math
import os
import random

import constants as const
import cv2
import numpy as np
import transformations.color as color
import transformations.distort as distort
import transformations.noise as noise
import transformations.rotation as rotation
import transformations.shadow as shadow
from skimage import img_as_ubyte
from skimage import transform as tf

function_list = []

def get_n_augmented_images(image, n_output_list = const.N_FILES_OUTPUT):
	'''
	Applies the transformations to the input image and returns a list of transformed images
	:param image: image to be augmented
	:param n_output_list: number of images returned as output
	:return list of transformed images
	'''
	images_list = []
	for _ in range(n_output_list):
		images_list.append(get_augmented_image(image))

	return images_list

def get_augmented_image(image):
	if not function_list :
		__init_function_list()

	# TODO: add multithreading
	tmp_function_list = function_list[ : ]
	for _ in range(const.N_TRANSFORMATIONS):
		function = random.choice(tmp_function_list)
		image = function(image)
		tmp_function_list.remove(function)

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

def __init_function_list():
	t = const.MaxTransformation
	__append_function_n_times(noise.add_random_saltpepper_noise,	t.SALT_PEPPER_NOISE)
	__append_function_n_times(noise.get_random_speckle_noise,	t.SPECKLE_NOISE)
	__append_function_n_times(noise.add_random_gauss_noise, 	t.GAUSS_NOISE)
	__append_function_n_times(noise.add_random_blur, 		t.BLUR)
	__append_function_n_times(shadow.add_n_random_shadows, 		t.SHADOW)
	__append_function_n_times(color.get_enhanced_image, 		t.ENHANCEMENTS)
	__append_function_n_times(color.random_color_shade, 		t.SHADE_COLOR)
	__append_function_n_times(distort.get_random_shear, 		t.SHEAR)
	__append_function_n_times(distort.get_random_skew, 		t.SKEW)
	__append_function_n_times(distort.get_random_warp, 		t.WARP)
	__append_function_n_times(rotation.get_random_rotation,		t.ROTATION)
	const.N_TRANSFORMATIONS = min(len(function_list),		const.N_TRANSFORMATIONS)

def __append_function_n_times(function, n):
	for _ in range(n):
		function_list.append(function)
