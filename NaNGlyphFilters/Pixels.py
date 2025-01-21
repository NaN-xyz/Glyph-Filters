# MenuTitle: Pixel
# -*- coding: utf-8 -*-
__doc__ = """
Pixel
"""

import random
from noise import pnoise2
from NaNGFNoise import noiseMap
from NaNGlyphsEnvironment import GSGlyph, GSLayer, GSComponent
from NaNGFGraphikshared import AllPathBounds, ClearPaths, ShapeWithinOutlines, drawRectangle
from NaNFilter import NaNFilter
from NaNGlyphsEnvironment import glyphsEnvironment as G


class Pixel(NaNFilter):

	gridsize = 30
	minsize, maxsize = 30, 80

	def setup(self):
		self.components = self.Fill_Halftone()

	def processLayer(self, thislayer, params):
		offsetpaths = self.saveOffsetPaths(thislayer, 10, 10, removeOverlap=False)
		outlinedata = G.outline_data_for_hit_testing(offsetpaths)

		bounds = AllPathBounds(thislayer)
		ClearPaths(thislayer)
		self.HalftoneGrid(thislayer, outlinedata, bounds, self.components)

	def Fill_Halftone(self):

		font = self.font
		assert font
		components = []

		for size in range(0, 5):
			shapename = "pixel" + str(size)
			if font.glyphs[shapename]:
				del font.glyphs[shapename]
			ng = GSGlyph()
			ng.name = shapename
			ng.category = "Mark"
			ng.export = True
			font.glyphs.append(ng)
			for master in font.masters:
				mid = master.id
				thislayer = GSLayer()
				thislayer.layerId = thislayer.associatedMasterId = mid
				ng.layers[mid] = thislayer
				thislayer.width = 0
				ox, oy = 0, 0
				w, h = self.gridsize, self.gridsize
				# grid = 10
				unit = 5

				if size == 4:
					ns = drawRectangle(ox + ((w - unit) / 2), oy + ((h - unit) / 2), w, h)
					thislayer.paths.append(ns)
					continue

				if size != 0:
					gridx = 10 * size
					gridy = gridx
				else:
					gridx = 10
					gridy = 5

				x, y = ox, oy
				switchx = False

				for x in range(ox, ox + w, gridx):
					for y in range(oy, oy + h, gridy):
						if switchx:
							if size == 0:
								adjust = 5
								switchx = not switchx
							else:
								adjust = gridx / 2
								switchx = not switchx
						else:
							adjust = 0
							switchx = not switchx

						ns = drawRectangle(x + adjust, y, unit, unit)
						thislayer.paths.append(ns)

					switchx = False
			components.append(ng)
		return components

	def HalftoneGrid(self, thislayer, outlinedata, bounds, components):

		ox = int(bounds[0])
		oy = int(bounds[1])
		w = int(bounds[2])
		h = int(bounds[3])

		unitw = self.gridsize
		unith = self.gridsize

		# noisescale = 0.001
		seedx = random.uniform(0, 100000)
		seedy = random.uniform(0, 100000)
		# minsize, maxsize = -1, 6
		for x in range(ox, ox + w, unitw):
			for y in range(oy, oy + h, unith):
				size = pnoise2((y + seedy), (x + seedx))
				size = noiseMap(size, 0, 15)
				size = int(abs(size)) + 1
				if size < 0:
					continue

				if size >= 5:
					size = 5
				glyph = components[size - 1]
				pixelcomponent = GSComponent(glyph)
				adjust = unitw / 2 - 2
				pixelcomponent.position = (x - adjust, y - adjust)

				finalshape = ((x + unitw, y + unith), (x, y + unith), (x, y), (x + unitw, y))
				if ShapeWithinOutlines(finalshape, outlinedata):
					if size > 5:
						thislayer.paths.append(drawRectangle(x, y, unitw, unith))
					else:
						thislayer.components.append(pixelcomponent)


Pixel()
