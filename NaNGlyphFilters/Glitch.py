# MenuTitle: Glitch
# -*- coding: utf-8 -*-
__doc__ = """
Glitch
"""

from NaNGFGraphikshared import AddPaths, AllPathBoundsFromPathList, ClearPaths, ShiftPath
from NaNGFNoise import noiseMap
from NaNGlyphsEnvironment import GSLayer
import random
from NaNGFNoise import pnoise1
from NaNGlyphsEnvironment import glyphsEnvironment as G
from NaNFilter import NaNFilter


class Glitch(NaNFilter):

	params = {
		"S": {"maxshift": 200},
		"M": {"maxshift": 300},
		"L": {"maxshift": 400}
	}
	sliceheight = 5

	def setup(self):
		pass

	def processLayer(self, thislayer, params):

		maxshift = params["maxshift"]
		# G.remove_overlap(thislayer)
		paths = list(thislayer.paths)
		ClearPaths(thislayer)
		slicedpaths = self.returnSlicedPaths(paths, self.sliceheight, thislayer)
		self.ShiftPathsNoise(slicedpaths, maxshift)
		ClearPaths(thislayer)
		AddPaths(slicedpaths, thislayer)
		G.remove_overlap(thislayer)

		self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=False, remStrayPoints=True, remOpenPaths=True, keepshape=False)

	def returnSlicedPaths(self, pathlist, sliceheight, thislayer):
		slicedpaths = []
		tmplayer = GSLayer()
		AddPaths(pathlist, tmplayer)
		bounds = AllPathBoundsFromPathList(pathlist, thislayer)
		ox, oy, w, h = bounds[0], bounds[1], bounds[2], bounds[3]

		starty = int(oy / sliceheight) * sliceheight - 1
		y = starty
		sh = sliceheight

		while y < starty + h:
			G.cut_layer(tmplayer, (ox - 1, y), (ox + w + 1, y))
			y += sh
			sh = sliceheight * random.randrange(1, 5)

		slicedpaths = tmplayer.paths
		del tmplayer
		return slicedpaths

	def ShiftPathsNoise(self, pathlist, maxshift):

		noisescale, seedy = 0.05, random.randrange(0, 100000)
		minsize, maxsize = 0, maxshift
		n = 0
		for p in pathlist:
			y_noiz = pnoise1(((1000 + n) + seedy) * noisescale, 3)
			ry = noiseMap(y_noiz, minsize, maxsize)
			ShiftPath(p, ry, "x")
			n += 1


Glitch()
