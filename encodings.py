import numpy as np 
from scipy import misc 
# f = misc.face()
# print face 

# import matplotlib.pyplot as plt 
# plt.imshow(face)
# plt.show()

class Encodings(object):
	""" the Encoding object extracts and encapsulates parameters from the image matrix
	"""

	def __init__(self, image):
		# source image as a numpy array
		self.image = misc.imread(image)
		self.row = self.image.shape[0]
		self.col = self.image.shape[1]
		self.introDisectRow = int(self.row / 4)
		self.introDisectCol = int(self.col / 4)
		
		# INTRO 
		# split the image matrix into a list of 16 submatrices
		self.matList = [x for a in np.vsplit(self.image, 4) for x in np.hsplit(a, 4)]
		self.chordsProgression = np.sum(self.image, axis=2) / (self.row * self.col)
		self.drumBeat = np.std(self.image, axis=2)
		self.tempo = 96
		self.strummingPattern = None
		self.quadBeatNum = 208 

		# CHORUS
		print self.matList[5].shape
		centralmatsub1 = np.concatenate((self.matList[5], self.matList[6]), axis=1)
		print centralmatsub1.shape
		centralmatsub2 = np.concatenate((self.matList[9], self.matList[10]), axis=1)
		print centralmatsub2.shape
		centralmat = np.concatenate((centralmatsub1, centralmatsub2), axis=0)
		print centralmat.shape
		centralmatflatten = np.array([x for a in centralmat for x in a])
		print centralmatflatten.shape
		matexpanded = np.concatenate((centralmatflatten, np.zeros((self.quadBeatNum*4*((centralmatflatten.shape[0] / (self.quadBeatNum*4))+1)-centralmatflatten.shape[0], 3), dtype=float)), axis=0)
		print matexpanded.shape
		centralmat = matexpanded.reshape(matexpanded.shape[0] / (self.quadBeatNum*4), self.quadBeatNum*4, 3)
		print centralmat.shape
		self.chorusMeanColor = np.sum(centralmat, axis=1) / (self.quadBeatNum*4)
		print self.chorusMeanColor.shape

		# # VERSES
		# np.array(self.matList)[[x for x in range(0,16) if x not in [5,6,9,10]]] 
		# self.verseMeanColor = self.average(, axis=1)

		# BRIDGE
		# topLeftMean = np.average(self.matList[0])
		# print topLeftMean
		# topRightMean = np.average(self.matList[3])
		# bottomLeftMean = np.average(self.matList[12])
		# bottomRightMean = np.average(self.matList[15])
		# self.bridgeMeanColor = np.average([topLeftMean, topRightMean, bottomLeftMean, bottomRightMean]) 
		# print self.bridgeMeanColor

		print self.matList[0].shape
		top = np.concatenate((self.matList[0], self.matList[3]), axis=1)
		print top.shape
		bottom = np.concatenate((self.matList[12], self.matList[15]), axis=1)
		print bottom.shape
		bridgemat = np.concatenate((top, bottom), axis=0)
		print bridgemat.shape
		bridgematflatten = np.array([x for a in bridgemat for x in a])
		print  bridgematflatten.shape
		bridgematexpanded = np.concatenate((bridgematflatten, np.zeros((self.quadBeatNum*4*((bridgematflatten.shape[0] / (self.quadBeatNum*4))+1)-bridgematflatten.shape[0], 3), dtype=float)), axis=0)
		print bridgematexpanded.shape
		bridgemat = bridgematexpanded.reshape(bridgematexpanded.shape[0] / (self.quadBeatNum*4), self.quadBeatNum*4, 3)
		print bridgemat.shape
		self.bridgeMeanColor = np.sum(bridgemat, axis=1) / (self.quadBeatNum*4)
		print self.bridgeMeanColor.shape

	def setTempo(self, new_tempo):
		self.tempo = new_tempo

	def setStrummingPattern(self, newStrummingPattern):
		self.strummingPattern = newStrummingPattern	

	def setQuadBeatNum(self, newQuadBeatNum):
		self.quadBeatNum = newQuadBeatNumL

	def printChorus(self):
		print self.chorusMeanColor

	# def printVerses(self):
	# 	print self.verseMeanColor

	def printBridge(self):
		print self.bridgeMeanColor


# Test
example = Encodings("example.jpg")

print 
example.printChorus()
print 
example.printBridge()



