#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from random import randint
import numpy as np
import cv2
import noise
import constants

def add_n_random_shadows(image, n, intensity_scale = 1, blur_scale = 1.0):
	for i in range(n):
		intensity = np.random.uniform(0.3, 0.7) * intensity_scale
		blur_width = noise.get_blur_given_intensity(intensity, blur_scale)

		choice = np.random.uniform(0, 4)
		if (choice < 1):
			image = add_n_triangles_shadow(image, 1, intensity, blur_width)
		elif (choice < 2):
			image = add_n_triangles_light(image, 1, intensity, blur_width)
		elif (choice < 3):
			image = add_single_light(image, intensity, blur_width)
		elif (choice < 4):
			image = add_single_shadow(image, intensity, blur_width)
	return image

def add_n_triangles_light(image, n, intensity = 0.5, blur_width = 6):
	inverted_colors = constants.WHITE - image
	inverted_shadow = add_n_triangles_shadow(inverted_colors, n, intensity, blur_width)
	return constants.WHITE - inverted_shadow

def add_n_triangles_shadow(image, n, intensity = 0.5, blur_width = 6):
	for i in range(n):
		image = add_polygon_shadow(image, 3, intensity, blur_width)
	return image

# tip: just stick with triangles, other polygons have incoherent shades
def add_polygon_light(image, n_sides = 3, intensity = 0.5, blur_width = 6):
	inverted_colors = constants.WHITE - image
	inverted_shadow = add_polygon_shadow(inverted_colors, n_sides, intensity, blur_width)
	return constants.WHITE - inverted_shadow

# tip: just stick with triangles, other polygons have incoherent shades
def add_polygon_shadow(image, n_sides = 3, intensity = 0.5, blur_width = 6):
	shadow_mask = 0 * image + constants.WHITE
	points = __get_points(n_sides, shadow_mask)

	centre = __get_centre(points)
	points1 = __scale_points(points.copy(), centre, 0.5)
	points2 = __scale_points(points.copy(), centre, 1.5)
	points3 = __scale_points(points.copy(), centre, 2)
	points4 = __scale_points(points.copy(), centre, 2.5)

	cv2.fillPoly(shadow_mask, [points4], constants.DARK_WHITE)
	cv2.fillPoly(shadow_mask, [points3], constants.LIGHT_GRAY)
	cv2.fillPoly(shadow_mask, [points2], constants.GRAY)
	cv2.fillPoly(shadow_mask, [points] , constants.DARK_GRAY)
	cv2.fillPoly(shadow_mask, [points1], constants.LIGHT_BLACK)

	return __apply_shadow_mask(image, blur_width, intensity, shadow_mask)

def add_single_light(image, intensity = 0.5, blur_width = 8):
	inverted_colors = constants.WHITE - image
	inverted_shadow = add_single_shadow(inverted_colors, intensity, blur_width)
	return constants.WHITE - inverted_shadow

