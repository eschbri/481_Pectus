CC = g++
LD = g++
CFLAGS = -c -g -std=c++11 -pedantic-errors -Wall
#LFLAGS = -g -lGL -lGLU -lglfw3 -lX11 -lXxf86vm -lXrandr -lpthread -lXi -ldl
LFLAGS = -lGL -lGLEW -lglfw3 -lX11 -lXi -lXrandr -lXxf86vm -lXinerama -lXcursor -lrt -lm -pthread -ldl
OBJS = common.o playground.o Window.o Controls.o Camera.o

PROG = exe_playground

default: $(PROG)

$(PROG): $(OBJS)
	$(LD) $(OBJS) -o $(PROG) $(LFLAGS)

playground.o: playground.cpp common.h Controls.h Window.h
	$(CC) $(CFLAGS) playground.cpp

common.o: common.h common.cpp
	$(CC) $(CFLAGS) common.cpp

Window.o: Window.h Window.cpp
	$(CC) $(CFLAGS) Window.cpp

Controls.o: Controls.h Controls.cpp Camera.h
	$(CC) $(CFLAGS) Controls.cpp

Camera.o: Camera.h Camera.cpp
	$(CC) $(CFLAGS) Camera.cpp

clean:
	rm $(PROG) *.o
