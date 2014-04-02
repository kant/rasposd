/*
 * Drawable.h
 *
 *  Created on: Apr 2, 2014
 *      Author: christian
 */

#ifndef DRAWABLE_H_
#define DRAWABLE_H_

class Drawable {
public:
	Drawable();
	virtual ~Drawable();

	virtual void draw() = 0;
};

#endif /* DRAWABLE_H_ */
