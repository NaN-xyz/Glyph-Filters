# MenuTitle: Microbe
# -*- coding: utf-8 -*-
__doc__ = """
Microbe
"""

from NaNFilter import NaNFilter
from NaNGFAngularizzle import ConvertPathsToSkeleton, setGlyphCoords
from NaNGFGraphikshared import AddAllPathsToLayer, ClearPaths
from NaNGlyphsEnvironment import glyphsEnvironment as G
from NaNCommonFilters import moonrocks


class Microbe(NaNFilter):
    params = {
        "S": {"offset": 15, "iterations": 25000, "maxsize": 40},
        "M": {"offset": 0, "iterations": 70000, "maxsize": 75},
        "L": {"offset": 0, "iterations": 100000, "maxsize": 100},
    }

    def processLayer(self, thislayer, params):
        G.remove_overlap(thislayer)
        offsetpaths = self.saveOffsetPaths(
            thislayer, params["offset"], params["offset"], removeOverlap=False
        )
        outlinedata = setGlyphCoords(ConvertPathsToSkeleton(offsetpaths, 30))
        microbepaths = moonrocks(thislayer, outlinedata, params["iterations"], shapetype="blob", maxgap=1, maxsize=params["maxsize"])
        ClearPaths(thislayer)
        if microbepaths:
            AddAllPathsToLayer(microbepaths, thislayer)
        self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)


Microbe()
