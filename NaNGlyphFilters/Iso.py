# MenuTitle: Iso
# -*- coding: utf-8 -*-
__doc__ = """
Iso
"""

import random
from NaNFilter import NaNFilter
from NaNGFGraphikshared import AllPathBounds, ClearPaths
from NaNGFSpacePartition import BreakUpSpace
from NaNGlyphsEnvironment import glyphsEnvironment as G


class Iso(NaNFilter):

	params = {
		"S": {"gridsize": 45},
		"M": {"gridsize": 45},
		"L": {"gridsize": 45},
	}

	def processLayer(self, thislayer, params):
		G.remove_overlap(thislayer)
		outlinedata = G.outline_data_for_hit_testing(thislayer)
		bounds = AllPathBounds(thislayer)

		ClearPaths(thislayer)

		newtris = self.SortCollageSpace(thislayer, outlinedata, params["gridsize"], bounds, action="overlap", snap=True)
		maxchain = random.randrange(200, 400)
		groups = BreakUpSpace(thislayer, newtris, params["gridsize"], maxchain)
		for g in groups:
			if len(g) > 2:
				for path in g:
					thislayer.paths.append(path)

		G.correct_path_direction(thislayer)
		self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)


Iso()
