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

	for direction, structure in outlinedata:
		nodelen = len(structure)
		spike = GSPath()
		n = 0

		while n < nodelen:
			x1, y1 = structure[n]
			minstep, maxstep = 10, 22
			maxstep = 22

			if direction=="False": maxstep=int(maxstep*0.5)
			step = random.randrange(minstep, maxstep)

			if n+step>=nodelen-1:
				break

			# --- set node pos for main or end
			if n<nodelen-1:
				x2, y2 = structure[n+step]
				n+=step
			else:
				x2, y2 = structure[0]

			a = atan2(y1-y2, x1-x2) + radians(90)

			midx, midy = x1 + ((x2-x1)/2), y1 + ((y2-y1)/2)

			pushdist = random.randrange(minpush, maxpush)

			linex, liney = MakeVector(pushdist, a)

			searchblack = DistanceToNextBlack(thislayer, [x1, y1], [x2, y2], outlinedata, 200)

			if direction=="False":
				linex*=0.7
				liney*=0.7
				pushdist*=0.7

			if searchblack is not None and searchblack < 200:
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
