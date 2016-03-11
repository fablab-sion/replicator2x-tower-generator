#!/usr/bin/python
import argparse
import sys
from subprocess import call

ARGS = None

def main(temperatures, bedTemp):
	temperaturesString = ",".join(['"{}"'.format(x) for x in temperatures])
	print temperaturesString
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
	      gcodeHeader = gcodeHeaderFile.read().replace('###ExtruderTemp###', str(temperatures[0])).replace('###BedTemp###', str(bedTemp))
	      gcodeString =  gcodeFile.read()

	      for tempNumber in range(1, len(temperatures)-1):
	        index =  gcodeString.find('Z' + str(tempNumber*10))
	        gcodeString = gcodeString[:index-18]+'\nM104 S' + str(temperatures[tempNumber])+' T0 \n'+gcodeString[index-17:len(gcodeString)]

	      gcodeOutFile.write(gcodeHeader + gcodeString)

	# Convert gcode to x3g
	call(["gpx", "-v", "towerOut.gcode", "tower.x3g"])


def parse_arguements():
    """Parse the command line arguments."""
    # Define a parser
    parser = argparse.ArgumentParser(description="Generate temperature calibration tower for Makerbot Replicator2x (g3x)")
    parser.add_argument('--list', '-l', type=int, nargs='*',
    					default=None,
                        help='list of temperatures')
    parser.add_argument('--bed', '-b', type=int,
                        default='110',
                        help='temperature of the bed')
    parser.add_argument('--from', '-f', type=int, dest='start',
    					default=None,
                        help='from temperature')
    parser.add_argument('--to', '-t', type=int,
    					default=None,
                        help='to temperature')
    parser.add_argument('--step', '-s', type=int,
    					default=None,
                        help='temperature step')
    # Parse the arguments
    return parser.parse_args()

if __name__ == "__main__":
    # Parse arguments
    ARGS = parse_arguements()
    if ARGS.list is not None:
    	temperatures = ARGS.list
    elif ARGS.start is not None and ARGS.to is not None and ARGS.step is not None:
    	temperatures = list(range(ARGS.start, ARGS.to + 1, ARGS.step))
    else:
    	sys.exit(1)
    print(temperatures)
    print(ARGS.bed)

    # Run the application
    sys.exit(main(temperatures, ARGS.bed))