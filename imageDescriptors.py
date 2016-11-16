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

		#self.image = 255 - self.image

		self.height = self.image.shape[0]
		self.width = self.image.shape[1]


	# Returns rotated image
	def rotate(self, degrees=0):
		image = self.image
		height = self.height
		width = self.width
		center = (height/2, width/2)

		rotationMat = cv2.getRotationMatrix2D(center, degrees, 1)
		rotated = cv2.warpAffine(image, rotationMat, (width, height), 
			borderMode=cv2.BORDER_CONSTANT, 
			borderValue=1)
		# TUDU: play around with borderMode and borderValue for different backgrounds

		return rotated


	def rotateDescriptor(self, numsteps=360):
		descriptor = [self.dotProduct(self.rotate(deg)) for deg in range(numsteps)]
		return descriptor

	def dotProduct(self, other):
		def L2():
			difference = self.image-other
			similarity = np.apply_along_axis(lambda x: np.linalg.norm(x), 2, difference)
			return similarity
		def L1():
			difference = self.image-other
			similarity = np.apply_along_axis(lambda x: np.sum(np.abs(x)), 2, difference)
			return similarity
		def dot():
			product = self.image * other
			similarity = np.apply_along_axis(lambda x: np.sum(x), 2, product)
			return similarity

		similarity = L1()
		return np.mean(similarity)


# stardavid = ImageInvariants("./data/stardavid.jpg")
# stardavid.rotateDescriptor()

image = ImageInvariants("./data/bishop.png")
histogram = image.rotateDescriptor()

open("output.txt", "w").close()
with open("output.txt", "a") as myfile:
	for h in histogram:
		myfile.write(str(h)+"\n")



"""
QUESTIONS:

 - How sensitive is this rotation group operation to the fringes of the images?
 	What are techniques to weight the background pixels less heavily
 - Sensitivity to different color but same shape/outline?

"""