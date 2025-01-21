# MenuTitle: Beastly
# -*- coding: utf-8 -*-
__doc__ = """
Beastly
"""

from NaNGlyphsEnvironment import GSNode, GSOFFCURVE, GSCURVE
from NaNGFGraphikshared import ClearPaths, AddPaths
from NaNGFAngularizzle import getListOfPoints, ConvertPathsToLineSegments
from NaNFilter import NaNFilter
from NaNCommonFilters import spikes
import random
from math import atan2, radians, cos, sin


def drawHair(bubble, x1, y1, midx, midy, x2, y2, pushdist):
	strayhair = random.randrange(0, 40)
	if strayhair == 20:  # Occasionally make the hair bigger
		a = atan2(y1 - y2, x1 - x2) + radians(90)
		midx += pushdist * cos(a)
		midy += pushdist * sin(a)

	hairdist = pushdist * 0.3

	def makeOffcurve(x, y, direction=1):
		variance = random.randrange(0, 10)
		a = atan2(y - midy, x - midx) + (radians(20 + variance) * direction)
		return hairdist * cos(a), hairdist * sin(a)

	if random.choice([0, 1]) == 0:
		out_offcurves = [makeOffcurve(x1, y1), makeOffcurve(x1, y1, direction=-1)]
		in_offcurves = [makeOffcurve(x2, y2), makeOffcurve(x2, y2, direction=-1)]
	else:
		out_offcurves = [makeOffcurve(x1, y1, direction=-1), makeOffcurve(x1, y1)]
		in_offcurves = [makeOffcurve(x2, y2, direction=-1), makeOffcurve(x2, y2)]

	bubble.nodes.append(
		GSNode([x1 - out_offcurves[0][0], y1 - out_offcurves[0][1]], type=GSOFFCURVE)
	)
	bubble.nodes.append(
		GSNode(
			[midx + out_offcurves[1][0], midy + out_offcurves[1][1]], type=GSOFFCURVE
		)
	)
	bubble.nodes.append(GSNode([midx, midy], type=GSCURVE))

	bubble.nodes.append(
		GSNode([midx + in_offcurves[1][0], midy + in_offcurves[1][1]], type=GSOFFCURVE)
	)
	bubble.nodes.append(
		GSNode([x2 - in_offcurves[0][0], y2 - in_offcurves[0][1]], type=GSOFFCURVE)
	)
	bubble.nodes.append(GSNode([x2, y2], type=GSCURVE))


class Fur(NaNFilter):
	params = {
		"S": {"offset": -5, "minfur": 35, "maxfur": 80},
		"M": {"offset": -10, "minfur": 40, "maxfur": 100},
		"L": {"offset": -20, "minfur": 60, "maxfur": 120},
	}

	def processLayer(self, thislayer, params):
		offsetpaths = self.saveOffsetPaths(
			thislayer, params["offset"], params["offset"], removeOverlap=False
		)
		pathlist = ConvertPathsToLineSegments(offsetpaths, 4)
		outlinedata = getListOfPoints(pathlist)

		ClearPaths(thislayer)

		spikepaths = spikes(outlinedata, params["minfur"], params["maxfur"], 5, 20, drawHair)
		AddPaths(spikepaths, thislayer)


Fur()
