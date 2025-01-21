# MenuTitle: Lines
# -*- coding: utf-8 -*-
__doc__ = """
Lines
"""

from NaNFilter import NaNFilter
from NaNGFGraphikshared import AddComponents, AllPathBounds, ClearPaths, CreateLineComponent, MakeRectangles, SnapToGrid, point_inside_polygon_faster, returnLineComponent, withinGlyphBlack
from NaNGlyphsEnvironment import glyphsEnvironment as G


class Lines(NaNFilter):
	params = {
		"S": {"iterations": 50},
		"M": {"iterations": 400},
		"L": {"iterations": 420},
	}

	strokesize = 8

	def setup(self):
		self.line_vertical_comp = CreateLineComponent(
			self.font, "vertical", self.strokesize, "LineVerticalComponent"
		)
		self.line_horizontal_comp = CreateLineComponent(
			self.font, "horizontal", self.strokesize, "LineHorizontalComponent"
		)

	def processLayer(self, thislayer, params):

		outlinedata = G.outline_data_for_hit_testing(thislayer)

		try:
			allrectangles = MakeRectangles([AllPathBounds(thislayer)], 5)
			direction = "horizontal"
			linecomps = []

			for tile in allrectangles:
				if direction == "horizontal":
					direction = "vertical"
				else:
					direction = "horizontal"

				linecomps.extend(
					self.DrawlinesTile(thislayer, outlinedata, tile, direction)
				)

			ClearPaths(thislayer)
			AddComponents(linecomps, thislayer)

		except Exception as e:
			print("Glyph (", thislayer.name, ") failed to execute:", e)

	def DrawlinesTile(self, thislayer, outlinedata, tile, direction):

		x, y, w, h = [int(el) for el in tile]
		tilecoords = [[x, y], [x, y + h], [x + w, y + h], [x + w, y]]
		lines = []
		linecomponents = []
		gap = 18
		checkgap = 3

		self.newline = []

		def add_line(x2, y2):
			if withinGlyphBlack(x2, y2, outlinedata) and point_inside_polygon_faster(
				x2, y2, tilecoords
			):
				self.newline.append([x2, y2])
			else:
				if len(self.newline) > 1:
					lines.append(self.newline)
					self.newline = []

		if direction == "horizontal":
			for y2 in range(y, y + h + gap, gap):
				for x2 in range(x, x + w, checkgap):
					add_line(x2, y2)

		if direction == "vertical":
			for x2 in range(x, x + w + gap, gap):
				for y2 in range(y, y + h, checkgap):
					add_line(x2, y2)

		lines = SnapToGrid(lines, self.strokesize)

		for line in lines:
			if line[0] == line[-1]:
				continue
			comp = returnLineComponent(
				line[0],
				line[-1],
				direction,
				[self.line_vertical_comp, self.line_horizontal_comp],
				100,
			)
			linecomponents.append(comp)

		return linecomponents


Lines()
