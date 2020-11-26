#MenuTitle: 09. Storm
# -*- coding: utf-8 -*-
__doc__="""
09. Storm
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFNoise import *
from NaNFilter import NaNFilter

def drawStorm(thislayer, outlinedata, step, minsize, maxsize, stormcomponent):

	b = AllPathBounds(thislayer)
	ox, oy, w, h = int(b[0])+1, b[1]+1, b[2], b[3]
	stormpaths = []

	freq = 0.005
	noiseseed = random.randrange(0,100000)
	n=0

	for y in range(oy, oy+h, step):
		for x in range(ox, ox+h, step):
			if withinGlyphBlack(x, y, outlinedata):
				noiz = snoise2(x*freq, y*freq, 3)
				size = noiseMap( noiz, minsize, maxsize )
				if size>4:
					stormcomp = GSComponent(stormcomponent)
					scale = (float(1)/maxsize)*size
					stormcomp.transform = ((scale, 0.0, 0.0, scale, x, y))
					thislayer.components.append(stormcomp)
				n+=1

	return stormpaths


class Storm(NaNFilter):
	gridsize, minsize, maxsize = 25, 20, 60

	def setup(self):
		self.stormcomponent = CreateShapeComponent(self.font, self.maxsize, self.maxsize, "circle", "StormShape")

	def processLayer(self, thislayer, params):
		pathlist = doAngularizzle(thislayer.paths, 4)
		outlinedata = setGlyphCoords(pathlist)
		stormpaths = drawStorm(thislayer, outlinedata, self.gridsize, self.minsize, self.maxsize, self.stormcomponent)
		ClearPaths(thislayer)
		AddAllPathsToLayer(stormpaths, thislayer)

Storm()
