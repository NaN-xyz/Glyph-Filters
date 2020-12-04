# MenuTitle: 06. MoonRocks
# -*- coding: utf-8 -*-
__doc__ = """
06. MoonRocks
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import NaNFilter
from NaNCommonFilters import moonrocks

class MoonRocks(NaNFilter):
    params = {
        "S": {"offset": -5, "iterations": 50},
        "M": {"offset": -15, "iterations": 400},
        "L": {"offset": -20, "iterations": 420},
    }

    def processLayer(self, thislayer, params):
        offsetpaths = self.saveOffsetPaths(
            thislayer, params["offset"], params["offset"], removeOverlap=False
        )
        outlinedata = setGlyphCoords(doAngularizzle(offsetpaths, 20))
        moonrocks(thislayer, outlinedata, params["iterations"], shapetype = "blob", maxgap = 8)


if __name__ == "__main__":
    MoonRocks()
