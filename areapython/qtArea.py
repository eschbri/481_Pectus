import sys
from PyQt5 import QtWidgets, QtGui
from scipy import misc
import numpy as np

class AreaRatioWindow(QtWidgets.QWidget):
	
	def __init__(self):
		super(AreaRatioWindow, self).__init__()			
		self.setWindowTitle('2d window')
		self.setGeometry(200, 200, 1000, 800)
		self.init_window()
		
	def init_window(self):
		#default bounday ratios, can later be changed by doctor
		self.leftBoundaryRatio = .25
		self.centerBoundaryRatio = .5
		self.rightBoundaryRatio = .75

		#display text in window
		self.text = QtWidgets.QLabel('Please select the position of the line')
		
		#center left lung vertical line button
		self.leftButton = QtWidgets.QPushButton('Set defect left boundary')

		#Center sternum vertical line button
		self.centerButton = QtWidgets.QPushButton('Set center vertical line')
		
		#Center right lung vertical line button
		self.rightButton = QtWidgets.QPushButton('Set defect right boundary')
		
		#display defect / chest area ratio
		self.areaRatioButton = QtWidgets.QPushButton('Calculate defect / chest ratio')
		self.areaRatioButton.clicked.connect(self.calculateDefectChestRatio)
		
		#display picture in window
		self.picture = QtWidgets.QLabel()
		self.picture.setPixmap(QtGui.QPixmap('paint2dchest100.png'))
		
		#this is the layout setup horizontal boxes in a wrapping vertical layout
		h_box_instruct = QtWidgets.QHBoxLayout()
		h_box_instruct.addWidget(self.text)
		
		h_box_buttons = QtWidgets.QHBoxLayout()
		h_box_buttons.addWidget(self.leftButton)
		h_box_buttons.addWidget(self.centerButton)
		h_box_buttons.addWidget(self.rightButton)
		h_box_buttons.addWidget(self.areaRatioButton)
		
		h_box_picture = QtWidgets.QHBoxLayout()
		h_box_picture.addWidget(self.picture)
		
		vertical_box = QtWidgets.QVBoxLayout()
		vertical_box.addLayout(h_box_instruct)
		vertical_box.addLayout(h_box_buttons)
		vertical_box.addLayout(h_box_picture)
		
		self.setLayout(vertical_box)
		
		self.show()

		
	def calculateDefectChestRatio(self):
		self.pixelCount('chest')
		self.pixelCount('defect')
		
		
	def pixelCount(self, areaType):
		if(areaType == 'chest'):
			image = misc.imread("paint2dchest100.png")
		else:
			image = misc.imread("outfile.png")
		X = image.shape[0]
		Y = image.shape[1]
		
		#starting position with y at the center
		starting_x = 0
		starting_y = self.centerBoundaryRatio * Y

		#the defect boundaries are default or chosen by the doctor
		rightBoundaryDefect = self.rightBoundaryRatio * Y
		leftBoundaryDefect = self.leftBoundaryRatio * Y
		
		#start with y at center line, and go down until inside chest then set the starting x value
		if(areaType == 'chest'):
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
		else:
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
		
		print Area_Pixels
		if(areaType == 'chest'):
			misc.imsave('outfile.png', image)
		else:
			misc.imsave('outfile2.png', image)
			self.picture.setPixmap(QtGui.QPixmap('outfile2.png'))
		
	
app = QtWidgets.QApplication(sys.argv)
window = AreaRatioWindow()
sys.exit(app.exec_())