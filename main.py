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

import utils.file as file
import utils.validation as validation

def main(args):
    image_file_name_list = file.get_files_path(args.input)
    output_path = validation.normalize_output_path(args.output)
    n_transformations = args.n

    for image_full_name in image_file_name_list:
        path, image_name = os.path.split(image_full_name)
        image = file.read_image(image_full_name)
        labels = file.read_labels(path, image_name)

        start = time.time()
        images_and_labels = augment.get_n_augmented_images_labels(image, labels, n_transformations)
        end = time.time()
        print("Image " + image_name + " augmented " + str(n_transformations) +
              " times in " + str("%.3f" % (end - start)) + " seconds")

        file.write_output_files(image_name, images_and_labels, output_path)


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
