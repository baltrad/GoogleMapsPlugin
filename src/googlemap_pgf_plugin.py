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

Actual plugin code that performs the generation of the google map
compatible png file.

@file
@author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2010-10-07
'''
import GmapCreator
import os
#
# @param files - an array of files, only first file will be used
# @param arguments array of two arguments, ["outfile", <name of file to be saved>]
# @return None
#
def generate(files, arguments):
  creator = GmapCreator.GmapCreator(files[0])
  img = creator.create_image()
  l = len(arguments)
  filename=None
  kw = {}
  for i in range(l):
    if arguments[i] == "outfile":
      filename = arguments[i+1]
    if arguments[i] == "zr_a":
      kw["zr_a"] = float(arguments[i+1])
    if arguments[i] == "zr_b":
      kw["zr_b"] = float(arguments[i+1])
                         
  
  dname = os.path.dirname(filename)
  if not os.path.exists(dname):
    os.makedirs(dname)
  elif os.path.exists(dname) and not os.path.isdir(dname):
    raise Exception, "%s already exists but is not a directory"%dname
  
  img.save(filename, transparency=0)
  legend_name = os.path.join(dname, "legend.png")
  if not os.path.exists(legend_name):
    GmapLegend.autogenerate_dbz_legend(gain=creator._gain,
                                     offset=creator._intercept,
                                     **kw).save(legend_name)
    #creator.gmappalette().legend(title="dbz", legendheight=196).save(legend_name)
  return None

if __name__ == '__main__':
    pass
