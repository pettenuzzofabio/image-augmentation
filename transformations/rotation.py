#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import math

import constants
import cv2
import numpy as np


def get_random_rotation(image, max_angle = constants.MAX_ANGLE):
	max_angle = abs(max_angle)
	angle = np.random.uniform(-1*max_angle, max_angle)
	return rotate_image_crop_borders(image, angle)

def rotate_image_crop_borders(image, rad_angle):
	h, w = image.shape[ : 2]
	image_center = w/2 , h/2
	
	degrees_angle = math.degrees(rad_angle)
	rotation_matrix = cv2.getRotationMatrix2D(image_center, degrees_angle, 1)
	
	sin = math.sin(rad_angle)
	cos = math.cos(rad_angle)
	bound_1 = int(w * abs(cos))
	bound_2 = int(h * abs(cos))
	bound_3 = int(w * abs(sin))
	bound_4 = int(h * abs(sin))
	
	rotation_matrix[0, 2] += ((bound_1 / 2) - image_center[0])
	rotation_matrix[1, 2] += ((bound_2 / 2) - image_center[1])
	
	rotated_image = cv2.warpAffine(image, rotation_matrix, (bound_1, bound_2))
	return rotated_image[bound_4 : h-bound_4, bound_3 : w-bound_3]
