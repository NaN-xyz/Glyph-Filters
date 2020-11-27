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
from Foundation import NSMakePoint

def withinGlyphBlack_faster(layer, x, y):
	if not layer.bounds:
		return
	definitelyOutside = NSMakePoint(layer.bounds.origin.x-1,y)
	pt = NSMakePoint(x,y)
	intersections = layer.calculateIntersectionsStartPoint_endPoint_decompose_(definitelyOutside, pt, True)
	return (len(intersections) % 2) == 1

def operateOnBlackAtInterval(layer, func, step_x, step_y=None):
	if step_y is None:
		step_y = step_x
	b = AllPathBounds(layer)
	ox, oy, w, h = int(b[0])+1, b[1]+1, b[2], b[3]
	results = []
	for y in range(oy, oy+h, step_y):
		for x in range(ox, ox+w, step_x):
			if not withinGlyphBlack_faster(layer, x, y):
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
		operateOnBlackAtInterval(thislayer, self.drawStorm, self.gridsize)
		ClearPaths(thislayer)

Storm()
