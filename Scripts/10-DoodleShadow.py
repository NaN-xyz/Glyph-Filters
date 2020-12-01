# MenuTitle: 10. DoodleShadow
# -*- coding: utf-8 -*-
__doc__ = """
10. DoodleShadow
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFSpacePartition import *
from NaNGFNoise import *

from NaNFilter import NaNFilter


class DoodleShadow(NaNFilter):

    params = {
        "S": {"offset": 10, "depth": random.randrange(40, 70)},
        "M": {"offset": 10, "depth": random.randrange(50, 100)},
        "L": {"offset": 10, "depth": random.randrange(60, 100)}
    }
    glyph_stroke_width = 16
    shadow_stroke_width = 6
    angle = -160 #random.randrange(0, 360)

    def setup(self):
        pass

    def processLayer(self, thislayer, params):

        offset, depth = params["offset"], params["depth"]

        thislayer.removeOverlap()
        pathlist = doAngularizzle(thislayer.paths, 20)
        outlinedata = setGlyphCoords(pathlist)
        bounds = AllPathBounds(thislayer)

        offsetpaths = self.saveOffsetPaths(
            thislayer, offset, offset, removeOverlap=True
        )
        pathlist2 = doAngularizzle(offsetpaths, 4)
        outlinedata2 = setGlyphCoords(pathlist2)

        ClearPaths(thislayer)

        noisepaths = NoiseOutline(thislayer, outlinedata)
        noiseoutline = self.expandMonolineFromPathlist(noisepaths, self.glyph_stroke_width)
        shadowpaths = DoShadow(thislayer, outlinedata, self.angle, depth, "lines")
        shadowoutline = self.expandMonolineFromPathlist(shadowpaths, self.shadow_stroke_width)

        AddAllPathsToLayer(noiseoutline, thislayer)
        AddAllPathsToLayer(shadowoutline, thislayer)
       
        thislayer.removeOverlap()


DoodleShadow()
