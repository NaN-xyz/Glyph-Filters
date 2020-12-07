# MenuTitle: 15. DoodleTriangles
# -*- coding: utf-8 -*-
__doc__ = """
15. DoodleTriangles
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFSpacePartition import *
from NaNGFNoise import *

from NaNFilter import NaNFilter


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

        offset, gridsize = params["offset"], params["gridsize"]
        pathlist = doAngularizzle(thislayer.paths, 20)
        outlinedata = getGlyphCoords(pathlist)
        bounds = AllPathBounds(thislayer)

        offsetpaths = self.saveOffsetPaths(
            thislayer, offset, offset, removeOverlap=True
        )
        pathlist2 = doAngularizzle(offsetpaths, 4)
        outlinedata2 = getGlyphCoords(pathlist2)

        ClearPaths(thislayer)

        noisepaths = NoiseOutline(thislayer, outlinedata)
        noiseoutline = self.expandMonolineFromPathlist(noisepaths, self.glyph_stroke_width)

        newtris = self.SortCollageSpace(thislayer, outlinedata, outlinedata2, gridsize, bounds, "stick", True)
        blacktris = ConvertPathlistDirection ( random.sample(newtris, int(len(newtris)/10)), -1 )

        strokedtris = self.expandMonolineFromPathlist(newtris, self.tri_stroke_width)
        AddAllPathsToLayer(strokedtris, thislayer)
        AddAllPathsToLayer(noiseoutline, thislayer)
        AddAllPathsToLayer(blacktris, thislayer)

        thislayer.removeOverlap()


DoodleTriangles()
