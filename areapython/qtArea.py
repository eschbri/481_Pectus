import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from scipy import misc
import numpy as np

class ClickableLabel(QtWidgets.QLabel):
	def __init__(self):
		QtWidgets.QLabel.__init__(self)
		self.__hallerListener = None

	def mouseReleaseEvent(self, mouseEvent):
		if not self.__hallerListener == None:
			self.__hallerListener(mouseEvent)

	def attach(self, fn, force = False):
		if self.__hallerListener == None or force:
			self.__hallerListener = fn

	def detach(self):
		self.__hallerListener = None

class HallerIndex():
	def __init__(self):
		self.clearHorz()
		self.clearVert()

	def calculate(self):
		if self.horz1 != None and self.horz2 != None and self.vert1 != None and self.vert2 != None:
			return abs(self.horz1 - self.horz2) / abs(self.vert1 - self.vert2)
		raise ValueError('Coordinates have not been set before calculation')

	def clearVert(self):
		self.vert1 = None
		self.vert2 = None

	def clearHorz(self):
		self.horz1 = None
		self.horz2 = None

	def setVert(self, vert):
		if self.vert1 == None:
			self.vert1 = float(vert)
			return
		if self.vert2 == None:
			self.vert2 = float(vert)
			return
		raise ValueError('Vertical coordinates have already been set')

	def setHorz(self, horz):
		if self.horz1 == None:
			self.horz1 = float(horz)
			return
		if self.horz2 == None:
			self.horz2 = float(horz)
			return
		raise ValueError('Horizontal coordinates have already been set')

	def horzIsSet(self):
		return self.horz2 != None

	def vertIsSet(self):
		return self.vert2 != None

class BackToFrontSternumToVertebreRatio():
	def __init__(self):
		self.clearLung()
		self.clearSternum()

	def calculate(self):
		if self.vert1 != None and self.vert2 != None and self.vert3 != None and self.vert4 != None:
			return abs(self.vert1 - self.vert2) / abs(self.vert3 - self.vert4)
		raise ValueError('Coordinates have not been set before calculation')

	def clearLung(self):
		self.vert1 = None
		self.vert2 = None

	def clearSternum(self):
		self.vert3 = None
		self.vert4 = None

	def setLung(self, vert):
		if self.vert1 == None:
			self.vert1 = float(vert)
			return
		if self.vert2 == None:
			self.vert2 = float(vert)
			return
		raise ValueError('Vertical coordinates have already been set')

	def setSternum(self, vert):
		if self.vert3 == None:
			self.vert3 = float(vert)
			return
		if self.vert4 == None:
			self.vert4 = float(vert)
			return
		raise ValueError('Vertical coordinates have already been set')

	def sternumIsSet(self):
		return self.vert4 != None

	def lungIsSet(self):
		return self.vert2 != None

