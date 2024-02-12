# MenuTitle: Doodle Shadow
# -*- coding: utf-8 -*-
__doc__ = """
Doodle Shadow
"""


from NaNGFAngularizzle import ConvertPathsToSkeleton, setGlyphCoords
from NaNGFGraphikshared import AddAllPathsToLayer, ClearPaths, DoShadow
from NaNGFNoise import NoiseOutline
import random

from NaNFilter import NaNFilter
from NaNGlyphsEnvironment import glyphsEnvironment as G


class DoodleShadow(NaNFilter):

    params = {
        "S": {"offset": 10, "depth": random.randrange(40, 85)},
        "M": {"offset": 10, "depth": random.randrange(50, 100)},
        "L": {"offset": 10, "depth": random.randrange(60, 100)}
    }
    glyph_stroke_width = 16
    shadow_stroke_width = 6
    angle = -160  # random.randrange(0, 360)

    def setup(self):
        pass

    def processLayer(self, thislayer, params):

        offset, depth = params["offset"], params["depth"]

        G.remove_overlap(thislayer)
        pathlist = ConvertPathsToSkeleton(thislayer.paths, 20)
        outlinedata = setGlyphCoords(pathlist)
        # bounds = AllPathBounds(thislayer)

        # offsetpaths = self.saveOffsetPaths(
        #     thislayer, offset, offset, removeOverlap=True
        # )
        # pathlist2 = ConvertPathsToSkeleton(offsetpaths, 4)
        # outlinedata2 = setGlyphCoords(pathlist2)

        ClearPaths(thislayer)

        noisepaths = NoiseOutline(thislayer, outlinedata)
        noiseoutline = self.expandMonolineFromPathlist(noisepaths, self.glyph_stroke_width)
        shadowpaths = DoShadow(thislayer, outlinedata, self.angle, depth, "lines")
        shadowoutline = self.expandMonolineFromPathlist(shadowpaths, self.shadow_stroke_width)

        AddAllPathsToLayer(noiseoutline, thislayer)
        AddAllPathsToLayer(shadowoutline, thislayer)

        G.remove_overlap(thislayer)
        self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)


DoodleShadow()
