#MenuTitle: 02. 80sFade
# -*- coding: utf-8 -*-
__doc__="""
02. 80sFade
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *

# COMMON
font = Glyphs.font
selectedGlyphs = beginFilterNaN(font)


# ====== OFFSET LAYER CONTROLS ================== 

def doOffset( Layer, hoffset, voffset ):
	try:
		offsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
		offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_( Layer, hoffset, voffset, False, False, 0.5, None,None)
	except Exception as e:
		print "offset failed"

def saveOffsetPaths( Layer , hoffset, voffset, removeOverlap):
	templayer = Layer.copy()
	templayer.name = "tempoutline"
	currentglyph = Layer.parent
	currentglyph.layers.append(templayer)
	tmplayer_id = templayer.layerId
	doOffset(templayer, hoffset, voffset)
	if removeOverlap==True: templayer.removeOverlap()
	offsetpaths = templayer.paths
	del currentglyph.layers[tmplayer_id]
	return offsetpaths

# ================================================



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


def Output80sFade():

	for glyph in selectedGlyphs:

		glyph.beginUndo()
		beginGlyphNaN(glyph)

		# --- °°°°°°°

		thislayer = font.glyphs[glyph.name].layers[0]
		thislayer.beginChanges()

		# ---
		
		#thislayer.removeOverlap()
		glyphsize = glyphSize(glyph)

		if glyphsize=="S": 
			offset = -5
			iterations = 50
		if glyphsize=="M": 
			offset = -15 
			iterations = 400
		if glyphsize=="L": 
			offset = -20
			iterations = 420

		# ----

		pathlist = doAngularizzle(thislayer.paths, 20)
		outlinedata = setGlyphCoords(pathlist)

		try:
			startrect = AllPathBounds(thislayer)
			allrectangles = MakeRectangles([startrect], 5)
			shape_components = CreateAllShapeComponents(font, 100, 100)

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

		except:
			print "Glyph (", glyph.name, ") failed to execute."

		# ---

		thislayer.endChanges()

		# --- °°°°°°°

		endGlyphNaN(glyph)
		glyph.endUndo()


# =======

Output80sFade()

# =======

#OutputFur()
#OutputSpikes()

endFilterNaN(font)







