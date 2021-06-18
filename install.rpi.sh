#!/bin/sh
sudo apt-get update
sudo apt-get install -y libatlas-base-dev libhdf5-dev libgtk2.0-dev libgtk-3-dev libopenjp2-7-dev libilmbase-dev libilmbase23 libopenexr-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev python-rpi.gpio python-spidev python-pip
pip3 install st7789 spidev Pillow Flask
