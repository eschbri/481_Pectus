import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# rulerLength
#

class rulerLength(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "rulerLength" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["John Doe (AnyWare Corp.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    It performs a simple thresholding on the input volume and optionally captures a screenshot.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# rulerLengthWidget
#

class rulerLengthWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # input volume selector
    #
    """
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume: ", self.inputSelector)
    


    #
    # output volume selector
    #
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.outputSelector.selectNodeUponCreation = True
    self.outputSelector.addEnabled = True
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = True
    self.outputSelector.showHidden = False
    self.outputSelector.showChildNodeTypes = False
    self.outputSelector.setMRMLScene( slicer.mrmlScene )
    self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    parametersFormLayout.addRow("Output Volume: ", self.outputSelector)

    #
    # threshold value
    #
    self.imageThresholdSliderWidget = ctk.ctkSliderWidget()
    self.imageThresholdSliderWidget.singleStep = 0.1
    self.imageThresholdSliderWidget.minimum = -100
    self.imageThresholdSliderWidget.maximum = 100
    self.imageThresholdSliderWidget.value = 0.5
    self.imageThresholdSliderWidget.setToolTip("Set threshold value for computing the output image. Voxels that have intensities lower than this value will set to zero.")
    parametersFormLayout.addRow("Image threshold", self.imageThresholdSliderWidget)

    #
    # check box to trigger taking screen shots for later use in tutorials
    #
    self.enableScreenshotsFlagCheckBox = qt.QCheckBox()
    self.enableScreenshotsFlagCheckBox.checked = 0
    self.enableScreenshotsFlagCheckBox.setToolTip("If checked, take screen shots for tutorials. Use Save Data to write them to disk.")
    parametersFormLayout.addRow("Enable Screenshots", self.enableScreenshotsFlagCheckBox)

    """

    #
    # ruler left selector
    #
    
    self.rulerSelector = slicer.qMRMLNodeComboBox()
    self.rulerSelector.nodeTypes = ["vtkMRMLAnnotationRulerNode"]
    self.rulerSelector.selectNodeUponCreation = True
    self.rulerSelector.addEnabled = False
    self.rulerSelector.removeEnabled = False
    self.rulerSelector.noneEnabled = False
    self.rulerSelector.showHidden = False
    self.rulerSelector.showChildNodeTypes = False
    self.rulerSelector.setMRMLScene( slicer.mrmlScene )
    self.rulerSelector.setToolTip( "Pick the left ruler to the algorithm." )
    parametersFormLayout.addRow("Left Ruler: ", self.rulerSelector)

    #
    # ruler middle selector
    #
    
    self.rulerSelector2 = slicer.qMRMLNodeComboBox()
    self.rulerSelector2.nodeTypes = ["vtkMRMLAnnotationRulerNode"]
    self.rulerSelector2.selectNodeUponCreation = True
    self.rulerSelector2.addEnabled = False
    self.rulerSelector2.removeEnabled = False
    self.rulerSelector2.noneEnabled = False
    self.rulerSelector2.showHidden = False
    self.rulerSelector2.showChildNodeTypes = False
    self.rulerSelector2.setMRMLScene( slicer.mrmlScene )
    self.rulerSelector2.setToolTip( "Pick the middle ruler to the algorithm." )
    parametersFormLayout.addRow("Center Ruler: ", self.rulerSelector2)

    #
    # ruler right selector
    #
    
    self.rulerSelector3 = slicer.qMRMLNodeComboBox()
    self.rulerSelector3.nodeTypes = ["vtkMRMLAnnotationRulerNode"]
    self.rulerSelector3.selectNodeUponCreation = True
    self.rulerSelector3.addEnabled = False
    self.rulerSelector3.removeEnabled = False
    self.rulerSelector3.noneEnabled = False
    self.rulerSelector3.showHidden = False
    self.rulerSelector3.showChildNodeTypes = False
    self.rulerSelector3.setMRMLScene( slicer.mrmlScene )
    self.rulerSelector3.setToolTip( "Pick the right ruler to the algorithm." )
    parametersFormLayout.addRow("Right Ruler: ", self.rulerSelector3)
    


    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("See Chart")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = True
    parametersFormLayout.addRow(self.applyButton)

    #table button
    self.tableButton = qt.QPushButton("See Table")
    self.tableButton.toolTip = "display table"
    self.tableButton.enabled = True
    parametersFormLayout.addRow(self.tableButton)


    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.tableButton.connect('clicked(bool)', self.onTableButton)
    """
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    """

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.rulerSelector.currentNode()
    #self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

  def onApplyButton(self):
    logic = rulerLengthLogic()
    logic.run(self.rulerSelector.currentNode(), self.rulerSelector2.currentNode(), self.rulerSelector3.currentNode(), True)
    """
    enableScreenshotsFlag = self.enableScreenshotsFlagCheckBox.checked
    imageThreshold = self.imageThresholdSliderWidget.value
    logic.run(self.inputSelector.currentNode(), self.outputSelector.currentNode(), imageThreshold, enableScreenshotsFlag)
    """
  def onTableButton(self):
    logic = rulerLengthLogic()
    logic.run(self.rulerSelector.currentNode(), self.rulerSelector2.currentNode(), self.rulerSelector3.currentNode(), False)

#
# rulerLengthLogic
#

class rulerLengthLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def hasImageData(self,volumeNode):
    """This is an example logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      logging.debug('hasImageData failed: no volume node')
      return False
    if volumeNode.GetImageData() is None:
      logging.debug('hasImageData failed: no image data in volume node')
      return False
    return True

  def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
    """Validates if the output is not the same as input
    """
    if not inputVolumeNode:
      logging.debug('isValidInputOutputData failed: no input volume node defined')
      return False
    if not outputVolumeNode:
      logging.debug('isValidInputOutputData failed: no output volume node defined')
      return False
    if inputVolumeNode.GetID()==outputVolumeNode.GetID():
      logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
      return False
    return True

  def takeScreenshot(self,name,description,type=-1):
    # show the message even if not taking a screen shot
    slicer.util.delayDisplay('Take screenshot: '+description+'.\nResult is available in the Annotations module.', 3000)

    lm = slicer.app.layoutManager()
    # switch on the type to get the requested window
    widget = 0
    if type == slicer.qMRMLScreenShotDialog.FullLayout:
      # full layout
      widget = lm.viewport()
    elif type == slicer.qMRMLScreenShotDialog.ThreeD:
      # just the 3D window
      widget = lm.threeDWidget(0).threeDView()
    elif type == slicer.qMRMLScreenShotDialog.Red:
      # red slice window
      widget = lm.sliceWidget("Red")
    elif type == slicer.qMRMLScreenShotDialog.Yellow:
      # yellow slice window
      widget = lm.sliceWidget("Yellow")
    elif type == slicer.qMRMLScreenShotDialog.Green:
      # green slice window
      widget = lm.sliceWidget("Green")
    else:
      # default to using the full window
      widget = slicer.util.mainWindow()
      # reset the type so that the node is set correctly
      type = slicer.qMRMLScreenShotDialog.FullLayout

    # grab and convert to vtk image data
    qpixMap = qt.QPixmap().grabWidget(widget)
    qimage = qpixMap.toImage()
    imageData = vtk.vtkImageData()
    slicer.qMRMLUtils().qImageToVtkImageData(qimage,imageData)

    annotationLogic = slicer.modules.annotations.logic()
    annotationLogic.CreateSnapShot(name, description, type, 1, imageData)

  #def run(self, inputVolume, outputVolume, imageThreshold, enableScreenshots=0):
  def run(self, rulerSelector, rulerSelector2, rulerSelector3, displayChart):
    """
    Run the actual algorithm
    """

    print 'RUN FUNCTION'

    print 'ruler left: ' + str(rulerSelector.GetDistanceMeasurement())
    print 'ruler middle: ' + str(rulerSelector2.GetDistanceMeasurement())
    print 'ruler right: ' + str(rulerSelector3.GetDistanceMeasurement())
    ratioLeft = rulerSelector.GetDistanceMeasurement() / rulerSelector2.GetDistanceMeasurement()
    print 'ratio: ' + str(ratioLeft)
    ratioRight = rulerSelector3.GetDistanceMeasurement() / rulerSelector2.GetDistanceMeasurement()
    print 'ratio: ' + str(ratioRight)
    ratioAvg = (ratioLeft + ratioRight) / 2
    print 'Avg ratio: ' + str(ratioAvg)
    if(displayChart):
        createChart(ratioLeft, ratioRight, ratioAvg)
    else:
        createTable(ratioLeft, ratioRight, ratioAvg)





    """

    if not self.isValidInputOutputData(inputVolume, outputVolume):
      slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
      return False

    logging.info('Processing started')

    # Compute the thresholded output volume using the Threshold Scalar Volume CLI module
    cliParams = {'InputVolume': inputVolume.GetID(), 'OutputVolume': outputVolume.GetID(), 'ThresholdValue' : imageThreshold, 'ThresholdType' : 'Above'}
    cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True)

    # Capture screenshot
    if enableScreenshots:
      self.takeScreenshot('rulerLengthTest-Start','MyScreenshot',-1)

    logging.info('Processing completed')

    """

    return True

def createChart(ratioLeft, ratioRight, ratioAvg):

  """
  make bar chart of ratios
  """
  #change to a layout with a chart viewer
  layoutM = slicer.app.layoutManager()
  layoutM.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpQuantitativeView)

  arrayNode = slicer.mrmlScene.AddNode(slicer.vtkMRMLDoubleArrayNode())
  array = arrayNode.GetArray()
  array.SetNumberOfTuples(3)
  array.SetNumberOfComponents(3)

  xAxisRuler = []
  #xAxisRuler.append('Left Left')
  #xAxisRuler.append('Right Ratio')
  #xAxisRuler.append('Avg ratio')
  xAxisRuler.append(1)
  xAxisRuler.append(2)
  xAxisRuler.append(3)

  rulerRatios = []
  rulerRatios.append(ratioLeft)
  rulerRatios.append(ratioRight)
  rulerRatios.append(ratioAvg)

  for i in range(0, 3):
    #print 'xaxis: ' + str(xAxisRuler[i]) + ' ruleratios: ' + str(rulerRatios[i])
    array.SetComponent(i, 0, xAxisRuler[i])
    array.SetComponent(i, 1, rulerRatios[i])
    array.SetComponent(i, 2, 0)


  #chart view node
  chartVNodes = slicer.mrmlScene.GetNodesByClass('vtkMRMLChartViewNode')
  chartVNodes.SetReferenceCount(chartVNodes.GetReferenceCount()-1)
  chartVNodes.InitTraversal()
  chartVNode = chartVNodes.GetNextItemAsObject()

  chartNode = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())

  chartNode.SetProperty('default', 'title', 'Length Ratios')
  chartNode.SetProperty('default', 'yAxisLabel', 'Ratios')
  chartNode.SetProperty('default', 'xAxisLabel', 'Rulers')
  chartNode.SetProperty('default', 'type', 'Scatter')
  chartNode.SetProperty('default', 'xAxisType', 'categorical')
  chartNode.SetProperty('default', 'showLegend', 'off')

  chartNode.AddArray('Ratios', arrayNode.GetID())
  chartVNode.SetChartNodeID(chartNode.GetID())


    #chartNode.setProperty('Ratios', 'lookupTable', )

def createTable(ratioLeft, ratioRight, ratioAvg):
  """
  make table ratios
  """
  tableObj = slicer.vtkMRMLTableNode()

  #Making table columns
  col = tableObj.AddColumn()
  col.SetName("Index Label")

  col = tableObj.AddColumn()
  col.SetName("Ruler left|right / ruler center")

  col = tableObj.AddColumn()
  col.SetName("Ratios")

  rIndex = tableObj.AddEmptyRow()
  cIndex = 0

  tableObj.SetCellText(rIndex, cIndex, str(1))
  cIndex += 1
  tableObj.SetCellText(rIndex, cIndex, "Ruler Left / Ruler Center")
  cIndex += 1
  tableObj.SetCellText(rIndex, cIndex, str(ratioLeft))

  rIndex = tableObj.AddEmptyRow()
  cIndex = 0
  tableObj.SetCellText(rIndex, cIndex, str(2))
  cIndex += 1
  tableObj.SetCellText(rIndex, cIndex, "Ruler Right / Ruler Center")
  cIndex += 1
  tableObj.SetCellText(rIndex, cIndex, str(ratioRight))

  rIndex = tableObj.AddEmptyRow()
  cIndex = 0
  tableObj.SetCellText(rIndex, cIndex, str(3))
  cIndex += 1
  tableObj.SetCellText(rIndex, cIndex, "Avg Ratios")
  cIndex += 1
  tableObj.SetCellText(rIndex, cIndex, str(ratioAvg))

  #add table to gui
  slicer.mrmlScene.AddNode(tableObj)
  slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpTableView)
  slicer.app.applicationLogic().GetSelectionNode().SetReferenceActiveTableID(tableObj.GetID())
  slicer.app.applicationLogic().PropagateTableSelection()


class rulerLengthTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_rulerLength1()

  def test_rulerLength1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        logging.info('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        logging.info('Loading %s...' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = rulerLengthLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
