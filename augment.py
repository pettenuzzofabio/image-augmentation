#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import random

import cv2
import numpy as np

import constants as const
import transformations.color as color
import transformations.geometric.distort as distort
import transformations.geometric.rotation as rotation
import transformations.labels as labels
import transformations.noise as noise
import transformations.shadow as shadow

function_list = []

def get_n_augmented_images_labels(image, labels_list, n_output_list = const.N_FILES_OUTPUT):
	'''
	Applies the transformations to the input image and returns
	a list of transformed images along with the corresponding labels
	:param image: image to be augmented
	:param labels_list: labels associated to the image
	:param n_output_list: number of images returned as output
	:return matrix of 2 arrays: list of transformed images and list of associated labels
	'''
	images_list = []
	total_labels_list = []
	for _ in range(n_output_list):
		image, labels_list = get_augmented_image_labels(image, labels_list)
		images_list.append(image)
		total_labels_list.append(labels_list)

	return [ images_list, labels_list ] # check if [] can be avoided

def get_augmented_image_labels(image, labels_list):
	if not function_list :
		__init_function_list()

	# TODO: add multithreading
	tmp_function_list = function_list[ : ]
	for _ in range(const.N_TRANSFORMATIONS):
		# Max integer value for Python 2. Integers in Python 3 are unbounded
		const.SEED = np.random.randint(2147483648)
		transformation_function = random.choice(tmp_function_list)
		transformed_image = transformation_function(image)
		cv2.imwrite("C:\\Users\\pette\\Documents\\image-augmentator\\transformed_image.png", transformed_image)
		transformed_labels = labels.get_transformed_labels(transformation_function, image.shape, labels_list)
		tmp_function_list.remove(transformation_function)

	return transformed_image, transformed_labels

def write_output_files(full_name, images_labels, output_path):
	name, extension = os.path.splitext(full_name)
	prefix = output_path + "\\" + name

	i = 0
	for image, labels_list in images_labels:
		output_name = prefix + str(i) + extension
		try:
			cv2.imwrite(output_name, image)
			# todo: write labels
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
