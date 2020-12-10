#MenuTitle: 11. BrokenFax
# -*- coding: utf-8 -*-
__doc__="""
11. BrokenFax
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import *

class BrokenFax(NaNFilter):
	params = {
		"S": {"offset": -20, "stepsize": 50 },
		"M": {"offset": -20, "stepsize": 50 },
		"L": {"offset": -30, "stepsize": 50 },
	}

	def processLayer(self, thislayer, params):
		thislayer.removeOverlap()
		pathlist = ConvertPathsToSkeleton(thislayer.paths, params["stepsize"])
		outlinedata = setGlyphCoords(pathlist)
		ClearPaths(thislayer)

		allpaths = []
		size = params["stepsize"]
		originx = thislayer.bounds.origin.x

		for _,structure in outlinedata:
			newpath = []

			for x1, y1 in structure:
				x2,y2 = int(x1/size) * size, int(y1/size) * size

				if len(newpath)>0:
					if x2!=newpath[-1][0] or y2!=newpath[-1][1]:
						newpath.append([x2,y2])
				else:
					newpath.append([x2,y2])

			allpaths.append(newpath)

		# shift
		# find lowest x in all paths
		lowestx = min([
			min([ node[0] for node in path]) # Min x in path
		for path in allpaths])

		# adjust x in paths by lowestx
		for path in allpaths:
			for node in path:
				node[0] = node[0] + (originx - lowestx)

		angularpaths = [ drawSimplePath(path) for path in allpaths]
		AddAllPathsToLayer(angularpaths, thislayer)
		thislayer.removeOverlap()

BrokenFax()
