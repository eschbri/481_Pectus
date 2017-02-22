#include <stdio.h>
#include <stdlib.h>
#include <iostream>

// Include GLEW, Always before gl.h and glfw.h because apparently its magic
#include <GL/glew.h>

#define GLM_FORCE_RADIANS
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

#include "common.h"
#include "Window.h"
#include "Controls.h"

using namespace glm;
using namespace std;

int main(){
	Window glfwWindow(1024, 768, "Hello World");
	Controls control(glfwWindow.getWindow());

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

	// Read in obj file
	vector<glm::vec3> verticies;
	vector<glm::vec2> uvs;
	vector<glm::vec3> normals;
	bool res = loadOBJ("../PT18E.obj", verticies, uvs, normals);
	if (!res){
		cerr << "Failed to load obj file\n";
		return -1;
	}
	vector<glm::vec3> colors;
	for (int i = 0; i < verticies.size(); ++i){
		colors.push_back(vec3(static_cast <float> (rand()) / static_cast <float> (RAND_MAX),
		static_cast <float> (rand()) / static_cast <float> (RAND_MAX),
		static_cast <float> (rand()) / static_cast <float> (RAND_MAX)));
	}

	// Create and compile our GLSL program from the shaders
	GLuint programID = LoadShaders("VertexShader.vertexshader", "FragmentShader.fragmentshader");
	glUseProgram(programID);

	// Create vertex buffer array
	GLuint vertexbuffer;
	glGenBuffers(1, &vertexbuffer);
	glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);
	glBufferData(GL_ARRAY_BUFFER, verticies.size() * sizeof(glm::vec3), &verticies[0], GL_STATIC_DRAW);

	// Add vertex attribute to the vertex buffer array
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(
			0,                  // attribute 0. No particular reason for 0, but must match the layout in the shader.
			3,                  // size
			GL_FLOAT,           // type
			GL_FALSE,           // normalized?
			0,                  // stride
			(char*)0            // array buffer offset
			);

	// Create and bind color buffer
	GLuint colorBufferId;
	glGenBuffers(1, & colorBufferId);
	glBindBuffer(GL_ARRAY_BUFFER, colorBufferId);
	glBufferData(GL_ARRAY_BUFFER, colors.size() * sizeof(glm::vec3), &colors[0], GL_STATIC_DRAW);
	
	// Add vertex attribute to color buffer
	glEnableVertexAttribArray(1);
	glVertexAttribPointer(
			1,
			3,
			GL_FLOAT,
			GL_FALSE,
			0,
			(char*)0
			);

	// Create a matrix for transformations
	GLuint matrixId = glGetUniformLocation(programID, "mvp");

	// Enable depth test
	glEnable(GL_DEPTH_TEST);
	glDepthFunc(GL_LESS);

	glm::mat4 model = glm::mat4(1.0f); // Create identity matrix
	glm::mat4 view; 
	glm::mat4 projection;

	while(!glfwWindow.closed()){
		// Clear screen
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

		// Read in controls and update the MVP matrix
		control.update();
		control.updateViewMatrix(view);
		control.updateProjectionMatrix(projection);
		glm::mat4 mvp = projection * view * model; // Order goes projection * (view * model)
		glUniformMatrix4fv(matrixId, 1, GL_FALSE, &mvp[0][0]);

		// Draw the triangle !
		glDrawArrays(GL_TRIANGLES, 0, verticies.size());

		// Swap buffers
		glfwWindow.swapBuffers();
	}

	return 0;
}
