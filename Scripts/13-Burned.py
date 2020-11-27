#MenuTitle: 13 Burned
# -*- coding: utf-8 -*-
__doc__="""
13. Burned
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFSpacePartition import *
from NaNGFNoise import *
from NaNFilter import NaNFilter


def ApplyBurn(thislayer, groups):

	for g in groups:
		if len(g)>2:
			thislayer.paths.extend(g)

def returnRoundedPaths(paths):

	roundedpathlist = []
	for p in paths:
		roundedpath = RoundPath(p, "nodes")
		try: 
			roundedpath = convertToFitpath(roundedpath, True)
			roundedpathlist.append(roundedpath)
		except:
			pass
	return roundedpathlist


class Burn(NaNFilter):
	params = {
		"S": { "offset": 0, "gridsize": 40 },
		"M": { "offset": 4, "gridsize": 45 },
		"L": { "offset": 4, "gridsize": 50 },
	}

	def processLayer(self, thislayer, params):
		pathlist = doAngularizzle(thislayer.paths, 20)
		outlinedata = setGlyphCoords(pathlist)
		bounds = AllPathBounds(thislayer)
		
		offsetpaths = self.saveOffsetPaths(thislayer, params["offset"], params["offset"], removeOverlap=True)
		pathlist2 = doAngularizzle(offsetpaths, 4)
		outlinedata2 = setGlyphCoords(pathlist2)
		bounds2 = AllPathBoundsFromPathList(pathlist2)

		ClearPaths(thislayer)

		newtris = self.SortCollageSpace(thislayer, outlinedata, outlinedata2, params["gridsize"], bounds, action="overlap", randomize=True)
		maxchain = random.randrange(200,400)
		groups = BreakUpSpace(thislayer, outlinedata, newtris, params["gridsize"], maxchain)
		ApplyBurn(thislayer, groups)
		#AddAllPathsToLayer(edgetris, thislayer)

		thislayer.removeOverlap()
		roundedpathlist = returnRoundedPaths(thislayer.paths)
		ClearPaths(thislayer)
		AddAllPathsToLayer(roundedpathlist, thislayer)

Burn()
