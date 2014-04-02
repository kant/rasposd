#!/usr/bin/python
from __future__ import division, print_function, unicode_literals

import pi3d
import osd
import numpy as np
import datetime

flight_data = np.genfromtxt('flightdata.csv', delimiter=',', names=True)

screen_width = 1280
screen_height = 720

d = osd.Display(w=screen_width, h=screen_height)

# Screen references
br = osd.Text(d, text="BR", xpos=screen_width-40, ypos=10)
bl = osd.Text(d, text="BL", xpos=0, ypos=10)
tr = osd.Text(d, text="TR", xpos=screen_width-40, ypos=screen_height-10)
tl = osd.Text(d, text="TL", xpos=0, ypos=screen_height-10)

cube1 = osd.Line(d, 10, xpos=0, ypos=0, width=10)
cube2 = osd.Line(d, 10, xpos=0, ypos=screen_height, width=10)
cube3 = osd.Line(d, 10, xpos=screen_width, ypos=screen_height, width=10)
cube4 = osd.Line(d, 10, xpos=screen_width, ypos=0, width=10)


# OSD components
horizon = osd.Line(d, 300, xpos=screen_width/2, ypos=screen_height/2, width=3)
time = osd.Text(d, xpos=1000, ypos=20)

gps_longitude = osd.Text(d, xpos=20, ypos=620)
gps_latitude = osd.Text(d, xpos=20, ypos=600)
north_angle = osd.Text(d, xpos=500, ypos=600)

alt_x = screen_width/2+300
alt_y = screen_height/2
altitude = osd.Text(d, xpos=alt_x+20, ypos=alt_y)
altitude_ruler = osd.Ruler(d, xpos=alt_x, ypos=alt_y, length=500, width=20, range=100, step=20, interstep=5, label='L')

speed_x = screen_width/2-300
speed_y = screen_height/2
speed = osd.Text(d, xpos=speed_x-50, ypos=speed_y, align='R')
speed_ruler = osd.Ruler(d, xpos=speed_x, ypos=speed_y, length=500, width=20, range=30, step=5, interstep=1, label='R')

# Fetch key presses
mykeys = pi3d.Keyboard()

i = 0
data = flight_data[i]

# Display scene
while d.pi3d_display.loop_running():

    altitude.set_text(str(data['altitude']))
    speed.set_text(str(data['r_speed']))
    time.set_text(datetime.datetime.fromtimestamp(data['time']/1000).strftime('%Y-%m-%d %H:%M:%S'))

    gps_longitude.set_text(str(data['gps_coord_long']) + "E")
    gps_latitude.set_text(str(data['gps_coord_lat']) + "N")

    horizon.set_rotation(data['roll'])

    altitude_ruler.set_value(data['altitude'])
    speed_ruler.set_value(data['r_speed'])

    d.draw()

    i += 1
    data = flight_data[i]

    # Exit control
    k = mykeys.read()
    if k >-1:
        if k==27:
            mykeys.close()
            d.destroy()
            break
