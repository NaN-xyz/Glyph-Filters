# MenuTitle: 29. SpeckledDirt
# -*- coding: utf-8 -*-
__doc__ = """
29. SpeckledDirt
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFSpacePartition import *
from NaNGFNoise import *
from NaNFilter import NaNFilter



class SpeckledDirt(NaNFilter):
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
        thislayer.removeOverlap()

        offsetpaths = self.saveOffsetPaths(
            thislayer, params["offset"], params["offset"], removeOverlap=True
        )
        outlinedata2 = setGlyphCoords(ConvertPathsToSkeleton(offsetpaths, 4))

        dirt = self.AddDirt(thislayer, outlinedata2, params["walklen"])
        if dirt is not None:
            dirt = ConvertPathlistDirection( removeOverlapPathlist(dirt), 1 )
            AddAllPathsToLayer(dirt, thislayer)
            thislayer.removeOverlap()

    def AddDirt(self, thislayer, outlinedata, walklen):

        start = defineStartXY(thislayer, outlinedata)

        if start is None:
            return None
        else:
            sx, sy = start[0], start[1]
            noisescale = 0.05
            seedx, seedy = random.randrange(0,100000), random.randrange(0,100000)
            minsize, maxsize = 0, 200
            dirt = []

            for n in range(0, walklen):

                x_noiz = pnoise1( (n+seedx)*noisescale, 3) 
                rx = noiseMap( x_noiz, minsize, maxsize )
                y_noiz = pnoise1( ((1000+n)+seedy)*noisescale, 3) 
                ry = noiseMap( y_noiz, minsize, maxsize )
                nx = sx + rx
                ny = sy + ry

                if withinGlyphBlack(nx, ny, outlinedata):
                    r = random.randrange(0,10)
                    if r==2:
                        size = random.randrange(6,22)
                        speck = drawSpeck(nx, ny, size, 6)
                        dirt.append(speck)
                        sx = nx
                        sy = ny


SpeckledDirt()
