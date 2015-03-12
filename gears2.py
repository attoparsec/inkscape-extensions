#! /usr/bin/env python
'''
Copyright (C) 2013 Matthew Dockrey  (gfish @ cyphertext.net)

Based on http://arc.id.au/GearDrawing.html by Dr A.R.Collins
And on the original gears.py by Aaron Spike and Tavmjong Bah
'''

import inkex
import simplestyle, sys
from math import *

from involute import *

class Gears(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--tab",
                        action="store", type="string",
                        dest="tab", default="Options",
                        help="The tab selected when OK was pressed")
        self.OptionParser.add_option("-t", "--teeth",
                        action="store", type="int",
                        dest="teeth", default=24,
                        help="Number of teeth")
        self.OptionParser.add_option("-p", "--pangle",
                        action="store", type="float",
                        dest="pressure_angle", default="20",
                        help="Pressure angle")
        self.OptionParser.add_option("-y", "--size_type",
                        action="store", type="int",
                        dest="type", default="1",
                        help="Size type (1 = module (mm), 2 = pitch diameter (inches), 3 = diametral pitch (inches)")
        self.OptionParser.add_option("-s", "--size",
                        action="store", type="float",
                        dest="size", default="5",
                        help="Size")
        self.OptionParser.add_option("-o", "--orientation",
                        action="store", type="int",
                        dest="orientation", default="1",
                        help="Gear orientation")

    def effect(self):
        Z = self.options.teeth
        phi = self.options.pressure_angle
        size_type = self.options.type
        size = self.options.size
        orientation = self.options.orientation

        # Convert size to module (mm) if needed
        if (size_type == 2): 
            # Pitch diameter
            size = 25.4 * size / Z
        elif (size_type == 3): 
            # Diametral pitch
            size = 25.4 / size

        m = self.unittouu(str(size) + "mm")

        if (orientation == 2):
            svg = CreateInternalGear(m, Z, phi)
        else:
            svg = CreateExternalGear(m, Z, phi)

        # Insert as a new element
        gear_style = { 'stroke': '#000000',
                       'stroke-width': '0.1',
                       'fill': 'none'
                       }
        g_attribs = {inkex.addNS('label','inkscape'): 'Gear ' + str(Z),
                     'transform': 'translate(' + str( self.view_center[0] ) + ',' + str( self.view_center[1] ) + ')',
                     'style' : simplestyle.formatStyle(gear_style),
                     'd' : svg }
        g = inkex.etree.SubElement(self.current_layer, inkex.addNS('path','svg'), g_attribs)

if __name__ == '__main__':
    e = Gears()
    e.affect()
