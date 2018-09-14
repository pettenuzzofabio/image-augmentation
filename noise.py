#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cv2
import numpy as np
from random import randint

def add_n_random_blur(image, n = randint(1, 4)):
	for i in range(n):
		choice = np.random.uniform(0,4)
		if (choice < 1):
			image = blur(image, randint(1, 3))
		elif (choice < 2):
			image = get_gauss_noise(image, np.randint(1, 100))
		elif (choice < 3):
			image = get_saltpepper_noise(image, np.random.uniform(0.0001, 0.001))
		elif (choice < 4):
			image = get_speckle_noise(image, np.random.uniform(0.01, 0.3))
	return image

# 0 < width < 3
def blur(image, width=9):
	for i in range(0, width, 1):
		size = 2**i + 1
		image = cv2.blur(image, (size, size))
	return image

def get_blur_given_intensity(intensity, blur_scale):
	intensity = intensity * blur_scale
	if(intensity < 0.4):
		return 5
	elif(intensity < 0.5):
		return 6
	return 7

# 1 <= var <= 100
def get_gauss_noise(image, var = 1):
	h, w = image.shape[:2]
	mean = 0
	sigma = var ** 0.5
	gauss = np.random.normal(mean, sigma, (h, w))
	gauss = gauss.reshape(h, w)
	return image + gauss

# tip: use it as first transformation, apply other noises afterwards
# 0.0001 < amount < 0.001
def get_saltpepper_noise(image, amount = 0.0001):
	s_vs_p = 0.5
	saltpepper = np.copy(image)
	num_salt = np.ceil(amount * image.size * s_vs_p)
	coords = [np.random.randint(0, i - 1, int(num_salt))
			  for i in image.shape]
	saltpepper[coords] = 1
	num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
	coords = [np.random.randint(0, i - 1, int(num_pepper))
			  for i in image.shape]
	saltpepper[coords] = 0
	return saltpepper

# tip: use it as first transformation, apply other noises afterwards
# 0.01 < intensity < 0.3
def get_speckle_noise(image, intensity = 0.1):
	h, w = image.shape[:2]
	min_matrix = 0 * image
	max_matrix = min_matrix + 255.0
	intensity *= 127.5

	speckle = -intensity/2 + np.random.randn(h,w) * intensity # -intensity/2 <= x <= intensity/2
	speckle = speckle.reshape(h, w)
	speckle = image + speckle
	speckle = np.minimum(speckle, max_matrix)
	return np.maximum(speckle, min_matrix)