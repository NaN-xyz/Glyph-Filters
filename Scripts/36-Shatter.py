# MenuTitle: 36. Shatter
# -*- coding: utf-8 -*-
__doc__ = """
36. Shatter
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFSpacePartition import *
from NaNGFNoise import *
from NaNFilter import NaNFilter


class Shatter(NaNFilter):

    params = {
        "S": {"maxshift": 200},
        "M": {"maxshift": 300},
        "L": {"maxshift": 400}
    }
    sliceheight = 50

    def setup(self):
        pass

    def processLayer(self, thislayer, params):

        maxshift = params["maxshift"]
        paths = copy.copy(thislayer.paths)
        bounds = AllPathBounds(thislayer)
        #print bounds
        ClearPaths(thislayer)
       
        slicedpaths = self.returnSlicedPaths(thislayer, thislayer.paths, self.sliceheight, bounds)
        print slicedpaths
        AddAllPathsToLayer(slicedpaths, thislayer)
        #thislayer.removeOverlap()

    def returnSlicedPaths(self, thislayer, pathlist, sliceheight, bounds):

        slicedpaths = []
        ox, oy, w, h = bounds[0], bounds[1], bounds[2], bounds[3]
        starty = oy
        y = oy + sliceheight

        while y < starty+h:

            #print "length of pathlist", len(pathlist)

            c = drawCircle(ox-1, y, 20, 20)
            thislayer.paths.append(c)

            tmplayer = GSLayer()
            AddAllPathsToLayer(pathlist, tmplayer)

            tmplayer.cutBetweenPoints(NSPoint(ox-1, y), NSPoint(ox+w+1, y))
            sh = sliceheight * random.randrange(1, 3)
            y+=sh

            #print "length of temp pathlist", len(tmplayer.paths)

            tp = [tmplayer.paths]
            slicedpaths.extend(tp)
            #print "number of sliced paths: ", len(slicedpaths) 
            del tmplayer

        return slicedpaths



Shatter()
