#ifndef WINDOW_H
#define WINDOW_H

#include <stdexcept>

// Forward declaration of Window
class GLFWwindow;

class Window{
public:
	Window(int height_, int width_, const char* title_);
	~Window();

	bool closed() const;
	void swapBuffers();
	
private:
	GLFWwindow* window;
};

// Base class for all exceptions which Window throws 
class WindowError : public std::runtime_error{
public:
	WindowError(const std::string& s)
		: runtime_error(s) {}
};

#endif
