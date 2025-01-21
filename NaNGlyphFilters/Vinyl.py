# MenuTitle: Vinyl
# -*- coding: utf-8 -*-
__doc__ = """
Vinyl
"""

import random
from NaNGFAngularizzle import ConvertPathsToLineSegments, getListOfPoints
from NaNGFGraphikshared import AddPaths, ClearPaths, DoShadow, RoundPaths, convertToFitpath
from NaNGlyphsEnvironment import glyphsEnvironment as G

from NaNFilter import NaNFilter


class Vinyl(NaNFilter):

	params = {
		"S": {"it": 5, "depthmin": 20, "depthmax": 65},
		"M": {"it": 5, "depthmin": 25, "depthmax": 75},
		"L": {"it": 5, "depthmin": 30, "depthmax": 85}
	}
	glyph_stroke_width = 16
	shadow_stroke_width = 6
	angle = -160  # random.randrange(0, 360)

	def processLayer(self, thislayer, params):

		it, depthmin, depthmax = params["it"], params["depthmin"], params["depthmax"]

		G.remove_overlap(thislayer)
		pathlist = ConvertPathsToLineSegments(thislayer.paths, 10)
		outlinedata = getListOfPoints(pathlist)

		ClearPaths(thislayer)

		shadowpaths = []
		for n in range(0, it):
			depth = random.randrange(depthmin, depthmax)
			angle = random.randrange(0, 360)
			shadowpaths.extend(DoShadow(thislayer, outlinedata, angle, depth, "paths"))
			AddPaths(shadowpaths, thislayer)

		G.remove_overlap(thislayer)

		roundpaths = RoundPaths(thislayer.paths, "nodes")
		blobs = []
		for p in roundpaths:
			blobs.append(convertToFitpath(p, True))

		ClearPaths(thislayer)

		AddPaths(blobs, thislayer)

		G.remove_overlap(thislayer)

		self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)


Vinyl()
