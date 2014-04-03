#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import pi3d


arialFont = pi3d.Font("tools/fonts/FreeMonoBoldOblique.ttf", (255, 255, 255, 255))

green = pi3d.Texture("home/christian/projects/pilotage-fpv/libosd/green.png")


class Display:
    
    def __init__(self, h, w):
        self.width = w
        self.height = h
        self.pi3d_display = pi3d.Display.create(h=h, w=w, x=w, y=h, frames_per_second=30)
        self.pi3d_display.set_background(0, 0, 0, 0)
        self.drawables = list()
        
        self.ortho_cam = pi3d.Camera(is_3d=False)
        
        self.shader = pi3d.Shader("uv_reflect")
        self.flatsh = pi3d.Shader("uv_flat")
    
    def add(self, drawable):
        self.drawables.append(drawable)

    def remove(self, drawable):
        self.drawables.remove(drawable)

    def draw(self):
        for drawable in self.drawables:
            drawable.draw()
            
    def loop_running(self):
        self.pi3d_display.loop_running()
        
    def destroy(self):
        self.pi3d_display.destroy()


class Drawable(object):
    def __init__(self):
        self.display.add(self)

    def destroy(self):
        self.display.remove(self)


class Text(Drawable):
    """Some text"""
    def __init__(self, d, text="", xpos=0, ypos=0, size=0.1, rotation=0, align="L", draw=1):
        self.xpos = xpos-d.width/2
        self.ypos = ypos-d.height/2
        self.align = align
        self.size = size
        self.display = d
        self.text = str(text)

        self.create_pi3d_obj()

        if draw:
            super(Text, self).__init__()

    def create_pi3d_obj(self):
        self.pi3d_obj = pi3d.String(font=arialFont, string=self.text, z=1, is_3d=False, camera=self.display.ortho_cam,
                                    size=self.size, x=self.xpos, y=self.ypos, justify=self.align)
        self.pi3d_obj.set_shader(self.display.flatsh)

        return

    def draw(self):
        self.pi3d_obj.draw()

    def set_text(self, text):
        self.text = text
        self.create_pi3d_obj()


class Line(Drawable):
    def __init__(self, d, length, xpos=0, ypos=0, width=1, rotation=0, draw=1):
        self.xpos = xpos-d.width/2
        self.ypos = ypos-d.height/2
        self.rotation = rotation
        self.display = d
        self.length = length
        self.width = width

        self.pi3d_obj = pi3d.Sprite(camera=self.display.ortho_cam, w=self.length, h=self.width,
                                    x=self.xpos, y=self.ypos, z=1, rz=self.rotation)

        if draw:
            super(Line, self).__init__()
    
    def draw(self):
        self.pi3d_obj.draw(self.display.shader, txtrs=[green])

    def set_rotation(self, rotation):
        self.rotation = rotation
        self.pi3d_obj.rotateToZ(self.rotation)


class Ruler(Drawable):
    def __init__(self, d, xpos, ypos, length, width, range, step=10, interstep=0, label='R', draw=1):
        self.xpos = xpos
        self.ypos = ypos
        self.display = d
        self.length = length
        self.width = width
        self.range = range
        self.step = step
        self.interstep = interstep
        self.drawables = list()

        self.unit_size = length/range

        self.label_dx = 0
        self.label_align = 'C'

        if label == 'R':
            self.label_dx = 10
            self.label_align = 'L'

        if label == 'L':
            self.label_dx = -40
            self.label_align = 'R'

        self.value = -1
        self.set_value(0)

        if draw:
            super(Ruler, self).__init__()

    def set_value(self, value):
        value = int(value)
        if value != self.value:
            self.drawables = list()

            for i in range(int(self.value-self.range/2), int(self.value+self.range/2)):
                if i % self.step == 0:

                    # Add line
                    self.drawables.append(
                        Line(
                            d=self.display,
                            length=self.width,
                            xpos=self.xpos,
                            ypos=self.ypos+(i-self.value)*self.unit_size,
                            draw=0
                        )
                    )

                    # Add label
                    self.drawables.append(
                        Text(
                            d=self.display,
                            text=str(i),
                            xpos=self.xpos+self.label_dx,
                            ypos=self.ypos+(i-self.value)*self.unit_size,
                            align=self.label_align,
                            draw=0
                        )
                    )
                else:
                    # Add interstep line
                    if self.interstep != 0 and i % self.interstep == 0:
                        self.drawables.append(
                            Line(
                                self.display,
                                self.width/3,
                                self.xpos,
                                self.ypos+(i-self.value)*self.unit_size,
                                draw=0
                            )
                        )

        # Remind new value
        self.value = value

    def draw(self):
        for drawable in self.drawables:
            drawable.draw()