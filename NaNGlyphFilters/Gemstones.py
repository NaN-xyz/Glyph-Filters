# MenuTitle: Gemstones
# -*- coding: utf-8 -*-
__doc__ = """
Gemstones
"""

from NaNGFAngularizzle import ConvertPathsToLineSegments, getListOfPoints
from NaNGFGraphikshared import AddPaths, ClearPaths, ConvertPathlistDirection, retractHandles
from NaNGlyphsEnvironment import GSNode, GSLINE
from NaNFilter import NaNFilter
from NaNCommonFilters import moonrocks, spikes
from NaNGlyphsEnvironment import glyphsEnvironment as G


def drawSpike(gspath, x1, y1, midx, midy, x2, y2, pushdist):
	gspath.nodes.append(GSNode([midx, midy], type=GSLINE))
	gspath.nodes.append(GSNode([x2, y2], type=GSLINE))


class Gemstones(NaNFilter):
	params = {
		"S": {"offset": -5, "minpush": 10, "maxpush": 20, "iterations": 50},
		"M": {"offset": -10, "minpush": 20, "maxpush": 40, "iterations": 400},
		"L": {"offset": -20, "minpush": 20, "maxpush": 40, "iterations": 420},
	}

	def processLayer(self, thislayer, params):
		offsetpaths = self.saveOffsetPaths(thislayer, params["offset"], params["offset"], removeOverlap=False)
		pathlist = ConvertPathsToLineSegments(offsetpaths, 4)
		outlinedata = getListOfPoints(pathlist)
		outlinedata2 = G.outline_data_for_hit_testing(offsetpaths)

		ClearPaths(thislayer)

		spikepaths = spikes(outlinedata, params["minpush"], params["maxpush"], 10, 22, drawSpike)
		AddPaths(spikepaths, thislayer)

		rockpaths = moonrocks(thislayer, outlinedata2, params["iterations"], maxgap=8)
		rockpaths = ConvertPathlistDirection(rockpaths, 1)
		AddPaths(rockpaths, thislayer)
		retractHandles(thislayer)

		self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)


Gemstones()
