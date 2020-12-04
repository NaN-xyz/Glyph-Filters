#MenuTitle: 27. Gemstones
# -*- coding: utf-8 -*-
__doc__="""
27. Gemstones
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import NaNFilter
from NaNCommonFilters import moonrocks

# RETURN SPIKEY PATHS

def Spikes(thislayer, outlinedata, minpush, maxpush):

	spikepaths = []

	for path in outlinedata:

		direction = path[0]
		structure = path[1]
		nodelen = len(structure)
		spike = GSPath()
		n = 0

		while n < nodelen:

			x1 = structure[n][0]
			y1 = structure[n][1]
			minstep = 10
			maxstep = 22

			if direction=="False": maxstep=int(maxstep*0.5)
			step = random.randrange(minstep, maxstep)

			if n+step>=nodelen-1:
				n = nodelen
				break

			# --- set node pos for main or end
			if n<nodelen-1:
				x2 = structure[n+step][0]
				y2 = structure[n+step][1]
				n+=step
			else:
				x2 = structure[0][0]
				y2 = structure[0][1]

			a = atan2(y1-y2, x1-x2)
			a += radians(90)

			midx = x1 + ((x2-x1)/2)
			midy = y1 + ((y2-y1)/2)

			pushdist = random.randrange(minpush, maxpush)

			linex = pushdist * cos(a)
			liney = pushdist * sin(a)

			searchblack = DistanceToNextBlack(thislayer, [x1, y1], [x2, y2], outlinedata, 200)

			if direction=="False":
				linex*=0.7
				liney*=0.7
				pushdist*=0.7

			if searchblack is not None:
				if searchblack < 200:
					linex*=0.7
					liney*=0.7
					pushdist*=0.7

			midx += linex
			midy += liney

			# draw spikes
			spike.nodes.append(GSNode([midx, midy], type = GSLINE))
			spike.nodes.append(GSNode([x2, y2], type = GSLINE))

		spike.closed = True
		spikepaths.append(spike)

	return spikepaths


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

		spikepaths = Spikes(thislayer, outlinedata, params["minpush"], params["maxpush"])
		AddAllPathsToLayer(spikepaths, thislayer)

		rockpaths = moonrocks(thislayer, outlinedata, params["iterations"], maxgap = 8)
		rockpaths = ConvertPathlistDirection(rockpaths, 1)
		AddAllPathsToLayer(rockpaths, thislayer)

Gemstones()
