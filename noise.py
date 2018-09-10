#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cv2
import numpy as np

def blur(image, width=9):
	for i in range(0, width, 1):
		size = 2**i + 1
		image = cv2.blur(image, (size, size))
	return image

def get_blur_given_intensity(intensity, blur_scale):
	# empirical relationship between blur and intensity
	# 0.3		=>		5
	# 0.4 - 0.55 =>		6
	# 0.55 - 0.7 =>		7
	intensity = intensity*blur_scale
	if(intensity < 0.4):
		return 5
	elif(intensity < 0.5):
		return 6
	return 7

# 1 <= var <= 100
def get_gauss_noise(image, var = 1):
	row, col = image.shape
	mean = 0
	sigma = var ** 0.5
	gauss = np.random.normal(mean, sigma, (row, col))
	gauss = gauss.reshape(row, col)
	return image + gauss

# suggestion: use as first transformation, apply other noises afterwards
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

# computationally expansive and less effective
def get_poisson_noise(image, iterations = 10):
	poisson = np.copy(image)
	for i in range(1, iterations):
		vals = len(np.unique(poisson))
		vals = 2 ** np.ceil(np.log2(vals))
		poisson = np.random.poisson(poisson * vals) / float(vals)
	return poisson

# suggestion: use as first transformation, apply other noises afterwards
# 0.01 < intensity < 0.3
def get_speckle_noise(image, intensity=0.1):
	row,col = image.shape
	min_matrix = 0 * image[:, :]
	max_matrix = min_matrix + 255.0
	intensity *= 127.5

	speckle = -intensity/2 + np.random.randn(row,col)*intensity # -intensity/2 <= x <= intensity/2
	speckle = speckle.reshape(row,col)
	speckle = image + speckle
	speckle = np.minimum(speckle,  max_matrix)
	return np.maximum(speckle,  min_matrix)
