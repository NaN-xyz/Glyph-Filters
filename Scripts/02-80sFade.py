#MenuTitle: 02. 80sFade
# -*- coding: utf-8 -*-
__doc__="""
02. 80sFade
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import NaNFilter


# THE MAIN CIRCLE FUNCTION ACTION

def do80sFade(thislayer, outlinedata, tilecoords, shape_components):

	b = AllPathBounds(thislayer)

	if b is not None:

		fadecomps = []
		size=random.randrange(4,15)
		r = random.randrange(0,len(shape_components))
		ox, oy, w, h = b[0], b[1], b[2], b[3]

		for y in range(oy, oy+h, 20):

			for x in range(ox, ox+w, 20):

				if withinGlyphBlack(x, y, outlinedata):

					if point_inside_polygon(x, y, tilecoords):

						if size>2:
							fadecomp = GSComponent(shape_components[r])
							scale = (float(1)/100)*size
							fadecomp.transform = ((scale, 0.0, 0.0, scale, x, y))
							#thislayer.components.append(fadecomp)
							fadecomps.append(fadecomp)
				size+=0.01

		return fadecomps


class EightiesFade(NaNFilter):
	params = {
		"S": {"offset": -5, "iterations": 50},
		"M": {"offset": -15, "iterations": 400},
		"L": {"offset": -20, "iterations": 420},
	}


	def processLayer(self, thislayer, params):
		pathlist = doAngularizzle(thislayer.paths, 20)
		outlinedata = setGlyphCoords(pathlist)

		try:
			startrect = AllPathBounds(thislayer)
			allrectangles = MakeRectangles([startrect], 5)
			shape_components = CreateAllShapeComponents(self.font, 100, 100)

			fadecomps = []

			for n in range(0, len(allrectangles)):
				x = allrectangles[n][0]
				y = allrectangles[n][1]
				w = allrectangles[n][2]
				h = allrectangles[n][3]
				tile = [x,y,w,h]
				tilecoords = [[x,y], [x,y+h], [x+w,y+h], [x+w,y]]
				fadecomps.extend(do80sFade(thislayer, outlinedata, tilecoords, shape_components) )

			ClearPaths(thislayer)
			AddAllComponentsToLayer(fadecomps, thislayer)

		except Exception as e:
			print("Layer (", thislayer.name, ") failed to execute.", e)

EightiesFade()
