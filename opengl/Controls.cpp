#include "Controls.h"
#include <GLFW/glfw3.h>
#define GLM_FORCE_RADIANS
#include <glm/gtc/matrix_transform.hpp>
#include <iostream>

using namespace std;

Controls::Controls(GLFWwindow* window_)
	: speed(3.0f), verticalAngle(0.0f), horizontalAngle(3.14f), fov(45.0f), window(window_)
{
	position = glm::vec3(0, 0, 5);

	// Direction : Spherical coordinates to Cartesian coordinates conversion
	direction = glm::vec3(cos(verticalAngle) * sin(horizontalAngle),
			sin(verticalAngle),
			cos(verticalAngle) * cos(horizontalAngle));

	// Right vector
	right = glm::vec3(
		sin(horizontalAngle - 3.14f/2.0f), 
		0,
		cos(horizontalAngle - 3.14f/2.0f)
	);

	// Up
	up = glm::cross(right, direction);
}

void Controls::update(){
	// glfwGetTime is called only once, the first time this function is called
	static double lastTime = glfwGetTime();

	// Compute time difference between current and last frame
	double currentTime = glfwGetTime();
	float deltaTime = float(currentTime - lastTime);
	
	// Move forward
	if (glfwGetKey( window, GLFW_KEY_UP ) == GLFW_PRESS){
		position += direction * deltaTime * speed;
	}
	// Move backward
	if (glfwGetKey( window, GLFW_KEY_DOWN ) == GLFW_PRESS){
		position -= direction * deltaTime * speed;
	}
	// Strafe right
	if (glfwGetKey( window, GLFW_KEY_RIGHT ) == GLFW_PRESS){
		position += right * deltaTime * speed;
	}
	// Strafe left
	if (glfwGetKey( window, GLFW_KEY_LEFT ) == GLFW_PRESS){
		position -= right * deltaTime * speed;
	}

	// For the next frame, the "last time" will be "now"
	lastTime = currentTime;
}

void Controls::updateViewMatrix(glm::mat4& viewMat){
	viewMat = glm::lookAt(position, // Camera is here
			position + direction, // and looks here
			up);
}

void Controls::updateProjectionMatrix(glm::mat4& projMat){
	projMat = glm::perspective(fov, 4.0f / 3.0f, 0.1f, 100.0f);
}

