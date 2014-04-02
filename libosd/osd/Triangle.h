/*
 * Triangle.h
 *
 *  Created on: Apr 2, 2014
 *      Author: christian
 */

#ifndef TRIANGLE_H_
#define TRIANGLE_H_

#include "Vertex.h"
#include "Shape.h"

class Triangle : public Shape  {
public:
	Triangle(float ax, float ay, float bx, float by, float cx, float cy);
	virtual ~Triangle();
	void draw();

private:
	Vertex *a, *b, *c;
};

#endif /* TRIANGLE_H_ */
