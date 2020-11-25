# MenuTitle: 06. MoonRocks
# -*- coding: utf-8 -*-
__doc__ = """
06. MoonRocks
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import NaNFilter


class MoonRocks(NaNFilter):
    params = {
        "S": {"offset": -5, "iterations": 50},
        "M": {"offset": -15, "iterations": 400},
        "L": {"offset": -20, "iterations": 420},
    }
    maxgap = 8
    shapetype = "blob"

    def processLayer(self, thislayer, params):
        offsetpaths = self.saveOffsetPaths(
            thislayer, params["offset"], params["offset"], removeOverlap=False
        )
        outlinedata = setGlyphCoords(doAngularizzle(offsetpaths, 20))

        list_dots = []
        b = AllPathBounds(thislayer)

        if b is None:
            return

        ox, oy, w, h = b[0], b[1], b[2], b[3]

        for f in range(0, params["iterations"]):

            x = random.randrange(ox, ox + w)
            y = random.randrange(oy, oy + h)

            if not withinGlyphBlack(x, y, outlinedata):
                continue

            rad = random.randrange(10, 250)
            inside = True
            for n in range(0, len(list_dots)):
                nx, ny, nr = list_dots[n]
                dist = math.hypot(nx - x, ny - y)  # alt method

                if dist < (nr + rad + self.maxgap):
                    inside = False
                    break

            if not inside:
                continue
            circle = drawCircle(x, y, rad * 2, rad * 2)
            circlea = setGlyphCoords(doAngularizzle([circle], 10))
            circlecoords = circlea[0][1]

            if ShapeWithinOutlines(circlecoords, outlinedata):
                list_dots.append([x, y, rad])

        print "Number of circles found:", len(list_dots)

        rocks = []
        for c in range(0, len(list_dots)):
            x, y, size = list_dots[c]
            if self.shapetype == "blob":
                circle = drawBlob(x, y, size * 2, 5, True)
            else:
                circle = drawCircle(x, y, size * 2, size * 2)
            rocks.append(circle)

        rocks = ConvertPathlistDirection(rocks, 1)
        AddAllPathsToLayer(rocks, thislayer)


MoonRocks()
