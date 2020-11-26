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

def operateOnBlackAtInterval(layer, outlinedata, func, step_x, step_y=None):
	if step_y is None:
		step_y = step_x
	b = AllPathBounds(layer)
	ox, oy, w, h = int(b[0])+1, b[1]+1, b[2], b[3]
	results = []
	for y in range(oy, oy+h, step_y):
		for x in range(ox, ox+w, step_x):
			if not withinGlyphBlack(x, y, outlinedata):
				continue
			result = func(x,y,layer)
			if result is not None:
				results.extend(result)

	return results

class Storm(NaNFilter):
	gridsize, minsize, maxsize = 25, 20, 60

	def setup(self):
		self.stormcomponent = CreateShapeComponent(self.font, self.maxsize, self.maxsize, "circle", "StormShape")

	def drawStorm(self, x,y,layer):
		freq = 0.005
		noiz = snoise2(x*freq, y*freq, 3)
		size = noiseMap( noiz, self.minsize, self.maxsize )
		if size <= 4:
			return
		stormcomp = GSComponent(self.stormcomponent)
		scale = (float(1)/self.maxsize)*size
		stormcomp.transform = ((scale, 0.0, 0.0, scale, x, y))
		layer.components.append(stormcomp)

	def processLayer(self, thislayer, params):
		pathlist = doAngularizzle(thislayer.paths, 4)
		outlinedata = setGlyphCoords(pathlist)
		operateOnBlackAtInterval(thislayer, outlinedata, self.drawStorm, self.gridsize)
		ClearPaths(thislayer)

Storm()
