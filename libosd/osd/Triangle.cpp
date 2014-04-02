/*
 * Triangle.cpp
 *
 *  Created on: Apr 2, 2014
 *      Author: christian
 */

#include <GLES2/gl2.h>
#include <EGL/egl.h>
#include <EGL/eglext.h>

#include "Triangle.h"
#include "Vertex.h"

Triangle::Triangle(float ax, float ay, float bx, float by, float cx, float cy) {

	this->a = new Vertex(ax, ay);
	this->b = new Vertex(bx, by);
	this->c = new Vertex(cx, cy);
}

Triangle::~Triangle() {
	// TODO Auto-generated destructor stub
}

void Triangle::draw() {
	GLfloat g_vertex_buffer_data[] =
			{ a->x, a->y, 0.0f, b->x, b->y, 0.0f, c->x, c->y, 0.0f };

	glVertexAttribPointer(0, //vertexPosition_modelspaceID, // The attribute we want to configure
			3,                  // size
			GL_FLOAT,           // type
			GL_FALSE,           // normalized?
			0,                  // stride
			g_vertex_buffer_data // (void*)0            // array buffer offset
			);

	// Draw the triangle !
	glDrawArrays(GL_TRIANGLES, 0, 3); // 3 indices starting at 0 -> 1 triangle
}
