# MenuTitle: Moon Rocks
# -*- coding: utf-8 -*-
__doc__ = """
Moon Rocks
"""

from NaNGFAngularizzle import ConvertPathsToLineSegments, getListOfPoints
from NaNGFGraphikshared import AddPaths, ConvertPathlistDirection
from NaNFilter import NaNFilter
from NaNCommonFilters import moonrocks


class MoonRocks(NaNFilter):
	params = {
		"S": {"offset": -5, "iterations": 150},
		"M": {"offset": -15, "iterations": 1200},
		"L": {"offset": -20, "iterations": 1220},
	}

	def processLayer(self, thislayer, params):
		offsetpaths = self.saveOffsetPaths(
			thislayer, params["offset"], params["offset"], removeOverlap=False
		)
		outlinedata = getListOfPoints(ConvertPathsToLineSegments(offsetpaths, 20))
		moonrockpaths = moonrocks(thislayer, outlinedata, params["iterations"], shapetype="blob", maxgap=8)
		ConvertPathlistDirection(moonrockpaths, 1)
		AddPaths(moonrockpaths, thislayer)
		self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)


MoonRocks()
