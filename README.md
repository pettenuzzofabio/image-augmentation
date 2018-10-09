# Image augmentation

Image dataset augmentation for machine learning projects

We all know that deep learning models are data hungry. They thrive when given tons of training examples.\
This data augmentation tool enlarges your dataset of pictures by generating multiple version of each image.\
It helps you getting more data, if... well you don't actually have "more data".

- Input: photos or scan of documents, certificates, invoices, pages, receipts...
- Output: images which simulate different lighting conditions, slight changes in picture perspective, minor crumples and warps

I've integrated it with YOLO v3 object detection algorithm, based on the darknet CNN, but it works also on other convolutional neural networks, hopefully improving their performance and reducing overfitting.

## Examples

|     | Image |
| --- | ----- |
| *Original Input*	| <img style="border: 1px solid grey" 	src="readme_images/test.png" 		width="100" alt="input image"> 			|
| shear 			| <img style="border: 1px solid grey" 	src="readme_images/shear.png" 		width="100" alt="shear"> 				|
| skew 			 	| <img style="border: 1px solid grey" 	src="readme_images/skew(2).png" 	width="100" alt="skew horizontal"> <img style="border: 1px solid grey" 	src="readme_images/skew(1).png" 	width="100" alt="skew vertical"> 		|
| warp 				| <img style="border: 1px solid grey" 	src="readme_images/warp(1).png" 	width="100" alt="warp"> <img style="border: 1px solid grey" 	src="readme_images/warp(2).png" 	width="100" alt="warp"> <img style="border: 1px solid grey" 	src="readme_images/warp(3).png" 	width="100" alt="warp"> |
| shadows 			| <img style="border: 1px solid grey" 	src="readme_images/shadows(1).png" 	width="100" alt="shadows"> <img style="border: 1px solid grey" 	src="readme_images/shadows(2).png" 	width="100" alt="shadows"> <img style="border: 1px solid grey" 	src="readme_images/shadows(3).png" 	width="100" alt="shadows"> <img style="border: 1px solid grey" 	src="readme_images/shadows(4).png" 	width="100" alt="shadows"> <img style="border: 1px solid grey" 	src="readme_images/shadows(5).png" 	width="100" alt="shadows">  <img style="border: 1px solid grey" 	src="readme_images/shadows(7).png" 	width="100" alt="shadows">	|
| rotation 			| <img style="border: 1px solid grey" 	src="readme_images/rotation.png" 	width="100" alt="rotation"> 			|
| salt & pepper noise | <img style="border: 1px solid grey" src="readme_images/saltpepper.png" 	width="100" alt="salt & pepper noise"> 	|
| speckle noise 	| <img style="border: 1px solid grey" 	src="readme_images/speckle.png" 	width="100" alt="speckle noise"> 		|
| gauss noise 		| <img style="border: 1px solid grey" 	src="readme_images/gauss.png" 		width="100" alt="gauss noise">  		|
| blur 				| <img style="border: 1px solid grey" 	src="readme_images/blur.png" 		width="100" alt="blur">  				|
| sharpness 		| <img style="border: 1px solid grey" 	src="readme_images/sharpness.png" 	width="100" alt="sharpness">  			|
| brightness 		| <img style="border: 1px solid grey" 	src="readme_images/brightness.png" 	width="100" alt="brightness">  			|
| contrast 			| <img style="border: 1px solid grey" 	src="readme_images/contrast.png" 	width="100" alt="contrast">  			|
| shade colors 		| <img style="border: 1px solid grey" 	src="readme_images/colors(1).png" 	width="100" alt="shade colors"> <img style="border: 1px solid grey" 	src="readme_images/colors(2).png" 	width="100" alt="shade colors"> <img style="border: 1px solid grey" 	src="readme_images/colors(3).png" 	width="100" alt="shade colors"> <img style="border: 1px solid grey" 	src="readme_images/colors(4).png" 	width="100" alt="shade colors"> <img style="border: 1px solid grey" 	src="readme_images/colors(5).png" 	width="100" alt="shade colors"> <img style="border: 1px solid grey" 	src="readme_images/colors(6).png" 	width="100" alt="shade colors"> <img style="border: 1px solid grey" 	src="readme_images/colors(7).png" 	width="100" alt="shade colors"> <img style="border: 1px solid grey" 	src="readme_images/colors(8).png" 	width="100" alt="shade colors"> |

### Requirements

- Python >= 2.7

Required packages:
- Pillow
- enum34
- numpy
- opencv-python
- six
- scipy
- scikit-image

OpenCV has to be manually installed. The other package can be installed  with `pip install [package_name]`
Please let me know if you find missing dependencies.

## Usage

### Command line

```
usage: main.py [-h] [--input [INPUT]] [--output [OUTPUT]] [--n [N]]

optional arguments:
  -h, --help         show this help message and exit
  --input [INPUT]    input files path, default: all images .jpg, .jpeg, .png
                     in ./input/
  --output [OUTPUT]  output files path, default: ./output/
  --n [N]            number of output images for each input image, default: 10
```
  
e.g. `python main.py`
  
### Integration with other code

If you want to integrate this code in your Machine Learning project
- `import augment` (specify the relative path of `augment.py` with respect to the file from which you're importing it)
- invoke the method 
```python
def get_n_augmented_images(image, n_output_list = constants.N_FILES_OUTPUT)
	'''
	Applies the transformations to the input image and returns a list of transformed images
	:param image: image to be augmented
	:param n_output_list: number of images returned as output
	:return list of transformed images
	'''
```

or, as an alternative, you can directly call the functions, e.g.:
- `import distort` (specify the relative path of `distort.py` with respect to the file from which you're importing it)
- invoke the method 
```python
get_random_warp(image, min_factor = constants.MIN_WARP, max_factor = constants.MAX_WARP)
```

### Edit parameters

In the file `constants.py` there are several parameters that can be tuned to better suit your project's needs:

```python
# default number of files given as output for each input image
N_FILES_OUTPUT    = 10

# allowed input images extensions
IMAGE_EXTENSIONS  = [".jpg", ".jpeg", ".png"]

# default input images path
FILES_INPUT_PATH  = "./input/"

# default output images path
FILES_OUTPUT_PATH = "./output/"
```

```python
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
    SALT_PEPPER_NOISE   = 0
    SPECKLE_NOISE       = 0
    GAUSS_NOISE         = 0
    BLUR                = 0
    SHADOW              = 1
    ENHANCEMENTS        = 0
    SHADE_COLORS        = 0

    # The following transformations
    # will alter pixel coordinates
    SHEAR               = 1
    SKEW                = 1
    WARP                = 1
    ROTATION            = 1

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
```



## Future developments

- augment bounding boxes (and possibly other landmarks) in the exactly same way as the augmented image, in order to better use transformations which alter pixel coordinates.
This can be accomplished by using `random.seed()`
- optimize & add multi threading
- image flip: this hasn't been implemented yet because for my purpose I need to distinguish between Left-something and Right-something
- add requirements.txt