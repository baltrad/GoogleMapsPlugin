'''
Copyright (C) 2010, 2011, 2012 Swedish Meteorological and Hydrological Institute, SMHI,

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

This class contains the necessary functions for generating Google
Maps compatible PNG images. Basically it fetches arrays from an ODIM
formatted HDF5 file, applies palettes and writes PNG files. The DBZH
quantity is written using a color palette, whereas the quality indicator
fields are written in black&white. 

@file
@author Anders Henja and Daniel Michelson (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2012-10-04
'''
import _rave, _raveio
from PIL import Image
import GmapColorMap
import numpy
import sys
from GmapLayerSettings import SETTINGS

class GmapCreator(object):
  def __init__(self, h5file, quantity="DBZH", **kw):
    self._gmappalette = None
    self._gain = None
    self._offset = None
    self._quant = None
    self._qinds = {}
  
    rio = _raveio.open(h5file)
    if rio.objectType == _rave.Rave_ObjectType_COMP:
      prod = rio.object.getImage(0)  # assume only one "composite" in this file
    elif rio.objectType == _rave.Rave_ObjectType_IMAGE:
      prod = rio.object
    self._quant = prod.getParameter(quantity)

    for i in range(self._quant.getNumberOfQualityFields()):
        qi = self._quant.getQualityField(i)
        task = qi.getAttribute("how/task")
        self._qinds[task] = qi

    if not "gain" in kw:
      self._gain = self._quant.gain
      if self._gain == 0.0:
        raise ValueError('gain == 0.0')
    else:
      self._gain = kw["gain"]
      
    if not "offset" in kw:
      self._offset = self._quant.offset
    else:
      self._offset = kw["offset"]
      
    self._gmappalette = GmapColorMap.PALETTES[SETTINGS[quantity].palette]


  def _create_images(self):
    qinds = {}
    img = Image.fromarray(self._quant.getData())

    for q in self._qinds.keys():
        try:
            o = SETTINGS[q]
        except KeyError:
            o = SETTINGS["default"]
        if o.create:
            if o.negate:
                qinds[q] = Image.fromarray(255 - self._qinds[q].getData())
            else:
                qinds[q] = Image.fromarray(self._qinds[q].getData())

    return img, qinds


  def gmappalette(self):
    return self._gmappalette

  
  def create_images(self):
    img, qinds = self._create_images()
    
    img.putpalette(self._gmappalette)
    for q in qinds.keys():
        try:
            o = SETTINGS[q]
        except KeyError:
            o = SETTINGS["default"]
        if o.rgba:
            qinds[q] = makeRGBA(qinds[q], background=o.rgba_bg, MAX=o.rgba_max)
    
    return img, qinds

## Create RGBA image with variable opacity
# @param Pimg PIL Image object of type 'P'
# @param background value (0-255) for the background grey value
# @param MAX value (0-1) giving the max value to receive 0% opacity, e.g. 0.7 = 179
# @return PIL Image object of type 'RGBA'
def makeRGBA(Pimg, background=51, MAX=0.7):
  MAX = round(MAX * 255, 0) # keep this as a float
  shape = Pimg.size[1], Pimg.size[0]
  bg = numpy.zeros(shape, numpy.uint8) + background
  Parr = numpy.reshape(numpy.fromstring(Pimg.tobytes(), numpy.uint8), shape)
  alpha = numpy.where(numpy.less(Parr, int(MAX)), Parr/MAX*255, 255)
  alpha = Image.fromarray(alpha.astype(numpy.uint8))
  RGBA = Image.fromarray(bg).convert("RGBA")
  RGBA.putalpha(alpha.convert("L"))
  return RGBA


if __name__ == "__main__":
  import GmapLegend
  #creator = GmapCreator("../testdata/swecomposite_gmap.h5",gain=0.5,offset=-32.0)
  creator = GmapCreator("../testdata/swecomposite_gmap.h5")
  img, qinds = creator.create_images()
  img.save("slask.png", transparency=0)
  GmapLegend.autogenerate_dbz_legend(gain=creator._gain,
                                     offset=creator._offset).save("legend.png")
  #creator.gmappalette().legend(title="dbz", legendheight=196).save("legend.png")
