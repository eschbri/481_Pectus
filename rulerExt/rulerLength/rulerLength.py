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

  xAxisRuler.append(1)
  xAxisRuler.append(2)
  xAxisRuler.append(3)

  rulerRatios = []
  rulerRatios.append(ratioLeft)
  rulerRatios.append(ratioRight)
  rulerRatios.append(ratioAvg)

  for i in range(0, 3):
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
