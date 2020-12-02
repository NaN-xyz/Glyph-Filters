#MenuTitle: 32. Microbe
# -*- coding: utf-8 -*-
__doc__="""
06. Microbe
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
		print("offset failed")

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

def Microbe(thislayer, outlinedata, iterations, maxgap, maxsize, shapetype):

	list_dots, rocks = [], []
	b = AllPathBounds(thislayer)

	if b is not None:

		ox, oy, w, h = b[0], b[1], b[2], b[3]

		for f in range(0, iterations):

			x = random.randrange(ox, ox+w)
			y = random.randrange(oy, oy+h)

			if withinGlyphBlack(x, y, outlinedata):

				rad = random.randrange(10,maxsize)
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


		print("Number of circles found:", len(list_dots))

		for c in range(0, len(list_dots)):
			x, y = list_dots[c][0], list_dots[c][1]
			size = list_dots[c][2]
			handles = True
			if shapetype=="blob": 
				if size<15: handles = False
				circle = drawBlob(x, y, size*2, 5, handles)
			else: 
				circle = drawCircle(x, y, size*2, size*2)
			rocks.append(circle)

		return rocks
		

def OutputMoonRocks():

	for glyph in selectedGlyphs:

		glyph.beginUndo()
		beginGlyphNaN(glyph)

		# --- °°°°°°°

		thislayer = font.glyphs[glyph.name].layers[0]
		thislayer.beginChanges()

		# ---
		
		glyphsize = glyphSize(glyph)

		if glyphsize=="S": 
			offset = 15
			iterations = 25000
			maxsize = 40
		if glyphsize=="M": 
			offset = 0
			iterations = 70000
			maxsize = 100
		if glyphsize=="L": 
			offset = 0
			iterations = 100000
			maxsize = 140

		maxgap = 1

		# ----

		offsetpaths = saveOffsetPaths(thislayer, offset, offset, removeOverlap=True)
		pathlist = doAngularizzle(offsetpaths, 30)
		outlinedata = setGlyphCoords(pathlist)
		
		microbepaths = Microbe(thislayer, outlinedata, iterations, maxgap, maxsize, "blob")
		microbepaths = ConvertPathlistDirection(microbepaths, 1)
		ClearPaths(thislayer)
		AddAllPathsToLayer(microbepaths, thislayer)

		# ---

		thislayer.endChanges()

		# --- °°°°°°°

		endGlyphNaN(glyph)
		glyph.endUndo()


# =======

OutputMoonRocks()

# =======

#OutputFur()
#OutputSpikes()

endFilterNaN(font)







