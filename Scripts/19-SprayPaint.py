#MenuTitle: 19. Spray Paint
# -*- coding: utf-8 -*-
__doc__="""
19. Spray Paint
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFNoise import *
from noise import *
from NaNFilter import NaNFilter


class Spray(NaNFilter):
	params = {"S": { "offset": -5}, "M": { "offset": -10}, "L": { "offset": -20} }

	def processLayer(self, thislayer, params):
		offsetpaths = self.saveOffsetPaths(thislayer, params["offset"], params["offset"], removeOverlap=False)
		pathlist = doAngularizzle(offsetpaths, 4)

		ClearPaths(thislayer)

		for path in pathlist:
			# only round shape if over certain size (for small forms)
			if isPathSizeBelowThreshold(path,120,120):
				structure = path
			else:
				structure = convertToFitpath(RoundPath(path,"nodes"), True)
			
			outlinedata = setGlyphCoords(doAngularizzle([structure], 7))

			if not outlinedata:
				continue

			structure = outlinedata[0][1]

			nodelen = len(structure)

			n = 0
			newpath = []

			noisescale = 0.01
			segwaylen = 40
			minshift, maxshift = 30, 90

			seed = random.randrange(0,100000)
			start_pushdist = 0
			last_pushdist = 0

			while n < nodelen:
				x_prev, y_prev = structure[n-1]
				x_curr, y_curr = structure[n]
				x_next, y_next = structure[(n+1) % nodelen]

				a1 = atan2(y_prev-y_next, x_prev-x_next)
				a2 = a1+radians(90)

				if n < nodelen-segwaylen:
					pushdist = pnoise1( (n+seed)*noisescale, 3) 
					pushdist = noiseMap( pushdist, minshift, maxshift )
					last_pushdist = pushdist
					if n==0:
						start_pushdist = pushdist

				else:
					pushdist = last_pushdist + ( ( start_pushdist-last_pushdist ) / segwaylen ) * (segwaylen-(nodelen-n)) 

				linex1, liney1 = MakeVector(pushdist, a2)
				linex2, liney2 = MakeVector(pushdist, a1)

				newpath.extend( [
								[x_curr-linex2, y_curr-liney2], 
								[x_curr+linex2, y_curr+liney2],
								[x_curr+linex1, y_curr+liney1]]
								)
				n+=1

			thislayer.paths.append(drawSimplePath(newpath))

Spray()


