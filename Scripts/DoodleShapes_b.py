# MenuTitle: 28. DoodleShapes b
# -*- coding: utf-8 -*-
__doc__ = """
28. DoodleShapes b
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFSpacePartition import *
from NaNGFNoise import *

from NaNFilter import NaNFilter


class DoodleShadow(NaNFilter):

    params = {
        "S": {"offset": 10},
        "M": {"offset": 10},
        "L": {"offset": 10}
    }
    shape_stroke_width = 16
    shadow_stroke_width = 6
    angle = -160 #random.randrange(0, 360)

    def setup(self):
        self.unit = 30
        self.sizes = [16, 8, 4, 2]#[16,8,4,2,1]
        self.shapetypes = ["circle","triangle","diamond"]

    def processLayer(self, thislayer, params):

        offset = params["offset"]

        thislayer.removeOverlap()
        pathlist = doAngularizzle(thislayer.paths, 20)
        outlinedata = setGlyphCoords(pathlist)
        bounds = AllPathBounds(thislayer)

        offsetpaths = self.saveOffsetPaths(
            thislayer, offset, offset, removeOverlap=True
        )

        self.setupChecker(bounds)

        ClearPaths(thislayer)

        noiseglyphoutline = NoiseOutline(thislayer, outlinedata, noisevars=[0.05, 0, 35])
        noiseglyphoutline = self.expandMonolineFromPathlist(noiseglyphoutline, self.shape_stroke_width)

        # foundshapes = self.ShapefitRandom(thislayer, outlinedata, bounds)
        foundshapes = ConvertPathlistDirection( self.ShapefitModular(thislayer, outlinedata), -1 )
        
        #AddAllPathsToLayer(foundshapes, thislayer)

        pathlist2 = doAngularizzle(foundshapes, 20)
        outlinedata2 = setGlyphCoords(pathlist2)

        shadowpaths = DoShadow(thislayer, outlinedata2, self.angle, 30, "lines")
        shadowoutline = self.expandMonolineFromPathlist(shadowpaths, self.shadow_stroke_width)
        #AddAllPathsToLayer(shadowoutline, thislayer)

        noisepaths = NoiseOutline(thislayer, outlinedata2, noisevars=[0.05, 0, 5])
        noisepaths_sorted = self.SortShapeSizes(noisepaths)
        noiseoutline = self.expandMonolineFromPathlist(noisepaths_sorted[1], self.shape_stroke_width)

        # shadowpaths = DoShadow(thislayer, outlinedata, self.angle, depth, "lines")
        # shadowoutline = self.expandMonolineFromPathlist(shadowpaths, self.shadow_stroke_width)

        AddAllPathsToLayer(noiseoutline, thislayer)
        AddAllPathsToLayer(noisepaths_sorted[0], thislayer)
        AddAllPathsToLayer(noiseglyphoutline, thislayer)

        # AddAllPathsToLayer(shadowoutline, thislayer)
       
        #thislayer.removeOverlap()

    def SortShapeSizes(self, shapes):

        boundary = 100
        small, large = [], []
        for shape in shapes:
            sw = shape.bounds.size.width
            if sw<boundary:
                small.append(shape)
            else:
                large.append(shape)
        return [small, large]


    def ShapefitModular(self, thislayer, outlinedata):

        # try and draw object if space not already occupied

        foundshapes = []

        for multiplier in self.sizes:

            shapesize = self.unit * multiplier

            for stepy in range(0, self.ysteps, multiplier):

                y = self.oy + (stepy*self.unit)

                for stepx in range(0, self.xsteps, multiplier):

                    x = self.ox + (stepx*self.unit)

                    shapepath = []

                    nx = x+shapesize/2
                    ny = y+shapesize/2

                    shapetype = random.choice(self.shapetypes)

                    if shapetype=="circle":
                        shape = drawCircle(nx, ny, shapesize-2, shapesize-2)
                    if shapetype=="diamond":
                        shape = drawDiamond(nx, ny, shapesize-2, shapesize-2)
                    if shapetype=="triangle":
                        shape = drawTriangle(nx, ny, shapesize-2, shapesize-2)
                    if shapetype=="pentagram":
                        shape = drawSidedPolygon(nx, ny, shapesize, 6)

                    shapepath.append(shape)
                    nshape = doAngularizzle(shapepath, 10)
                    nshape = setGlyphCoords(nshape)
                    finalshape = nshape[0][1]
                    
                    if ShapeWithinOutlines(finalshape, outlinedata):

                        if self.isSlotFree(stepx, stepy, multiplier):

                            foundshapes.append(shape)
                            self.updateChecker(stepx, stepy, multiplier)


        return foundshapes



    def isSlotFree(self, stepx, stepy, multiplier):
        free = True
        for ypos in range(stepy, stepy+multiplier):
            for xpos in range(stepx, stepx+multiplier):
                try:
                    if self.checker[ypos][xpos] == False:
                        free = False
                        break
                except:
                    free = False
                    break
        return free

    def setupChecker(self, bounds):
        self.available_slots = []
        self.ox, self.oy, self.ow, self.oh = bounds
        self.ysteps = self.oh // self.unit
        self.xsteps = self.ow // self.unit
        self.checker = []

        for stepy in range(0, self.ysteps + 3):
            xlist = []
            for stepx in range(0, self.xsteps + 3):
                xlist.append(True)
            self.checker.append(xlist)

    def setAvailableSlots(self, thislayer, outlinedata):
        for stepy in range(0, self.ysteps + 3, 1):

            y = self.oy + (stepy * self.unit)

            for stepx in range(0, self.xsteps + 3, 1):

                x = self.ox + (stepx * self.unit)
                shapepath = []
                nx, ny = x + self.unit / 2, y + self.unit / 2
                shape = drawTriangle(nx, ny, 6, 6)
                shapepath.append(shape)

                nshape = doAngularizzle(shapepath, 10)
                nshape = setGlyphCoords(nshape)
                finalshape = nshape[0][1]

                if ShapeWithinOutlines(finalshape, outlinedata):
                    self.checker[stepy][stepx] = True
                    self.available_slots.append([stepx, stepy])
                else:
                    self.checker[stepy][stepx] = False


    def updateChecker(self, stepx, stepy, multiplier):
        for ypos in range(stepy, stepy+multiplier):
            for xpos in range(stepx, stepx+multiplier):
                try:
                    self.checker[ypos][xpos] = False
                except:
                    pass

    # def updateChecker(self, xpos, ypos):
    #     self.checker[ypos][xpos] = False

    #     item = [xpos, ypos]
    #     if item in self.available_slots:
    #         self.available_slots.remove(item)

DoodleShadow()
