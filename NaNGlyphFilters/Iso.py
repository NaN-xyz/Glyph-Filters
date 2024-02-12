# MenuTitle: Iso
# -*- coding: utf-8 -*-
__doc__ = """
Iso
"""

import random
from NaNFilter import NaNFilter
from NaNGFAngularizzle import ConvertPathsToSkeleton, setGlyphCoords
from NaNGFGraphikshared import AllPathBounds, ClearPaths
from NaNGFSpacePartition import BreakUpSpace
from NaNGlyphsEnvironment import glyphsEnvironment as G


class Iso(NaNFilter):

	params = {
		"S": {"offset": 0, "gridsize": 45},
		"M": {"offset": 4, "gridsize": 45},
		"L": {"offset": 4, "gridsize": 45},
	}

	def processLayer(self, thislayer, params):
		G.remove_overlap(thislayer)
		pathlist = ConvertPathsToSkeleton(thislayer.paths, 20)
		outlinedata = setGlyphCoords(pathlist)
		bounds = AllPathBounds(thislayer)

		offsetpaths = self.saveOffsetPaths(thislayer, params["offset"], params["offset"], removeOverlap=True)
		pathlist2 = ConvertPathsToSkeleton(offsetpaths, 4)
		outlinedata2 = setGlyphCoords(pathlist2)

		ClearPaths(thislayer)

		newtris = self.SortCollageSpace(thislayer, outlinedata, outlinedata2, params["gridsize"], bounds, action="overlap", snap=True)
		maxchain = random.randrange(200, 400)
		groups = BreakUpSpace(thislayer, outlinedata, newtris, params["gridsize"], maxchain)
		for g in groups:
			if len(g) > 2:
				for path in g:
					thislayer.paths.append(path)

		G.correct_path_direction(thislayer)
		self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)


Iso()
