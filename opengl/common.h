#ifndef COMMON_H
#define COMMON_H

#include <GL/glew.h>
#include <vector>
#include <glm/glm.hpp>

bool loadOBJ(
	const char * path, 
	std::vector<glm::vec3> & out_vertices, 
	std::vector<glm::vec2> & out_uvs, 
	std::vector<glm::vec3> & out_normals
);

GLuint LoadShaders(const char* vertex_file_path, const char* fragment_file_path);

#endif
