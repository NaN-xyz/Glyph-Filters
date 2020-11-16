#MenuTitle: 06. MoonRocks
# -*- coding: utf-8 -*-
__doc__="""
06. MoonRocks
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

def MoonRocks(thislayer, outlinedata, iterations, maxgap, shapetype):

	list_dots, rocks = [], []
	b = AllPathBounds(thislayer)

	if b is not None:

		ox, oy, w, h = b[0], b[1], b[2], b[3]

		for f in range(0, iterations):

			x = random.randrange(ox, ox+w)
			y = random.randrange(oy, oy+h)

			if withinGlyphBlack(x, y, outlinedata):

				rad = random.randrange(10,250)
				inside = True
				bufferdistcircle = maxgap

				for n in range(0, len(list_dots)):

					nx = list_dots[n][0]
					ny = list_dots[n][1]
					nr = list_dots[n][2]
					dist = math.hypot(nx - x, ny - y) #alt method

					if dist<(nr+rad+bufferdistcircle):
						inside=False
						break

				if inside==True:
					circles = []
					circle = drawCircle(x, y, rad*2, rad*2)
					circles.append(circle)
					circlea = doAngularizzle(circles, 10)
					circlea = setGlyphCoords(circlea)
					circlecoords = circlea[0][1]

					if ShapeWithinOutlines(circlecoords, outlinedata):
						list_dots.append([x, y, rad])


		print "Number of circles found:", len(list_dots)

		for c in range(0, len(list_dots)):
			x, y = list_dots[c][0], list_dots[c][1]
			size = list_dots[c][2]
			if shapetype=="blob": 
				circle = drawBlob(x, y, size*2, 5, True)
			else: 
				circle = drawCircle(x, y, size*2, size*2)
			rocks.append(circle)

		return rocks
		

def OutputMoonRocks(maxgap, shapetype):

	for glyph in selectedGlyphs:

		glyph.beginUndo()
		beginGlyphNaN(glyph)

		# --- °°°°°°°

		thislayer = font.glyphs[glyph.name].layers[0]
		thislayer.beginChanges()

		# ---
		
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

		offsetpaths = saveOffsetPaths(thislayer, offset, offset, removeOverlap=False)
		pathlist = doAngularizzle(offsetpaths, 20)
		outlinedata = setGlyphCoords(pathlist)
		
		rockpaths = MoonRocks(thislayer, outlinedata, iterations, maxgap, shapetype)
		rockpaths = ConvertPathlistDirection(rockpaths, 1)
		AddAllPathsToLayer(rockpaths, thislayer)

		# ---

		thislayer.endChanges()

		# --- °°°°°°°

		endGlyphNaN(glyph)
		glyph.endUndo()


# =======

OutputMoonRocks(maxgap=8, shapetype="blob")

# =======

#OutputFur()
#OutputSpikes()

endFilterNaN(font)







