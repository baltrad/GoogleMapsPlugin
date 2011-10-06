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

Setup script for installing the google maps plugin for rave.
Requires rave and pyhl (hlhdf).

Usage:
  python setup.py install [--prefix=...]
  
  --prefix default is /opt/baltrad
  
  In order to use this plugin you are required to generate a
  products.js script in the web-directory by invoking the
  GenerateProductInfo.py script.
  
  You will also need a php-capable www-server like apache
  that is configured to have a path to the web-catalog.
@file
@author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2010-11-30
'''
from distutils.core import setup

if __name__ == "__main__":
  import sys, distutils, os, glob
  try:
    import _pyhl
  except Exception, e:
    print "Gmap rave plugin requires _pyhl in order to work properly"

  try:
    import _rave
  except Exception, e:
    print "Gmap rave plugin requires _rave in order to work properly"
    
  # Setup the default install prefix
  prefix = "/opt/baltrad"

  # Get the install prefix if one is specified from the command line
  for arg in sys.argv:
    if arg.startswith('--prefix='):
      prefix = arg[9:]
      prefix = os.path.expandvars(prefix)
  
  ipath = prefix+"/rave_gmap"
  
  setup(name='RAVE Google Maps Plugin',
        version='0.1',
        description='Google Maps plugin for RAVE',
        author='Anders Henja',
        author_email='anders@baltrad.eu',
        url='http://www.baltrad.eu',
        extra_path = ipath + "/Lib",  # all modules go here
        packages=[""],
        package_dir={"": "src"},
        data_files=[(ipath+'/web/css', glob.glob('web/css/*.css')),
                    (ipath+'/web/img', glob.glob('web/img/*.png')+glob.glob('web/img/*.jpg')+glob.glob('web/img/*.gif')),
                    (ipath+'/web/img', glob.glob('web/img/*.ico')),
                    (ipath+'/web/js', glob.glob('web/js/*.js')),
                    (ipath+'/web', glob.glob('web/*.php')),
                    (ipath+'/web', glob.glob('web/*.xml')),
                    (ipath+'/Lib', glob.glob('src/*.ttf')),
                    (ipath, ["README", "README.ravepgf", "README2", "LICENSE", "COPYING", "COPYING.LESSER"])]
       )
  
  # Only perform this operation during installation
  isinstalling = 0
  for item in sys.argv:
    if item=="install":
      isinstalling = 1
  if isinstalling:
    source = ipath + '/Lib.pth'
    dest = distutils.sysconfig.get_python_lib() + '/rave_gmap.pth'
    try:
      os.rename(source, dest)  # doesn't work in some environments
    except:
      import shutil
      shutil.copyfile(source, dest)
      os.unlink(source)
