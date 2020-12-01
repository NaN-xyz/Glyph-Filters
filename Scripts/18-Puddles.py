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

	p1x, p1y = p1
	p2x, p2y = p2

	midx, midy = Midpoint(p1, p2)

	a1 = atan2(p1y-p2y, p1x-p2x)
	a2 = a1 - radians(90)
	a3 = a2 - radians(20)
	a4 = a2 + radians(20)

	pushx1, pushy1 = MakeVector(curvedist + (thickness/2), a2)
	pushx2, pushy2 = MakeVector(curvedist - (thickness/2), a2)

	hlen = dist*0.15
	mlen = (dist*0.21)

	handlex1, handley1 = MakeVector(mlen, a1)
	handlex2, handley2 = MakeVector(mlen, a3)
	handlex2b, handley2b = MakeVector(mlen, a3 - radians(20))
	handlex3, handley3 = MakeVector(mlen, a4)
	handlex3b, handley3b = MakeVector(mlen, a4 + radians(20))
	handlex4, handley4 = MakeVector(mlen*0.8, a1)

	# draw path

	nail = GSPath()
	nail.nodes = [
		GSNode( [p1x, p1y] , type=GSLINE),
		GSNode( [p1x+handlex2, p1y+handley2] , type=GSOFFCURVE),
		GSNode( [midx+pushx1+handlex1, midy+pushy1+handley1] , type=GSOFFCURVE),
		GSNode( [midx+pushx1, midy+pushy1] , type=GSCURVE),
		GSNode( [midx+pushx1-handlex1, midy+pushy1-handley1] , type=GSOFFCURVE),
		GSNode( [p2x+handlex3, p2y+handley3] , type=GSOFFCURVE),
		GSNode( [p2x, p2y] , type=GSCURVE),
		GSNode( [p2x+handlex3b, p2y+handley3b] , type=GSOFFCURVE),
		GSNode( [midx+pushx2-handlex4, midy+pushy2-handley4] , type=GSOFFCURVE),
		GSNode( [midx+pushx2, midy+pushy2] , type=GSCURVE),
		GSNode( [midx+pushx2+handlex4, midy+pushy2+handley4] , type=GSOFFCURVE),
		GSNode( [p1x+handlex2b, p1y+handley2b] , type=GSOFFCURVE),
		GSNode( [p1x, p1y] , type=GSCURVE),
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

