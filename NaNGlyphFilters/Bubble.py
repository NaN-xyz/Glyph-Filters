# MenuTitle: Bubble
# -*- coding: utf-8 -*-
__doc__ = """
Bubble
"""

from NaNGlyphsEnvironment import GSPath, GSNode, GSOFFCURVE, GSCURVE
from NaNGFAngularizzle import ConvertPathsToLineSegments, getListOfPoints
from NaNGFGraphikshared import ClearPaths, DistanceToNextBlack, Direction
from NaNFilter import NaNFilter
from NaNGlyphsEnvironment import glyphsEnvironment as G
import random
from math import atan2, radians, sin, cos


class Bubble(NaNFilter):
	params = {
		"S": {"offset": -5, "minpush": 30, "maxpush": 40, "minstep": 10, "maxstep": 30},
		"M": {"offset": -25, "minpush": 50, "maxpush": 70, "minstep": 10, "maxstep": 40},
		"L": {"offset": -30, "minpush": 60, "maxpush": 80, "minstep": 10, "maxstep": 40}
	}

	def processLayer(self, thislayer, params):
		offset = params["offset"]
		G.remove_overlap(thislayer)
		offsetpaths = self.saveOffsetPaths(
			thislayer, offset, offset, removeOverlap=False
		)
		pathlist = ConvertPathsToLineSegments(offsetpaths, 4)
		outlinedata = getListOfPoints(pathlist)
		ClearPaths(thislayer)

		for direction, structure in outlinedata:
			nodelen = len(structure)
			bubble = GSPath()
			n = 0

			while n < nodelen:
				x1, y1 = structure[n]
				minstep, maxstep = params["minstep"], params["maxstep"]
				minpush, maxpush = params["minpush"], params["maxpush"]

				if direction == Direction.CLOCKWISE:
					minstep = int(minstep * 0.7)
					maxstep = int(maxstep * 0.7)
				step = random.randrange(minstep, maxstep)

				if n + step >= nodelen - 1:
					n = nodelen
					break

				if n < nodelen - 1:
					x2, y2 = structure[n + step]
					n += step
				else:
					x2, y2 = structure[0][0]

				a = atan2(y1 - y2, x1 - x2) + radians(90)
				pushdist = random.randrange(minpush, maxpush)

				# --- chech if there's space for a full bubble
				beamdist = 200
				searchblack = DistanceToNextBlack([x1, y1], [x2, y2], outlinedata, beamdist)
				if searchblack is not None and searchblack < beamdist:
					pushdist *= 0.8

				linex, liney = pushdist * cos(a), pushdist * sin(a)

				if direction == Direction.CLOCKWISE:
					linex *= 0.7
					liney *= 0.7

				# DRAW THE POINTS
				bubble.nodes.append(GSNode([x1 + linex, y1 + liney], type=GSOFFCURVE))
				bubble.nodes.append(GSNode([x2 + linex, y2 + liney], type=GSOFFCURVE))
				bubble.nodes.append(GSNode([x2, y2], type=GSCURVE))

			bubble.closed = True
			thislayer.paths.append(bubble)


Bubble()
