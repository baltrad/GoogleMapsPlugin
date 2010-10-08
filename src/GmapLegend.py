'''
Copyright (C) 2010 Swedish Meteorological and Hydrological Institute, SMHI,

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

Provides support for different legends and palettes. This is yet a modified
version of the original software created by the people mentioned in README
and README2.

@file
@author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2010-10-07
'''
import Image,ImageDraw, ImageFont
import numpy

_REFLECTIVITY = {-128.0: [189,215,231], # Lower bound
                   0.0: [189,215,231],
                   5.0: [107,174,214],
                   10.0: [33,113,181],
                   15.0: [65,171,93],
                   20.0: [35,139,69],
                   25.0: [0,109,44],
                   30.0: [255,255,0],
                   35.0: [253,141,60],
                   40.0: [227,26,28],
                   45.0: [203,24,29],
                   50.0: [165,15,21],
                   55.0: [174,1,126],
                   60.0: [122,1,119],
                   65.0: [73,0,106],
                   70.0: [30,0,60],
                   75.0: [15,0,15],
                   80.0: [5,0,5],
                   85.0: [0,0,0],
                   90.0: [0,0,0],
                   128.0: [0,0,0] # Upper bound
                }

_HYDROMET = { -5: [255,255,255], # Lower bound
              60: [64,128,255], # Rain
             150: [255,128,0], # Clutter
             180: [255,255,0], # Clutter / external emitters
             250: [250,250,250], # Snow
             260: [0,0,0] # Upper bound
            } 
 
class GmapLegend(object):
  VALUE_TYPE_PHYSICAL = 0
  VALUE_TYPE_DIGITALNUMBER = 1
  TYPE_DISCRETE = 0
  TYPE_CONTINOUS = 1
  LENGTH = 256
  
  def __init__(self, table, valuetype, type, intercept=-32.0, slope=0.5):
    self._valuetype = valuetype
    self._type = type
    self._table = table
    self._palette = []
    self._intercept = intercept
    self._slope = slope
    self._intervalsPhysical=[]
    self._intervalsDigitalNumbers=[]
    
    self._generate()
  
  def _generate(self):
    keys = self._table.keys()
    keys.sort()
    j=0
    for i in range(len(keys)-1):
      lowKey = keys[i]
      highKey = keys[i+1]
      if self._valuetype == GmapLegend.VALUE_TYPE_PHYSICAL:
        lowDN = int(round( (lowKey-self._intercept)/self._slope))
        highDN = int(round( (highKey-self._intercept)/self._slope))
        lowPhys = lowKey
        highPhys = lowKey
      elif self._valuetype == GmapLegend.VALUE_TYPE_DIGITALNUMBER:
        lowPhys = int(round( (lowKey*self._slope)+self._intercept))
        highPhys = int(round( (highKey*self._slope)+self._intercept))
        lowDN = lowKey
        highDN = highKey
      
      lowRGB = self._table.get(lowKey)
      highRGB = self._table.get(highKey)

      if (lowDN >= 0) & (lowDN < GmapLegend.LENGTH):
        self._intervalsPhysical.append(lowPhys)
        self._intervalsDigitalNumbers.append(lowDN)
      
      DNS = self._linearsequenceint(highDN-lowDN, lowDN, highDN-1)
      
      if self._type == GmapLegend.TYPE_CONTINOUS:
        R = self._linearsequenceint(highDN-lowDN, lowRGB[0], highRGB[0])
        G = self._linearsequenceint(highDN-lowDN, lowRGB[1], highRGB[1])
        B = self._linearsequenceint(highDN-lowDN, lowRGB[2], highRGB[2])
      elif self._type == GmapLegend.TYPE_DISCRETE:
        R = [lowRGB[0]]*(highDN-lowDN)
        G = [lowRGB[1]]*(highDN-lowDN)
        B = [lowRGB[2]]*(highDN-lowDN)
        
      for d,r,g,b in zip(DNS,R,G,B):
        # print(d,r,g,b)
        # Out of range color is black
        if j==0:
          r=0
          g=0
          b=0
        
        # Out of range color is white
        if j==255:
          r=255
          g=255
          b=255
          
        if (d>=0) & (d<GmapLegend.LENGTH):
          self._palette.extend( (r,g,b) )
          j+=1
    if len(self._palette) != 768:
      raise Exception('palette did not become 768 in length')
            
  def _linearsequence(self, seqlen, minval, maxval):
    seq = [0]*seqlen
    min = float(minval)
    max = float(maxval)
    intercept = min
    slope = (max-min)/float(seqlen-1)
    for i in range(seqlen):
        seq[i] = (float(i)*slope)+intercept
    return seq
    
  def _linearsequenceint(self, seqlen, minval, maxval):
    tmp = self._linearsequence(seqlen, minval, maxval)
    return map(int, map(round, tmp))
    
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
    
    a = numpy.linspace(255, 0, num=legendheight)
    legend = numpy.ones((legendheight,legendwidth+textwidth), numpy.uint8)*255
    for i in range(a.size):
      for j in range(legendwidth):
        legend[i,j] = int(a[i])
    legendimg = Image.fromarray(legend, "L")
    legendimg.putpalette(self._palette)
    legendimg = legendimg.convert("RGBA")
    draw = ImageDraw.Draw(legendimg)
    font = ImageFont.truetype(fontpath,fontsize)
    for iph,idn in zip(self._intervalsPhysical, self._intervalsDigitalNumbers):
      draw.text((legendwidth+2, abs(GmapLegend.LENGTH-idn)+4),str(int(iph)),(0,0,0),font=font)
      draw = ImageDraw.Draw(legendimg)

    # FIXME add background and transparency
    font = ImageFont.truetype(fontpath,titlesize)
    draw.text((legendwidth+2, 1), title,(0,0,0),font=font)
    
    return legendimg

# PRESETS for simplicity
REFLECTIVITY=GmapLegend(_REFLECTIVITY, GmapLegend.VALUE_TYPE_PHYSICAL, GmapLegend.TYPE_CONTINOUS)
HYDROMET=GmapLegend(_HYDROMET, GmapLegend.VALUE_TYPE_DIGITALNUMBER, GmapLegend.TYPE_CONTINOUS)

