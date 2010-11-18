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

Actual plugin code that performs the generation of the google map
compatible png file.

@file
@author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2010-10-07
'''
import GmapCreator

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
  for i in range(l):
    if arguments[i] == "outfile":
      filename = arguments[i+1]
      break
  
  img.save(filename, transparency=0)
  return None

if __name__ == '__main__':
    pass