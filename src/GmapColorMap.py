'''
Copyright (C) 2010- Swedish Meteorological and Hydrological Institute (SMHI)

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


PALETTES = {}


# Miscellaneous colors, most originally in RAVE
BLACK      = (  0,  0,  0)
DARKBLUE   = (  0,  0,128)
BLUE       = (  0,  0,255)
CYAN       = (  0,255,255)
DARKGREEN  = (  0,128,  0)
GREEN      = (  0,255,  0)
DARKYELLOW = (128,128,  0)
YELLOW     = (255,255,  0)
ORANGE     = (255,128,  0)
BROWN      = (153, 85, 51)
DARKRED    = (128,  0,  0)
RED        = (255,  0,  0)
PINK       = (255,  0,128)
MAGENTA    = (255,  0,255)
PUREWHITE  = (255,255,255)
GREY1      = ( 21, 21, 21)
GREY2      = ( 42, 42, 42)
GREY3      = ( 63, 63, 63)
GREY4      = ( 84, 84, 84)
GREY5      = (105,105,105)
GREY6      = (126,126,126)
GREY7      = (147,147,147)
GREY8      = (168,168,168)
GREY9      = (189,189,189)
WEBSAFEGREY= (204,204,204)
GREY10     = (210,210,210)
GREY11     = (231,231,231)
GREY12     = (252,252,252)
NODATAGREY = ( 51, 51, 51)
BACKGROUND = (238,204,  0)

# NEXRAD-esque colors, based on Thomas Boevith's work. The following colors are all websafe.
NLIGHTBLUE     = (187,221,238)
NMEDBLUE       = (102,170,221)
NBLUE          = ( 34,119,187)
NDARKGREEN     = ( 68,170, 85)
NGREENISH      = ( 34,136, 68)
NGREEN         = (  0,102, 51)
NORANGE        = (255,136, 68)
NRED           = (221, 34, 34)
NDARKERRED     = (204, 17, 34)
NDARKESTRED    = (170, 17, 17)
NPURPLE        = (170,  0,119)
NDARKPURPLE    = (119,  0,119)
NDARKESTPURPLE = ( 68,  0,102)
NDARK          = ( 34,  0, 68)
NDARKER        = ( 17,  0, 17)
BALTRAD_COLORS = (NLIGHTBLUE, NMEDBLUE, NBLUE, NDARKGREEN, NGREENISH, NGREEN, 
                  YELLOW, NORANGE, NRED, NDARKERRED, NDARKESTRED, 
                  NPURPLE, NDARKPURPLE, NDARKESTPURPLE, NDARK, NDARKER, BLACK)
DANIELS_COLORS = (BLACK, DARKBLUE, BLUE, CYAN, DARKGREEN, GREEN,
                  DARKYELLOW, YELLOW, ORANGE, DARKRED, RED, PINK, 
                  MAGENTA, PUREWHITE)
DANIELS_21     = (GREY3,GREY5,GREY7,GREY9,CYAN,DARKBLUE,BLUE,DARKGREEN,GREEN,DARKYELLOW,
                  YELLOW,ORANGE,BROWN,DARKRED,RED,PINK,MAGENTA,NPURPLE,NDARKPURPLE,NDARKESTPURPLE,BLACK)
TEST_COLORS    = (BLACK, BLUE, GREEN, RED, PUREWHITE)


## Takes a set of input colors and generates a palette by interpolating them to 255 RGB combinations.
# @param COLORS list of tuples, where each tuple contains three ints in the interval 0-255
# The length of the list should divide 255 evenly, otherwise the palette will be padded accordingly.
def interpolate_to_palette(COLORS):
    nrcolors = len(COLORS)-1
    step = 256/float(nrcolors)
    pad = 0
    if int(step)*nrcolors != 256:
        pad = 256 - (int(step)*nrcolors)
    palette = []
    for i in range(nrcolors):
        Rlo, Glo, Blo = COLORS[i]
        Rhi, Ghi, Bhi = COLORS[i+1]
        Rstep = (Rhi-Rlo)/(step+1)
        Gstep = (Ghi-Glo)/(step+1)
        Bstep = (Bhi-Blo)/(step+1)
        for j in range(int(step)):
            palette += (int(round(Rlo+(j*Rstep))),
                        int(round(Glo+(j*Gstep))),
                        int(round(Blo+(j*Bstep))))
    for i in range(pad):
        palette += COLORS[-1]
    return palette


#dbzh = interpolate_to_palette(BALTRAD_COLORS)
dbzh = interpolate_to_palette(DANIELS_21)
# Tweak to give BALTRAD_COLORS a better shade for "nodata"
dbzh[767], dbzh[766], dbzh[765] = NODATAGREY
PALETTES["DBZH"] = dbzh


## Writes the contents of a palette to a text file, one RGB combination per line. The first RGB combination
# is for value 0.   
# @param palette tuple of int RGB values that is 768 values long.
# @param filename string containing the name of the text file to write.
def dump_palette_to_file(palette, filename):
    fd = open(filename, 'w')
    for i in range(0,768,3):
        l = []
        for j in range(3):
            l.append(palette[i+j])
        fd.write("%i %i %i\n" % (l[0], l[1], l[2]))
    fd.close()

if __name__ == "__main__":
    print __doc__
