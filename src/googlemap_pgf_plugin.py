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

Actual plugin code that performs the generation of the Google Maps
compatible PNG files.

@file
@author Anders Henja and Daniel Michelson (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2012-10-04
'''
import GmapCreator
import GmapLegend
import os

ravebdb = None
try:
  import rave_bdb
  ravebdb = rave_bdb.rave_bdb()
except:
  pass

## Creates a dictionary from a rave argument list
#@param arglist the argument list
#@return a dictionary
def arglist2dict(arglist):
  result={}
  for i in range(0, len(arglist), 2):
    result[arglist[i]] = arglist[i+1]
  return result

##
# Converts a string into a number, either int or float
# @param sval the string to translate
# @return the translated value
# @throws ValueError if value not could be translated
#
def toNumber(sval):
  if isinstance(sval, (int, long)):
    return float(sval)
  elif isinstance(sval, float):
    return sval
  else:
    try:
      return int(sval)
    except ValueError, e:
      return float(sval)

  
##
# Generator of PNG images and legend
# @param file - input HDF5 file
# @param arguments array of two arguments, ["outfile", <name of file to be saved>]
# @return None
#
def generate_images(file, arguments):
  creator = GmapCreator.GmapCreator(file)
  img, qinds = creator.create_images()
  filename=None
  args = arglist2dict(arguments)
  kw = {}
  
  if "outfile" in args.keys():
    filename = args["outfile"]
  if "zr_a" in args.keys():
    kw["zr_a"] = toNumber(args["zr_a"])
  if "zr_b" in args.keys():
    kw["zr_b"] = toNumber(args["zr_b"])

  dname, fstr = os.path.split(filename)
  if not os.path.exists(dname):
    os.makedirs(dname)
  elif os.path.exists(dname) and not os.path.isdir(dname):
    raise Exception, "%s already exists but is not a directory"%dname
  
  img.save(filename, transparency=0)
  legend_name = os.path.join(dname, "legend.png")
  if not os.path.exists(legend_name):
    GmapLegend.autogenerate_dbz_legend(gain=creator._gain,
                                     offset=creator._offset,
                                     **kw).save(legend_name)
    #creator.gmappalette().legend(title="dbz", legendheight=196).save(legend_name)

  for q in qinds.keys():
    task, qimg = q, qinds[q]
    qdname = os.path.join(dname, task)
    qfilename = os.path.join(qdname, fstr)
    if not os.path.exists(qdname):
        os.makedirs(qdname)
    if q == 'fi.fmi.ropo.detector.classification':
      qimg.save(qfilename, transparency=0)
    else:
      qimg.save(qfilename)

  return None

#
# @param files - an array of files, only first file will be used
# @param arguments array of two arguments, ["outfile", <name of file to be saved>]
# @return None
#
def generate(files, arguments):
  tmp = None
  if ravebdb != None and not os.path.exists(files[0]):
    try:
      tmp = ravebdb.get_file(files[0])
      return generate_images(tmp, arguments)
    finally:
      if os.path.exists(tmp):
        os.unlink(tmp)
  else:
    return generate_images(files[0], arguments)

if __name__ == '__main__':
  pass

