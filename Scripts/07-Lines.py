#MenuTitle: 07. Lines
# -*- coding: utf-8 -*-
__doc__="""
07. Lines
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

def expandMonoline(Layer, noodleRadius):
	try:
		offsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
		offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_( Layer, noodleRadius, noodleRadius, True, False, 0.5, None,None)
	except Exception as e:
		logToConsole( "expandMonoline: %s\n%s" % (str(e), traceback.format_exc()) )

# ================================================



# THE MAIN ACTION

def DrawlinesTile(thislayer, outlinedata, tile, direction):

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
		comp = returnLineComponent([sx,sy], [ex,ey], direction, [line_vertical_comp,line_horizontal_comp], 100)
		linecomponents.append(comp)

	return linecomponents

		




def OutputLines():

	global line_vertical_comp, line_horizontal_comp
	line_vertical_comp = CreateLineComponent(font, "vertical", 2, "LineVerticalComponent")
	line_horizontal_comp = CreateLineComponent(font, "horizontal", 2, "LineHorizontalComponent")

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

		pathlist = doAngularizzle(thislayer.paths, 40)
		outlinedata = setGlyphCoords(pathlist)

		try:
			startrect = AllPathBounds(thislayer)
			allrectangles = MakeRectangles([startrect], 5)
			direct = True
			linecomps = []

			for n in range(0, len(allrectangles)):
				x = allrectangles[n][0]
				y = allrectangles[n][1]
				w = allrectangles[n][2]
				h = allrectangles[n][3]
				tile = [x,y,w,h]
				tilecoords = [[x,y], [x,y+h], [x+w,y+h], [x+w,y]]

				if direct == True: direction="vertical"
				else: direction="horizontal"

				dlines = DrawlinesTile(thislayer, outlinedata, tile, direction)
				linecomps.extend( dlines )
				direct = not direct

			ClearPaths(thislayer)
			AddAllComponentsToLayer(linecomps, thislayer)

		except:
			print "Glyph (", glyph.name, ") failed to execute."

		# ---

		thislayer.endChanges()

		# --- °°°°°°°

		endGlyphNaN(glyph)
		glyph.endUndo()


# =======

OutputLines()

# =======

#OutputFur()
#OutputSpikes()

endFilterNaN(font)







