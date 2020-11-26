#MenuTitle: 08. Beastly
# -*- coding: utf-8 -*-
__doc__="""
08. Beastly
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import NaNFilter

class Fur(NaNFilter):
	params = {
		"S": { "offset": -5, "minfur": 20, "maxfur": 50 },
		"M": { "offset": -10, "minfur": 40, "maxfur": 100 },
		"L": { "offset": -20, "minfur": 60, "maxfur": 120 }
	}

	def doFur(self, thislayer, outlinedata, minpush, maxpush):

		for direction, structure in outlinedata:
			nodelen = len(structure)
			bubble = GSPath()
			n = 0

			while n < nodelen:
				x1,y1 = structure[n]

				minstep, maxstep = 5, 20

				if direction=="False": maxstep=int(maxstep*0.5)
				step = random.randrange(minstep, maxstep)
				pushdist = random.randrange(minpush, maxpush)

				# every now and again allow a wild hair
				strayhair = random.randrange(0,60)

				if strayhair == 20 and direction!="False":
					pushdist = pushdist * 1.3
					step = minstep

				if n+step>=nodelen-1:
					n = nodelen
					break

				if n<nodelen-1:
					x2,y2 = structure[n+step]
					y2,y2 = structure[n+step]
					n+=step
				else:
					x2,y2 = structure[0]
					y2,y2 = structure[0]

				# if distance([x1, y1], [x2, y2]) < 1:
				# 	continue

				a = atan2(y1-y2, x1-x2) + radians(90)

				midx, midy = x1 + ((x2-x1)/2), y1 + ((y2-y1)/2)

				pushdist = random.randrange(minpush, maxpush)

				strayhair = random.randrange(0,40)
				if strayhair == 20:
					pushdist = pushdist * 2

				linex = pushdist * cos(a)
				liney = pushdist * sin(a)

				searchblack = DistanceToNextBlack(thislayer, [x1, y1], [x2, y2], outlinedata, searchlimit=200)

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


				hairdist = pushdist * 0.3


				def makeOffcurve(x, y, direction=1):
					variance = random.randrange(0,10)
					a = atan2(y-midy, x-midx) + (radians(20+variance) * direction)
					return hairdist * cos(a), hairdist * sin(a)

				midline1a = makeOffcurve(x1, y1)
				midline1b = makeOffcurve(x1, y1, direction = -1)
				midline2a = makeOffcurve(x2, y2)
				midline2b = makeOffcurve(x2, y2, direction = -1)

				# draw the fur

				if random.choice([0,1]) == 0:
					# 1a,1b,2b,2a
					bubble.nodes.append(GSNode([x1-midline1a[0], y1-midline1a[1]], type = GSOFFCURVE))
					bubble.nodes.append(GSNode([midx+midline1b[0], midy+midline1b[1]], type = GSOFFCURVE))
					bubble.nodes.append(GSNode([midx, midy], type = GSCURVE))

					bubble.nodes.append(GSNode([midx+midline2b[0], midy+midline2b[1]], type = GSOFFCURVE))
					bubble.nodes.append(GSNode([x2-midline2a[0], y2-midline2a[1]], type = GSOFFCURVE))
					bubble.nodes.append(GSNode([x2, y2], type = GSCURVE))

				else:
					# 1b,1a,2a,2b
					bubble.nodes.append(GSNode([x1-midline1b[0], y1-midline1b[1]], type = GSOFFCURVE))
					bubble.nodes.append(GSNode([midx+midline1a[0], midy+midline1a[1]], type = GSOFFCURVE))
					bubble.nodes.append(GSNode([midx, midy], type = GSCURVE))

					bubble.nodes.append(GSNode([midx+midline2a[0], midy+midline2a[1]], type = GSOFFCURVE))
					bubble.nodes.append(GSNode([x2-midline2b[0], y2-midline2b[1]], type = GSOFFCURVE))
					bubble.nodes.append(GSNode([x2, y2], type = GSCURVE))

			bubble.closed = True

			thislayer.paths.append(bubble)

			# simple = drawSimplePath(structure)
			# thislayer.paths.append(simple)

	def processLayer(self, thislayer, params):
		offsetpaths = self.saveOffsetPaths(thislayer, params["offset"], params["offset"], removeOverlap=False)
		pathlist = doAngularizzle(offsetpaths, 4)
		outlinedata = setGlyphCoords(pathlist)

		ClearPaths(thislayer)

		self.doFur(thislayer, outlinedata, params["minfur"], params["maxfur"])

Fur()
