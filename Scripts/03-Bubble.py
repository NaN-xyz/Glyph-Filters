#MenuTitle: 03. Bubble
# -*- coding: utf-8 -*-
__doc__="""
03. Bubble
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import NaNFilter


class Bubble(NaNFilter):
	params = {
		"S": { "offset": -5 },
		"M": { "offset": -10 },
		"L": { "offset": -20 }
	}

	def processLayer(self, thislayer, params):
		offset = params["offset"]
		offsetpaths = self.saveOffsetPaths(thislayer, offset, offset, removeOverlap=False)
		pathlist = doAngularizzle(offsetpaths, 4)
		outlinedata = setGlyphCoords(pathlist)
		ClearPaths(thislayer)
		minpush = 60
		maxpush = 80
		for direction, structure in outlinedata:
			nodelen = len(structure)
			bubble = GSPath()
			n = 0

			while n < nodelen:
				x1, y1 = structure[n]
				minstep, maxstep = 10, 40

				if direction=="False": maxstep=int(maxstep*0.5)
				step = random.randrange(minstep, maxstep)

				if n+step>=nodelen-1:
					n = nodelen
					break

				# --- set node pos for main or end

				if n<nodelen-1:
					x2,y2 = structure[n+step]
					n+=step
				else:
					x2,y2 = structure[0][0]

				a = atan2(y1-y2, x1-x2) + radians(90)
				pushdist = random.randrange(minpush, maxpush) 
				linex, liney = pushdist * cos(a), pushdist * sin(a)

				if direction=="False":
					linex*=0.5
					liney*=0.5

				# DRAW THE POINTS
				bubble.nodes.append(GSNode([x1+linex, y1+liney], type = GSOFFCURVE))
				bubble.nodes.append(GSNode([x2+linex, y2+liney], type = GSOFFCURVE))
				bubble.nodes.append(GSNode([x2, y2], type = GSCURVE))

			bubble.closed = True
			thislayer.paths.append(bubble)


Bubble()
