#!/usr/bin/env python
'''
Copyright (C) 2010, 2011- Swedish Meteorological and Hydrological Institute (SMHI)

This file is part of RAVE.

RAVE is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RAVE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with RAVE.  If not, see <http://www.gnu.org/licenses/>.
'''
## Palette definitions and whatnot.

## @file
## @author Daniel Michelson, SMHI
## @date 2010-12-20

import os, string, copy
import Image, ImageFont, ImagePalette, ImageDraw
import rave_zr
import GmapColorMap

FONT = os.path.join(os.path.split(GmapColorMap.__file__)[0], "UbuntuTitling-Bold.ttf")


def autogenerate_dbz_legend(width=20, height=256, 
                        gain=0.4, offset=-30.0,
                        zr_a=200.0, zr_b=1.4,
                        palette=GmapColorMap.dbzh, 
                        discrete=0, 
                        font=FONT, fontsize=12, titlesize=16):

    palette = copy.deepcopy(palette)
    this = Image.new('P', (width, height))
    data = list(this.getdata())
    for i in range(height):
        for j in range(width):
            data[(i*width)+j] = (height-1)-i  # initialize data to 0-255
    this.putdata(data)
    
    xshift, yshift = 40, 20
    that = Image.new('P', (width+xshift*2, height+yshift+(yshift/2)))
    that.paste(this, (xshift,yshift))
    
    for i in range(3):
        palette[i] = 255   # White background
        palette[767-i] = 0 # Black lines
    that.putpalette(palette)
    
    draw = ImageDraw.Draw(that)
    dfont = ImageFont.truetype(font, fontsize)
        
    # Put a box around the palette
    draw.line(((xshift,yshift),(xshift+width,yshift),
               (xshift+width,yshift+height-1),(xshift,yshift+height-1),
               (xshift,yshift)), fill=255)
        
    # Put ticks every 10 dBZ
    lowest, highest = offset, 255*gain+offset
    for dbz in range(-40,110,10):
        raw = (dbz-offset)/gain
        if 0 <= raw <= 255:
            draw.line(((xshift-5,yshift+255-raw),(xshift-1,yshift+255-raw)),fill=255) # left
            draw.text((0,yshift+255-raw-(0.5*fontsize-1)), 
                      string.rjust(str(dbz),6), font=dfont, fill=255)
    
    # Put ticks at selected values of mm/h
    for rr in (0.1, 0.3, 1, 3, 10, 30, 100, 300):
        raw = rave_zr.R2raw(rr, gain, offset, zr_a, zr_b)
        if 0 <= raw <= 255:
            draw.line(((xshift+width,yshift+255-raw),
                       (xshift+width+5,yshift+255-raw)), fill=255) # right
            draw.text((xshift+width+5,yshift+255-raw-(0.5*fontsize-1)),
                      string.rjust(str(rr), 6), font=dfont, fill=255)
    
    # Add titles
    dfont = ImageFont.truetype(font, titlesize)
    draw.text((5, 4), "dBZ", font=dfont, fill=255)
    draw.text((xshift+width-6, 4), "mm/h", font=dfont, fill=255)

    # Put a box around the whole thing
    xsize, ysize = that.size
    draw.line(((0,0),(xsize-1,0),(xsize-1,ysize-1),(0,ysize-1),(0,0)), fill=255)
    
    return that


if __name__ == "__main__":
    import sys
    from optparse import OptionParser
    
    usage = "usage: %prog -o <outfile> -p <parameter> -g <gain> -f <offset> -a <zr_A> -b <zr_b> -c <colors> [h]"
    usage += "\n\nGenerate legends for display through the Google Maps front end."
    parser = OptionParser(usage=usage)

    parser.add_option("-o", "--output", dest="outfile",
                      help="Name of output file to write the legend.")

    parser.add_option("-p", "--parameter", dest="param", default="DBZ",
                      help="Which radar parameter, ie. DBZ, VRAD, RHOHV, etc.")

    parser.add_option("-g", "--gain", dest="gain", default="0.5",
                      help="Linear gain coefficient, defaults to 0.5")

    parser.add_option("-f", "--offset", dest="offset", default="-32.0",
                      help="Linear offset coefficient, defaults to -32")

    parser.add_option("-a", "--zr-a", dest="zra", default="200.0",
                      help="Coefficient A in Z-R relation, defaults to 200")

    parser.add_option("-b", "--zr-b", dest="zrb", default="1.4",
                      help="Exponent b in Z-R relation, defaults to 1.4")

    parser.add_option("-c", "--colors", dest="colors", default="DBZH",
                      help="Color-table (palette) name, from GmapColorMap, defaults to DBZH ...")

    parser.add_option("-s", "--show", dest="show", default="True",
                      help="Display the result. Defaults to True")

    (options, args) = parser.parse_args()

    if options.outfile != None:  # More checks should be added.

        if options.colors == "DANIELS_21": options.colors = GmapColorMap.DANIELS_21
        
        if options.param.upper() == "DBZ":
            legend = autogenerate_dbz_legend(gain = float(options.gain),
                                             offset = float(options.offset),
                                             zr_a = float(options.zra),
                                             zr_b = float(options.zrb),
                                             colors = GmapColorMap.PALETTES[options.colors])
        legend.save(options.outfile)
        
        if eval(options.show):
            legend.show()
        
    else:
        parser.print_help()
        sys.exit(1)
