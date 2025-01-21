# MenuTitle: Dirt
# -*- coding: utf-8 -*-
__doc__ = """
Dirt
"""

from NaNGFAngularizzle import ConvertPathsToLineSegments, getListOfPoints
from NaNGFGraphikshared import ClearPaths, AddPaths, retractHandles, ConvertPathlistDirection, removeOverlapPathlist, defineStartXY, withinGlyphBlack, drawSpeck
from NaNGFNoise import NoiseOutline, noiseMap, pnoise1
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

		outlinedata = getListOfPoints(ConvertPathsToLineSegments(thislayer.paths, 20))

		ClearPaths(thislayer)
		noisepaths = NoiseOutline(thislayer, outlinedata, noisevars=[0.2, 0, 15])
		AddPaths(noisepaths, thislayer)
		retractHandles(thislayer)
		G.remove_overlap(thislayer)

		offsetpaths = self.saveOffsetPaths(
			thislayer, params["offset"], params["offset"], removeOverlap=True
		)

		outlinedata2 = G.outline_data_for_hit_testing(offsetpaths)

		dirt = self.AddDirt(thislayer, outlinedata2, params["walklen"])

		if dirt is not None:
			dirt = removeOverlapPathlist(dirt)
			dirt = ConvertPathlistDirection(dirt, 1)
			AddPaths(dirt, thislayer)
			# G.remove_overlap(thislayer)

		self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)

	def AddDirt(self, thislayer, outlinedata, walklen):

		start = defineStartXY(thislayer, outlinedata)

		if start is None:
			return None
		else:
			sx, sy = start[0], start[1]
			noisescale = 0.05
			seedx, seedy = random.randrange(0, 100000), random.randrange(0, 100000)
			minsize, maxsize = 0, 200
			dirt = []

			for n in range(0, walklen):

				x_noiz = pnoise1((n + seedx) * noisescale, 3)
				rx = noiseMap(x_noiz, minsize, maxsize)
				y_noiz = pnoise1(((1000 + n) + seedy) * noisescale, 3)
				ry = noiseMap(y_noiz, minsize, maxsize)
				nx = sx + rx
				ny = sy + ry

				if withinGlyphBlack(nx, ny, outlinedata):
					r = random.randrange(0, 10)
					if r == 2:
						size = random.randrange(7, 22)
						speck = drawSpeck(nx, ny, size, 6)
						dirt.append(speck)
						sx = nx
						sy = ny
			return dirt


Dirt()
