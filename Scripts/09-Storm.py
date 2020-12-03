#MenuTitle: 09. Storm
# -*- coding: utf-8 -*-
__doc__="""
09. Storm
"""

from NaNGFGraphikshared import CreateShapeComponent, operateOnBlackAtInterval, ClearPaths
from NaNGFNoise import snoise2, noiseMap
from NaNFilter import NaNFilter

try:
    from GlyphsApp import *
except Exception as e:
    from glyphsLib import *


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
