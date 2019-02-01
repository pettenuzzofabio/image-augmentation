#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cv2
import numpy as np

def get_transformed_labels(transformation_function, shape, labels_list):
	if(not ".geometric." in transformation_function.__module__):
		return labels_list

	labels_image, n_labels = __get_image_from_labels(shape, labels_list)
	transformed_image_labels = transformation_function(labels_image)
	return __get_labels_from_image(transformed_image_labels, n_labels)

def __get_image_from_labels(shape, labels_list):
	label_image = np.zeros(shape[ : 2], dtype = np.uint8)

	n_rectangles = len(labels_list)
	pace = int(round(255 / (n_rectangles + 1)))
	color = pace
	for label in labels_list:
		label_image = __draw_label_rectangle(label_image, label, color)
		color += pace

	return label_image, n_rectangles

def __draw_label_rectangle(image, label, color = 255):
	h, w = image.shape[ : 2]
	center_x = int(round(float(label[1]) * w))
	center_y = int(round(float(label[2]) * h))
	half_width = int(round(float(label[3]) / 2 * w))
	half_height = int(round(float(label[4]) / 2 * h))
	image = cv2.rectangle(image, (center_x - half_width, center_y - half_height),
			      (center_x + half_width, center_y + half_height),
			      color, 1)
	return image

def __get_labels_from_image(image, n_labels):
	labels = []

	h, w = image.shape[ : 2]
	pace = int(round(255 / (n_labels + 1)))
	color = pace
	epsilon = int(pace / 10)
	for i in range(n_labels):
		new_label = [i] + __get_rectangle_values(image, color, epsilon, h, w)
		labels.append(new_label)
		color += pace

	return labels

def __get_rectangle_values(image, color, epsilon, h, w):
	rows, cols = np.where(image - color < epsilon)[ : 2]
	min_row = min(rows)
	max_row = max(rows)
	min_col = min(cols)
	max_col = max(cols)
	w_rectangle = (max_col - min_col) / w
	h_rectangle = (max_row - min_row) / h
	center_x = np.mean([max_col, min_col]) / w
	center_y = np.mean([max_row, min_row]) / h
	return [ center_x, center_y, w_rectangle, h_rectangle ]
