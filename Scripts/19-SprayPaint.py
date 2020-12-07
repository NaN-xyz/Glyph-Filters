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

	noisescale = 0.01
	segwaylen = 40
	minshift, maxshift = 30, 90

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

			outlinedata = getGlyphCoords(doAngularizzle([structure], 7))

			if not outlinedata:
				continue

			thislayer.paths.append(self.makePathSpiky(outlinedata[0][1]))

	def makePathSpiky(self, structure):
			nodelen = len(structure)
			newpath = []
			seed = random.randrange(0,100000)
			start_pushdist = 0
			last_pushdist = 0

			for n in range(0,nodelen):
				x_prev, y_prev = structure[n-1]
				x_curr, y_curr = structure[n]
				x_next, y_next = structure[(n+1) % nodelen]

				angle = atan2(y_prev-y_next, x_prev-x_next)

				if n < nodelen-self.segwaylen:
					pushdist = pnoise1( (n+seed)*self.noisescale, 3)
					pushdist = noiseMap( pushdist, self.minshift, self.maxshift )
					last_pushdist = pushdist
					if n==0:
						start_pushdist = pushdist

				else:
					pushdist = last_pushdist + ( ( start_pushdist-last_pushdist ) / self.segwaylen ) * (self.segwaylen-(nodelen-n)) 

				linex1, liney1 = MakeVector(pushdist, angle+radians(90))
				linex2, liney2 = MakeVector(pushdist, angle)

				newpath.extend( [
								[x_curr-linex2, y_curr-liney2],
								[x_curr+linex2, y_curr+liney2],
								[x_curr+linex1, y_curr+liney1]]
								)

			return drawSimplePath(newpath)

Spray()


