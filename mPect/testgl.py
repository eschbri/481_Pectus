from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtGui
from PyQt4.QtOpenGL import *

from ctypes import sizeof, c_float, c_uint, c_void_p
from linalg import matrix as m
from linalg import quaternion as q

import cube

class PectusGL(QGLWidget):
    def __init__(self, verts, norms, faces, parent = None):
        super(PectusGL, self).__init__(parent)
        self.verts = verts
        self.norms = norms
        self.faces = faces

        self.lastPos = QtCore.QPoint()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        #glVertexPointer(3, GL_FLOAT, self.recordLen, self.vertexOffset)
        #glNormalPointer(GL_FLOAT, self.recordLen, self.normalOffest)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glScale(.5, .5, .5)
        glMultMatrixf(m.column_major(q.matrix(q.quaternion())))

        offset = 0
	for size in cube.sizes:
		glBegin(GL_TRIANGLE_STRIP)
		for i in range(offset, offset+size):
			index = cube.indicies[i]
			glColor3f(*cube.colors[index])
			glNormal3f(*cube.normals[index])
			glVertex3f(*cube.verticies[index])
		glEnd()
		offset += size

        glPopMatrix()

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def resizeGL(self, w, h):
        print("Resize")

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)

        self.__init_object()

    def __init_object(self):
        print("Do nothing")
        '''
        # enable arrays
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        # Get data and calculate offsets
        indicies = cube.indicies
        data = self.__flatten(*zip(self.verts, self.norms))
        self.vertexOffset = c_void_p(0 * sizeof(c_float))
        self.normalOffest = c_void_p(3 * sizeof(c_float))
        self.recordLen = 6 * sizeof(c_float)

        # Copy data to buffers
        indiciesBuffer = (c_uint*len(indicies))(*indicies)
        dataBuffer = (c_float*len(data))(*data)

        # Load buffers to GPU
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indiciesBuffer, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, dataBuffer, GL_STATIC_DRAW)
        '''

    def __flatten(self, *lll):
        return [u for ll in lll for l in ll for u in l]



if __name__ == '__main__':
    app = QtGui.QApplication(["Winfred's PyQt OpenGL"])
    widget = PectusGL(cube.verticies, cube.normals, cube.faces)
    widget.show()
    app.exec_()
