# MenuTitle: Doodle Triangles
# -*- coding: utf-8 -*-
__doc__ = """
Doodle Triangles
"""

import random
from NaNFilter import NaNFilter
from NaNGFAngularizzle import ConvertPathsToLineSegments, getListOfPoints
from NaNGFGraphikshared import AddPaths, AllPathBounds, ClearPaths, ConvertPathlistDirection
from NaNGFNoise import NoiseOutline
from NaNGlyphsEnvironment import glyphsEnvironment as G


class DoodleTriangles(NaNFilter):

	params = {
		"S": {"gridsize": 60},
		"M": {"gridsize": 60},
		"L": {"gridsize": 70},
	}
	glyph_stroke_width = 16
	tri_stroke_width = 4

	def setup(self):
		pass

	def processLayer(self, thislayer, params):

		G.remove_overlap(thislayer)

		gridsize = params["gridsize"]
		pathlist = ConvertPathsToLineSegments(thislayer.paths, 20)
		outlinedata = getListOfPoints(pathlist)
		bounds = AllPathBounds(thislayer)

		ClearPaths(thislayer)

		noisepaths = NoiseOutline(thislayer, outlinedata)
		noiseoutline = self.expandMonolineFromPathlist(noisepaths, self.glyph_stroke_width)

		newtris = self.SortCollageSpace(thislayer, outlinedata, gridsize, bounds, "stick", True)
		blacktris = ConvertPathlistDirection(random.sample(newtris, int(len(newtris) / 10)), -1)

		strokedtris = self.expandMonolineFromPathlist(newtris, self.tri_stroke_width)
		AddPaths(strokedtris, thislayer)
		AddPaths(noiseoutline, thislayer)
		AddPaths(blacktris, thislayer)

		G.remove_overlap(thislayer)
		self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)


DoodleTriangles()
