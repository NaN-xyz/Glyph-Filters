# MenuTitle: Moon Rocks
# -*- coding: utf-8 -*-
__doc__ = """
Moon Rocks
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import NaNFilter
from NaNCommonFilters import moonrocks

class MoonRocks(NaNFilter):
    params = {
        "S": {"offset": -5, "iterations": 150},
        "M": {"offset": -15, "iterations": 1200},
        "L": {"offset": -20, "iterations": 1220},
    }

    def processLayer(self, thislayer, params):
        offsetpaths = self.saveOffsetPaths(
            thislayer, params["offset"], params["offset"], removeOverlap=False
        )
        outlinedata = setGlyphCoords(ConvertPathsToSkeleton(offsetpaths, 20))
        moonrockpaths = moonrocks(thislayer, outlinedata, params["iterations"], shapetype = "blob", maxgap = 8)
        ConvertPathlistDirection(moonrockpaths, 1)
        AddAllPathsToLayer(moonrockpaths, thislayer)
        self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)

MoonRocks()
