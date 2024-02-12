# MenuTitle: Maps
# -*- coding: utf-8 -*-
__doc__ = """
Maps
"""

import random
from NaNGFAngularizzle import ConvertPathsToSkeleton, setGlyphCoords
from NaNGFConfig import glyphSize
from NaNGFGraphikshared import AddAllComponentsToLayer, AddAllPathsToLayer, AllPathBounds, ClearPaths, ConvertPathDirection, CreateLineComponent, Fill_Drawlines, RoundPath, returnRoundedPaths, convertToFitpath
from NaNGFSpacePartition import BreakUpSpace
from NaNGlyphsEnvironment import glyphsEnvironment as G
from NaNGlyphsEnvironment import GSLayer
from NaNFilter import NaNFilter


class Maps(NaNFilter):

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
        pathlist = ConvertPathsToSkeleton(thislayer.paths, 20)
        outlinedata = setGlyphCoords(pathlist)
        bounds = AllPathBounds(thislayer)

        offsetpaths = self.saveOffsetPaths(
            thislayer, offset, offset, removeOverlap=True
        )
        pathlist2 = ConvertPathsToSkeleton(offsetpaths, 4)
        outlinedata2 = setGlyphCoords(pathlist2)
        # bounds2 = AllPathBoundsFromPathList(pathlist2)

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

        self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)

    def processLayerSmall(self, thislayer):
        G.remove_overlap(thislayer)
        roundedpathlist = returnRoundedPaths(thislayer.paths)
        ClearPaths(thislayer)
        AddAllPathsToLayer(roundedpathlist, thislayer)

    def ApplyCollageGraphixxx(self, layer, groups, drawtype, linecomponents):

        for g in groups:
            if len(g) < 2:
                continue

            templayer = GSLayer()
            G.add_paths(templayer, g)
            G.remove_overlap(templayer)

            for p in templayer.paths:
                nodelen = len(p.nodes)
                if nodelen < 4:
                    continue

                roundedpath = RoundPath(p, "nodes")
                roundedpath = convertToFitpath(roundedpath, True)
                if not roundedpath:
                    continue

                if drawtype == "vertical" or drawtype == "horizontal":

                    rw = roundedpath.bounds.size.width
                    rh = roundedpath.bounds.size.height
                    if (rw > 130 or rh > 130):
                        all_lines = Fill_Drawlines(
                            layer, roundedpath, drawtype, 20, linecomponents
                        )
                        AddAllComponentsToLayer(all_lines, layer)

                if drawtype == "blob":
                    # disallow small blobs
                    rw = roundedpath.bounds.size.width
                    rh = roundedpath.bounds.size.height
                    if (rw > 80 and rh > 80) and (rw < 180 or rh < 180):
                        ConvertPathDirection(roundedpath, -1)
                        layer.paths.append(roundedpath)

            del templayer


Maps()
