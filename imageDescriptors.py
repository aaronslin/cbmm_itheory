import tensorflow as tf
import numpy as np
import cv2

def showImage(image, title="Title"):
	cv2.imshow(title, image)
	cv2.waitKey(0)


class ImageInvariants:
	def __init__(self, image_path, max_height=64):
		self.image = cv2.imread(image_path).astype(np.float32)
		height, width, channels = self.image.shape
		if height>max_height:
			self.image = cv2.resize(self.image, (max_height, width*max_height/height))

		self.height = self.image.shape[0]
		self.width = self.image.shape[1]


	# Returns rotated image
	def rotate(self, degrees=0):
		image = self.image
		height = self.height
		width = self.width
		center = (height/2, width/2)

		rotationMat = cv2.getRotationMatrix2D(center, degrees, 1)
		rotated = cv2.warpAffine(image, rotationMat, (height, width), 
			borderMode=cv2.BORDER_CONSTANT, 
			borderValue=1)
		# TUDU: play around with borderMode and borderValue for different backgrounds

		return rotated


	def rotateDescriptor(self, numsteps=360):
		descriptor = [self.dotProduct(self.rotate(deg)) for deg in range(numsteps)]
		for d in descriptor:
			print d
		return descriptor

	def dotProduct(self, other):
		def L2(x):
			return np.linalg.norm(x)
		def L1(x):
			return np.sum(np.abs(x))

		difference = self.image-other
		similarity = np.apply_along_axis(L2, 2, difference)
		#print "\t", self.image, other
		return np.mean(similarity)



knight = ImageInvariants("./data/knight1.jpg")
knight.rotateDescriptor()


"""
QUESTIONS:

 - How sensitive is this rotation group operation to the fringes of the images?
 	What are techniques to weight the background pixels less heavily
 - Sensitivity to different color but same shape/outline?

"""