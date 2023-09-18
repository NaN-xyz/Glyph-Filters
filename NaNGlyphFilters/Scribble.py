# MenuTitle: Scribble
# -*- coding: utf-8 -*-
__doc__ = """
Scribble
"""

from NaNGFGraphikshared import AddAllPathsToLayer, ClearPaths, defineStartXY, drawSimplePath, retractHandles, withinGlyphBlack
from NaNGFAngularizzle import ConvertPathsToSkeleton, setGlyphCoords
from NaNFilter import NaNFilter
from NaNGFNoise import NoiseOutline, noiseMap
from NaNGlyphsEnvironment import glyphsEnvironment as G
import random


class Scribble(NaNFilter):
    params = {
        "S": {"offset": -13, "iterations": 2, "walklen": 100},
        "M": {"offset": -15, "iterations": 3, "walklen": 800},
        "L": {"offset": -18, "iterations": 3, "walklen": 900},
    }
    pen = 8

    def processLayer(self, thislayer, params):

        G.remove_overlap(thislayer)
        outlinedata = setGlyphCoords(ConvertPathsToSkeleton(thislayer.paths, 20))

        ClearPaths(thislayer)

        noisepaths = NoiseOutline(thislayer, outlinedata, noisevars=[0.05, 0, 35])
        noiseoutline = self.expandMonolineFromPathlist(noisepaths, self.pen)
        outlinedata2 = setGlyphCoords(ConvertPathsToSkeleton(noisepaths, 4))
        
        allscribbles = []
        for n in range(0, params["iterations"]):
            scribble = self.ScribblePath(thislayer, outlinedata2, params["walklen"])
            if scribble is not None:
                scribble = drawSimplePath(scribble, False, False)
                scribblemono = self.expandMonolineFromPathlist([scribble], self.pen)
                AddAllPathsToLayer(scribblemono, thislayer)

        retractHandles(thislayer)
        AddAllPathsToLayer(noiseoutline, thislayer)
        G.remove_overlap(thislayer)
        self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)

    def ScribblePath(self, thislayer, outlinedata, walklen):

        start = defineStartXY(thislayer, outlinedata)
        if start is None:
            return None
        else:
            sx, sy = start[0], start[1]
            noisescale = 0.05
            seedx, seedy = random.randrange(0,100000), random.randrange(0,100000)
            minsize, maxsize = 0, 80
            walkpath = []

            for n in range(0, walklen):
                rx = noiseMap( random.random(), minsize, maxsize ) - 10
                ry = noiseMap( random.random(), minsize, maxsize ) - 10
                nx = sx + rx
                ny = sy + ry
                if withinGlyphBlack(nx, ny, outlinedata):
                    sx = nx
                    sy = ny
                    walkpath.append([sx, sy])
            return walkpath

Scribble()