class AreaRatioWindow(QtWidgets.QWidget):
	
	def __init__(self):
		super(AreaRatioWindow, self).__init__()			
		self.setWindowTitle('2d window')
		#self.setGeometry(200, 200, 1000, 800)
		self.init_window()
		
	def init_window(self):
		#slice number files
		self.slice1 = 'paint2dchest100.png'
		self.slice2 = 'paint2dchest200.png'
		self.slice3 = 'paint2dchest300.png'
		self.slice4 = 'paint2dchest400.png'
		self.slice5 = 'paint2dchest500.png'
		self.slice6 = 'paint2dchest600.png'
		self.slice7 = 'paint2dchest700.png'
		self.slice8 = 'paint2dchest800.png'
		self.slice9 = 'paint2dchest900.png'
		self.slice10 = 'paint2dchest1000.png'
		self.slice11 = 'paint2dchest110.png'
		self.slice12 = 'paint2dchest120.png'

		#Haller index
		self.hallerIndex = HallerIndex()

		#lung back to front / sternum to vertebre ratio
		self.backToFrontSternumToVertebreRatio = BackToFrontSternumToVertebreRatio()

		#current slice
		self.currentSlice = self.slice7

		#if slice has changed
		self.sliceChanged = False

		#default bounday ratios, can later be changed by doctor
		self.leftBoundaryRatio = .25
		self.centerBoundaryRatio = .5
		self.rightBoundaryRatio = .75

		#boundary line on or off 
		self.boundaryLineOn = False

		#currently displayed 2d image
		self.displayPictureFile = self.slice7

		#if boundary ratios have been changed
		self.boundaryRatiosChanged = True

		#if already ran defect/chest ratio
		self.ran_defect_chest_ratio = False


		#saved solution text defect / chest ratio
		self.defectChestRatioSolution = ''

		#bool representing if listener is attached
		self.listenerAttached = False

		#haller index horizontal count
		self.hallerHoriCount = 0 
				
		#lung vertical count
		self.lungCount = 0 

		#Sternum to vertebre count
		self.STVCount = 0 
				
		#haller index horizontal count
		self.hallerVertCount = 0 

		#saved solution text asymmetric ratio 
		self.asymmetricRatio = ''

		#display app title
		self.appTitle = QtWidgets.QLabel('Below are the options to set boundaries and calulate area ratios')

		#display text in window
		self.text = QtWidgets.QLabel('Please select an option')

		#set Haller display
		self.hallerDisplay = QtWidgets.QLabel('Haller index: ')

		#set lung / sternum to vertebre ratio
		self.lungSternumToVertebreDisplay = QtWidgets.QLabel('Lung back to front / Sternum to vertebre ratio: ')

		#display current slice text
		self.sliceText = QtWidgets.QLabel('You are currently on slice 7')
		
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

		#display picture in window
		#self.picture = QtWidgets.QLabel()
		self.picture = ClickableLabel()
		self.picture.setPixmap(QtGui.QPixmap(self.displayPictureFile))

		#switch back to default images
		self.defaultImage = QtWidgets.QPushButton('Switch back to default image')
		self.defaultImage.clicked.connect(self.switchDefaultImageButton)

		#slider widget to display different 2d slices
		self.slider = QtWidgets.QSlider(Qt.Vertical)
		self.slider.valueChanged[int].connect(self.changeSlice)
		self.slider.setMaximum(12)
		self.slider.setMinimum(1)
		self.slider.setValue(6)

		#set Haller horizontal selector
		self.hallerHorz = QtWidgets.QPushButton('Set horizontal Haller')
		self.hallerHorz.clicked.connect(self.attachHallerHorzListener)

		#set Haller vertical selector
		self.hallerVert = QtWidgets.QPushButton('Set vertical Haller')
		self.hallerVert.clicked.connect(self.attachHallerVertListener)

		#set Haller label
		self.hallerLabel = QtWidgets.QLabel('Haller index Buttons')

		#set lung back to front vertical selector
		self.lungBackToFront = QtWidgets.QPushButton('Set vertical lung back to front')
		self.lungBackToFront.clicked.connect(self.attachHallerLungListener)

		#set sternum to vertebre vertical selector
		self.sternumToVertebre = QtWidgets.QPushButton('Set vertical sternum to vertebre')
		self.sternumToVertebre.clicked.connect(self.attachHallerSTVListener)

		#set lung / sternum to vertebre ratio
		self.lungSternumToVertebreLabel = QtWidgets.QLabel('Lung back to front / Sternum to vertebre ratio Buttons')

		#right panel picture
		self.rightPanelPicture = QtWidgets.QLabel()
		self.rightPanelPicture.setPixmap(QtGui.QPixmap('body202cropped.png'))
		
		#this is the layout setup horizontal boxes in a wrapping vertical layout
		h_box_instruct = QtWidgets.QHBoxLayout()
		h_box_instruct.addWidget(self.appTitle)
		
		h_box_buttons = QtWidgets.QHBoxLayout()
		h_box_buttons.addWidget(self.leftButton)
		h_box_buttons.addWidget(self.centerButton)
		h_box_buttons.addWidget(self.rightButton)

		h_box_switch_boundary_line = QtWidgets.QHBoxLayout()
		h_box_switch_boundary_line.addWidget(self.defaultImage)
		h_box_switch_boundary_line.addWidget(self.boundary_lines)

		h_box_ratios = QtWidgets.QHBoxLayout()
		h_box_ratios.addWidget(self.areaRatioButton)
		h_box_ratios.addWidget(self.asymmetryRatioButton)

		h_box_haller_buttons = QtWidgets.QHBoxLayout()
		h_box_haller_buttons.addWidget(self.hallerHorz)
		h_box_haller_buttons.addWidget(self.hallerVert)

		h_box_lungSToV_buttons = QtWidgets.QHBoxLayout()
		h_box_lungSToV_buttons.addWidget(self.lungBackToFront)
		h_box_lungSToV_buttons.addWidget(self.sternumToVertebre)

		h_box_status = QtWidgets.QHBoxLayout()
		h_box_status.addWidget(self.text)

		h_box_curr_slice = QtWidgets.QHBoxLayout()
		h_box_curr_slice.addWidget(self.sliceText)

		h_box_haller_label = QtWidgets.QHBoxLayout()
		h_box_haller_label.addWidget(self.hallerLabel)

		h_box_haller_status = QtWidgets.QHBoxLayout()
		h_box_haller_status.addWidget(self.hallerDisplay)

		h_box_lungSToV_status = QtWidgets.QHBoxLayout()
		h_box_lungSToV_status.addWidget(self.lungSternumToVertebreDisplay)

		h_box_lungSToV_label = QtWidgets.QHBoxLayout()
		h_box_lungSToV_label.addWidget(self.lungSternumToVertebreLabel)
		
		h_box_picture = QtWidgets.QHBoxLayout()
		h_box_picture.addWidget(self.picture)
		h_box_picture.addWidget(self.slider)
		h_box_picture.setAlignment(self.picture, Qt.AlignTop)
		
		vertical_box = QtWidgets.QVBoxLayout()
		vertical_box.addLayout(h_box_instruct)
		vertical_box.addLayout(h_box_buttons)
		vertical_box.addLayout(h_box_switch_boundary_line)
		vertical_box.addLayout(h_box_ratios)
		vertical_box.addLayout(h_box_haller_label)
		vertical_box.addLayout(h_box_haller_buttons)
		vertical_box.addLayout(h_box_lungSToV_label)
		vertical_box.addLayout(h_box_lungSToV_buttons)
		vertical_box.addLayout(h_box_status)
		vertical_box.addLayout(h_box_curr_slice)
		vertical_box.addLayout(h_box_haller_status)		
		vertical_box.addLayout(h_box_lungSToV_status)
		vertical_box.addLayout(h_box_picture)

		right_vertical_box = QtWidgets.QVBoxLayout()
		right_vertical_box.addWidget(self.rightPanelPicture)

		outer_h_box = QtWidgets.QHBoxLayout()
		outer_h_box.addLayout(vertical_box)
		outer_h_box.addLayout(right_vertical_box)
		
		self.setLayout(outer_h_box)
		
		self.show()

	def attachHallerHorzListener(self):
		self.hallerIndex.clearHorz()
		self.picture.attach(self.hallerHorzHandler)
	def attachHallerVertListener(self):
		self.hallerIndex.clearVert()
		self.picture.attach(self.hallerVertHandler)

	def attachHallerLungListener(self):
		self.backToFrontSternumToVertebreRatio.clearLung()
		self.picture.attach(self.lungHandler)
	def attachHallerSTVListener(self):
		self.backToFrontSternumToVertebreRatio.clearSternum()
		self.picture.attach(self.sternumHandler)

	def generateMouseMark(self, event, picture, saveFile):
			image = misc.imread(picture)

			X = image.shape[0]
			Y = image.shape[1]

			coordY = event.x() 
			coordX = event.y() 

			print "x: " + str(event.x()) + " y: " + str(event.y()) 

			image[coordX][coordY][0] = 220
			image[coordX][coordY][1] = 20
			image[coordX][coordY][2] = 60
			for i in range(0,7):
				if(coordY+i < Y):
					image[coordX][coordY+i][0] = 220
					image[coordX][coordY+i][1] = 20
					image[coordX][coordY+i][2] = 60  
				if(coordY-i > 0):
					image[coordX][coordY-i][0] = 220
					image[coordX][coordY-i][1] = 20
					image[coordX][coordY-i][2] = 60
				if(coordX+i < X):
					image[coordX+i][coordY][0] = 220
					image[coordX+i][coordY][1] = 20
					image[coordX+i][coordY][2] = 60
				if(coordX-i > 0):
					image[coordX-i][coordY][0] = 220
					image[coordX-i][coordY][1] = 20
					image[coordX-i][coordY][2] = 60
			misc.imsave(saveFile, image)
			self.picture.setPixmap(QtGui.QPixmap(saveFile))

	def lungHandler(self, event):
		if(self.hallerHoriCount > 0 or self.hallerVertCount > 0):
			self.clearClickAttach(self.currentSlice)
		self.lungCount += 1
		if(self.lungCount > 3):
			self.lungCount = 1
		if not self.backToFrontSternumToVertebreRatio.lungIsSet():
			self.backToFrontSternumToVertebreRatio.setLung(event.y())
			if(self.lungCount == 1 and self.STVCount != 3):
				self.generateMouseMark(event, self.displayPictureFile, 'tempLungSTVRatio.png')
			else:
				self.generateMouseMark(event, 'tempLungSTVRatio.png', 'tempLungSTVRatio.png')
				self.lungCount += 1
		if self.backToFrontSternumToVertebreRatio.lungIsSet():
			self.picture.detach()
			self.STVCount = 0
		self.displayLungSTVRatio()

	def sternumHandler(self, event):
		if(self.hallerHoriCount > 0 or self.hallerVertCount > 0):
			self.clearClickAttach(self.currentSlice)
		self.STVCount += 1
		if(self.STVCount > 3):
			self.STVCount = 1
		if not self.backToFrontSternumToVertebreRatio.sternumIsSet():
			self.backToFrontSternumToVertebreRatio.setSternum(event.y())
			if(self.STVCount == 1 and self.lungCount != 3):
				self.generateMouseMark(event, self.displayPictureFile, 'tempLungSTVRatio.png')
			else:
				self.generateMouseMark(event, 'tempLungSTVRatio.png', 'tempLungSTVRatio.png')
				self.STVCount += 1
		if self.backToFrontSternumToVertebreRatio.sternumIsSet():
			self.picture.detach()
			self.lungCount = 0
		self.displayLungSTVRatio()

	def displayLungSTVRatio(self):
		try:
			index = self.backToFrontSternumToVertebreRatio.calculate()
			self.lungSternumToVertebreDisplay.setText('lung back to front / sternum to vertebre ratio: ' 
				+ str(index))
		except ValueError as e:
			self.lungSternumToVertebreDisplay.setText('lung back to front / sternum to vertebre ratio: ')

	def hallerHorzHandler(self, event):
		if(self.lungCount > 0 or self.STVCount > 0):
			self.clearClickAttach(self.currentSlice)
		self.hallerHoriCount += 1
		if(self.hallerHoriCount > 3):
			self.hallerHoriCount = 1
		if not self.hallerIndex.horzIsSet():
			self.hallerIndex.setHorz(event.x())
			if(self.hallerHoriCount == 1 and self.hallerVertCount != 3):
				self.generateMouseMark(event, self.displayPictureFile, 'tempHaller.png')
			else:
				self.generateMouseMark(event, 'tempHaller.png', 'tempHaller.png')
				self.hallerHoriCount += 1
		if self.hallerIndex.horzIsSet():
			self.picture.detach()
			self.hallerVertCount = 0
		self.displayHallerIndex()

	def hallerVertHandler(self, event):
		if(self.lungCount > 0 or self.STVCount > 0):
			self.clearClickAttach(self.currentSlice)
		self.hallerVertCount += 1
		if(self.hallerVertCount > 3):
			self.hallerVertCount = 1
		if not self.hallerIndex.vertIsSet():
			self.hallerIndex.setVert(event.y())
			if(self.hallerVertCount == 1 and self.hallerHoriCount != 3):
				self.generateMouseMark(event, self.displayPictureFile, 'tempHaller.png')
			else:
				self.generateMouseMark(event, 'tempHaller.png', 'tempHaller.png')
				self.hallerVertCount += 1
		if self.hallerIndex.vertIsSet():
			self.picture.detach()
			self.hallerHoriCount = 0
		self.displayHallerIndex()

	def displayHallerIndex(self):
		try:
			index = self.hallerIndex.calculate()
			self.hallerDisplay.setText('Haller Index: ' + str(index))
		except ValueError as e:
			self.hallerDisplay.setText('Haller Index: ')
				


	def changeSlice(self, sliceNumber):
		#the numbers in the picture from top to bottem goes from 1 to 12 so we have to reverse
		self.text.setText("Please pick an option")
		self.sliceChanged = True
		self.ran_asymmetry_ratio = False
		self.ran_defect_chest_ratio = False

		self.hallerHoriCount = 0
		self.hallerVertCount = 0

		if sliceNumber == 12:
			self.sliceText.setText('You are currently on slice 1')
			self.switchDefaultImage(self.slice1)
		elif sliceNumber == 11:
			self.sliceText.setText('You are currently on slice 2')
			self.switchDefaultImage(self.slice2)
		elif sliceNumber == 10:
			self.sliceText.setText('You are currently on slice 3')
			self.switchDefaultImage(self.slice3)
		elif sliceNumber == 9:
			self.sliceText.setText('You are currently on slice 4')
			self.switchDefaultImage(self.slice4)
		elif sliceNumber == 8:
			self.sliceText.setText('You are currently on slice 5')
			self.switchDefaultImage(self.slice5)
		elif sliceNumber == 7:
			self.sliceText.setText('You are currently on slice 6')
			self.switchDefaultImage(self.slice6)
		elif sliceNumber == 6:
			self.sliceText.setText('You are currently on slice 7')
			self.switchDefaultImage(self.slice7)
		elif sliceNumber == 5:
			self.sliceText.setText('You are currently on slice 8')
			self.switchDefaultImage(self.slice8)
		elif sliceNumber == 4:
			self.sliceText.setText('You are currently on slice 9')
			self.switchDefaultImage(self.slice9)
		elif sliceNumber == 3:
			self.sliceText.setText('You are currently on slice 10')
			self.switchDefaultImage(self.slice10)
		elif sliceNumber == 2:
			self.sliceText.setText('You are currently on slice 11')
			self.switchDefaultImage(self.slice11)
		elif sliceNumber == 1:
			self.sliceText.setText('You are currently on slice 12')
			self.switchDefaultImage(self.slice12)

	def setLeftBoundary(self):
		maxPercent = (float(self.centerBoundaryRatio) * 100) - 1
		if(maxPercent < 0):
			maxPercent = 0
		currentPercent = float(self.leftBoundaryRatio) * 100

		percent, ok = QtWidgets.QInputDialog.getInt(self, "Set Left Boundary", "Percentage of Image:", currentPercent, 5, maxPercent, 1)
		self.leftBoundaryRatio = float(percent) / 100
		if(ok):
			self.boundaryRatiosChanged = True
			self.text.setText('Please select an option')
			self.switchDefaultImage(self.currentSlice)
			self.displayBoundaryLine()
			self.ran_defect_chest_ratio = False
			self.ran_asymmetry_ratio = False
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
			self.switchDefaultImage(self.currentSlice)
			self.displayBoundaryLine()
			self.ran_defect_chest_ratio = False
			self.ran_asymmetry_ratio = False
			print "successfully set new center boundary ratio"

	def setRightBoundary(self):
		minPercent = (float(self.centerBoundaryRatio) * 100) + 1
		currentPercent = float(self.rightBoundaryRatio) * 100

		percent, ok = QtWidgets.QInputDialog.getInt(self, "Set Right line", "Percentage of Image:", currentPercent, minPercent, 95, 1)
		self.rightBoundaryRatio = float(percent) / 100
		if(ok):
			self.boundaryRatiosChanged = True
			self.text.setText('Please select an option')
			self.switchDefaultImage(self.currentSlice)
			self.displayBoundaryLine()
			self.ran_defect_chest_ratio = False
			self.ran_asymmetry_ratio = False
			print "successfully set new right boundary ratio"

	def switchDefaultImageButton(self):	
		self.switchDefaultImage(self.currentSlice)


	def switchDefaultImage(self, sliceNumber):
		self.hallerHoriCount = 0 
		self.lungCount = 0 
		self.STVCount = 0 
		self.hallerVertCount = 0 
		self.hallerIndex.clearHorz()
		self.hallerIndex.clearVert()
		self.backToFrontSternumToVertebreRatio.clearLung()
		self.backToFrontSternumToVertebreRatio.clearSternum()
		self.hallerDisplay.setText('Haller Index: ')
		self.lungSternumToVertebreDisplay.setText('lung back to front / sternum to vertebre ratio: ')

		self.picture.detach()
		self.currentSlice = sliceNumber
		self.displayPictureFile = sliceNumber
		self.boundaryLineOn = False
		self.picture.setPixmap(QtGui.QPixmap(self.displayPictureFile))

	def clearClickAttach(self, sliceNumber):
		self.hallerHoriCount = 0 
		self.lungCount = 0 
		self.STVCount = 0 
		self.hallerVertCount = 0 
		self.hallerIndex.clearHorz()
		self.hallerIndex.clearVert()
		self.backToFrontSternumToVertebreRatio.clearLung()
		self.backToFrontSternumToVertebreRatio.clearSternum()
		self.hallerDisplay.setText('Haller Index: ')
		self.lungSternumToVertebreDisplay.setText('lung back to front / sternum to vertebre ratio: ')

		self.currentSlice = sliceNumber
		self.displayPictureFile = sliceNumber
		self.boundaryLineOn = False
		self.picture.setPixmap(QtGui.QPixmap(self.displayPictureFile))

	def clearClickAttachWithDetach(self):
		self.hallerHoriCount = 0 
		self.lungCount = 0 
		self.STVCount = 0 
		self.hallerVertCount = 0 
		self.hallerIndex.clearHorz()
		self.hallerIndex.clearVert()
		self.backToFrontSternumToVertebreRatio.clearLung()
		self.backToFrontSternumToVertebreRatio.clearSternum()
		self.hallerDisplay.setText('Haller Index: ')
		self.lungSternumToVertebreDisplay.setText('lung back to front / sternum to vertebre ratio: ')
		self.picture.detach()


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
		self.clearClickAttachWithDetach()
		if(self.centerBoundaryRatio > .65 or self.centerBoundaryRatio < .35):
			self.text.setText('***the center boundary has to be less than 66% or greater then 34% to perform this calculation***')
			return 
		if(self.ran_defect_chest_ratio and not self.boundaryRatiosChanged and not self.sliceChanged):
			self.displayPictureFile = 'outfile2.png'
			self.boundaryLineOn = False
			self.text.setText(self.defectChestRatioSolution)
			self.picture.setPixmap(QtGui.QPixmap(self.displayPictureFile))
		else:
			chestPixels = self.pixelCount('chest', self.currentSlice)
			defectPixels = self.pixelCount('defect', "outfile.png")
			ratio = float(defectPixels) / chestPixels

			self.defectChestRatioSolution = ('Defect contains: ' + str(defectPixels) + ' pixels. Chest contains: ' + str(chestPixels) 
				+ ' pixels. The defect / chest ratio is: ' + str(ratio))
			self.text.setText(self.defectChestRatioSolution)

	def calculateAsymmetryRatio(self):
		self.clearClickAttachWithDetach()
		if(self.ran_asymmetry_ratio and not self.boundaryRatiosChanged and not self.sliceChanged):
			self.displayPictureFile = 'outfileRight.png'
			self.boundaryLineOn = False
			self.text.setText(self.asymmetricRatio)
			self.picture.setPixmap(QtGui.QPixmap(self.displayPictureFile))
		else:
			leftPixels = self.pixelCount('left', self.currentSlice)
			rightPixels = self.pixelCount('right', "outfileLeft.png")
			ratio = float(leftPixels) / rightPixels
					
			self.asymmetricRatio = ('Left contains: ' + str(leftPixels) + ' pixels. Right contains: ' + str(rightPixels) 
				+ ' pixels. The left / right ratio is: ' + str(ratio))
			self.text.setText(self.asymmetricRatio)
		
		
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
			self.sliceChanged = False
			self.picture.setPixmap(QtGui.QPixmap(self.displayPictureFile))
		elif(areaType == 'left'):
			misc.imsave('outfileLeft.png', image)
		elif(areaType == 'right'):
			misc.imsave('outfileRight.png', image)
			self.displayPictureFile = 'outfileRight.png'
			self.ran_asymmetry_ratio = True
			self.boundaryRatiosChanged = False
			self.boundaryLineOn = False
			self.sliceChanged = False
			self.picture.setPixmap(QtGui.QPixmap(self.displayPictureFile))

		return Area_Pixels
		
	
app = QtWidgets.QApplication(sys.argv)
window = AreaRatioWindow()
sys.exit(app.exec_())
