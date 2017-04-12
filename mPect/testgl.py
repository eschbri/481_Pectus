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
        self.verts = self.__flatten(verts)
        self.norms = self.__flatten(norms)
        self.faces = self.__flatten(faces)
        self.colors = self.__flatten(cube.colors)
        self.uniforms = ['fullTransformMatrix']
        self.uniformLocations = {}

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glVertexPointer(3, GL_FLOAT, 0, self.verts)
        glNormalPointer(GL_FLOAT, 0, self.norms)
        glColorPointer(3, GL_FLOAT, 0, self.colors)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glScale(.5, .5, .5)
        glMultMatrixf(m.column_major(q.matrix(q.quaternion())))

        offset = 0
	for size in cube.sizes:
            glDrawElements(GL_TRIANGLE_STRIP, size, GL_UNSIGNED_INT, cube.indicies[offset:offset + size])
	    offset += size

        glPopMatrix()

    def resizeGL(self, w, h):
        print("Resize")

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)

        self.__initProgram()
        self.__initObject()

    def __initObject(self):
        print("Do nothing")
        # enable arrays
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        '''
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

    def __initProgram(self):
        vertShader = self.__compileShader(GL_VERTEX_SHADER, 'VertexShaderCode.glsl')
        fragShader = self.__compileShader(GL_FRAGMENT_SHADER, 'FragmentShaderCode.glsl')

        program = glCreateProgram()
        glAttachShader(program, vertShader)
        glAttachShader(program, fragShader)

	if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
		raise RuntimeError(glGetProgramInfoLog(program))
	
	for uniform in self.uniforms:
		self.locations[uniform] = glGetUniformLocation(program, uniform)
	
	glUseProgram(program)

    def __compileShader(self, shader_type, sourceFile):
        with open(sourceFile, 'r') as f:
            shader = glCreateShader(shader_type)
            glShaderSource(shader, f.read())
            glCompileShader(shader)
            if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
                raise RuntimeError(glGetShaderInfoLog(shader))
            return shader
        
    def __flatten(self, *lll):
        return [u for ll in lll for l in ll for u in l]



if __name__ == '__main__':
    app = QtGui.QApplication(["Winfred's PyQt OpenGL"])
    widget = PectusGL(cube.verticies, cube.normals, cube.faces)
    widget.show()
    app.exec_()
