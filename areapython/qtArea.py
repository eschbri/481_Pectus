import sys
from PyQt5 import QtWidgets, QtGui
from scipy import misc
import numpy as np

class AreaRatioWindow(QtWidgets.QWidget):
	
	def __init__(self):
		super(AreaRatioWindow, self).__init__()			
		self.setWindowTitle('2d window')
		#self.setGeometry(200, 200, 1000, 800)
		self.init_window()
		
	def init_window(self):
		#default bounday ratios, can later be changed by doctor
		self.leftBoundaryRatio = .25
		self.centerBoundaryRatio = .5
		self.rightBoundaryRatio = .75

		#boundary line on or off 
		self.boundaryLineOn = False

		#currently displayed 2d image
		self.displayPictureFile = 'paint2dchest100.png'

		#if boundary ratios have been changed
		self.boundaryRatiosChanged = True

		#if already ran defect/chest ratio
		self.ran_defect_chest_ratio = False

		#if already ran asymmetry ratio
		self.ran_asymmetry_ratio = False

		#display app title
		self.appTitle = QtWidgets.QLabel('Welcome to the 2d application')

		#display text in window
		self.text = QtWidgets.QLabel('Please select an option')
		
		#set left lung vertical line button
		self.leftButton = QtWidgets.QPushButton('Set defect left boundary')
		self.leftButton.clicked.connect(self.setLeftBoundary)

		#Center sternum vertical line button
		self.centerButton = QtWidgets.QPushButton('Set center vertical line')
		self.centerButton.clicked.connect(self.setCenterBoundary)

		#set right lung vertical line button
		self.rightButton = QtWidgets.QPushButton('Set defect right boundary')
		self.rightButton.clicked.connect(self.setRightBoundary)
		
		#display defect / chest area ratio
		self.areaRatioButton = QtWidgets.QPushButton('Calculate defect / chest ratio')
		self.areaRatioButton.clicked.connect(self.calculateDefectChestRatio)

		#display left / right area ratio
		self.asymmetryRatioButton = QtWidgets.QPushButton('Calculate left / right ratio')
		self.asymmetryRatioButton.clicked.connect(self.calculateAsymmetryRatio)

		#display boundary lines
		self.boundary_lines = QtWidgets.QPushButton('Toggle display Boundary Lines')
		self.boundary_lines.clicked.connect(self.displayBoundaryLine)

		#switch back to default images
		self.defaultImage = QtWidgets.QPushButton('Switch back to default image')
		self.defaultImage.clicked.connect(self.switchDefaultImage)
		
		#display picture in window
		self.picture = QtWidgets.QLabel()
		self.picture.setPixmap(QtGui.QPixmap(self.displayPictureFile))
		
		#this is the layout setup horizontal boxes in a wrapping vertical layout
		h_box_instruct = QtWidgets.QHBoxLayout()
		h_box_instruct.addWidget(self.appTitle)
		
		h_box_buttons = QtWidgets.QHBoxLayout()
		h_box_buttons.addWidget(self.leftButton)
		h_box_buttons.addWidget(self.centerButton)
		h_box_buttons.addWidget(self.rightButton)
		h_box_buttons.addWidget(self.areaRatioButton)
		h_box_buttons.addWidget(self.asymmetryRatioButton)

		h_box_switch_boundary_line = QtWidgets.QHBoxLayout()
		h_box_switch_boundary_line.addWidget(self.defaultImage)
		h_box_switch_boundary_line.addWidget(self.boundary_lines)

		h_box_status = QtWidgets.QHBoxLayout()
		h_box_status.addWidget(self.text)
		
		h_box_picture = QtWidgets.QHBoxLayout()
		h_box_picture.addWidget(self.picture)
		
		vertical_box = QtWidgets.QVBoxLayout()
		vertical_box.addLayout(h_box_instruct)
		vertical_box.addLayout(h_box_buttons)
		vertical_box.addLayout(h_box_switch_boundary_line)
		vertical_box.addLayout(h_box_status)
		vertical_box.addLayout(h_box_picture)
		
		self.setLayout(vertical_box)
		
		self.show()

	def setLeftBoundary(self):
		maxPercent = (float(self.centerBoundaryRatio) * 100) - 1
		if(maxPercent < 0):
			maxPercent = 0
		currentPercent = float(self.leftBoundaryRatio) * 100

		percent, ok = QtWidgets.QInputDialog.getInt(self, "Set Left Boundary", "Percentage of Image:", currentPercent, 0, maxPercent, 1)
		self.leftBoundaryRatio = float(percent) / 100
		if(ok):
			self.boundaryRatiosChanged = True
			self.text.setText('Please select an option')
			self.switchDefaultImage()
			self.displayBoundaryLine()
			print "successfully set new left boundary ratio"

	def setCenterBoundary(self):
		maxPercent = (float(self.rightBoundaryRatio) * 100) - 1
		if(maxPercent < 0):
			maxPercent = 0		
		minPercent = (float(self.leftBoundaryRatio) * 100) + 1
		currentPercent = float(self.centerBoundaryRatio) * 100

		percent, ok = QtWidgets.QInputDialog.getInt(self, "Set Center line", "Percentage of Image:", currentPercent, minPercent, maxPercent, 1)
		self.centerBoundaryRatio = float(percent) / 100
		if(ok):
			self.boundaryRatiosChanged = True
			self.text.setText('Please select an option')
			self.switchDefaultImage()
			self.displayBoundaryLine()
			print "successfully set new center boundary ratio"

	def setRightBoundary(self):
		minPercent = (float(self.centerBoundaryRatio) * 100) + 1
		currentPercent = float(self.rightBoundaryRatio) * 100

		percent, ok = QtWidgets.QInputDialog.getInt(self, "Set Right line", "Percentage of Image:", currentPercent, minPercent, 99, 1)
		self.rightBoundaryRatio = float(percent) / 100
		if(ok):
			self.boundaryRatiosChanged = True
			self.text.setText('Please select an option')
			self.switchDefaultImage()
			self.displayBoundaryLine()
			print "successfully set new right boundary ratio"		


	def switchDefaultImage(self):
		self.displayPictureFile = 'paint2dchest100.png'
		self.boundaryLineOn = False
		self.picture.setPixmap(QtGui.QPixmap(self.displayPictureFile))

	def displayBoundaryLine(self):
		image = misc.imread(self.displayPictureFile)
		X = image.shape[0]
		Y = image.shape[1]

		#draw or erase left boundary line
		y = self.leftBoundaryRatio * Y
		if(self.boundaryLineOn):
			self.picture.setPixmap(QtGui.QPixmap(self.displayPictureFile))
		else:
			for x in range(0, X):
				image[x][y][0] = 178
				image[x][y][1] = 34
				image[x][y][2] = 34

			#draw or erase left center line
			y = self.centerBoundaryRatio * Y
			for x in range(0, X):
				image[x][y][0] = 178
				image[x][y][1] = 34
				image[x][y][2] = 34

			#draw or erase right center line
			y = self.rightBoundaryRatio * Y
			for x in range(0, X):
				image[x][y][0] = 178
				image[x][y][1] = 34
				image[x][y][2] = 34

		misc.imsave('temp.png', image)
		self.picture.setPixmap(QtGui.QPixmap('temp.png'))

		self.boundaryLineOn = not self.boundaryLineOn

		
	def calculateDefectChestRatio(self):
		if(self.ran_defect_chest_ratio and not self.boundaryRatiosChanged):
			self.displayPictureFile = 'outfile2.png'
			self.boundaryLineOn = False
			self.picture.setPixmap(QtGui.QPixmap(self.displayPictureFile))
		else:
			chestPixels = self.pixelCount('chest', "paint2dchest100.png")
			defectPixels = self.pixelCount('defect', "outfile.png")
			ratio = float(defectPixels) / chestPixels
			self.text.setText('Defect contains: ' + str(defectPixels) + ' pixels. Chest contains: ' + str(chestPixels) 
				+ ' pixels. The defect / chest ratio is: ' + str(ratio))

	def calculateAsymmetryRatio(self):
		if(self.ran_asymmetry_ratio and not self.boundaryRatiosChanged):
			self.displayPictureFile = 'outfileRight.png'
			self.boundaryLineOn = False
			self.picture.setPixmap(QtGui.QPixmap(self.displayPictureFile))
		else:
			leftPixels = self.pixelCount('left', "paint2dchest100.png")
			rightPixels = self.pixelCount('right', "outfileLeft.png")
			ratio = float(leftPixels) / rightPixels
			self.text.setText('Left contains: ' + str(leftPixels) + ' pixels. Right contains: ' + str(rightPixels) 
				+ ' pixels. The left / right ratio is: ' + str(ratio))
		
		
	def pixelCount(self, areaType, filename):
		image = misc.imread(filename)
		X = image.shape[0]
		Y = image.shape[1]
		
		#starting position with y at the center
		starting_x = 0
		starting_y = self.centerBoundaryRatio * Y

		#the defect boundaries are default or chosen by the doctor
		rightBoundaryDefect = self.rightBoundaryRatio * Y
		leftBoundaryDefect = self.leftBoundaryRatio * Y

		#center line
		centerLine = self.centerBoundaryRatio * Y
		
		#start with y at center line, and go down until inside chest then set the starting x value
		if(areaType == 'chest' or areaType == 'left' or areaType == 'right'):
			x = 0
			y = self.centerBoundaryRatio * Y
			hitChest = False
			while(True):
				if(image[x][y][0] != 255):
					hitChest = True
				elif(hitChest and image[x][y][0] == 255):
					starting_x = x
					break;			
				x += 1		
			if areaType == 'left':
				starting_y -= 1
			elif areaType == 'right':
				starting_y += 1		
		
		Area_Pixels = 0
		
		stack = [[starting_x, starting_y]]
		
		visited = np.zeros((X,Y))
		visited[starting_x, starting_y] = 1	
		
		if(areaType == 'chest'):
			while len(stack) != 0:
				x, y = stack.pop()
				Area_Pixels += 1
				image[x][y][0] = 100
				image[x][y][1] = 100
				image[x][y][2] = 255
			
				if x+1 < X and image[x+1][y][0] == 255 and visited[x+1, y] == 0:
					visited[x+1, y] = 1
					stack.append([x+1, y])
				if x-1 >= 0 and image[x-1][y][0] == 255 and visited[x-1, y] == 0:
					visited[x-1, y] = 1
					stack.append([x-1, y])
				if y+1 < Y and image[x][y+1][0] == 255 and visited[x, y+1] == 0:
					visited[x, y+1] = 1
					stack.append([x, y+1])
				if y-1 >= 0 and image[x][y-1][0] == 255 and visited[x, y-1] == 0:
					visited[x, y-1] = 1
					stack.append([x, y-1])
		elif(areaType == 'defect'):
			while len(stack) != 0:
				x, y = stack.pop()
				Area_Pixels += 1
				image[x][y][0] = 173
				image[x][y][1] = 255
				image[x][y][2] = 47
			
				if x+1 < X and image[x+1][y][0] == 255 and visited[x+1, y] == 0:
					visited[x+1, y] = 1
					stack.append([x+1, y])
				if x-1 >= 0 and image[x-1][y][0] == 255 and visited[x-1, y] == 0:
					visited[x-1, y] = 1
					stack.append([x-1, y])
				if y+1 < Y and image[x][y+1][0] == 255 and visited[x, y+1] == 0 and (y + 1) < rightBoundaryDefect:
					visited[x, y+1] = 1
					stack.append([x, y+1])
				if y-1 >= 0 and image[x][y-1][0] == 255 and visited[x, y-1] == 0 and (y - 1) > leftBoundaryDefect:
					visited[x, y-1] = 1
					stack.append([x, y-1])
		elif(areaType == 'left'):
			while len(stack) != 0:
				x, y = stack.pop()
				Area_Pixels += 1
				image[x][y][0] = 0
				image[x][y][1] = 255
				image[x][y][2] = 0
			
				if x+1 < X and image[x+1][y][0] == 255 and visited[x+1, y] == 0:
					visited[x+1, y] = 1
					stack.append([x+1, y])
				if x-1 >= 0 and image[x-1][y][0] == 255 and visited[x-1, y] == 0:
					visited[x-1, y] = 1
					stack.append([x-1, y])
				if y+1 < Y and image[x][y+1][0] == 255 and visited[x, y+1] == 0 and (y + 1) < centerLine:
					visited[x, y+1] = 1
					stack.append([x, y+1])
				if y-1 >= 0 and image[x][y-1][0] == 255 and visited[x, y-1] == 0:
					visited[x, y-1] = 1
					stack.append([x, y-1])
		elif(areaType == 'right'):
			while len(stack) != 0:
				x, y = stack.pop()
				Area_Pixels += 1
				image[x][y][0] = 0
				image[x][y][1] = 0
				image[x][y][2] = 255
			
				if x+1 < X and image[x+1][y][0] == 255 and visited[x+1, y] == 0:
					visited[x+1, y] = 1
					stack.append([x+1, y])
				if x-1 >= 0 and image[x-1][y][0] == 255 and visited[x-1, y] == 0:
					visited[x-1, y] = 1
					stack.append([x-1, y])
				if y+1 < Y and image[x][y+1][0] == 255 and visited[x, y+1] == 0:
					visited[x, y+1] = 1
					stack.append([x, y+1])
				if y-1 >= 0 and image[x][y-1][0] == 255 and visited[x, y-1] == 0 and y-1>centerLine:
					visited[x, y-1] = 1
					stack.append([x, y-1])

		
		print Area_Pixels
		if(areaType == 'chest'):
			misc.imsave('outfile.png', image)
		elif(areaType == 'defect'):
			misc.imsave('outfile2.png', image)
			self.displayPictureFile = 'outfile2.png'
			self.ran_defect_chest_ratio = True
			self.boundaryRatiosChanged = False
			self.boundaryLineOn = False
			self.picture.setPixmap(QtGui.QPixmap(self.displayPictureFile))
		elif(areaType == 'left'):
			misc.imsave('outfileLeft.png', image)
		elif(areaType == 'right'):
			misc.imsave('outfileRight.png', image)
			self.displayPictureFile = 'outfileRight.png'
			self.ran_asymmetry_ratio = True
			self.boundaryRatiosChanged = False
			self.boundaryLineOn = False
			self.picture.setPixmap(QtGui.QPixmap(self.displayPictureFile))

		return Area_Pixels
		
	
app = QtWidgets.QApplication(sys.argv)
window = AreaRatioWindow()
sys.exit(app.exec_())