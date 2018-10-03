# Image augmentation

Image augmentation for machine learning projects

We all know that deep learning models are data hungry. They thrive when given many training examples.\
This data augmentation tool enlarges your dataset of images by generating multiple version of each image.\
It is conceived to help you getting more data, if...well you don't actually have "more data".

- Input: grayscale photos or scan to documents, certificates, pages, receipts...
- Output: images which simulate different lighting conditions, slight changes in picture perspective, minor crumples and warps

Invariants that should be preserved:
 - the position of the objects contained with respect to the size of the image
 - the proportions of the image

### Requirements

- Python >= 2.7

Required packages:
- Pillow
- enum34
- numpy
- opencv-python
- scipy
- scikit-image

Please let me know if you find missing dependencies.

## Usage


### Command line

`usage: main.py [-h] [--input [INPUT]] [--output [OUTPUT]] [--n [N]]

optional arguments:
  -h, --help         show this help message and exit
  --input [INPUT]    input files path, default: all images .jpg, .jpeg, .png
                     in ./input/
  --output [OUTPUT]  output files path, default: ./output/
  --n [N]            number of output images for each input image, default: 10`
  
e.g. `python main.py `
  
### Integration with other code

If you want to integrate this code in your Machine Learning project
- `import augment` (specify the relative path of `augment.py` with respect to the file from which you're importing it)
- invoke the method 
`def get_n_augmented_images(image, n_output_list = constants.N_FILES_OUTPUT)
	'''
	Applies the transformations to the input image and returns a list of transformed images
	:param image: image to be augmented
	:param n_output_list: number of images returned as output
	:return list of transformed images
	'''`

### Edit parameters

In the file `constants.py` there are several parameters that can be edited 

`
# default number of files given as output for each input image
N_FILES_OUTPUT    = 10

# allowed input images extensions
IMAGE_EXTENSIONS  = [".jpg", ".jpeg", ".png"]

# default input images path
FILES_INPUT_PATH  = "./input/"

# default output images path
FILES_OUTPUT_PATH = "./output/"
`

`
# max number of transformations
# that are randomly applied for each output image.
# If N_TRANSFORMATIONS > total number of transformations
# specified in the MaxTransformations field
# N_TRANSFORMATIONS will be reset as:
# min( sum_MaxTransformations_fields, N_TRANSFORMATIONS) )
N_TRANSFORMATIONS = 2

# MaxTransformations contains, for each transformation,
# the number of times that each transformation is performed.
# Useful to apply some transformations more often ( n > 1 )
# or to exclude them` altogether ( n = 0 )
class MaxTransformations:
    SALT_PEPPER_NOISE   = 1
    SPECKLE_NOISE       = 0
    GAUSS_NOISE         = 0
    BLUR                = 0
    SHADOW              = 0
    ENHANCEMENTS        = 0
    SHADE_COLORS        = 0

    # The following transformations
    # will alter pixel coordinates
    SHEAR               = 0
    SKEW                = 0
    WARP                = 0
    ROTATION            = 0

# MIN/MAX AVG BLURRING
MIN_BLUR 		= 1
MAX_BLUR 		= 3

# MIN/MAX GAUSS NOISE
MIN_GAUSS_NOISE 	= 1
MAX_GAUSS_NOISE 	= 100

# MIN/MAX SALT AND PEPPER NOISE
MIN_SALT_PEPPER_NOISE 	= 0.0001
MAX_SALTPEPPER_NOISE 	= 0.001

# MIN/MAX SPECKLE
MIN_SPECKLE_NOISE 	= 0.01
MAX_SPECKLE_NOISE 	= 0.3

# MIN/MAX SHADOW
MIN_SHADOW       	= 0.3
MAX_SHADOW       	= 0.7

# MIN/MAX IMAGE BRIGHTNESS
MIN_BRIGHTNESS   	= 0.6
MAX_BRIGHTNESS   	= 1.4

# MIN/MAX IMAGE CONTRAST
MIN_CONTRAST   	        = 0.5
MAX_CONTRAST   	        = 1.7

# MIN/MAX IMAGE SHARPNESS
MIN_SHARPNESS   	= 0.1
MAX_SHARPNESS   	= 3.0

# MIN/MAX COLOR SHADING
MIN_COLOR_SHADE 	= 0.06
MAX_COLOR_SHADE 	= 0.35

# MAX SHEAR DISTORTION
MAX_SHEAR        	= 0.1

# MAX SKEW DISTORTION
MAX_SKEW        	= 0.1

# MIN/MAX WARP DISTORTION
MIN_WARP        	= 14
MAX_WARP        	= 50

# MIN/MAX ROTATION ANGLE
MAX_ANGLE        	= 0.1

# By default s&p and speckle noise
# is followed by blurring
ADD_BLUR_AFTER_SP_AND_SPECKLE_NOISE = True

READ_IMAGE_AS_GRAYSCALE = True
`


<!--

[ The tool converts a set of images into a much larger set of slightly altered images.
 The tool scans a directory containing image files, and creates new images by performing a set of augmentation operations. 
]

## Getting Started

### Prerequisites

It targets grayscale images, but it can be easily extended to handle other kind of images as well. 

I've integrated it with YOLO v3 object detection algorithm, based on the darknet CNN.
But it can be used to train other convolutional neural networks and should both improve their performance and reduce overfitting.

-->

## Future developments

- image flip: this hasn't been implemented yet because for my project I need to distinguish between Left-something and Right-something
