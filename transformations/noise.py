#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from random import randint

import constants
import cv2
import numpy as np


def add_n_random_blur(image, n = randint(1, 4)):
	for i in range(n):
		choice = np.random.uniform(0,4)
		if (choice < 1):
			image = blur(image, randint(1, 3))
		elif (choice < 2):
			image = get_gauss_noise(image, randint(1, 100))
		elif (choice < 3):
			image = get_saltpepper_noise(image, np.random.uniform(0.0001, 0.001))
		elif (choice < 4):
			image = get_speckle_noise(image, np.random.uniform(0.01, 0.3))
	return image

def add_random_blur(image):
	intensity = randint(constants.MIN_BLUR, constants.MAX_BLUR)
	return blur(image, intensity)

def blur(image, width = 9):
	for i in range(0, width, 1):
		size = 2**i + 1
		image = cv2.blur(image, (size, size))
	return image

def get_blur_given_intensity(intensity, blur_scale):
	intensity = intensity * blur_scale
	if(intensity < 0.4):
		return 5
	elif (intensity < 0.5):
		return 6
	return 7

def add_random_gauss_noise(image):
	intensity = randint(constants.MIN_GAUSS_NOISE, constants.MAX_GAUSS_NOISE)
	return get_gauss_noise(image, intensity)

def get_gauss_noise(image, intensity = 1):
	h, w = image.shape[:2]
	mean = 0
	sigma = intensity ** 0.5
	gauss = np.random.normal(mean, sigma, (h, w))
	gauss = gauss.reshape(h, w)
	return image + gauss

def add_random_saltpepper_noise(image):
	intensity = np.random.uniform(constants.MIN_SALT_PEPPER_NOISE, constants.MAX_SALTPEPPER_NOISE)
	return get_saltpepper_noise(image, intensity)

# tip: use it as first transformation, apply other noises afterwards
def get_saltpepper_noise(image, intensity = 0.0001, add_blur = constants.ADD_BLUR_AFTER_SP_AND_SPECKLE_NOISE):
	s_vs_p = 0.5
	saltpepper = np.copy(image)
	num_salt = np.ceil(intensity * image.size * s_vs_p)
	coords = __get_coordinates_saltpepper(image, num_salt)
	saltpepper[coords] = 1
	num_pepper = np.ceil(intensity * image.size * (1. - s_vs_p))
	coords = __get_coordinates_saltpepper(image, num_pepper)
	saltpepper[coords] = 0
	if (add_blur):
		return blur(saltpepper, 1)
	return saltpepper

def __get_coordinates_saltpepper(image, num_salt):
	return tuple([np.random.randint(0, i - 1, int(num_salt))
		      for i in image.shape])

def get_random_speckle_noise(image):
	intensity = np.random.uniform(constants.MIN_SPECKLE_NOISE, constants.MAX_SPECKLE_NOISE)
	return get_speckle_noise(image, intensity)

# tip: use it as first transformation, apply other noises afterwards
def get_speckle_noise(image, intensity = 0.1, add_blur = constants.ADD_BLUR_AFTER_SP_AND_SPECKLE_NOISE):
	h, w = image.shape[ : 2 ]
	min_matrix = 0 * image
	max_matrix = min_matrix + 255.0
	intensity *= 127.5

	speckle = -intensity/2 + np.random.randn(h,w) * intensity # -intensity/2 <= speckle <= intensity/2
	speckle = speckle.reshape(h, w)
	speckle = image + speckle
	speckle = np.minimum(speckle, max_matrix)
	speckle = np.maximum(speckle, min_matrix)
	if (add_blur and intensity > 26):
		return blur(speckle, 1)
	return speckle