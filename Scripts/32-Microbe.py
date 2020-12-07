#MenuTitle: 32. Microbe
# -*- coding: utf-8 -*-
__doc__="""
06. Microbe
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import NaNFilter
from NaNCommonFilters import moonrocks

class Microbe(NaNFilter):
    params = {
        "S": {"offset": 15, "iterations": 25000,  "maxsize":  40},
        "M": {"offset": 0,  "iterations": 70000,  "maxsize": 100},
        "L": {"offset": 0,  "iterations": 100000, "maxsize": 140},
    }

    def processLayer(self, thislayer, params):
        offsetpaths = self.saveOffsetPaths(
            thislayer, params["offset"], params["offset"], removeOverlap=False
        )
        outlinedata = getGlyphCoords(ConvertPathsToSkeleton(offsetpaths, 30))
        ClearPaths(thislayer)
        moonrocks(thislayer, outlinedata, params["iterations"], shapetype = "blob", maxgap = 1, maxsize=params["maxsize"])

Microbe()
