/*
 * Rectangle.h
 *
 *  Created on: Apr 2, 2014
 *      Author: christian
 */

#ifndef RECTANGLE_H_
#define RECTANGLE_H_

#include "Triangle.h"
#include "Vertex.h"

class Rectangle : public Shape {
public:
	Rectangle(float xpos, float ypos, float xsize, float ysize);
	virtual ~Rectangle();

	void draw();

private:
	Vertex *anchor;
	int x, y;
	Triangle *triangles[2];
};

#endif /* RECTANGLE_H_ */
