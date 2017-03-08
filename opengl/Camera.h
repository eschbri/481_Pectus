#ifndef CAMERA_H
#define CAMERA_H

#include <glm/glm.hpp>

class Camera{
public:
	Camera();
	glm::mat4 getWorldToViewMatrix() const;

	void moveForward();
	void moveBackward();
	void strafeLeft();
	void straceRight();
	void moveUp();
	void moveDown();

private:
	glm::vec3 position;
	glm::vec3 viewDirection;
	const glm::vec3 up;
	glm::vec3 strafeDirection;
	static const float movementSpeed_c;
};

#endif
