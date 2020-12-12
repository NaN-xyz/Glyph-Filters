#MenuTitle: Microbe
# -*- coding: utf-8 -*-
__doc__="""
Microbe
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
        thislayer.removeOverlap()
        offsetpaths = self.saveOffsetPaths(
            thislayer, params["offset"], params["offset"], removeOverlap=False
        )
        outlinedata = setGlyphCoords(ConvertPathsToSkeleton(offsetpaths, 30))
        ClearPaths(thislayer)
        microbepaths = moonrocks(thislayer, outlinedata, params["iterations"], shapetype="blob", maxgap = 1, maxsize=params["maxsize"])
        AddAllPathsToLayer(microbepaths, thislayer)
        self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)

Microbe()
