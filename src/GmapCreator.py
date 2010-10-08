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

This class contains the nessecary functions for generating a google
map compatible png-image. Basically it fetches an array from a ODIM
formatted HDF5 file, applies a color legend and writes a .png file.
This is yet a modified version of the original software created by
the people mentioned in README and README2.

@file
@author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2010-10-07
'''
import _pyhl
import Image
import GmapLegend

class GmapCreator(object):
  _nodelist = None
  _palette = None
  
  def __init__(self, h5file):
    self._nodelist = _pyhl.read_nodelist(h5file)
    
  def set_palette(self, palette):
    self._palette = palette
  
  def get_image(self, dataset):
    node = self._nodelist.fetchNode(dataset)
    img = Image.fromarray(node.data(), "L")
    return img
  
  def create_image(self, node="/dataset1/data1/data"):
    img = self.get_image(node)
    if self._palette != None:
      img.putpalette(self._palette)
    return img
  
if __name__ == "__main__":
  creator = GmapCreator("../testdata/swecomposite_gmap.h5")
  creator.set_palette(GmapLegend.REFLECTIVITY.palette())
  img = creator.create_image()
  img.save("slask.png", transparency=0)
  GmapLegend.REFLECTIVITY.legend(title="dBZ").save("legend.png")
  