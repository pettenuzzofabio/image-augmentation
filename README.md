# Image augmentator

Grayscale image augmentation for machine learning

We all know that deep learning models are data hungry. They thrive when given many training examples.\
This data augmentation tool enlarges your dataset of images by generating multiple version of each image.\
It is conceived to help you getting more data, if...well you don't actually have "more data".

- Input: grayscale photos or scan to documents, certificates, pages, receipts...
- Output: images which simulate different lighting conditions, slight changes in picture perspective, minor crumples and warps

Invariants that should be preserved:
 - the position of the objects contained with respect to the size of the image
 - the proportions of the image


<!--

[ The tool converts a set of images into a much larger set of slightly altered images.
 The tool scans a directory containing image files, and creates new images by performing a set of augmentation operations. 
]

## Getting Started

### Prerequisites

By default it does not flip the image, so that the neural network is able to distinguish between Left-something and Right-something
It targets grayscale images, but it can be easily extended to handle other kind of images as well. 

I've integrated it with YOLO v3 object detection algorithm, based on the darknet CNN.
But it can be used to train other convolutional neural networks and should both improve their performance and reduce overfitting.

-->

## WIP, release of version 1.0 estimate for the end of September 2018
