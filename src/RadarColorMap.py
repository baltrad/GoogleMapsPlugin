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

Predefined color maps

@file
@author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2010-10-07
'''
VALUE_TYPE_PHYSICAL = 0
VALUE_TYPE_DIGITALNUMBER = 1

COLOR_TYPE_CONTINOUOS = 0
COLOR_TYPE_DISCRETE = 1


class RadarColorMap(object):
  def __init__(self, valuetype, colortype, map):
    self._valuetype = valuetype
    self._colortype = colortype
    self._map = map
      
  def valuetype(self):
    return self._valuetype
    
  def colortype(self):
    return self._colortype
    
  def map(self):
    return self._map

_REFLECTIVITY={-128.0: [189,215,231], # Lower bound
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

COLORMAPS={}
COLORMAPS["DBZH"] = RadarColorMap(VALUE_TYPE_PHYSICAL, COLOR_TYPE_CONTINOUOS, _REFLECTIVITY)
COLORMAPS["CLASS"] = RadarColorMap(VALUE_TYPE_DIGITALNUMBER, COLOR_TYPE_CONTINOUOS, _HYDROMET)


                                  