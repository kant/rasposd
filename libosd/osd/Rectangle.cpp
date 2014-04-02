/*
 * Rectangle.cpp
 *
 *  Created on: Apr 2, 2014
 *      Author: christian
 */

#include "Rectangle.h"

Rectangle::Rectangle(float xpos, float ypos, float xsize, float ysize) {

	this->anchor = new Vertex(xpos, ypos);
	this->x = xsize;
	this->y = ysize;

	/* A rectangle is two triangles */
	this->triangles[0] = new Triangle(
		anchor->x, 		anchor->y,
		anchor->x+x, 	anchor->y+y,
		anchor->x+x, 	anchor->y
	);

	this->triangles[1] = new Triangle(
		anchor->x, 		anchor->y,
		anchor->x+x, 	anchor->y+y,
		anchor->x, 		anchor->y+y
	);
}

Rectangle::~Rectangle() {
	delete(triangles[0]);
	delete(triangles[1]);
}

void Rectangle::draw() {
	triangles[0]->draw();
	triangles[1]->draw();
}
