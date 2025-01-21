# MenuTitle: Distressed
# -*- coding: utf-8 -*-
__doc__ = """
Distressed
"""

from GlyphsApp import GSLayer
from NaNGFGraphikshared import ShiftPath, AllPathBounds, ClearPaths
from NaNGFAngularizzle import ConvertPathsToLineSegments, getListOfPoints
from NaNGFSpacePartition import BreakUpSpace
from NaNGlyphsEnvironment import glyphsEnvironment as G
from NaNFilter import NaNFilter
import random


def ApplyBurn(thislayer, groups):

	for g in groups:

		if len(g) <= 2:
			continue

		shiftmax = random.randrange(1, 50)
		shiftype = random.choice(["x", "y", "xy"])

		templayer = GSLayer()
		G.add_paths(templayer, g)
		templayer.removeOverlap()

		for p in templayer.paths:
			ShiftPath(p, shiftmax, shiftype)
			G.add_paths(thislayer, [p])
			# nodelen = len(p.nodes)


class Distressed(NaNFilter):

	def processLayer(self, thislayer, params):

		# offset = params["offset"]
		gridsize = 30  # params["gridsize"]

		pathlist = ConvertPathsToLineSegments(thislayer.paths, 20)
		outlinedata = getListOfPoints(pathlist)
		bounds = AllPathBounds(thislayer)

		ClearPaths(thislayer)

		newtris = self.SortCollageSpace(thislayer, outlinedata, gridsize, bounds, "stick", randomize=True)
		maxchain = random.randrange(30, 60)
		groups = BreakUpSpace(thislayer, newtris, gridsize, maxchain)
		ApplyBurn(thislayer, groups)
		# AddPaths(edgetris, thislayer)
		# thislayer.removeOverlap()


Distressed()
