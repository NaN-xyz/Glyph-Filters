# MenuTitle: Doodle Shadow
# -*- coding: utf-8 -*-
__doc__ = """
Doodle Shadow
"""


from NaNGFAngularizzle import ConvertPathsToLineSegments, getListOfPoints
from NaNGFGraphikshared import AddPaths, ClearPaths, DoShadow
from NaNGFNoise import NoiseOutline
import random

from NaNFilter import NaNFilter
from NaNGlyphsEnvironment import glyphsEnvironment as G


class DoodleShadow(NaNFilter):

	params = {
		"S": {"depth": random.randrange(40, 85)},
		"M": {"depth": random.randrange(50, 100)},
		"L": {"depth": random.randrange(60, 100)}
	}
	glyph_stroke_width = 16
	shadow_stroke_width = 6
	angle = -160  # random.randrange(0, 360)

	def setup(self):
		pass

	def processLayer(self, thislayer, params):

		depth = params["depth"]

		G.remove_overlap(thislayer)
		pathlist = ConvertPathsToLineSegments(thislayer.paths, 20)
		outlinedata = getListOfPoints(pathlist)

		ClearPaths(thislayer)

		noisepaths = NoiseOutline(thislayer, outlinedata)
		noiseoutline = self.expandMonolineFromPathlist(noisepaths, self.glyph_stroke_width)
		shadowpaths = DoShadow(thislayer, outlinedata, self.angle, depth, "lines")
		shadowoutline = self.expandMonolineFromPathlist(shadowpaths, self.shadow_stroke_width)

		AddPaths(noiseoutline, thislayer)
		AddPaths(shadowoutline, thislayer)

		G.remove_overlap(thislayer)
		self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)


DoodleShadow()
