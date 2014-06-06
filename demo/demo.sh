#!/bin/sh

echo "Binding gpsd to GPS device"
sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock

cd ../recorder

echo "Starting data recorder"
sudo python recorder.py &

sleep 3

echo "Starting data visualisation overlay"
../demo/QtOSD/bin/QtOSD -platform eglfs &

echo "All services started, press ENTER to end"
read val

echo "Killing QtOSD"
killall QtOSD

echo "Killing recorder"
sudo killall python

echo "All services killed, program ended"
