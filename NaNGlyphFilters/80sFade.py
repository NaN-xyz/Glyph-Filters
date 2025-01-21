# MenuTitle: 80s Fade
# -*- coding: utf-8 -*-
__doc__ = """
80s Fade
"""

from NaNGlyphsEnvironment import GSComponent
from NaNGlyphsEnvironment import glyphsEnvironment as G
from NaNGFGraphikshared import (
	AllPathBounds,
	MakeRectangles,
	ClearPaths,
	AddComponents,
	CreateAllShapeComponents,
	withinGlyphBlack,
	point_inside_polygon,
)
from NaNFilter import NaNFilter
import random


class EightiesFade(NaNFilter):
	def processLayer(self, thislayer, params):

		outlinedata = G.outline_data_for_hit_testing(thislayer)

		try:
			startrect = AllPathBounds(thislayer)
			if startrect is None:
				return
			allrectangles = MakeRectangles([startrect], 5)
			shape_components = CreateAllShapeComponents(self.font, 100, 100)

			fadecomps = []

			for n in range(0, len(allrectangles)):
				x, y, w, h = allrectangles[n]
				tilecoords = [[x, y], [x, y + h], [x + w, y + h], [x + w, y]]
				fadecomps.extend(
					self.do80sFade(startrect, outlinedata, tilecoords, shape_components)
				)

			ClearPaths(thislayer)
			AddComponents(fadecomps, thislayer)

		except Exception as e:
			print(("Layer (", thislayer.name, ") failed to execute.", e))

	def do80sFade(self, b, outlinedata, tilecoords, shape_components):

		fadecomps = []
		size = random.randrange(4, 15)
		r = random.choice(shape_components)
		ox, oy, w, h = b[0], b[1], b[2], b[3]

		for y in range(oy, oy + h, 20):
			for x in range(ox, ox + w, 20):
				if (
					withinGlyphBlack(x, y, outlinedata)
					and point_inside_polygon(x, y, tilecoords)
					and size > 2
				):
					fadecomp = GSComponent(r)
					scale = size / 100.0
					fadecomp.scale = (scale, scale)
					fadecomp.position = (x, y)  # ?
					fadecomps.append(fadecomp)
				size += 0.01

		return fadecomps


EightiesFade()
