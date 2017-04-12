""" 
Modern OpenGL with python. 
render a color triangle with pyopengl using PySide/PyQt4. 
 
@author: Mack Stone 
"""  
  
import ctypes  
  
import numpy  
from OpenGL.GL import *  
from OpenGL.GL import shaders  
from PyQt4 import QtGui, QtOpenGL  

import cube
  
VERTEX_SHADER = """ 
#version 330 
 
layout (location=0) in vec3 position; 
layout (location=1) in vec3 color; 
 
out vec3 theColor; 
 
void main() 
{ 
    gl_Position = vec4(position, 1); 
    theColor = color;
} 
"""  
  
FRAGMENT_SHADER = """ 
#version 330 
 
in vec3 theColor; 
out vec4 outputColor; 
 
void main() 
{ 
    outputColor = vec4(theColor, 1); 
} 
"""  
  
class PectusGL(QtOpenGL.QGLWidget):  
    def __init__(self, verts, norms, faces, parent = None):
        super(PectusGL, self).__init__(parent)
        self.verts = numpy.array(verts, dtype=numpy.float32)
        self.norms = numpy.array(norms, dtype=numpy.float32)
        self.colors = numpy.array(cube.colors, dtype=numpy.float32)

        self.normOffset = self.verts.nbytes
        self.colorOffset = self.normOffset + self.norms.nbytes

        self.faces = (ctypes.c_uint * len(faces))(*faces)
        #self.faces = numpy.array(faces, dtype=numpy.uint32)

    def initializeGL(self):  
        glViewport(0, 0, self.width(), self.height())  
  
        # compile shaders and program  
        vertexShader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)  
        fragmentShader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)  
        self.shaderProgram = shaders.compileProgram(vertexShader, fragmentShader)  
  
        # triangle position and color  
        vertexData = numpy.array([0.0, 0.5, 0.0,  
                                0.5, -0.366, 0.0,
                                -0.5, -0.366, 0.0, 
                                1.0, 0.0, 0.0, 
                                0.0, 1.0, 0.0, 
                                0.0, 0.0, 1.0, ],  
                                dtype=numpy.float32)  
  
        # create VAO  
        self.VAO = glGenVertexArrays(1)  
        glBindVertexArray(self.VAO)  
  
        # create allData
        alldata = numpy.concatenate((self.verts, self.norms, self.colors))

        # create VBO
        VBO = glGenBuffers(1)  
        glBindBuffer(GL_ARRAY_BUFFER, VBO)  
        glBufferData(GL_ARRAY_BUFFER, alldata.nbytes, alldata, GL_STATIC_DRAW)  
  
        # enable array and set up data  
        glEnableVertexAttribArray(0)  
        glEnableVertexAttribArray(1)  
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)  
        # the last parameter is a pointer  
        # python donot have pointer, have to using ctypes  
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(9 * ctypes.sizeof(ctypes.c_float))  )
  
        glBindBuffer(GL_ARRAY_BUFFER, 0)  
        glBindVertexArray(0)  
  
    def paintGL(self):  
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  
  
        glBindVertexArray(self.VAO)  
  
        # draw triangle  
        glDrawElements(GL_TRIANGLES, len(self.faces), GL_UNSIGNED_INT, 0);
  
        glBindVertexArray(0)  
        glUseProgram(0)  
  
  
def main():  
    import sys  
  
    app = QtGui.QApplication(sys.argv)  
  
    glformat = QtOpenGL.QGLFormat()  
    glformat.setVersion(3, 3)  
    glformat.setProfile(QtOpenGL.QGLFormat.CoreProfile)  
    w = PectusGL(cube.verts, cube.norms, cube.faces, glformat)  
    w.resize(640, 480)  
    w.show()  
    sys.exit(app.exec_())  
  
if __name__ == '__main__':  
    main()  
