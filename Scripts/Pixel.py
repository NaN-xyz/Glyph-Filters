#MenuTitle: Pixel
# -*- coding: utf-8 -*-
__doc__="""
Pixel
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFNoise import *
from NaNFilter import NaNFilter

class Pixel(NaNFilter):

	gridsize = 30
	minsize, maxsize = 30, 80

	def processLayer(self, thislayer, params):

		offsetpaths = self.saveOffsetPaths(thislayer, 10, 10, removeOverlap=False)
		pathlist = ConvertPathsToSkeleton(offsetpaths, 4)
		outlinedata = setGlyphCoords(pathlist)
		components = self.Fill_Halftone(thislayer)
		bounds = AllPathBounds(thislayer)
		ClearPaths(thislayer)
		self.HalftoneGrid(thislayer, outlinedata, bounds, components)


	def Fill_Halftone(self, thislayer):

		components = []

		for size in range(0,5):
			font = self.font
			shapename = "pixel"+str(size)
			if font.glyphs[shapename]: del font.glyphs[shapename]
			ng = GSGlyph()
			ng.name = shapename
			ng.category = "Mark"
			ng.export = True
			font.glyphs.append(ng)
			thislayer = font.glyphs[ng.name].layers[0]
			thislayer.width = 0

			ox, oy = 0, 0
			w, h = 40, 40
			grid = 10
			unit = 5

			if size!=0:
				gridx = 10 * size
				gridy = gridx
			else:
				gridx = 10
				gridy = 5

			x, y = ox, oy
			switchx = False

			for x in range(ox, ox+w, gridx):
				for y in range(oy, oy+h, gridy):
					if switchx==True:
						if size==0:
							adjust = 5
							switchx = not switchx
						else:
							adjust = gridx/2
							switchx = not switchx
					else:
						adjust=0
						switchx = not switchx

					ns = drawRectangle( x + adjust, y , unit, unit)
					thislayer.paths.append(ns)

				switchx = False 
			components.append(ng)
		return components

	def HalftoneGrid(self, thislayer, outlinedata, bounds, components):

		ox = int( bounds[0] )
		oy = int( bounds[1] )
		w = int( bounds[2] )
		h = int( bounds[3] )
		
		unitw = 40
		unith = 40

		noisescale = 0.001
		seedx = random.uniform(0,100000)
		seedy = random.uniform(0,100000)
		minsize, maxsize = -1, 6

		for x in range(ox, ox+w, unitw):
			for y in range(oy, oy+h, unith):
				size = pnoise2( (y+seedy),(x+seedx)) 
				size = noiseMap( size, 0, 15 )
				size = int(abs(size)) + 1

				if size>4: size=5
				if size>0:
					glyph = components[size-1]
					pixelcomponent = GSComponent(glyph)
					adjust = unitw/2 -2
					pixelcomponent.transform = ((1, 0.0, 0.0, 1, x-adjust, y-adjust))

				shapepath = []
				shape = drawRectangle(x, y, unitw, unith)
				shapepath.append(shape)
				nshape = ConvertPathsToSkeleton(shapepath, 10)
				nshape = setGlyphCoords(nshape)
				finalshape = nshape[0][1]
				
				if ShapeWithinOutlines(finalshape, outlinedata):
					if size==5:
						thislayer.paths.append( drawRectangle(x,y, unitw, unith))
					else:
						thislayer.components.append(pixelcomponent)

Pixel()
