#include <stdio.h>
#include <stdlib.h>
#include <iostream>

// Include GLEW, Always before gl.h and glfw.h because apparently its magic
#include <GL/glew.h>

#include <GLFW/glfw3.h>

#define GLM_FORCE_RADIANS
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

#include "common.h"
#include "Window.h"

using namespace glm;
using namespace std;

static const GLfloat g_vertex_buffer_data[] = {
	0.0f,  1.0f, 0.0f,
	1.0f, 0.0f, 0.0f,

	-1.0f, -1.0f, 0.0f,
	0.0f, 1.0f, 0.0f,

	1.0f, -1.0f, 0.0f,
	0.0f, 0.0f, 1.0f,
};

int main(){
	Window glfwWindow(1024, 768, "Hello World");

	// Initialize GLEW
	glewExperimental=true; // Needed in core profile
	if (glewInit() != GLEW_OK) {
		fprintf(stderr, "Failed to initialize GLEW\n");
		return -1;
	}

	// Black background
	glClearColor(0.0f, 0.0f, 0.0f, 0.0f);

	// Create Vertex Array Object
	GLuint VertexArrayID;
	glGenVertexArrays(1, &VertexArrayID);
	glBindVertexArray(VertexArrayID);

	// Create vertex buffer array
	GLuint vertexbuffer;
	glGenBuffers(1, &vertexbuffer);
	glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);
	glBufferData(GL_ARRAY_BUFFER, sizeof(g_vertex_buffer_data), g_vertex_buffer_data, GL_STATIC_DRAW);

	// Create and compile our GLSL program from the shaders
	GLuint programID = LoadShaders("SimpleVertexShader.vertexshader", "SimpleFragmentShader.fragmentshader");
	glUseProgram(programID);

	// Add vertex attribute to the vertex buffer array
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(
		0,                  // attribute 0. No particular reason for 0, but must match the layout in the shader.
		3,                  // size
		GL_FLOAT,           // type
		GL_FALSE,           // normalized?
		sizeof(float) * 6,                  // stride
		(void*)0            // array buffer offset
	);

	glEnableVertexAttribArray(1);
	glVertexAttribPointer(
			1,
			3,
			GL_FLOAT,
			GL_FALSE,
			sizeof(float) * 6,
			(char*)(sizeof(float) * 3)
			);

	// Create a matrix for transformations
	GLuint matrixId = glGetUniformLocation(programID, "mvp");
	glm::mat4 model = glm::mat4(1.0f); // Create identity matrix
	glm::mat4 view = glm::lookAt(glm::vec3(4, 3, 3), // Camera is at (4, 3, 3) in world space
			glm::vec3(0, 0, 0), // and looks at the origin
			glm::vec3(0, 1, 0)); // Head is up (set to 0, -1, 0 to look upside down
	glm::mat4 projection = glm::perspective(45.0f / 4.0f, 4.0f / 3.0f, 0.1f, 100.0f);
	glm::mat4 mvp = projection * view * model;
	glUniformMatrix4fv(matrixId, 1, GL_FALSE, &mvp[0][0]);

	while(!glfwWindow.closed()){
		// Clear screen
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

		// Draw the triangle !
		glDrawArrays(GL_TRIANGLES, 0, 3); // Starting from vertex 0; 3 vertices total -> 1 triangle

		// Swap buffers
		glfwWindow.swapBuffers();
	}

	return 0;
}
