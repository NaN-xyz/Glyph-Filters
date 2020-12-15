# MenuTitle: Marker Hatch
# -*- coding: utf-8 -*-
__doc__ = """
Marker Hatch
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFSpacePartition import *
from NaNGFNoise import *
from NaNFilter import NaNFilter


class Shatter(NaNFilter):

    params = {
        "S": {"offset":20, "sliceheight": 5},
        "M": {"offset":0, "sliceheight": 10},
        "L": {"offset":0, "sliceheight": 10}
    }
    sliceheight = 10
    angle = 45

    def setup(self):
        pass

    def processLayer(self, thislayer, params):
        if glyphSize(thislayer.parent) == "S":
            self.processLayerSmall(thislayer, params)
        else:
            self.processLayerLarge(thislayer, params)

    def processLayerSmall(self, thislayer, params):
        paths = copy.copy(thislayer.paths)
        rounded = returnRoundedPaths(paths)
        ClearPaths(thislayer)
        AddAllPathsToLayer(rounded, thislayer)
        #retractHandles(thislayer)
        self.doclean(thislayer)

    def processLayerLarge(self, thislayer, params):

        sliceheight = params["sliceheight"]
        thislayer.removeOverlap()

        bounds = AllPathBounds(thislayer)
        thislayercopy = thislayer.copy()
        ClearPaths(thislayer)
       
        spaths = self.returnSlicedPaths(thislayer, thislayercopy, sliceheight, bounds)

        n=1
        maxshift = 20
        for sh, row in spaths:
            for p in row:
                if n%2==0: d=random.randrange(0,maxshift)
                else: d=random.randrange(maxshift*-1,0)
                self.shufflePaths(row, d)
            n+=1
            rounded = returnRoundedPaths(row)

            AddAllPathsToLayer(rounded, thislayer)
            retractHandles(thislayer)
            self.doclean(thislayer)
        

    def doclean(self, thislayer):
        self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)

    def shufflePaths(self, row, d):
        shiftx = d * cos(radians(self.angle))
        shifty = d * sin(radians(self.angle))
        for path in row:
            path.applyTransform((
                                    1, # x scale factor
                                    0, # x skew factor
                                    0, # y skew factor
                                    1, # y scale factor
                                    shiftx, # x position
                                    shifty  # y position
                                    ))

    def returnSlicedPaths(self, thislayer, thislayercopy, sliceheight, bounds):

        slicedpaths = []
        ox, oy, w, h = bounds[0], bounds[1], bounds[2], bounds[3]
        starty = oy
        y = oy
        dist = thislayer.width*3
        sh = 0

        angle = self.angle + random.randrange(-5,5)

        while y < oy+h+dist:

            rowpaths = []
            tmplayer = thislayercopy.copy()

            shiftx = dist * cos(radians(self.angle))
            shifty = dist * sin(radians(self.angle))

            cutax1, cutay1 = ox-1, y-dist-sh
            cutax2, cutay2 = ox+1+shiftx, y-sh+shifty
            cutbx1, cutby1 = ox-1, y-dist
            cutbx2, cutby2 = ox+1+shiftx, y+shifty
            # c = drawCircle(cutax1-20, cutay1, 20, 20)
            # thislayer.paths.append(c)

            buff = 15 #increase top+bottom margin of container
            slicepoly = [ [cutax1-2, cutay1-buff], [cutax2+2, cutay2-buff], [cutbx2+2, cutby2+buff], [cutbx1-2, cutby1+buff] ]
            slicepath = drawSimplePath(slicepoly)
            slicedata = setGlyphCoords(ConvertPathsToSkeleton([slicepath], 20))[0][1]
            #thislayer.paths.append(slicepath)

            tmplayer.cutBetweenPoints(NSPoint(cutax1, cutay1), NSPoint(cutax2, cutay2))
            tmplayer.cutBetweenPoints(NSPoint(cutbx1, cutby1), NSPoint(cutbx2, cutby2))

            for path in tmplayer.paths:
                try:
                    pathdata = setGlyphCoords(ConvertPathsToSkeleton([path], 20))[0][1]
                    if self.WithinSlice(pathdata, slicedata):
                        rowpaths.append(path)
                except:
                    pass

            del tmplayer
            sh = sliceheight * random.randrange(1, 20)
            y += sh#+sliceheight
            slicedpaths.append([sh, rowpaths])

        return slicedpaths

    def WithinSlice(self, shape, glyph):
        for nx, ny in shape:
            if not point_inside_polygon(nx,ny,glyph):
                return False
        return True


Shatter()
