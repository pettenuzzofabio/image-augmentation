#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import math

import cv2
import numpy as np
from skimage import transform as tf

import constants as const


def get_random_shear(image):
	factor = __get_random_shear_direction(const.MAX_SHEAR)
	return shear_image(image, factor)


def __get_random_shear_direction(max_factor):
	max_factor = abs(max_factor)
	np.random.seed(const.SEED)
	return np.random.uniform(-1 * max_factor, max_factor)


def shear_image(image, factor):
	# TODO: adjust factor to w/h proportion
	h, w = image.shape[ : 2]
	isImageRotated = False
	if(h > w):
		image = np.rot90(image)
		isImageRotated = True
		w = h

	afine_tf = tf.AffineTransform(shear = factor)
	# cv2.INTER_NEAREST does not interpolate.
	# Thid is essential for label transformation
	modified = tf.warp(image, inverse_map = afine_tf, order = cv2.INTER_NEAREST, preserve_range = True).astype(np.uint8)

	crop_factor = 0.7
	if __get_shear_direction(factor):
		modified = modified[ :, int(factor * w * crop_factor) : ]
	else:
		modified = modified[ :, : w - int(-1 * factor * w * crop_factor) ]

	if isImageRotated:
		return np.rot90(modified, 3)

	return modified


def __get_shear_direction(factor):
	return factor > 0


def get_random_skew(image, max_factor = const.MAX_SKEW):
	max_factor = abs(max_factor)
	np.random.seed(const.SEED)
	factor = np.random.uniform(-1 * max_factor, max_factor)
	return skew_image(image, factor)


def skew_image(image, factor):
	factor = abs(factor) * -1
	h, w = image.shape[ : 2]
	points1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])

	direction = np.random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
	if direction == 'UP':
		points2 = np.float32([
					[0, 0],
				      	[w, 0],
				      	[int(w * factor), h],
				      	[w - int(w * factor), h]
				      	])
	elif direction == 'LEFT':
		points2 = np.float32([
					[0, 0],
				      	[w, int(h * factor)],
				      	[0, h],
				      	[w, int(h - h * factor)]
				      	])
	elif direction == 'RIGHT':
		points2 = np.float32([
					[0, int(h * factor)],
				      	[w, 0],
				      	[0, int(h - h * factor)],
				     	[w, h]
				      	])
	else:
		points2 = np.float32([
					[int(w * factor), 0],
				      	[w - int(w * factor), 0],
				      	[0, h],
				      	[w, h]
				      	])

	transform_matrix = cv2.getPerspectiveTransform(points1, points2)
	# cv2.INTER_NEAREST does not interpolate.
	# Thid is essential for label transformation
	return cv2.warpPerspective(image, transform_matrix, (w, h), flags = cv2.INTER_NEAREST)


def get_random_warp(image, min_factor = const.MIN_WARP, max_factor = const.MAX_WARP):
	np.random.seed(const.SEED)
	factor = np.random.randint(min_factor, max_factor)
	return __warp_image(image, factor)


def __warp_image(image, factor):
	h, w = image.shape[ : 2]
	factor = __normalize_factor(factor, h, w)
	x_center, y_center = __get_random_warp_center(factor, h, w)
	wave_length = factor * 36 * np.random.randint(1, 5)
	warp_direction = np.random.choice(['X', 'Y', 'X_AND_Y'])
	image_output = np.zeros(image.shape, dtype = image.dtype)

	for y in range(h):
		for x in range(w):
			distance_from_center = __get_manhattan_distance(x, y, x_center, y_center)
			wave_intensity = __get_wave_intensity(distance_from_center, factor)

			if wave_intensity > 0:
				offset_x = __get_offset(y, wave_intensity, wave_length)
				offset_y = __get_offset(x, wave_intensity, wave_length)
				if warp_direction == 'X':
					image_output[y, x] = image[
								y,
								__normalize((x + offset_x), w),
								]
				elif warp_direction == 'Y':
					image_output[y, x] = image[
								__normalize((y + offset_y), h),
								x,
								]
				else:
					image_output[y, x] = image[
								__normalize((y + offset_y), h),
								__normalize((x + offset_x), w),
								]

			else:
				image_output[y, x] = image[y, x]

	return image_output

def __normalize(value, max_value, min_value = 0):
	if value < min_value:
		return min_value
	if value > max_value:
		return max_value
	return value


def __get_manhattan_distance(x, y, x_center, y_center):
	return abs(x - x_center) + abs(y - y_center)


def __get_random_warp_center(factor, rows, cols):
	max_warp_length = factor ** 2
	x_center = np.random.randint(max_warp_length, cols - max_warp_length + 1)
	y_center = np.random.randint(max_warp_length, rows - max_warp_length + 1)
	return x_center, y_center


def __get_offset(index, wave_intensity, wave_length):
	return int(wave_intensity * math.sin(2 * 3.14 * index / wave_length))


def __normalize_factor(factor, rows, cols):
	while (factor ** 2) * 2 > rows or (factor ** 2) * 2 > cols:
		factor = int(factor / 2)

	return factor


def __get_wave_intensity(distance, factor):
	for i in range(1, factor):
		if distance < factor * i:
			return factor - i

	return 0
