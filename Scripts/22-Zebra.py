# MenuTitle: 22. Zebra
# -*- coding: utf-8 -*-
__doc__ = """
22. Zebra
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import NaNFilter

from itertools import izip

# Note that this is *not* the same as the pairwise recipe in the itertools page
def pairs(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)


# THE MAIN NOISE WAVE FUNCTION ACTION


def NoiseWaves(thislayer, outlinedata, b, minsize, maxsize):

    noisescale = 0.002
    yshift = maxsize / 4

    if b is None:
        return []

    tx, ty, tw, th = b
    seedx = random.randrange(0, 100000)
    seedy = random.randrange(0, 100000)

    waves = []
    searchstep = 2

    for y in range(ty, ty + th, 20):
        lines = []
        wave = []

        for x in range(tx, tx + tw + 40, searchstep):
            if withinGlyphBlack(x, y, outlinedata):
                noiz = abs(
                    snoise2((y + seedy) * noisescale, (x + seedx) * noisescale, 4)
                )
                size = noiseMap(noiz, minsize, maxsize)
                wave.append([x, y + size - yshift])
            elif len(wave) > 4:
                lines.append(wave)
                wave = []

        if lines:
            waves.append(lines)

    wavepaths = []
    # draw the wave data in to paths

    for lines1, lines2 in pairs(waves):
        if len(lines1) != len(lines2):
            continue

        for wav, wav2 in zip(lines1, lines2):
            np = convertToFitpath(wav + list(reversed(wav2)), True)
            wavepaths.append(np)

    return wavepaths


class Zebra(NaNFilter):
    minsize, maxsize = 40, 200

    def processLayer(self, thislayer, params):
        offsetpaths = self.saveOffsetPaths(thislayer, 0, 0, removeOverlap=True)
        pathlist = ConvertPathsToSkeleton(offsetpaths, 20)
        bounds = AllPathBoundsFromPathList(pathlist)
        outlinedata = setGlyphCoords(pathlist)

        wavepaths = NoiseWaves(
            thislayer, outlinedata, bounds, self.minsize, self.maxsize
        )

        ClearPaths(thislayer)
        wavepaths = ConvertPathlistDirection(wavepaths, -1)
        AddAllPathsToLayer(wavepaths, thislayer)


Zebra()
