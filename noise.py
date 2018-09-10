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
	# 0.3 => 5 		0.4 - 0.55 => 6 		0.55 - 0.7 => 7
	intensity = intensity*blur_scale
	if(intensity < 0.4):
		return 5
	elif(intensity < 0.5):
		return 6
	return 7

def get_gauss_noise(image, var = 0.1):
	row, col, ch = image.shape
	mean = 0
	sigma = var ** 0.5
	gauss = np.random.normal(mean, sigma, (row, col, ch))
	gauss = gauss.reshape(row, col, ch)
	return image + gauss

def get_saltpepper_noise(image, amount = 0.004):
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

def get_poisson_noise(image):
	vals = len(np.unique(image))
	vals = 2 ** np.ceil(np.log2(vals))
	poisson = np.random.poisson(image * vals) / float(vals)
	return poisson

def get_speckle_noise(image):
	row,col,ch = image.shape
	speckle = np.random.randn(row,col,ch)
	speckle = speckle.reshape(row,col,ch)
	speckle = image + image * speckle
	return speckle
