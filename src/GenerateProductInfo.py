'''
Copyright (C) 2010 Swedish Meteorological and Hydrological Institute, SMHI,

This file is part of the google maps plugin for rave.

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

Generates the necessary java script for beeing able to distinguish between
various products that is shown in the google map gui

@file
@author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2010-11-18
'''

import _projection
import sys
import xml.etree.ElementTree as xml
from xml.dom import minidom

import area
import string, math

#
# Supports generation of a javascript file containing the product definitions.
# 
# Future improvments could be to adjust so that we are able to distinguish between
# different quality parameters and hence the need to separate name and area might
# be necessary.
#
class GenerateProductInfo(object):
  filename = None
  
  # Constructor
  #
  # @param self - self
  # $param filename filename of xml file containing the product definitions
  #
  def __init__(self, filename):
    self.filename = filename
    self.tree = xml.parse(filename)
  
  # Generates a java script that can be included in the google map gui
  # code.
  # @param self - self
  # @param outname the name of the java script file
  def generate(self, outname="products.js"):
    fp = open(outname, 'w')
    
    fp.write("function RadarProduct() {\n")
    fp.write("  this.product = '';\n")
    fp.write("  this.description = '';\n")
    fp.write("  this.lon = 0.0;\n")
    fp.write("  this.lat = 0.0;\n")
    fp.write("  zoom = 5;\n")
    fp.write("  this.nelon = 0.0;\n")
    fp.write("  this.nelat = 0.0;\n")
    fp.write("  this.swlon = 0.0;\n")
    fp.write("  this.swlat = 0.0;\n")
    fp.write("}\n")
    
    fp.write('\nvar radar_products = {};\n\n')
    fp.write('var radar_option_list = new Array();\n\n')
    
    entries = self.tree.findall('product')
    
    index = 0   # Counter to get option list
    
    for entry in entries:
      n = entry.get('name')
      d = entry.get('description')
      z = entry.get('zoom')
        
      try:
        a = area.area(n)
        pj = string.join(a.pcs.definition, ' ')
        proj = _projection.new('a', 'b', pj)
        llxy = (a.extent[0],a.extent[1])
        urxy = (a.extent[2],a.extent[3])
        ll = proj.inv(llxy)
        ur = proj.inv(urxy)
        ll = (ll[0]*180.0/math.pi, ll[1]*180.0/math.pi)
        ur = (ur[0]*180.0/math.pi, ur[1]*180.0/math.pi)
        clon = round(ur[0] - (ur[0] - ll[0])/2.0)
        clat = round(ur[1] - (ur[1] - ll[1])/2.0)
        
        # And generate the entry for this product
        fp.write('\n//Product '+n+', ' + d + '\n')
        fp.write("radar_products['%s'] = new RadarProduct;\n"%(n))
        fp.write("radar_products['%s'].description = '%s';\n"%(n,d))
        fp.write("radar_products['%s'].lon = %f;\n"%(n,clon))
        fp.write("radar_products['%s'].lat = %f;\n"%(n,clat))
        fp.write("radar_products['%s'].zoom = %s;\n"%(n,z))
        fp.write("radar_products['%s'].nelon = %f;\n"%(n,ur[0]))
        fp.write("radar_products['%s'].nelat = %f;\n"%(n,ur[1]))
        fp.write("radar_products['%s'].swlon = %f;\n"%(n,ll[0]))
        fp.write("radar_products['%s'].swlat = %f;\n"%(n,ll[1]))
        fp.write("\n")
        fp.write("radar_option_list[%d] = '%s';\n\n"%(index,n))
        
        index = index + 1
        
      except Exception:
        import traceback
        traceback.print_exc(file=sys.stdout)
      
    fp.close()
      

if __name__=="__main__":
  if len(sys.argv) != 2:
    print("Usage: GenerateProductInfo <input-list>")
    print("  input-list: A xml file containing a list of areas that should be used")
    print("")
    print("format of the xml file should be:")
    print('''
  <productlist>
    <product name="swegmaps_2000" description="SMHI Composite" zoom="4"/>
    <product name="area" description="description" zoom="4"/>
    ...
  </productlist>''')
    sys.exit(255)
  
  a = GenerateProductInfo(sys.argv[1])
  a.generate()
