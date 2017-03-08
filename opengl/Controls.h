#ifndef CONTROLS_H
#define CONTROLS_H

#include <glm/glm.hpp>
#include "Camera.h"

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
	Camera camera;
	double lastTime;
	float verticalAngle;
	float horizontalAngle;
	float fov;
	GLFWwindow* window;
};

#endif
