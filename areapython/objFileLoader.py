import numpy as np

class ObjFileLoader:
	def __init__(self):
		self.modelArray = []

		self.verticesCoords = []
		self.textureCoords = []
		self.normalCoords = []

		self.verticesIndex = []
		self.textureIndex = []
		self.normalIndex = []

	def loadModel(self, filename):
		for line in open(filename, 'r'):
			lineSplit = line.split()

			if(lineSplit[0] == 'v'):
				self.verticesCoords.append(lineSplit[1:4])
			elif(lineSplit[0] == 'vt'):
				self.textureCoords.append(lineSplit[1:3])
			elif(lineSplit[0] == 'vn'):
				self.normalCoords.append(lineSplit[1:4])
			elif(lineSplit[0] == 'f'):
				for coord in lineSplit[1:4]:
					c = coord.split('/')
					self.verticesIndex.append(int(c[0])-1)
					self.textureIndex.append(int(c[1])-1)
					self.normalIndex.append(int(c[2])-1)

		for i in self.verticesIndex:
			self.modelArray.append(i)

		for i in self.textureIndex:
			self.modelArray.append(i)

		for i in self.normalIndex:
			self.modelArray.append(i)

		self.modelArray = np.array(self.modelArray, dtype='float32')