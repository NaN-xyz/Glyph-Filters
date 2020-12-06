#MenuTitle: 27. Gemstones
# -*- coding: utf-8 -*-
__doc__="""
27. Gemstones
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import NaNFilter
from NaNCommonFilters import moonrocks, spikes

def drawSpike(gspath, x1, y1, midx, midy, x2, y2, pushdist):
	gspath.nodes.append(GSNode([midx, midy], type = GSLINE))
	gspath.nodes.append(GSNode([x2, y2], type = GSLINE))


class Gemstones(NaNFilter):
	params = {
		"S": { "offset": -5, "minpush": 10, "maxpush": 20, "iterations": 50 },
		"M": { "offset": -10, "minpush": 20, "maxpush": 40, "iterations": 400 },
		"L": { "offset": -20, "minpush": 20, "maxpush": 40, "iterations": 420 },
	}

	def processLayer(self, thislayer, params):
		offsetpaths = self.saveOffsetPaths(thislayer, params["offset"], params["offset"], removeOverlap=False)
		pathlist = doAngularizzle(offsetpaths, 4)
		outlinedata = setGlyphCoords(pathlist)

		ClearPaths(thislayer)

		spikepaths = spikes(thislayer, outlinedata, params["minpush"], params["maxpush"], 10, 22, drawSpike)
		AddAllPathsToLayer(spikepaths, thislayer)

		rockpaths = moonrocks(thislayer, outlinedata, params["iterations"], maxgap = 8)
		rockpaths = ConvertPathlistDirection(rockpaths, 1)
		AddAllPathsToLayer(rockpaths, thislayer)
		retractHandles(thislayer)

Gemstones()
