#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import pi3d

# Load diplay, nearly full screen
DISPLAY = pi3d.Display.create(x=1280, y=720)
DISPLAY.set_background(0, 0, 0, 255)


ortho_cam = pi3d.Camera(is_3d=False)


# Load shaders
shader = pi3d.Shader("uv_reflect")
flatsh = pi3d.Shader("uv_flat")

texture = pi3d.Texture("green.png")


#green = pi3d.Texture(file_string, blend, flip, size, defer, mipmap)

# Load ttf font and set the font colour to 'raspberry'
arialFont = pi3d.Font("../tools/fonts/FreeMonoBoldOblique.ttf", (0,255,0,255))
mystring = pi3d.String(font=arialFont, string="Altitude : 504m", z=1, is_3d=False, camera=ortho_cam, size=0.1)
mystring.set_shader(flatsh)


fps = pi3d.String(font=arialFont, string="... fps", z=1, is_3d=False, camera=ortho_cam, size=0.1)

myPlane = pi3d.Sprite(w=100, h=10, name="plane", z=1)

# Fetch key presses
mykeys = pi3d.Keyboard()

# Display scene
while DISPLAY.loop_running():
    
    mystring.draw()
    
    myPlane.draw(shader, txtrs=[texture])
    
    k = mykeys.read()
    if k >-1:
        if k==27:
            mykeys.close()
            DISPLAY.destroy()
            break
