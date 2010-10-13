'''
Created on Oct 8, 2010

@author: anders
'''
import RadarColorMap
from GmapPalette import GmapPalette

QUANTITY_DBZH = "DBZH"

CONTINOUS = 0
DISCRETE = 1

TABLE_LENGTH = 256

class GmapColors(object):
  
  def __init__(self):
    pass
  
  def palette(self, quantity, intercept, slope):
    colormap = None
    
    if RadarColorMap.COLORMAPS.has_key(quantity):
      colormap = RadarColorMap.COLORMAPS[quantity]
    
    valuetype = colormap.valuetype()
    colortype = colormap.colortype()
    table = colormap.map()
    
    keys = table.keys()
    keys.sort()
    j=0
    
    cpalette = []
    intervalsPhysical = []
    intervalsDigitalNumbers = []
    print "off=%f, slope=%f"%(intercept, slope)
    for i in range(len(keys)-1):
      lowKey = keys[i]
      highKey = keys[i+1]
      if valuetype == RadarColorMap.VALUE_TYPE_PHYSICAL:
        lowDN = int(round( (lowKey-intercept)/slope))
        highDN = int(round( (highKey-intercept)/slope))
        lowPhys = lowKey
        highPhys = lowKey
      elif valuetype == RadarColorMap.VALUE_TYPE_DIGITALNUMBER:
        lowPhys = int(round( (lowKey*slope)+intercept))
        highPhys = int(round( (highKey*slope)+intercept))
        lowDN = lowKey
        highDN = highKey
      
      lowRGB = table.get(lowKey)
      highRGB = table.get(highKey)

      if (lowDN >= 0) & (lowDN < TABLE_LENGTH):
        intervalsPhysical.append(lowPhys)
        intervalsDigitalNumbers.append(lowDN)
      
      DNS = self._linearsequenceint(highDN-lowDN, lowDN, highDN-1)

      if colortype == RadarColorMap.COLOR_TYPE_CONTINOUOS:
        R = self._linearsequenceint(highDN-lowDN, lowRGB[0], highRGB[0])
        G = self._linearsequenceint(highDN-lowDN, lowRGB[1], highRGB[1])
        B = self._linearsequenceint(highDN-lowDN, lowRGB[2], highRGB[2])
      elif colortype == RadarColorMap.COLOR_TYPE_DISCRETE:
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
        
        if (d>=0) & (d<TABLE_LENGTH):
          cpalette.extend( (r,g,b) )
          j+=1
    
    print "LENGTH=%d"%len(cpalette)
    if len(cpalette) != TABLE_LENGTH*3:
      raise Exception('palette did not become %d in length'%(TABLE_LENGTH*3))

    return GmapPalette(quantity, TABLE_LENGTH, cpalette, intervalsPhysical, intervalsDigitalNumbers)
            
  def _linearsequence(self, seqlen, minval, maxval):
    seq = [0]*int(seqlen)
    min = float(minval)
    max = float(maxval)
    intercept = min
    slope = (max-min)/float(seqlen-1)
    for i in range(int(seqlen)):
        seq[i] = (float(i)*slope)+intercept
    return seq
    
  def _linearsequenceint(self, seqlen, minval, maxval):
    tmp = self._linearsequence(seqlen, minval, maxval)
    return map(int, map(round, tmp))

  