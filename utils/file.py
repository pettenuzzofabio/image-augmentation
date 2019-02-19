#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from os import listdir
from os.path import join

import cv2

import constants as const
import utils.validation as validation


def get_files_path(path):
    path = os.path.abspath(path)
    validation.validate_path(path)

    files_path = []
    if os.path.isdir(path):
        files_path.extend([path + "\\" + f for f in listdir(path)
                           if validation.is_valid_file(join(path, f))])

    else:
        files_path.extend([path])

    return files_path


def read_image(image_full_name):
    if const.READ_IMAGE_AS_GRAYSCALE:
        image = cv2.imread(image_full_name, 0)
    else:
        image = cv2.imread(image_full_name)
    return image


def read_labels(path, image_name):
    name, _extension = os.path.splitext(image_name)
    try:
        labels_file = open(path + "\\" + name + ".txt", "r")
        lines = labels_file.readlines()
    except:
        print("The label file " + name + ".txt does not exist. Labels won't be transformed for the image " + image_name)
        return None

    return _extract_labels_from_lines(lines)


def _extract_labels_from_lines(lines):
    labels = []
    for single_line in lines:
        single_line = single_line.split()
        label = single_line[0]
        center_x = single_line[1]
        center_y = single_line[2]
        w_rectangle = single_line[3]
        h_rectangle = single_line[4]
        labels.append([label, center_x, center_y, w_rectangle, h_rectangle])
    return labels


def write_output_files(full_name, images_and_labels, output_path):
    name, extension = os.path.splitext(full_name)
    prefix = output_path + "\\" + name

    i = 0

    for image, labels_list in images_and_labels:
        tmp_prefix = prefix + str(i)
        output_image_name = tmp_prefix + extension
        output_txt_name = tmp_prefix + ".txt"

        _write_labels_to_disk(output_txt_name, labels_list)
        _write_image_to_disk(output_image_name, image)

        i += 1


def _write_image_to_disk(output_image_name, image):
    try:
        cv2.imwrite(output_image_name, image)
    except:
        print("An error occurred while writing the file " + output_image_name)


def _write_labels_to_disk(output_txt_name, labels_list):
    try:
        if labels_list != None :
            with open(output_txt_name, "w") as text_file:
                for single_label in labels_list:
                    text_file.write(str(single_label[0]) + " " + str(single_label[1]) + " " + str(single_label[2]) + " " + str(
                        single_label[3]) + " " + str(single_label[4]) + "\n")
    except:
        print("An error occurred while writing the file " + output_txt_name)

