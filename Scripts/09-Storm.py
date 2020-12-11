#MenuTitle: 09. Storm
# -*- coding: utf-8 -*-
__doc__="""
09. Storm
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFNoise import *
from NaNFilter import NaNFilter

class Storm(NaNFilter):
	gridsize = 30
	minsize, maxsize = 30, 80

	def setup(self):
		self.stormcomponent = CreateShapeComponent(self.font, self.maxsize, self.maxsize, "rectangle", "StormShape")

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
