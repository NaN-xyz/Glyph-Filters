# MenuTitle: 17. Scribble
# -*- coding: utf-8 -*-
__doc__ = """
17. Scribble
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFSpacePartition import *
from NaNGFNoise import *
from NaNFilter import NaNFilter



class Scribble(NaNFilter):
    params = {
        "S": {"offset": -13, "iterations": 2, "walklen": 100},
        "M": {"offset": -15, "iterations": 3, "walklen": 800},
        "L": {"offset": -18, "iterations": 3, "walklen": 900},
    }
    pen = 8

    def processLayer(self, thislayer, params):

        outlinedata = setGlyphCoords(doAngularizzle(thislayer.paths, 20))

        ClearPaths(thislayer)

        noisepaths = NoiseOutline(thislayer, outlinedata, noisevars=[0.05, 0, 35])
        noiseoutline = self.expandMonolineFromPathlist(noisepaths, self.pen)

        allscribbles = []
        for n in range(0, params["iterations"]):
            scribble = self.ScribblePath(thislayer, outlinedata, params["walklen"])
            if scribble is not None:
                scribble = drawSimplePath(scribble, False, False)
                scribblemono = self.expandMonolineFromPathlist([scribble], self.pen)
                AddAllPathsToLayer(scribblemono, thislayer)

        retractHandles(thislayer)
        AddAllPathsToLayer(noiseoutline, thislayer)
        thislayer.removeOverlap()

    def ScribblePath(self, thislayer, outlinedata, walklen):

        start = defineStartXY(thislayer, outlinedata)
        print start

        if start is None:
            return None
        else:
            sx, sy = start[0], start[1]
            noisescale = 0.05
            seedx, seedy = random.randrange(0,100000), random.randrange(0,100000)
            minsize, maxsize = 0, 80
            walkpath = []

            for n in range(0, walklen):
                x_noiz = pnoise1( (n+seedx)*noisescale, 3) 
                rx = noiseMap( x_noiz, minsize, maxsize )
                y_noiz = pnoise1( ((1000+n)+seedy)*noisescale, 3) 
                ry = noiseMap( y_noiz, minsize, maxsize )
                nx = sx + rx
                ny = sy + ry
                if withinGlyphBlack(nx, ny, outlinedata):
                    sx = nx
                    sy = ny
                    walkpath.append([sx, sy])
            return walkpath

Scribble()
