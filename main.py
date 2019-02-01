#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division

import argparse
import os
import sys
import time
from os import listdir
from os.path import isfile, join

import cv2

import augment
import constants


def main(args):
    image_file_name_list = __get_files_path(args.input)
    output_path = __normalize_output_path(args.output)
    n_transformations = args.n

    for image_full_name in image_file_name_list:
        path, image_name = os.path.split(image_full_name)
        image = __read_image(image_full_name)
        labels = __read_labels(path, image_name)

        start = time.time()
        images_labels = augment.get_n_augmented_images_labels(image, labels, n_transformations)
        end = time.time()
        print("Image " + image_name + " augmented " + str(n_transformations) +
              " times in " + str("%.3f" % (end - start)) + " seconds")

        augment.write_output_files(image_name, images_labels, output_path)


def __get_files_path(path):
    path = os.path.abspath(path)
    __validate_path(path)

    files_path = []
    if os.path.isdir(path):
        files_path.extend([path + "\\" + f for f in listdir(path)
                           if isfile(join(path, f))])

    else:
        files_path.extend([path])

    return files_path


def __validate_path(path):
    if not os.path.exists(path):
        print("The path " + path + " is not valid.")
        sys.exit()


def __normalize_output_path(path):
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except:
            print("The path " + path + " is not a valid directory.")
            sys.exit()

    return os.path.abspath(path)


def __read_image(image_full_name):
    if constants.READ_IMAGE_AS_GRAYSCALE:
        image = cv2.imread(image_full_name, 0)
    else:
        image = cv2.imread(image_full_name)
    return image


def __read_labels(path, image_name):
    name, _extension = os.path.splitext(image_name)
    labels_file = open(path + "\\" + name + ".txt", "r")
    lines = labels_file.readlines()

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


def __parse_arguments():
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

    parser.add_argument(
        '--input', nargs='?', type=str, default=str(constants.FILES_INPUT_PATH),
        help='input files path, default: all images ' +
             str(', '.join(constants.IMAGE_EXTENSIONS)) + ' in ' +
             str(constants.FILES_INPUT_PATH)
    )

    parser.add_argument(
        '--output', nargs='?', type=str,
        default=str(os.path.abspath(constants.FILES_OUTPUT_PATH)),
        help='output files path, default: ' + str(constants.FILES_OUTPUT_PATH)
    )

    parser.add_argument(
        '--n', nargs='?', type=int, default=constants.N_FILES_OUTPUT,
        help='number of output images for each input image, default: ' +
             str(constants.N_FILES_OUTPUT)
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = __parse_arguments()
    main(args)
