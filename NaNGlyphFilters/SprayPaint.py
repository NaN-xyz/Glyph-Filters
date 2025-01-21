# MenuTitle: Spray Paint
# -*- coding: utf-8 -*-
__doc__ = """
Spray Paint
"""

import random
from NaNFilter import NaNFilter
from NaNGFAngularizzle import ConvertPathsToLineSegments, getListOfPoints
from NaNGFGraphikshared import ClearPaths, AddPaths, MakeVector, RoundPath, drawSimplePath, isSizeBelowThreshold, convertToFitpath
from NaNGFNoise import noiseMap
from math import atan2, radians


class Spray(NaNFilter):
	params = {
		"S": {"offset": -5},
		"M": {"offset": -10},
		"L": {"offset": -20}
	}

	noisescale = 0.01
	segwaylen = 5
	minshift, maxshift = 30, 90

	def processLayer(self, thislayer, params):
		offsetpaths = self.saveOffsetPaths(thislayer, params["offset"], params["offset"], removeOverlap=False)
		pathlist = ConvertPathsToLineSegments(offsetpaths, 4)
		ClearPaths(thislayer)
		new_paths = []
		for path in pathlist:
			# only round shape if over certain size (for small forms)
			if isSizeBelowThreshold(path, 120, 120):
				structure = path
			else:
				structure = convertToFitpath(RoundPath(path, "nodes"), True)
			outlinedata = getListOfPoints(ConvertPathsToLineSegments([structure], 7))

			if not outlinedata:
				continue
			new_paths.extend([self.makePathSpiky(outlinedata[0][1])])

		AddPaths(new_paths, thislayer)

	def makePathSpiky(self, structure):
		nodelen = len(structure)
		newpath = []
		# seed = random.randrange(0, 100000)
		start_pushdist = 0
		last_pushdist = 0

		for n in range(0, nodelen):
			x_prev, y_prev = structure[n - 1]
			x_curr, y_curr = structure[n]
			x_next, y_next = structure[(n + 1) % nodelen]

			angle = atan2(y_prev - y_next, x_prev - x_next)

			if n < nodelen - self.segwaylen:
				pushdist = noiseMap(random.random(), self.minshift, self.maxshift)
				last_pushdist = pushdist
				if n == 0:
					start_pushdist = pushdist

			else:
				pushdist = last_pushdist + ((start_pushdist - last_pushdist) / self.segwaylen) * (self.segwaylen - (nodelen - n))

			spikewidth = 5

			linex1, liney1 = MakeVector(pushdist, angle + radians(90))
			linex2, liney2 = MakeVector(spikewidth, angle)

			newpath.extend([
				[x_curr - linex2, y_curr - liney2],
				[x_curr + linex2, y_curr + liney2],
				[x_curr + linex1, y_curr + liney1]]
			)

		return drawSimplePath(newpath)


Spray()
