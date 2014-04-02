#include <stdio.h>
#include <unistd.h>
#include "../common/startScreen.h"
#include "../common/LoadShaders.h"

#include "Rectangle.h"

int main(int argc, const char **argv) {
	InitGraphics();
	printf("Screen started\n");
	// Create and compile our GLSL program from the shaders
	GLuint programID = LoadShaders("simplevertshader.glsl",	"simplefragshader.glsl");
	printf("Shaders loaded\n");


	do {

		// Clear the screen
		glClear (GL_COLOR_BUFFER_BIT);

		// Use our shader
		glUseProgram(programID);

		Triangle *triangle = new Triangle(-0.5, -0.5, 0.5, -0.5, 0.5, 0.5);
		triangle->draw();

		Rectangle *line = new Rectangle(-1, -1, 1, 1);
		line->draw();

		// see above glEnableVertexAttribArray(vertexPosition_modelspaceID);
		glEnableVertexAttribArray(0);

		uint32_t GScreenWidth = 1280;
		uint32_t GScreenHeight = 720;

		void* image = malloc(GScreenWidth * GScreenHeight * 4);

		glBindFramebuffer(GL_FRAMEBUFFER, 0);
		glReadPixels(0, 0, GScreenWidth, GScreenHeight, GL_RGBA,
				GL_UNSIGNED_BYTE, image); //GScreenWidth,GScreenHeight,

		updateScreen();

	} while (1);

}

