#include "Window.h"
#include <GLFW/glfw3.h>

Window::Window(int width_, int height_, const char* title_){
	if (!glfwInit()){
		throw WindowError("Failed to initialize GLFW");
	}
	glfwWindowHint(GLFW_SAMPLES, 4); // 4x antialiasing
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3); // We want OpenGL 3.3
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
	glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE); // To make MacOS happy; should not be needed
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE); //We don't want the old OpenGL 

	// Open a window and create its OpenGL context
	window = glfwCreateWindow( width_, height_, title_, NULL, NULL);
	if( window == NULL ){
		throw WindowError("Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible.");
    	}
	glfwMakeContextCurrent(window);
}

Window::~Window(){
	glfwTerminate();
}

bool Window::closed() const{
	return glfwWindowShouldClose(window) == 0;
}

GLFWwindow* Window::getWindow() const{
	return window;
}

void Window::swapBuffers(){
	glfwSwapBuffers(window);
	glfwPollEvents();
}
