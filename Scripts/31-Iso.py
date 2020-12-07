#MenuTitle: 31. Iso
# -*- coding: utf-8 -*-
__doc__="""
31. Iso
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFSpacePartition import *
from NaNFilter import NaNFilter


class Iso(NaNFilter):

	params = {
		"S": {"offset": 0, "gridsize": 45},
		"M": {"offset": 4, "gridsize": 45},
		"L": {"offset": 4, "gridsize": 45},
	}

	def processLayer(self, thislayer, params):
		pathlist = ConvertPathsToSkeleton(thislayer.paths, 20)
		outlinedata = getGlyphCoords(pathlist)
		bounds = AllPathBounds(thislayer)

		offsetpaths = self.saveOffsetPaths(thislayer, params["offset"], params["offset"], removeOverlap=True)
		pathlist2 = ConvertPathsToSkeleton(offsetpaths, 4)
		outlinedata2 = getGlyphCoords(pathlist2)

		ClearPaths(thislayer)

		newtris = self.SortCollageSpace(thislayer, outlinedata, outlinedata2, params["gridsize"], bounds, action="overlap", snap=True)
		maxchain = random.randrange(200,400)
		groups = BreakUpSpace(thislayer, outlinedata, newtris, params["gridsize"], maxchain)
		for g in groups:
			if len(g)>2:
				for path in g:
					thislayer.paths.append(path)

		thislayer.correctPathDirection()

Iso()
