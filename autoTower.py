#!/usr/bin/python

import sys
from subprocess import call

# Define temperatures
temperatures = sys.argv[1:len(sys.argv)]
temperaturesString = '"' + ('","'.join(temperatures)) + '"'

# Change scad file
with open('tower.scad', 'r') as scadBaseFile:
  with open('towerOut.scad', 'w') as scadOutFile:
    scadOutFile.write(scadBaseFile.read().replace('###NumberOfBlocks###', str(len(temperatures))).replace('###Labels###', temperaturesString))
# Generate stl
call(["openscad", "-o", "tower.stl", "towerOut.scad"])
# Slice, output in .gcode
call(["miracle_grue", "-c", "miracle.json", "-o", "tower.gcode", "tower.stl"])

# Replace temperatures in gcode
with open('tower.gcode', 'r') as gcodeFile:
  with open('header.gcode', 'r') as gcodeHeaderFile:
    with open('towerOut.gcode', 'w') as gcodeOutFile:
      #set first temperature in header
      gcodeHeader = gcodeHeaderFile.read().replace('###SetTemp###', 'M104 S' + str(temperatures[0]) + ' T0')
      gcodeString =  gcodeFile.read()

      for tempNumber in range(1, len(temperatures)):
        index =  gcodeString.find('Z' + str(tempNumber*10))
        gcodeString = gcodeString[:index-18]+'\nM104 S' + str(temperatures[tempNumber])+' T0 \n'+gcodeString[index-17:len(gcodeString)]

      gcodeOutFile.write(gcodeHeader + gcodeString)

# Convert gcode to x3g
call(["gpx", "-v", "towerOut.gcode", "tower.x3g"])