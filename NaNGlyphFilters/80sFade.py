# MenuTitle: 80s Fade
# -*- coding: utf-8 -*-
__doc__ = """
80s Fade
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import NaNFilter


class EightiesFade(NaNFilter):
    def processLayer(self, thislayer, params):
        pathlist = ConvertPathsToSkeleton(thislayer.paths, 20)
        outlinedata = setGlyphCoords(pathlist)

        try:
            startrect = AllPathBounds(thislayer)
            allrectangles = MakeRectangles([startrect], 5)
            shape_components = CreateAllShapeComponents(self.font, 100, 100)

            fadecomps = []

            for n in range(0, len(allrectangles)):
                x, y, w, h = allrectangles[n]
                tilecoords = [[x, y], [x, y + h], [x + w, y + h], [x + w, y]]
                fadecomps.extend(
                    self.do80sFade(thislayer, outlinedata, tilecoords, shape_components)
                )

            ClearPaths(thislayer)
            AddAllComponentsToLayer(fadecomps, thislayer)

        except Exception as e:
            print(("Layer (", thislayer.name, ") failed to execute.", e))

    def do80sFade(self, thislayer, outlinedata, tilecoords, shape_components):
        b = AllPathBounds(thislayer)

        if b is None:
            return []

        fadecomps = []
        size = random.randrange(4, 15)
        r = random.choice(shape_components)
        ox, oy, w, h = b[0], b[1], b[2], b[3]

        for y in range(oy, oy + h, 20):
            for x in range(ox, ox + w, 20):
                if (
                    withinGlyphBlack(x, y, outlinedata)
                    and point_inside_polygon(x, y, tilecoords)
                    and size > 2
                ):
                    fadecomp = GSComponent(r)
                    scale = size / 100.0
                    fadecomp.transform = (scale, 0.0, 0.0, scale, x, y)
                    fadecomps.append(fadecomp)
                size += 0.01

        return fadecomps


EightiesFade()
