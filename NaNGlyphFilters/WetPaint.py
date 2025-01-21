# MenuTitle: Wet Paint
# -*- coding: utf-8 -*-
__doc__ = """
Wet Paint
"""

from NaNFilter import NaNFilter
from NaNGFAngularizzle import ConvertPathsToLineSegments, Direction, getListOfPoints
from NaNGFGraphikshared import DistanceToNextBlack, convertToFitpath
from NaNGFNoise import noiseMap
from NaNGlyphsEnvironment import glyphsEnvironment as G
from math import atan2, degrees
import math
import random


class Drip(NaNFilter):
	params = {
		"S": {"maxdrip": 150, "iterations": 1},
		"M": {"maxdrip": 350, "iterations": 2},
		"L": {"maxdrip": 400, "iterations": 2}
	}

	def getDrippableSegments(self, outlinedata):
		# find drippable segments within path and store indices
		indices = []
		degvariance = 40

		for direction, nodes in outlinedata:
			index = []
			index_start, index_end = -999, -999
			# collect all possible drippable segments within certain angle

			for n in range(0, len(nodes) - 1):
				x1, y1 = nodes[n]
				x2, y2 = nodes[n + 1]
				a = atan2(y1 - y2, x1 - x2)
				deg = degrees(a)

				if abs(deg) > (180 - degvariance) and abs(deg) < (180 + degvariance):
					if index_start == -999:
						index_start = n
					else:
						index_end = n
				else:
					if index_start != -999:
						index.append([index_start, index_end])
					index_start = -999

			indices.append(index)

		return indices

	def doDrip(self, thislayer, indices, outlinedata, maxdrip):
		# run through each drippable segment and do something
		for p in range(0, len(outlinedata)):
			direction, structure = outlinedata[p]
			# nodelen = len(structure)
			segs = indices[p]

			for seg in segs:
				index_start, index_end = seg

				# seedx = random.randrange(0, 100000)
				# noisescale = 0.1

				steps = float(index_end - index_start)
				steppos = 0

				for n in range(index_start, index_end):
					angle = 180 / steps * steppos
					t = math.sin(math.radians(angle))
					adjust = 1

					x, y = structure[n]

					if n < index_end:
						x2, y2 = structure[n + 1]

						searchblack = DistanceToNextBlack((x, y), (x2, y2), outlinedata, searchlimit=200)
						# print searchblack

						if searchblack is not None and searchblack < 200:
							adjust = 0.2

					# insert distance to next black checker here

					size = noiseMap(random.random(), 0, maxdrip)
					if direction == Direction.CLOCKWISE:
						size *= 0.2
					size = t * abs(size) * adjust

					structure[n][1] = y - size

					steppos += 1

	def processLayer(self, thislayer, params):
		for n in range(0, params["iterations"]):
			pathlist = ConvertPathsToLineSegments(thislayer.paths, 10)  # small seg size = slower
			outlinedata = getListOfPoints(pathlist)
			indices = self.getDrippableSegments(outlinedata)

			# Modifies outlinedata
			self.doDrip(thislayer, indices, outlinedata, params["maxdrip"])

			# draw updated outline
			for path in outlinedata:
				p = convertToFitpath(path[1], True)
				thislayer.paths.append(p)
		G.remove_overlap(thislayer)
		self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=True)


Drip()
