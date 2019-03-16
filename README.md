# Image augmentation

We all know that deep learning models are data hungry. They thrive when given tons of training examples.\
This data augmentation tool enlarges your dataset of pictures by generating multiple version of each image.\
It helps you getting more data, if... well you don't actually have "more data".

- Input: photos or scan of documents, certificates, invoices, pages, receipts... [ + labels in YOLO format ]
- Output: simulation of different lighting conditions, slight changes of perspective, minor crumples and warps [ + transformed labels in YOLO format ]

I've tested it with YOLO v3 object detection algorithm, based on the darknet CNN, but it works also on other convolutional neural networks, hopefully improving their performance and reducing overfitting.

## Examples

|     | Image |
| --- | ----- |
| *Original Input*	| <img style="border: 1px solid grey" 	src="readme_images/test.png" 		width="100" alt="input image"> 			|
| Shear 			| <img style="border: 1px solid grey" 	src="readme_images/shear.png" 		width="100" alt="shear"> 				|
| Skew 			 	| <img style="border: 1px solid grey" 	src="readme_images/skew(2).png" 	width="100" alt="skew horizontal"> <img style="border: 1px solid grey" 	src="readme_images/skew(1).png" 	width="100" alt="skew vertical"> 		|
| Warp 				| <img style="border: 1px solid grey" 	src="readme_images/warp(1).png" 	width="100" alt="warp"> <img style="border: 1px solid grey" 	src="readme_images/warp(2).png" 	width="100" alt="warp"> <img style="border: 1px solid grey" 	src="readme_images/warp(3).png" 	width="100" alt="warp"> |
| Shadows 			| <img style="border: 1px solid grey" 	src="readme_images/shadows(1).png" 	width="100" alt="shadows"> <img style="border: 1px solid grey" 	src="readme_images/shadows(2).png" 	width="100" alt="shadows"> <img style="border: 1px solid grey" 	src="readme_images/shadows(3).png" 	width="100" alt="shadows"> <img style="border: 1px solid grey" 	src="readme_images/shadows(4).png" 	width="100" alt="shadows"> <img style="border: 1px solid grey" 	src="readme_images/shadows(5).png" 	width="100" alt="shadows">  <img style="border: 1px solid grey" 	src="readme_images/shadows(7).png" 	width="100" alt="shadows">	|
| Rotation 			| <img style="border: 1px solid grey" 	src="readme_images/rotation.png" 	width="100" alt="rotation"> 			|
| Salt & pepper noise | <img style="border: 1px solid grey" src="readme_images/saltpepper.png" 	width="100" alt="salt & pepper noise"> 	|
| Speckle noise 	| <img style="border: 1px solid grey" 	src="readme_images/speckle.png" 	width="100" alt="speckle noise"> 		|
| Gauss noise 		| <img style="border: 1px solid grey" 	src="readme_images/gauss.png" 		width="100" alt="gauss noise">  		|
| Blur 				| <img style="border: 1px solid grey" 	src="readme_images/blur.png" 		width="100" alt="blur">  				|
| Sharpness 		| <img style="border: 1px solid grey" 	src="readme_images/sharpness.png" 	width="100" alt="sharpness">  			|
| Brightness 		| <img style="border: 1px solid grey" 	src="readme_images/brightness.png" 	width="100" alt="brightness">  			|
| Contrast 			| <img style="border: 1px solid grey" 	src="readme_images/contrast.png" 	width="100" alt="contrast">  			|
| Shade colors 		| <img style="border: 1px solid grey" 	src="readme_images/colors(2).png" 	width="100" alt="shade colors"> <img style="border: 1px solid grey" 	src="readme_images/colors(3).png" 	width="100" alt="shade colors"> <img style="border: 1px solid grey" 	src="readme_images/colors(4).png" 	width="100" alt="shade colors"> <img style="border: 1px solid grey" 	src="readme_images/colors(5).png" 	width="100" alt="shade colors"> <img style="border: 1px solid grey" 	src="readme_images/colors(6).png" 	width="100" alt="shade colors"> <img style="border: 1px solid grey" 	src="readme_images/colors(7).png" 	width="100" alt="shade colors"> |


## Usage

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

OpenCV has to be manually installed. The other packages can be installed  with `pip install [package_name]`\
Please let me know if you find missing dependencies.

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
  
e.g. `python main.py --input /path/to/input/folder/ --output /path/to/output/folder/ --n 5`

### Labels format

The labels should be formatted according to the YOLO / darknet format:

```
class_number box1_x1_ratio box1_y1_ratio box1_width_ratio box1_height_ratio
class_number box2_x1_ratio box2_y1_ratio box2_width_ratio box2_height_ratio
....
```

