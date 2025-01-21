# MenuTitle: Maps
# -*- coding: utf-8 -*-
__doc__ = """
Maps
"""

import random
from NaNGFAngularizzle import ConvertPathsToLineSegments, getListOfPoints
from NaNGFConfig import glyphSize
from NaNGFGraphikshared import AddComponents, AddPaths, AllPathBounds, ClearPaths, ConvertPathDirection, CreateLineComponent, Fill_Drawlines, RoundPaths, RoundPath, convertToFitpath
from NaNGFSpacePartition import BreakUpSpace
from NaNGlyphsEnvironment import glyphsEnvironment as G
from NaNGlyphsEnvironment import GSLayer
from NaNFilter import NaNFilter


class Maps(NaNFilter):

	params = {
		"S": {"gridsize": 10},
		"M": {"gridsize": 30},
		"L": {"gridsize": 40},
	}

	def setup(self):
		self.linecomponents = []
		line_vertical_comp = CreateLineComponent(
			self.font, "vertical", 6, "LineVerticalComponent"
		)
		line_horizontal_comp = CreateLineComponent(
			self.font, "horizontal", 6, "LineHorizontalComponent"
		)
		self.linecomponents.extend([line_vertical_comp, line_horizontal_comp])

	def processLayer(self, thislayer, params):
		if glyphSize(thislayer.parent) == "S":
			self.processLayerSmall(thislayer)
		else:
			self.processLayerLarge(thislayer, params)

	def processLayerLarge(self, thislayer, params):
		gridsize = params["gridsize"]
		pathlist = ConvertPathsToLineSegments(thislayer.paths, 20)
		outlinedata = getListOfPoints(pathlist)
		bounds = AllPathBounds(thislayer)

		ClearPaths(thislayer)

		iterations = [
			(random.randrange(200, 400), "vertical"),
			(random.randrange(200, 400), "horizontal"),
			(random.randrange(70, 100), "blob"),
		]

		for maxchain, shape in iterations:
			newtris = self.SortCollageSpace(
				thislayer, outlinedata, gridsize, bounds, "stick"
			)
			groups = BreakUpSpace(thislayer, newtris, gridsize, maxchain)
			self.ApplyCollageGraphixxx(thislayer, groups, shape, self.linecomponents)

		self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)

	def processLayerSmall(self, thislayer):
		G.remove_overlap(thislayer)
		roundedpathlist = RoundPaths(thislayer.paths)
		ClearPaths(thislayer)
		AddPaths(roundedpathlist, thislayer)

	def ApplyCollageGraphixxx(self, layer, groups, drawtype, linecomponents):

		for g in groups:
			if len(g) < 2:
				continue

			templayer = GSLayer()
			G.add_paths(templayer, g)
			G.remove_overlap(templayer)

			for p in templayer.paths:
				nodelen = len(p.nodes)
				if nodelen < 4:
					continue

				roundedpath = RoundPath(p, "nodes")
				roundedpath = convertToFitpath(roundedpath, True)
				if not roundedpath:
					continue

				if drawtype == "vertical" or drawtype == "horizontal":

					rw = roundedpath.bounds.size.width
					rh = roundedpath.bounds.size.height
					if (rw > 130 or rh > 130):
						all_lines = Fill_Drawlines(
							layer, roundedpath, drawtype, 20, linecomponents
						)
						AddComponents(all_lines, layer)

				if drawtype == "blob":
					# disallow small blobs
					rw = roundedpath.bounds.size.width
					rh = roundedpath.bounds.size.height
					if (rw > 80 and rh > 80) and (rw < 180 or rh < 180):
						ConvertPathDirection(roundedpath, -1)
						layer.paths.append(roundedpath)

			del templayer


Maps()
