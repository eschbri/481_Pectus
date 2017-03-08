#include "Controls.h"
#include <GLFW/glfw3.h>
#define GLM_FORCE_RADIANS
#include <glm/gtc/matrix_transform.hpp>
#include <iostream>

using namespace std;

Controls::Controls(GLFWwindow* window_)
	: lastTime(glfwGetTime()), verticalAngle(0.0f), horizontalAngle(3.14f), fov(45.0f), window(window_)
{
}

void Controls::update(){
	// Compute time difference between current and last frame
	double currentTime = glfwGetTime();
	
	// Move forward
	if (glfwGetKey( window, GLFW_KEY_UP ) == GLFW_PRESS){
		camera.moveForward();
	}
	// Move backward
	if (glfwGetKey( window, GLFW_KEY_DOWN ) == GLFW_PRESS){
		camera.moveBackward();
	}
	// Strafe right
	if (glfwGetKey( window, GLFW_KEY_RIGHT ) == GLFW_PRESS){
		camera.straceRight();
	}
	// Strafe left
	if (glfwGetKey( window, GLFW_KEY_LEFT ) == GLFW_PRESS){
		camera.strafeLeft();
	}

	// For the next frame, the "last time" will be "now"
	lastTime = currentTime;
}

void Controls::updateViewMatrix(glm::mat4& viewMat){
	viewMat = camera.getWorldToViewMatrix();
}

void Controls::updateProjectionMatrix(glm::mat4& projMat){
	projMat = glm::perspective(fov, 4.0f / 3.0f, 0.1f, 100.0f);
}

