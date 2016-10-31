import tensorflow as tf
import numpy as np
import cv2

def showImage(image, title="Title"):
	cv2.imshow(title, image)
	cv2.waitKey(0)


class ImageInvariants:
	def __init__(self, image_path, max_height=512):
		self.image = cv2.imread(image_path)
		height, width, channels = self.image.shape
		if height>max_height:
			self.image = cv2.resize(self.image, (max_height, width*max_height/height))

		self.height = self.image.shape[0]
		self.width = self.image.shape[1]


	# Returns the histogram descriptor
	def rotate(self, degrees=0):
		image = self.image
		height = self.height
		width = self.width
		center = (height/2, width/2)

		rotationMat = cv2.getRotationMatrix2D(center, degrees, 1)
		rotated = cv2.warpAffine(image, rotationMat, (height, width), 
			borderMode=cv2.BORDER_TRANSPARENT, 
			borderValue=1)
		# TUDU: play around with borderMode and borderValue for different backgrounds

		return rotated

	def dotProduct(self, numSteps = 360)





knight = ImageInvariants("./data/knight1.jpg")
knight.rotationalDescriptor()


"""
QUESTIONS:

 - How sensitive is this rotation group operation to the fringes of the images?
 	What are techniques to weight the background pixels less heavily

"""