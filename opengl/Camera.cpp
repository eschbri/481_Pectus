#include "Camera.h"
#define GLM_FORCE_RADIANS
#include <glm/gtc/matrix_transform.hpp>

using glm::vec3;
using glm::vec4;
using glm::cross;
using glm::lookAt;

const float Camera::movementSpeed_c = 0.01f;

Camera::Camera()
	: position(.5, 0, 1), viewDirection(0, 0, -1.0f), up(0, 1.0f, 0)
{
	strafeDirection = cross(viewDirection, up);
}

glm::mat4 Camera::getWorldToViewMatrix() const{
	return lookAt(position, position + viewDirection, up);
}

void Camera::moveForward(){
	position += movementSpeed_c * viewDirection;
}

void Camera::moveBackward(){
	position -= movementSpeed_c * viewDirection;

}

void Camera::strafeLeft(){
	position -= movementSpeed_c * strafeDirection;

}

void Camera::straceRight(){
	position += movementSpeed_c * strafeDirection;

}

void Camera::moveUp(){
	position += movementSpeed_c * up;

}

void Camera::moveDown(){
	position -= movementSpeed_c * up;
}
