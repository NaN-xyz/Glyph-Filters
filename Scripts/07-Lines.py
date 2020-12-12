# MenuTitle: 07. Lines
# -*- coding: utf-8 -*-
__doc__ = """
07. Lines
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import NaNFilter


class Lines(NaNFilter):
    params = {
        "S": {"offset": -5, "iterations": 50},
        "M": {"offset": -15, "iterations": 400},
        "L": {"offset": -20, "iterations": 420},
    }

    strokesize = 8

    def setup(self):
        self.line_vertical_comp = CreateLineComponent(
            self.font, "vertical", self.strokesize , "LineVerticalComponent"
        )
        self.line_horizontal_comp = CreateLineComponent(
            self.font, "horizontal", self.strokesize , "LineHorizontalComponent"
        )

    def processLayer(self, thislayer, params):

        outlinedata = setGlyphCoords(ConvertPathsToSkeleton(thislayer.paths, 40))

        try:
            allrectangles = MakeRectangles([AllPathBounds(thislayer)], 5)
            direction = "horizontal"
            linecomps = []

            for tile in allrectangles:
                if direction == "horizontal":
                    direction = "vertical"
                else:
                    direction = "horizontal"

                linecomps.extend(
                    self.DrawlinesTile(thislayer, outlinedata, tile, direction)
                )

            ClearPaths(thislayer)
            AddAllComponentsToLayer(linecomps, thislayer)

        except Exception as e:
            print("Glyph (", thislayer.name, ") failed to execute:", e)

    def DrawlinesTile(self, thislayer, outlinedata, tile, direction):

        x, y, w, h = [int(el) for el in tile]
        tilecoords = [[x, y], [x, y + h], [x + w, y + h], [x + w, y]]
        lines = []
        linecomponents = []
        gap = 18
        checkgap = 3

        self.newline = []

        def add_line(x2, y2):
            if withinGlyphBlack(x2, y2, outlinedata) and point_inside_polygon_faster(
                x2, y2, tilecoords
            ):
                self.newline.append([x2, y2])
            else:
                if len(self.newline) > 1:
                    lines.append(self.newline)
                    self.newline = []

        if direction == "horizontal":
            for y2 in range(y, y + h + gap, gap):
                for x2 in range(x, x + w, checkgap):
                    add_line(x2, y2)

        if direction == "vertical":
            for x2 in range(x, x + w + gap, gap):
                for y2 in range(y, y + h, checkgap):
                    add_line(x2, y2)

        lines = SnapToGrid(lines, self.strokesize )

        for l in lines:
            comp = returnLineComponent(
                l[0],
                l[-1],
                direction,
                [self.line_vertical_comp, self.line_horizontal_comp],
                100,
            )
            linecomponents.append(comp)

        return linecomponents


Lines()
