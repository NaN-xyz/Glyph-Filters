# MenuTitle: Burned
# -*- coding: utf-8 -*-
__doc__ = """
Burned
"""
import random

from NaNGFAngularizzle import ConvertPathsToLineSegments, getListOfPoints
from NaNGFGraphikshared import ClearPaths, AddPaths, AllPathBounds, RoundPath, convertToFitpath
from NaNFilter import NaNFilter
from NaNGFSpacePartition import BreakUpSpace
from NaNGlyphsEnvironment import glyphsEnvironment as G


def returnRoundedPaths(paths):
	roundedpathlist = []
	for p in paths:
		roundedpath = RoundPath(p, "nodes")
		try:
			roundedpathlist.append(convertToFitpath(roundedpath, True))
		except Exception as e:
			print(("returnRoundedPaths failed:", e))
	return roundedpathlist


class Burn(NaNFilter):
	params = {
		"S": {"gridsize": 40},
		"M": {"gridsize": 45},
		"L": {"gridsize": 50},
	}

	def processLayer(self, thislayer, params):
		maxchain = random.randrange(200, 400)
		outlinedata = getListOfPoints(ConvertPathsToLineSegments(thislayer.paths, 20))
		bounds = AllPathBounds(thislayer)

		ClearPaths(thislayer)

		newtris = self.SortCollageSpace(
			thislayer,
			outlinedata,
			params["gridsize"],
			bounds,
			action="overlap",
			randomize=True,
		)
		if not newtris:
			raise ValueError("Layer '%s' had no 'inside'. Are the path directions correct?" % thislayer)

		groups = BreakUpSpace(thislayer, newtris, params["gridsize"], maxchain)

		for g in groups:
			if len(g) > 2:
				G.add_paths(thislayer, g)

		G.remove_overlap(thislayer)
		roundedpathlist = returnRoundedPaths(thislayer.paths)
		ClearPaths(thislayer)
		AddPaths(roundedpathlist, thislayer)
		self.CleanOutlines(
			thislayer,
			remSmallPaths=True,
			remSmallSegments=True,
			remStrayPoints=True,
			remOpenPaths=True,
			keepshape=False,
		)


Burn()
