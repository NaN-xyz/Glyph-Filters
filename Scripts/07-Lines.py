#MenuTitle: 07. Lines
# -*- coding: utf-8 -*-
__doc__="""
07. Lines
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import NaNFilter

class Lines(NaNFilter):
	params = {
		"S": { "offset": -5, "iterations":  50  },
		"M": { "offset": -15, "iterations": 400 },
		"L": { "offset": -20, "iterations": 420 }
	}

	def setup(self):
		self.line_vertical_comp = CreateLineComponent(self.font, "vertical", 2, "LineVerticalComponent")
		self.line_horizontal_comp = CreateLineComponent(self.font, "horizontal", 2, "LineHorizontalComponent")

	def processLayer(self, thislayer, params):

		outlinedata = setGlyphCoords(doAngularizzle(thislayer.paths, 40))

		try:
			allrectangles = MakeRectangles([AllPathBounds(thislayer)], 5)
			direction = "horizontal"
			linecomps = []

			for n in range(0, len(allrectangles)):
				x,y,w,h = allrectangles[n]
				tile = [x,y,w,h]
				tilecoords = [[x,y], [x,y+h], [x+w,y+h], [x+w,y]]

				if direction == "horizontal": direction="vertical"
				else: direction="horizontal"

				dlines = self.DrawlinesTile(thislayer, outlinedata, tile, direction)
				linecomps.extend( dlines )

			ClearPaths(thislayer)
			AddAllComponentsToLayer(linecomps, thislayer)

		except Exception as e:
			print "Glyph (", thislayer.name, ") failed to execute:", e

	def DrawlinesTile(self, thislayer, outlinedata, tile, direction):

		x = int(tile[0])
		y = int(tile[1])
		w = int(tile[2])
		h = int(tile[3])

		tilecoords = [[x,y], [x,y+h], [x+w,y+h], [x+w,y]]
		lines = []
		linecomponents = []
		gap = 20
		checkgap = 2

		if direction=="horizontal":
			for y2 in range(y, y+h+gap, gap):
				newline = []
				for x2 in range(x, x+w, checkgap):
					if withinGlyphBlack(x2, y2, outlinedata) and point_inside_polygon_faster(x2, y2, tilecoords):
							newline.append([x2, y2])
					else:
						if len(newline)>1:
							lines.append(newline)
							newline = []
				y2 = 0
				if len(newline)>1: lines.append(newline)

		if direction=="vertical":
			for x2 in range(x, x+w+gap, gap):
				newline = []
				for y2 in range(y, y+h, checkgap):
					if withinGlyphBlack(x2, y2, outlinedata) and point_inside_polygon_faster(x2, y2, tilecoords):
							newline.append([x2, y2])
					else:
						if len(newline)>1:
							lines.append(newline)
							newline = []
				x2 = 0
				if len(newline)>1: lines.append(newline)

		for l in lines:
			sx, sy = l[0][0], l[0][1]
			ex, ey = l[-1][0], l[-1][1]
			comp = returnLineComponent([sx,sy], [ex,ey], direction, [self.line_vertical_comp,self.line_horizontal_comp], 100)
			linecomponents.append(comp)

		return linecomponents

Lines()
