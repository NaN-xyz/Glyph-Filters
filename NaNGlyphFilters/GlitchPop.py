# MenuTitle: Glitch Pop
# -*- coding: utf-8 -*-
__doc__ = """
Glitch Pop
"""

from GlyphsApp import GSLayer
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFSpacePartition import *
from NaNGlyphsEnvironment import glyphsEnvironment as G
from NaNGFConfig import glyphSize

from NaNFilter import NaNFilter


class GlitchPop(NaNFilter):

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
        bounds2 = AllPathBoundsFromPathList(pathlist2)

        ClearPaths(thislayer)

        maxchain = 150

        newtris = self.SortCollageSpace(
            thislayer, outlinedata, outlinedata2, gridsize, bounds, "stick"
        )
        groups = BreakUpSpace(thislayer, outlinedata, newtris, gridsize, maxchain)
        self.ApplyGlitchCollage(thislayer, groups, self.linecomponents)

        G.remove_overlap(thislayer)
        self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)

    def processLayerSmall(self, thislayer):
        G.remove_overlap(thislayer)
        roundedpathlist = returnRoundedPaths(thislayer.paths)
        ClearPaths(thislayer)
        AddAllPathsToLayer(roundedpathlist, thislayer)

    def ApplyGlitchCollage(self, layer, groups, linecomponents):

        for g in groups:
            if len(g) < 2:
                continue

            templayer = GSLayer()
            templayer.paths = g
            G.remove_overlap(templayer)

            linetype = False

            for p in templayer.paths: 
                
                nodelen = len(p.nodes)
                if nodelen < 4:
                    continue

                roundedpath = RoundPath(p, "nodes")
                roundedpath = convertToFitpath(roundedpath, True)
                if not roundedpath:
                    continue

                if random.choice([0,1,2,3])==1:
                    tr = random.choice([0,2])
                    if tr==1:
                        self.HalftoneShape(layer, p, "triangle")
                    elif tr==0:
                        self.HalftoneShape(layer, p, "square")
                    else:
                        layer.paths.append(roundedpath)
                else:
                    if nodelen>9:
                        
                        if nodelen>20:
                            noodlepaths = self.expandMonolineFromPathlist([roundedpath], 6)
                            AddAllPathsToLayer(noodlepaths, layer)
                        else:

                            if random.choice([0,1])==0:

                                if linetype==False:
                                    direction="vertical"
                                else:
                                    direction="horizontal"

                                linetype = not linetype
                                linecomps = Fill_Drawlines(layer, roundedpath, direction, 15, linecomponents)
                                AddAllComponentsToLayer(linecomps, layer)

                            else:
                                self.Fill_Halftone(layer, roundedpath, "circle")
                    else:
                        layer.paths.append(p)

            del templayer


    def DrawlinesTile(self, outlinedata, tile, direction):

        x, y, w, h = [int(el) for el in tile]
        tilecoords = [[x, y], [x, y + h], [x + w, y + h], [x + w, y]]
        lines = []
        linecomponents = []
        gap = 20
        checkgap = 2

        self.newline = []

        def add_line(x2, y2):
            if point_inside_polygon(x2, y2, outlinedata):
                self.newline.append([x2, y2])
            else:
                if len(self.newline) > 1:
                    lines.append(self.newline)
                    self.newline = []

        if direction == "horizontal":
            for y2 in range(y, y + h + gap, gap):
                for x2 in range(x, x + w, checkgap):
                    print(direction, x2, y2)
                    add_line(x2, y2)

        if direction == "vertical":
            for x2 in range(x, x + w + gap, gap):
                for y2 in range(y, y + h, checkgap):
                    print(direction, x2, y2)
                    add_line(x2, y2)

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


    def HalftoneShape(self, thislayer, shape, shapetype):

        t = shape
        shapelist = PathToNodeList(t)

        x = int (t.bounds.origin.x)
        y = int (t.bounds.origin.y)
        w = int (t.bounds.size.width)
        h = int (t.bounds.size.height)

        grid = 13
        size = random.randrange(12, 24)

        for col in range(x, x+w, grid):
            for row in range(y, y+h, grid):
                if point_inside_polygon(col, row, shapelist):
                    nx = math.floor(col/grid) * grid
                    ny = math.floor(row/grid) * grid
                    if shapetype=="triangle":
                        c = drawTriangle(nx, ny, size, size)
                    elif shapetype=="circle":
                        c = drawCircle(nx, ny, size, size)
                    else:
                        c = drawTriangle(nx, ny, size, size)
                    thislayer.paths.append(c)
            size+=0.3


    def Fill_Halftone(self, thislayer, shape, shapetype):

        t = shape
        shapelist = PathToNodeList(t)

        x = int (t.bounds.origin.x)
        y = int (t.bounds.origin.y)
        w = int (t.bounds.size.width)
        h = int (t.bounds.size.height)

        grid = 13
        size = random.randrange(12, 24)
        size = 8

        for row in range(y, y+h, grid):
            for col in range(x, x+w, grid):
                if point_inside_polygon(col, row, shapelist):
                    nx = math.floor(col/grid) * grid
                    ny = math.floor(row/grid) * grid
                    if row%2==0:
                        adjust = grid/2
                    else:
                        adjust = 0
                    c = drawCircle(nx+adjust, ny, size, size)
                    G.add_paths(thislayer, [c])
            size+=0.1


GlitchPop()
