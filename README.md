Replicator2x temperature tower generator
=============
Generate gpx file for temperature test with Makerbot Replicator 2x

Prerequisites
-----------
Makerbot software in path
openocd in path
Python

Usage
-----------

    python autoTower.py temperatures
    exemple : python autoTower.py 210 220 230 240

Working principle
-----------------
1. Change temperatures in scad file
2. Generate stl
3. Slice stl into gcode with Makerbot "miracle grue"
4. Change temperatures in gcode
5. Convert gcode to gpx



