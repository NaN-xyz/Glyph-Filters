# MenuTitle: Dirt
# -*- coding: utf-8 -*-
__doc__ = """
Dirt
"""

from NaNGFAngularizzle import ConvertPathsToSkeleton, setGlyphCoords
from NaNGFGraphikshared import ClearPaths, AddAllPathsToLayer, retractHandles, ConvertPathlistDirection, removeOverlapPathlist, defineStartXY, withinGlyphBlack, drawSpeck
from NaNGFNoise import NoiseOutline, noiseMap
from NaNFilter import NaNFilter
import random
from NaNGlyphsEnvironment import glyphsEnvironment as G


class Dirt(NaNFilter):
    params = {
        "S": {"offset": -13, "walklen": 400},
        "M": {"offset": -15, "walklen": 2000},
        "L": {"offset": -18, "walklen": 3000},
    }

    def processLayer(self, thislayer, params):

        outlinedata = setGlyphCoords(ConvertPathsToSkeleton(thislayer.paths, 20))

        ClearPaths(thislayer)
        noisepaths = NoiseOutline(thislayer, outlinedata, noisevars=[0.2, 0, 15])
        AddAllPathsToLayer(noisepaths, thislayer)
        retractHandles(thislayer)
        G.remove_overlap(thislayer)

        offsetpaths = self.saveOffsetPaths(
            thislayer, params["offset"], params["offset"], removeOverlap=True
        )
        outlinedata2 = setGlyphCoords(ConvertPathsToSkeleton(offsetpaths, 4))

        dirt = self.AddDirt(thislayer, outlinedata2, params["walklen"])

        if dirt is not None:
            dirt = ConvertPathlistDirection( removeOverlapPathlist(dirt), 1 )
            AddAllPathsToLayer(dirt, thislayer)
            G.remove_overlap(thislayer)

        self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)

    def AddDirt(self, thislayer, outlinedata, walklen):

        start = defineStartXY(thislayer, outlinedata)

        if start is None:
            return None
        else:
            sx, sy = start[0], start[1]
            noisescale = 0.05
            seedx, seedy = random.randrange(0,100000), random.randrange(0,100000)
            minsize, maxsize = -100, 100
            dirt = []

            for n in range(0, walklen):
                rx = noiseMap( random.random(), minsize, maxsize )
                ry = noiseMap( random.random(), minsize, maxsize )
                nx = sx + rx
                ny = sy + ry

                if withinGlyphBlack(nx, ny, outlinedata):
                    r = random.randrange(0,10)
                    if r==2:
                        size = random.randrange(7,22)
                        speck = drawSpeck(nx, ny, size, 6)
                        dirt.append(speck)
                        sx = nx
                        sy = ny
            return dirt


Dirt()
