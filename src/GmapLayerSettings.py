'''
Copyright (C) 2014- Swedish Meteorological and Hydrological Institute, SMHI,

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

Managed quantities and quality indicator/index layers from XML lookup.

@file
@author Daniel Michelson (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2014-04-09
'''
import sys, os, copy
from xml.etree import ElementTree as ET
import GmapLayerSettings

CONFIG_FILE = os.path.join(os.path.split(GmapLayerSettings.__file__)[0], 
                           "gmap_layer_settings.xml")

initialized = 0

SETTINGS = {}


## Initializes the settings dictionary by reading contents from XML file
def init():
    global initialized
    if initialized: return
    
    C = ET.parse(CONFIG_FILE)
    OPTIONS = C.getroot()

    Q = OPTIONS.find("quantities")

    for e in list(Q):
        opts = options()
        for k, i in e.items():
            opts.__setattr__(k, i)
        SETTINGS[e.tag] = opts

    Q = OPTIONS.find("qc-layers")

    default = Q.find("default")
    default_opts = options()
    for k, i in default.items():
        default_opts.__setattr__(k, eval(i))
    SETTINGS["default"] = default_opts

    for e in list(Q):
        if e.tag != "default":
            opts = copy.deepcopy(default_opts)
            for k, i in e.items():
                opts.__setattr__(k, eval(i))
        SETTINGS[e.tag] = opts

    initialized = 1


## Generic object used to organize things
class options(object):
    pass


init()

if __name__ == "__main__":
    pass
