'''
Created on Oct 11, 2010

@author: anders
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
    
    for iph,idn in zip(self._physicalIntervals, self._dnIntervals):
      draw.text((legendwidth+2, abs(self._tableLength-idn)+4),str(int(iph)),(0,0,0),font=font)
      draw = ImageDraw.Draw(legendimg)

    # FIXME add background and transparency
    font = ImageFont.truetype(fontpath,titlesize)
    draw.text((legendwidth+2, 1), title,(0,0,0),font=font)
    
    return legendimg   