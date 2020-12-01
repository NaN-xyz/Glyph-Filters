#MenuTitle: 18. Puddles
# -*- coding: utf-8 -*-
__doc__="""
18. Puddles
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import NaNFilter


def drawToenail(p1, p2, thickness):
	dist =  distance(p1,p2)
	curvedist = dist * 0.3

	mid = Midpoint(p1, p2)

	a1 = atan2(p1[1]-p2[1], p1[0]-p2[0])
	a2 = a1 - radians(90)
	a3 = a2 - radians(20)
	a4 = a2 + radians(20)

	push1 = MakeVector(curvedist + (thickness/2), a2)
	push2 = MakeVector(curvedist - (thickness/2), a2)

	hlen = dist*0.15
	mlen = (dist*0.21)

	handle1  = MakeVector(mlen, a1)
	handle2  = MakeVector(mlen, a3)
	handle2b = MakeVector(mlen, a3 - radians(20))
	handle3	 = MakeVector(mlen, a4)
	handle3b = MakeVector(mlen, a4 + radians(20))
	handle4  = MakeVector(mlen*0.8, a1)

	# draw path

	nail = GSPath()
	nail.nodes = [
		GSNode( p1 , type=GSLINE),
		GSNode( [p1[0]+handle2[0], p1[1]+handle2[1]] , type=GSOFFCURVE),
		GSNode( [mid[0]+push1[0]+handle1[0], mid[1]+push1[1]+handle1[1]] , type=GSOFFCURVE),
		GSNode( [mid[0]+push1[0], mid[1]+push1[1]] , type=GSCURVE),
		GSNode( [mid[0]+push1[0]-handle1[0], mid[1]+push1[1]-handle1[1]] , type=GSOFFCURVE),
		GSNode( [p2[0]+handle3[0], p2[1]+handle3[1]] , type=GSOFFCURVE),
		GSNode( p2, type=GSCURVE),
		GSNode( [p2[0]+handle3b[0], p2[1]+handle3b[1]] , type=GSOFFCURVE),
		GSNode( [mid[0]+push2[0]-handle4[0], mid[1]+push2[1]-handle4[1]] , type=GSOFFCURVE),
		GSNode( [mid[0]+push2[0], mid[1]+push2[1]] , type=GSCURVE),
		GSNode( [mid[0]+push2[0]+handle4[0], mid[1]+push2[1]+handle4[1]] , type=GSOFFCURVE),
		GSNode( [p1[0]+handle2b[0], p1[1]+handle2b[1]] , type=GSOFFCURVE),
		GSNode( p1, type=GSCURVE),
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

			if n+step >= nodelen-1:
				pt2 = structure[0]
				n = nodelen
			else:
				if n<nodelen-1:
					pt2 = structure[n+step]
					n += step + gap               # <------------------------------------------- !!!
				else:
					pt2 = structure[0]

			variance = random.randrange(0,10)
			toenail = drawToenail(pt2, pt1, thickness)
			thislayer.paths.append(toenail)




class Puddles(NaNFilter):
	def processLayer(self, thislayer, params):
		print(thislayer)
		pathlist = doAngularizzle(thislayer.paths, 4)
		outlinedata2 = setGlyphCoords(pathlist)

		offsetpaths = self.saveOffsetPaths(thislayer, -10, -10, removeOverlap=False)
		pathlist = doAngularizzle(offsetpaths, 4)
		outlinedata = setGlyphCoords(pathlist)

		offsetpaths = self.saveOffsetPaths(thislayer, 20, 20, removeOverlap=True)
		pathlist = doAngularizzle(offsetpaths, 4)
		outlinedata3 = setGlyphCoords(pathlist)

		offsetpaths = self.saveOffsetPaths(thislayer, 60, 60, removeOverlap=True)
		pathlist = doAngularizzle(offsetpaths, 4)
		outlinedata4 = setGlyphCoords(pathlist)

		ClearPaths(thislayer) 


		Toenail(thislayer, outlinedata, 30, 50, gap=4, thickness=25)
		Toenail(thislayer, outlinedata3, 40, 60, gap=100, thickness=20)
		Toenail(thislayer, outlinedata4, 50, 70, gap=100, thickness=10)
		thislayer.cleanUpPaths()

Puddles()

