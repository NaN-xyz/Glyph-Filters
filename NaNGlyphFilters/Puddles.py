# MenuTitle: Puddles
# -*- coding: utf-8 -*-
__doc__ = """
Puddles
"""

from NaNGFGraphikshared import ChangeNodeStart, ClearPaths, MakeVector, Midpoint, NegateVector, SumVectors, distance
from NaNGlyphsEnvironment import GSLINE, GSOFFCURVE, GSCURVE, GSPath, GSNode
from NaNFilter import NaNFilter
from math import atan2, radians
from NaNGFAngularizzle import ConvertPathsToLineSegments, getListOfPoints
from NaNGlyphsEnvironment import glyphsEnvironment as G
import copy
import random


class Puddles(NaNFilter):

	params = {
		"S": {"offset1": -15, "offset2": 20, "offset3": 60},
		"M": {"offset1": -15, "offset2": 20, "offset3": 60},
		"L": {"offset1": -15, "offset2": 20, "offset3": 60}
	}

	def processLayer(self, thislayer, params):

		offset1, offset2, offset3 = params["offset1"], params["offset2"], params["offset3"]

		offsetpaths = self.saveOffsetPaths(thislayer, offset1, offset1, removeOverlap=False)
		pathlist = ConvertPathsToLineSegments(offsetpaths, 4)
		outlinedata = getListOfPoints(pathlist)

		offsetpaths = self.saveOffsetPaths(thislayer, offset2, offset2, removeOverlap=True)
		pathlist = ConvertPathsToLineSegments(offsetpaths, 4)
		# outlinedata3 = getListOfPoints(pathlist)

		offsetpaths = self.saveOffsetPaths(thislayer, offset3, offset3, removeOverlap=True)
		pathlist = ConvertPathsToLineSegments(offsetpaths, 4)
		outlinedata4 = getListOfPoints(pathlist)

		ClearPaths(thislayer)

		Toenail(thislayer, outlinedata, 30, 50, gap=4, thickness=25)
		# Toenail(thislayer, outlinedata3, 40, 60, gap=100, thickness=20)
		Toenail(thislayer, outlinedata4, 50, 70, gap=100, thickness=10)
		G.clean_up_paths(thislayer)
		self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)


def drawToenail(p1, p2, thickness):
	dist = distance(p1, p2)

	mid = Midpoint(p1, p2)

	a1 = atan2(p1[1] - p2[1], p1[0] - p2[0])
	a2 = a1 - radians(90)
	a3 = a2 - radians(20)
	a4 = a2 + radians(20)

	curvedist = dist * 0.3
	push1 = MakeVector(curvedist + (thickness / 2), a2)
	push2 = MakeVector(curvedist - (thickness / 2), a2)

	mlen = dist * 0.21
	handle1 = MakeVector(mlen, a1)
	handle2 = MakeVector(mlen, a3)
	handle2b = MakeVector(mlen, a3 - radians(20))
	handle3 = MakeVector(mlen, a4)
	handle3b = MakeVector(mlen, a4 + radians(20))
	handle4 = MakeVector(mlen * 0.8, a1)

	# draw path

	nail = GSPath()
	nail.nodes = [
		GSNode(p1, type=GSLINE),
		GSNode(SumVectors(p1, handle2), type=GSOFFCURVE),
		GSNode(SumVectors(mid, push1, handle1), type=GSOFFCURVE),
		GSNode(SumVectors(mid, push1), type=GSCURVE),
		GSNode(SumVectors(mid, push1, NegateVector(handle1)), type=GSOFFCURVE),
		GSNode(SumVectors(p2, handle3), type=GSOFFCURVE),
		GSNode(p2, type=GSCURVE),
		GSNode(SumVectors(p2, handle3b), type=GSOFFCURVE),
		GSNode(SumVectors(mid, push2, NegateVector(handle4)), type=GSOFFCURVE),
		GSNode(SumVectors(mid, push2), type=GSCURVE),
		GSNode(SumVectors(mid, push2, handle4), type=GSOFFCURVE),
		GSNode(SumVectors(p1, handle2b), type=GSOFFCURVE),
		GSNode(p1, type=GSCURVE),
	]
	nail.closed = True

	return nail


def Toenail(thislayer, outlinedata, min_nail, max_nail, gap, thickness):

	for _, structure in outlinedata:
		if not structure:
			continue

		structure = ChangeNodeStart(copy.copy(structure))
		nodelen = len(structure)
		n = 0

		while n < nodelen:
			pt1 = structure[n]
			step = random.randrange(min_nail, max_nail)

			if n + step >= nodelen - 1:
				pt2 = structure[0]
				n = nodelen
			else:
				if n < nodelen - 1:
					pt2 = structure[n + step]
					n += step + gap  # <------------------------------------------- !!!
				else:
					pt2 = structure[0]

			# variance = random.randrange(0, 10)
			toenail = drawToenail(pt2, pt1, thickness)

			minwh = 40
			bounds = toenail.bounds
			if bounds.size.width > minwh and bounds.size.height > minwh:
				thislayer.paths.append(toenail)


Puddles()
