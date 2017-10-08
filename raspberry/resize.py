'''
Resize using an efficient os walk, to 512*384 size.
'''

import os
import constants
import numpy as np
from scipy import misc, ndimage

def resize(image, dim1=constants.DIM1, dim2=constants.DIM2):
	return misc.imresize(image, (dim1, dim2))

def fileWalk(directory, destPath):
	try:
		os.makedirs(destPath)
	except OSError:
		if not os.path.isdir(destPath):
			raise

	for subdir, dirs, files in os.walk(directory):
		for file in files:
			if len(file) <= 4 or (file[-4:] != '.jpg' and file[-5:] != '.jpeg'):
				continue

			pic = misc.imread(os.path.join(subdir, file))
			dim1 = len(pic)
			dim2 = len(pic[0])
			if dim1 > dim2:
				pic = np.rot90(pic)

			picResized = resize(pic,constants.DIM1, constants.DIM2)
			misc.imsave(os.path.join(destPath, file), picResized)

def rpi_resize(directory='./input'):
	# function to be used as
	# rpi_resize(os.path.join(os.getcwd(),'input'))

	 for subdir, dirs, files in os.walk(directory):
 		for file in files:
 			if len(file) <= 4 or (file[-4:] != '.jpg' and file[-5:] != '.jpeg'):
 				continue

 			pic = misc.imread(os.path.join(subdir, file))
 			dim1 = len(pic)
 			dim2 = len(pic[0])
 			if dim1 > dim2:
 				pic = np.rot90(pic)

 			picResized = resize(pic,constants.DIM1, constants.DIM2)
 			misc.imsave(os.path.join('./input_resized', 'resized_input.jpg'), picResized)
			return picResized

def main():
	prepath = os.path.join(os.getcwd(), 'data')
	glassDir = os.path.join(prepath, 'broken_glass')
	#dpaperDir = os.path.join(prepath, 'disposable_paper_cups')
	#eggDir = os.path.join(prepath, 'egg_packaging')
	#plasticDir = os.path.join(prepath, 'plastic_bottle')
	#foilDir = os.path.join(prepath, 'foil')
	#crumpled_paperDir = os.path.join(prepath, 'crumpled_paper')
	#recDir = os.path.join(prepath, 'receipt')

	destPath = os.path.join(os.getcwd(), 'dataset-resized')
	try:
		os.makedirs(destPath)
	except OSError:
		if not os.path.isdir(destPath):
			raise

	#glass_bottle
	fileWalk(glassDir, os.path.join(destPath, 'bg'))

	#PAPER
	#fileWalk(dpaperDir, os.path.join(destPath, 'disposable_paper_cups'))

	##EGG
	#fileWalk(eggDir, os.path.join(destPath, 'egg_packaging'))

	#plasticDir
	#fileWalk(plasticDir, os.path.join(destPath, 'plastic_bottle'))

	#foilDir
	#fileWalk(foilDir, os.path.join(destPath, 'foil'))

	#crumpled_paperDir
	#fileWalk(crumpled_paperDir, os.path.join(destPath, 'crumpled_paper'))

	#recDir
	#fileWalk(recDir, os.path.join(destPath, 'receipt'))

if __name__ == '__main__':
    main()
