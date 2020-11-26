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

				variance = random.randrange(0,10)

				# get push distance for xy1 to midxy
				a = atan2(y1-midy, x1-midx)
				a += radians(20+variance)
				midlinex1a = hairdist * cos(a)
				midliney1a = hairdist * sin(a)

				variance = random.randrange(0,10)

				a = atan2(y1-midy, x1-midx)
				a -= radians(20+variance)
				midlinex1b = hairdist * cos(a)
				midliney1b = hairdist * sin(a)

				#

				variance = random.randrange(0,10)

				a = atan2(y2-midy, x2-midx)
				a += radians(20+variance)
				midlinex2a = hairdist * cos(a)
				midliney2a = hairdist * sin(a)

				variance = random.randrange(0,10)

				a = atan2(y2-midy, x2-midx)
				a -= radians(20+variance)
				midlinex2b = hairdist * cos(a)
				midliney2b = hairdist * sin(a)


				# draw the fur

				r = random.choice([0,1])

				if r == 0:

					bubble.nodes.append(GSNode([x1-midlinex1a, y1-midliney1a], type = GSOFFCURVE))
					bubble.nodes.append(GSNode([midx+midlinex1b, midy+midliney1b], type = GSOFFCURVE))
					bubble.nodes.append(GSNode([midx, midy], type = GSCURVE))

					bubble.nodes.append(GSNode([midx+midlinex2b, midy+midliney2b], type = GSOFFCURVE))
					bubble.nodes.append(GSNode([x2-midlinex2a, y2-midliney2a], type = GSOFFCURVE))
					bubble.nodes.append(GSNode([x2, y2], type = GSCURVE))

				else:

					bubble.nodes.append(GSNode([x1-midlinex1b, y1-midliney1b], type = GSOFFCURVE))
					bubble.nodes.append(GSNode([midx+midlinex1a, midy+midliney1a], type = GSOFFCURVE))
					bubble.nodes.append(GSNode([midx, midy], type = GSCURVE))

					bubble.nodes.append(GSNode([midx+midlinex2a, midy+midliney2a], type = GSOFFCURVE))
					bubble.nodes.append(GSNode([x2-midlinex2b, y2-midliney2b], type = GSOFFCURVE))
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
