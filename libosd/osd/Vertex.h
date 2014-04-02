/*
 * Vertex.h
 *
 *  Created on: Apr 2, 2014
 *      Author: christian
 */

#ifndef VERTEX_H_
#define VERTEX_H_

class Vertex {

public:
	Vertex(float x, float y);
	virtual ~Vertex();

	float x, y;

private:
};

#endif /* VERTEX_H_ */
