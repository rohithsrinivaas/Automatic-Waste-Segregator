'''
Removes any interference due to Bin's background

'''


import cv2
import numpy as np

def background_subtract(image_name = './input/image.jpg',background_pixel = [185,185,185]):

	b_factor = background_pixel[0]
	g_factor = background_pixel[1]
	r_factor = background_pixel[2]

	image = cv2.imread(image_name)

	# define range of blue color in HSV
	lower = np.array([10,10,10])
	upper = np.array([180,180,180])
	'''
	Wood in the smart bin has rgb range
	in [10,10,10] to [180,180,180]
	Do not delete it.
	'''
	# Manual Threshold the RGB image to get only blue colors
	mask = cv2.inRange(image, lower, upper)
	ret,mask_inv = cv2.threshold(mask,0,255,cv2.THRESH_BINARY_INV)

	ret,mask = cv2.threshold(mask,0,255,cv2.THRESH_BINARY)
	# Bitwise-AND mask and original image

	mask = mask//255
	r_mask = r_factor*mask
	g_mask = g_factor*mask
	b_mask = b_factor*mask
	mask = np.dstack([r_mask,g_mask,b_mask])

	result = cv2.bitwise_and(image,image, mask= mask_inv)
	result = result + mask
	cv2.imwrite('./input_masked/input_masked.jpg',result)

if __name__=='__main__':
	background_subract()
