#ifndef CONTROLS_H
#define CONTROLS_H

#include <glm/glm.hpp>

// Forward declaration
class GLFWwindow;

class Controls{
public:
	Controls(GLFWwindow* window_);
	void update();
	void attachWindow(const GLFWwindow& winow);
	void updateViewMatrix(glm::mat4& viewMat);
	void updateProjectionMatrix(glm::mat4& projMat);
private:
	glm::vec3 position;
	glm::vec3 direction;
	glm::vec3 right;
	glm::vec3 up;
	float speed; // Speed for keyboard controls
	float verticalAngle;
	float horizontalAngle;
	float fov;
	GLFWwindow* window;
};

#endif
