# MenuTitle: Doodle Triangles
# -*- coding: utf-8 -*-
__doc__ = """
Doodle Triangles
"""

import random
from NaNFilter import NaNFilter
from NaNGFAngularizzle import ConvertPathsToSkeleton, setGlyphCoords
from NaNGFGraphikshared import AddAllPathsToLayer, AllPathBounds, ClearPaths, ConvertPathlistDirection
from NaNGFNoise import NoiseOutline
from NaNGlyphsEnvironment import glyphsEnvironment as G


class DoodleTriangles(NaNFilter):

    params = {
        "S": {"offset": 0, "gridsize": 60},
        "M": {"offset": 4, "gridsize": 60},
        "L": {"offset": 4, "gridsize": 70},
    }
    glyph_stroke_width = 16
    tri_stroke_width = 4

    def setup(self):
        pass

    def processLayer(self, thislayer, params):

        G.remove_overlap(thislayer)

        offset, gridsize = params["offset"], params["gridsize"]
        pathlist = ConvertPathsToSkeleton(thislayer.paths, 20)
        outlinedata = setGlyphCoords(pathlist)
        bounds = AllPathBounds(thislayer)

        offsetpaths = self.saveOffsetPaths(
            thislayer, offset, offset, removeOverlap=True
        )
        pathlist2 = ConvertPathsToSkeleton(offsetpaths, 4)
        outlinedata2 = setGlyphCoords(pathlist2)

        ClearPaths(thislayer)

        noisepaths = NoiseOutline(thislayer, outlinedata)
        noiseoutline = self.expandMonolineFromPathlist(noisepaths, self.glyph_stroke_width)

        newtris = self.SortCollageSpace(thislayer, outlinedata, outlinedata2, gridsize, bounds, "stick", True)
        blacktris = ConvertPathlistDirection(random.sample(newtris, int(len(newtris) / 10)), -1)

        strokedtris = self.expandMonolineFromPathlist(newtris, self.tri_stroke_width)
        AddAllPathsToLayer(strokedtris, thislayer)
        AddAllPathsToLayer(noiseoutline, thislayer)
        AddAllPathsToLayer(blacktris, thislayer)

        G.remove_overlap(thislayer)
        self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)


DoodleTriangles()
