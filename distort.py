#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from random import randint
import cv2
import math
import numpy as np
from skimage import img_as_ubyte
from skimage import transform as tf

# those should be performed as last transformations,
# after we have precisely detect our landmark in the original image
# since they will significantly alter the image inner propritions

def get_random_shear(image, max_factor = 0.1):
	factor = __get_random_shear_direction(max_factor)
	return shear_image(image, factor)

def __get_random_shear_direction(max_factor):
	max_factor = abs(max_factor)
	return np.random.uniform(-1 * max_factor, max_factor)

def shear_image(image, factor):
	_, w = image.shape[ : 2]
	afine_tf = tf.AffineTransform(shear = factor)
	modified = tf.warp(image, inverse_map = afine_tf, preserve_range=True).astype(np.uint8)
	crop_factor = 0.7

	if (__get_shear_direction(factor)):
		return modified[ :, int(factor * w * crop_factor) : ]
	else:
		return modified[ :, : w-int(-1 * factor * w * crop_factor) ]

def __get_shear_direction(factor):
	return factor > 0

def get_random_skew(image, max_factor=0.1):
	max_factor = abs(max_factor)
	factor = np.random.uniform(-1 * max_factor, max_factor)
	return skew_image(image, factor)

def skew_image(image, factor):
	factor = abs(factor) * -1
	h, w = image.shape[ : 2]
	points1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])

	direction = np.random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
	if (direction == 'UP'):
		points2 = np.float32([[0, 0], [w, 0], [int(w * factor), h], [w - int(w * factor), h]])
	elif (direction == 'LEFT'):
		points2 = np.float32([[0, 0], [w, int(h * factor)], [0, h], [w, int(h - h * factor)]])
	elif (direction == 'RIGHT'):
		points2 = np.float32([[0, int(h * factor)], [w, 0], [0, int(h - h * factor)], [w, h]])
	else:
		points2 = np.float32([[int(w * factor), 0], [w - int(w * factor), 0], [0, h], [w, h]])

	transform_matrix = cv2.getPerspectiveTransform(points1, points2)
	return cv2.warpPerspective(image, transform_matrix, (w, h))

def get_random_warp(image, max_factor = 50, min_factor = 14):
	factor = randint(min_factor, max_factor)
	return warp_image(image, factor)

def warp_image(image, factor):
	h, w = image.shape[ : 2]
	factor = __normalize_factor(factor, h, w)
	x_center, y_center = __get_random_warp_center(factor, h, w)
	wave_length = factor * 36 * randint(1, 4)
	warp_direction = np.random.choice(['X', 'Y', 'X_AND_Y'])
	image_output = np.zeros(image.shape, dtype = image.dtype)

	for y in range(h):
	    for x in range(w):
			distance_from_center = __get_manhattan_distance(x, y, x_center, y_center)
			wave_intensity = __get_wave_intensity(distance_from_center, factor)

			if (wave_intensity > 0):
				offset_x = __get_offset(y, wave_intensity, wave_length)
				offset_y = __get_offset(x, wave_intensity, wave_length)
				if (warp_direction == 'X'):
					image_output[y, x] = image[y, (x + offset_x) % w]
				elif (warp_direction == 'Y'):
					image_output[y, x] = image[(y + offset_y) % h, x]
				else:
					image_output[y, x] = image[(y + offset_y) % h, (x + offset_x) % w]
			else:
				image_output[y, x] = image[y, x]
	return image_output

def __get_manhattan_distance(x, y, x_center, y_center):
	return abs(x - x_center) + abs(y - y_center)

def __get_random_warp_center(factor, rows, cols):
	max_warp_length = factor ** 2
	x_center = randint(max_warp_length, cols - max_warp_length)
	y_center = randint(max_warp_length, rows - max_warp_length)
	return x_center, y_center

def __get_offset(index, wave_intensity, wave_length):
	return int(wave_intensity * math.sin(2 * 3.14 * index / wave_length))

def __normalize_factor(factor, rows, cols):
	while (factor ** 2) * 2 > rows or (factor ** 2) * 2 > cols:
		factor = int(factor / 2)
	return factor

def __get_wave_intensity(distance, factor):
	for i in range(1, factor):
		if (distance < factor * i):
			return factor - i
	return 0