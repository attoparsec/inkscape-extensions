#! /usr/bin/env python
'''
Copyright (C) 2013 Matthew Dockrey  (gfish @ cyphertext.net)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

Based on coloreffect.py by Jos Hirth and Aaron C. Spike
'''

import inkex
import simplestyle, sys

class Cleanup(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument("-s", "--stroke",
                        action="store", type=float,
                        dest="stroke", default=0.5,
                        help="Stroke weight")
        self.arg_parser.add_argument("-o", "--opacity",
                        action="store", type=float,
                        dest="opacity", default="100.0",
                        help="Opacity")

    def effect(self):
        if len(self.svg.selected)==0:
            self.getAttribs(self.document.getroot())
        else:
            for id,node in self.svg.selected.items():
                self.getAttribs(node)

    def getAttribs(self,node):
        self.changeStyle(node)
        for child in node:
            self.getAttribs(child)

    def changeStyle(self,node):
        if node.attrib.has_key('style'):
            # References for style attribute:
            # http://www.w3.org/TR/SVG11/styling.html#StyleAttribute,
            # http://www.w3.org/TR/CSS21/syndata.html
            #
            # The SVG spec is ambiguous as to how style attributes should be parsed.
            # For example, it isn't clear whether semicolons are allowed to appear
            # within strings or comments, or indeed whether comments are allowed to
            # appear at all.
            #
            # The processing here is just something simple that should usually work,
            # without trying too hard to get everything right.
            # (Won't work for the pathalogical case that someone escapes a property
            # name, probably does the wrong thing if colon or semicolon is used inside
            # a comment or string value.)
            style = node.get('style') # fixme: this will break for presentation attributes!
            if style:
                #inkex.debug('old style:'+style)
                declarations = style.split(';')
                for i,decl in enumerate(declarations):
                    parts = decl.split(':', 2)
                    if len(parts) == 2:
                        (prop, val) = parts
                        prop = prop.strip().lower()
                        if prop == 'stroke-width':
                            new_val = str(self.options.stroke)
                            declarations[i] = prop + ':' + new_val
                        if prop == 'opacity':
                            new_val = str(self.options.opacity / 100)
                            declarations[i] = prop + ':' + new_val
                #inkex.debug('new style:'+';'.join(declarations))
                node.set('style', ';'.join(declarations))

if __name__ == '__main__':
    e = Cleanup()
    e.run()