def add_single_shadow(image, intensity = 0.5, blur_width = 8):
	h, w = image.shape[:2]
	top_y = __get_random_number(w)
	top_x = __get_random_number(h)
	bot_x = __get_random_number(h)
	bot_y = __get_random_number(w)
	x_m = np.mgrid[0:h, 0:w][0]
	y_m = np.mgrid[0:h, 0:w][1]
	shadow_mask = 0 * image
	shadow_mask[((x_m - top_x)*(bot_y - top_y) - (bot_x - top_x)*(y_m - top_y) >= 0)] = constants.DARK_GRAY

	space = 50
	if(bot_x < top_x and top_y > bot_y):
		shadow_mask[((x_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (y_m - top_y) < 0)] = constants.LIGHT_BLACK
		top_x -= __get_random_space(space)
		bot_x -= __get_random_space(space)
		top_y += __get_random_space(space)
		bot_y += __get_random_space(space)
		shadow_mask[((x_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (y_m - top_y) >= 0)] = constants.GRAY
		top_x -= __get_random_space(space)
		bot_x -= __get_random_space(space)
		top_y += __get_random_space(space)
		bot_y += __get_random_space(space)
		shadow_mask[((x_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (y_m - top_y) >= 0)] = constants.LIGHT_GRAY
		top_x -= __get_random_space(space)
		bot_x -= __get_random_space(space)
		top_y += __get_random_space(space)
		bot_y += __get_random_space(space)
		shadow_mask[((x_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (y_m - top_y) >= 0)] = constants.DARK_WHITE

	if (bot_x < top_x and top_y < bot_y):
		shadow_mask[((x_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (y_m - top_y) < 0)] = constants.LIGHT_BLACK
		top_x += __get_random_space(space)
		bot_x += __get_random_space(space)
		top_y += __get_random_space(space)
		bot_y += __get_random_space(space)
		shadow_mask[((x_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (y_m - top_y) >= 0)] = constants.GRAY
		top_x += __get_random_space(space)
		bot_x += __get_random_space(space)
		top_y += __get_random_space(space)
		bot_y += __get_random_space(space)
		shadow_mask[((x_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (y_m - top_y) >= 0)] = constants.LIGHT_GRAY
		top_x += __get_random_space(space)
		bot_x += __get_random_space(space)
		top_y += __get_random_space(space)
		bot_y += __get_random_space(space)
		shadow_mask[((x_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (y_m - top_y) >= 0)] = constants.DARK_WHITE

	if (bot_x > top_x and top_y > bot_y):
		shadow_mask[((x_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (y_m - top_y) < 0)] = constants.LIGHT_BLACK
		top_x -= __get_random_space(space)
		bot_x -= __get_random_space(space)
		top_y -= __get_random_space(space)
		bot_y -= __get_random_space(space)
		shadow_mask[((x_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (y_m - top_y) >= 0)] = constants.GRAY
		top_x -= __get_random_space(space)
		bot_x -= __get_random_space(space)
		top_y -= __get_random_space(space)
		bot_y -= __get_random_space(space)
		shadow_mask[((x_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (y_m - top_y) >= 0)] = constants.LIGHT_GRAY
		top_x -= __get_random_space(space)
		bot_x -= __get_random_space(space)
		top_y -= __get_random_space(space)
		bot_y -= __get_random_space(space)
		shadow_mask[((x_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (y_m - top_y) >= 0)] = constants.DARK_WHITE

	if (bot_x > top_x and top_y < bot_y):
		shadow_mask[((x_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (y_m - top_y) < 0)] = constants.LIGHT_BLACK
		top_x += __get_random_space(space)
		bot_x += __get_random_space(space)
		top_y -= __get_random_space(space)
		bot_y -= __get_random_space(space)
		shadow_mask[((x_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (y_m - top_y) >= 0)] = constants.GRAY
		top_x += __get_random_space(space)
		bot_x += __get_random_space(space)
		top_y -= __get_random_space(space)
		bot_y -= __get_random_space(space)
		shadow_mask[((x_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (y_m - top_y) >= 0)] = constants.LIGHT_GRAY
		top_x += __get_random_space(space)
		bot_x += __get_random_space(space)
		top_y -= __get_random_space(space)
		bot_y -= __get_random_space(space)
		shadow_mask[((x_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (y_m - top_y) >= 0)] = constants.DARK_WHITE

	return __apply_shadow_mask(image, blur_width, intensity, shadow_mask)

def __get_points(n_sides, image):
	points = []
	h, w = image.shape[:2]
	for i in range(n_sides):
		points.append([np.int32(w * 1.5 * np.random.uniform() - w * 0.25),
					   np.int32(h * 1.5 * np.random.uniform() - h * 0.25)])
	points = np.array(points)
	points = points.reshape((-1, 1, 2))
	return points

def __scale_points(points, centre, scale):
	for p in points:
		p = [__scale_point(p[0], centre, scale + np.random.uniform()/2)]

	return points

def __scale_point(point, centre, scale = 0.1):
	point[0] = int(round(centre[0] + (point[0] - centre[0]) * scale))
	point[1] = int(round(centre[1] + (point[1] - centre[1]) * scale))

def __get_centre(points):
	sum_points = sum(points[1:], points[0])[0]
	n_points = len(points)
	return (__get_average(n_points, sum_points[0]), __get_average(n_points, sum_points[1]))

def __get_average(n_points, sum):
	return int(round(sum / n_points))

def __get_random_number(number):
	return number * np.random.uniform()

def __get_random_space(space):
	return space + space * np.random.uniform()

def __apply_shadow_mask(image, blur_width, intensity, shadow_mask):
	shadow_mask = __normalize_shadow_mask(blur_width, intensity, shadow_mask)
	image = np.multiply(image, shadow_mask)
	return image.astype(np.uint8)

def __random_normalize_shadow_mask(shadow_mask):
	intensity = np.random.uniform(0.3,0.7)
	blur_width = np.random.uniform(4,7)
	return __normalize_shadow_mask(blur_width, intensity, shadow_mask)

def __normalize_shadow_mask(blur_width, intensity, shadow_mask):
	shadow_mask = noise.blur(shadow_mask, blur_width)
	normalized_mask = (shadow_mask / 250.0)
	ones_matrix = 0*shadow_mask + 1.0
	normalized_mask = np.minimum(normalized_mask + (1.0 - normalized_mask) * (1.0 - intensity) ,  ones_matrix)
	return normalized_mask