An example is provided at ``` input/test.txt ```

### Integration in external projects

If you want to integrate this code in your Machine Learning project
- `import augment` (specify the relative path of `augment.py` with respect to the file from which you're importing it)
- invoke the function 
```python
def generate_n_augmented_images_labels(image, labels_list, n_output_list = const.N_FILES_OUTPUT):
	'''
	Applies the transformations to the input image and returns
	a generator of transformed images along with the corresponding labels
	:param image: image to be augmented
	:param labels_list: labels associated to the image
	:param n_output_list: number of images and labels returned as output
	:return a generator of: list of transformed images and list of associated labels
	'''
```

or, as an alternative, you can directly call the functions in the package `transformations`, e.g.:
- `import transformations.shadow` (specify the relative path of `distort.py` with respect to the file from which you're importing it)
- invoke the function 
```python
add_n_shadows(image, n_shadow = 4, intensity = 0.5, blur_scale = 1.0):
```

### Edit parameters

In the file `constants.py` there are several parameters that can be tuned to better suit your project's needs:

```python
# default number of files given as output for each input image
N_FILES_OUTPUT		= 100

# allowed input images extensions
IMAGE_EXTENSIONS	= [ ".jpg", ".jpeg", ".png", ".bmp", ".jp2", ".dib", ".webp", ".sr", ".ras", ".tiff", ".tif", ".pbm", ".pgm", ".ppm" ]

# default input files path
FILES_INPUT_PATH	= "./input/"

# default output files path
FILES_OUTPUT_PATH	= "./output/"
```

```python



'''
max number of transformations
that are randomly applied for each output image.
If N_TRANSFORMATIONS > total number of transformations
specified in the MaxTransformation field
N_TRANSFORMATIONS will be reset as sum_MaxTransformation_fields
'''
N_TRANSFORMATIONS	= 3

'''
MaxTransformation contains, for each transformation,
the maximum number of times that each transformation is performed.
Useful to apply some transformations more often ( n > 1 )
or to exclude them` altogether ( n = 0 )
'''


class MaxTransformation:
    SALT_PEPPER_NOISE   = 1
    SPECKLE_NOISE       = 1
    GAUSS_NOISE         = 1
    BLUR                = 1

    SHADOW              = 1
    ENHANCEMENTS        = 1
    SHADE_COLOR         = 1

    # The following transformations
    # will alter pixel coordinates
    SHEAR               = 1
    SKEW                = 1
    WARP                = 1
    ROTATION            = 1

# MIN/MAX AVG BLURRING
MIN_BLUR                = 1
MAX_BLUR                = 3

# MIN/MAX GAUSS NOISE
MIN_GAUSS_NOISE         = 1
MAX_GAUSS_NOISE         = 100

# MIN/MAX SALT AND PEPPER NOISE
MIN_SALT_PEPPER_NOISE   = 0.0001
MAX_SALTPEPPER_NOISE    = 0.001

# MIN/MAX SPECKLE
MIN_SPECKLE_NOISE       = 0.01
MAX_SPECKLE_NOISE       = 0.3

# MIN/MAX SHADOW
MIN_SHADOW              = 0.3
MAX_SHADOW              = 0.7

# MIN/MAX IMAGE BRIGHTNESS
MIN_BRIGHTNESS          = 0.6
MAX_BRIGHTNESS          = 1.4

# MIN/MAX IMAGE CONTRAST
MIN_CONTRAST            = 0.5
MAX_CONTRAST            = 1.7

# MIN/MAX IMAGE SHARPNESS
MIN_SHARPNESS           = 0.1
MAX_SHARPNESS           = 5.0

# MIN/MAX COLOR SHADING
MIN_COLOR_SHADE         = 0.06
MAX_COLOR_SHADE         = 0.35

# MAX SHEAR DISTORTION
MAX_SHEAR               = 0.05

# MAX SKEW DISTORTION
MAX_SKEW                = 0.05

# MIN/MAX WARP DISTORTION
MIN_WARP                = 14
MAX_WARP                = 51

# MIN/MAX ROTATION ANGLE
MAX_ANGLE               = 0.02

# By default salt&pepper and speckle noise
# is followed by blurring
ADD_BLUR_AFTER_SPECKLE_NOISE    = True
ADD_BLUR_AFTER_SP_NOISE         = True

READ_IMAGE_AS_GRAYSCALE         = False
```



## Future developments

- Add centered scaling
- Optimize & add multi threading
- Image flip: this hasn't been implemented yet because for my purpose I need to distinguish between Left-something and Right-something
- Add requirements.txt
