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

This class contains the nessecary functions for generating a google
map compatible png-image. Basically it fetches an array from a ODIM
formatted HDF5 file, applies a color palette and writes a .png file.

@file
@author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2010-10-07
'''
import _pyhl
import Image
import GmapColors

class GmapCreator(object):
  _colors = None
  _gmappalette = None
  _nodelist = None
  _node = None
  _gain = None
  _intercept = None
  _quantity = None
  
  def __init__(self, h5file, dataset="/dataset1/data1/data", whatgroup="/dataset1/what", **kw):
    self._colors = GmapColors.GmapColors()
    self._nodelist = _pyhl.read_nodelist(h5file)
    self._node = self._nodelist.fetchNode(dataset)
    
    if not kw.has_key("gain"):
      self._gain = self._nodelist.fetchNode(whatgroup + "/gain").data()
      if self._gain == 0.0:
        raise ValueError('gain == 0.0')
    else:
      self._gain = kw["gain"]
      
    if not kw.has_key("intercept"):
      self._intercept = self._nodelist.fetchNode(whatgroup + "/offset").data()
    else:
      self._intercept = kw["intercept"]
      
    if not kw.has_key("quantity"):
      self._quantity = self._nodelist.fetchNode(whatgroup + "/quantity").data()
    else:
      self._quantity = kw["quantity"]

    self._gmappalette = self._colors.palette(self._quantity, self._intercept, self._gain)

  def _create_image(self):
    img = Image.fromarray(self._node.data(), "L")
    return img

  def quantity(self):
    return self._quantity
  
  def gmappalette(self):
    return self._gmappalette
  
  def create_image(self):
    img = self._create_image()
    
    img.putpalette(self._gmappalette.palette())
    
    return img
  
if __name__ == "__main__":
  import GmapLegend
  #creator = GmapCreator("../testdata/swecomposite_gmap.h5",gain=0.5,intercept=-32.0)
  creator = GmapCreator("../testdata/swecomposite_gmap.h5")
  img = creator.create_image()
  img.save("slask.png", transparency=0)
  GmapLegend.autogenerate_dbz_legend(gain=creator._gain,
                                     offset=creator._intercept,
                                     zr_a=200.0, zr_b=1.4).save("legend.png")
  #creator.gmappalette().legend(title="dbz", legendheight=196).save("legend.png")
  
