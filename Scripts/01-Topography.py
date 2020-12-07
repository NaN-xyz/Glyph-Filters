# MenuTitle: 25. Topography
# -*- coding: utf-8 -*-
__doc__ = """
25. Topography
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFSpacePartition import *

from NaNFilter import NaNFilter


class Topography(NaNFilter):

    params = {
        "S": {"offset": 0, "gridsize": 10},
        "M": {"offset": 4, "gridsize": 30},
        "L": {"offset": 4, "gridsize": 40},
    }

    def setup(self):
        self.linecomponents = []
        line_vertical_comp = CreateLineComponent(
            self.font, "vertical", 6, "LineVerticalComponent"
        )
        line_horizontal_comp = CreateLineComponent(
            self.font, "horizontal", 6, "LineHorizontalComponent"
        )
        self.linecomponents.extend([line_vertical_comp, line_horizontal_comp])

    def processLayer(self, thislayer, params):
        if glyphSize(thislayer.parent) == "S":
            self.processLayerSmall(thislayer)
        else:
            self.processLayerLarge(thislayer, params)

    def processLayerLarge(self, thislayer, params):
        offset, gridsize = params["offset"], params["gridsize"]
        pathlist = doAngularizzle(thislayer.paths, 20)
        outlinedata = getGlyphCoords(pathlist)
        bounds = AllPathBounds(thislayer)

        offsetpaths = self.saveOffsetPaths(
            thislayer, offset, offset, removeOverlap=True
        )
        pathlist2 = doAngularizzle(offsetpaths, 4)
        outlinedata2 = getGlyphCoords(pathlist2)
        bounds2 = AllPathBoundsFromPathList(pathlist2)

        ClearPaths(thislayer)

        iterations = [
            (random.randrange(200, 400), "vertical"),
            (random.randrange(200, 400), "horizontal"),
            (random.randrange(70, 100), "blob"),
        ]

        for maxchain, shape in iterations:
            newtris = self.SortCollageSpace(
                thislayer, outlinedata, outlinedata2, gridsize, bounds, "stick"
            )
            groups = BreakUpSpace(thislayer, outlinedata, newtris, gridsize, maxchain)
            self.ApplyCollageGraphixxx(thislayer, groups, shape, self.linecomponents)

    def processLayerSmall(self, thislayer):
        thislayer.removeOverlap()
        roundedpathlist = returnRoundedPaths(thislayer.paths)
        ClearPaths(thislayer)
        AddAllPathsToLayer(roundedpathlist, thislayer)

    def ApplyCollageGraphixxx(self, layer, groups, drawtype, linecomponents):

        for g in groups:
            if len(g) < 2:
                continue

            templayer = GSLayer()
            templayer.paths = g
            templayer.removeOverlap()

            for p in templayer.paths:
                nodelen = len(p.nodes)
                if nodelen < 4:
                    continue

                roundedpath = RoundPath(p, "nodes")
                roundedpath = convertToFitpath(roundedpath, True)
                if not roundedpath:
                	continue

                if drawtype == "vertical" or drawtype == "horizontal":
                    try:
                        all_lines = Fill_Drawlines(
                            layer, roundedpath, drawtype, 15, linecomponents
                        )
                        AddAllComponentsToLayer(all_lines, layer)
                    except:
                        pass

                if drawtype == "blob":
                    # disallow small blobs
                    rw = roundedpath.bounds.size.width
                    rh = roundedpath.bounds.size.height
                    if (rw > 30 and rh > 30) and (rw < 200 or rh < 200):
                        layer.paths.append(roundedpath)

            del templayer


Topography()
