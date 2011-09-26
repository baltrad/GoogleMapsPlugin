'''
Copyright (C) 2010, 2011 Swedish Meteorological and Hydrological Institute, SMHI,

This file is part of GoogleMapsPlugin.

GoogleMapsPlugin is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GoogleMapsPlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with GoogleMapsPlugin.  If not, see <http://www.gnu.org/licenses/>.
------------------------------------------------------------------------*/

Class for managing a palette

@file
@author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2010-10-07
'''
import Image,ImageDraw, ImageFont
import numpy

class GmapPalette(object):
  def __init__(self, quantity, tbllen, palette, physicalIntervals, dnIntervals):
    self._quantity = quantity
    self._tableLength = tbllen
    self._palette = palette
    self._physicalIntervals = physicalIntervals
    self._dnIntervals = dnIntervals
  
  def quantity(self):
    return self._quantity
  
  def palette(self):
    return self._palette
  
  def legend(self, **kw):
    print "CHANGE DEFAULT FONT FOR LEGEND SINCE IT IS UBUNTU-SPECIFIC"
    legendwidth = 20
    legendheight = 256
    textwidth = 40
    fontpath = "/usr/share/fonts/truetype/ttf-ubuntu-title/Ubuntu-Title.ttf"
    fontsize = 12
    title = "dBZ"
    titlesize = 18

    if kw.has_key("legendwith"):
      legendwidth = kw["legendwidth"]
    if kw.has_key("legendheight"):
      legendheight = kw["legendheight"]
    if kw.has_key("textwidth"):
      textwidth = kw["textwidth"]
    if kw.has_key("fontpath"):
      fontpath = kw["fontpath"]
    if kw.has_key("fontsize"):
      fontsize = kw["fontsize"]
    if kw.has_key("title"):
      title = kw["title"]
    if kw.has_key("titlesize"):
      titlesize = kw["titlesize"]    
    
    a = numpy.linspace(255, 0, num=legendheight).astype(numpy.uint8)
    scale = numpy.ones((legendheight,legendwidth+textwidth), numpy.uint8)*255
    for j in range(legendwidth):
      scale[:,j] = a

    # padding
    legend = numpy.ones((legendheight + 33, legendwidth+textwidth + 10),
                        numpy.uint8) * 255
    legend[23:23+legendheight, 10:10+legendwidth+textwidth] = scale

    # border
    legend[0, :] = 0
    legend[-1, :] = 0
    legend[:, 0] = 0
    legend[:, -1] = 0
    
    legendimg = Image.fromarray(legend, "L")
    legendimg.putpalette(self._palette)
    legendimg = legendimg.convert("RGBA")
    draw = ImageDraw.Draw(legendimg)
    font = ImageFont.truetype(fontpath,fontsize)
    
    for iph,idn in zip(self._physicalIntervals, self._dnIntervals):
      draw.text((legendwidth+12, abs(self._tableLength-idn)+4+23),str(int(iph)),(0,0,0),font=font)
      draw = ImageDraw.Draw(legendimg)

    # FIXME add background and transparency
    font = ImageFont.truetype(fontpath,titlesize)
    draw.text((legendwidth+2, 1), title,(0,0,0),font=font)
    
    return legendimg   
