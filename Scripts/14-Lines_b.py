#MenuTitle: 14. Lines b
# -*- coding: utf-8 -*-
__doc__="""
14. Lines b
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
	gap = 18
	checkgap = 3

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
		dist = distance([sx,sy],[ex,ey])

		#keeping same scalex, scaley makes an interesting effect

		if direction=="vertical": 
			comp = GSComponent(line_vertical_comp)
			scaley = (float(1)/100)*dist
			#scalex = random.randrange(1,8)
			scalex = 1
		else: 
			comp = GSComponent(line_horizontal_comp)
			scalex = (float(1)/100)*dist
			#scaley = random.randrange(1,8)
			scaley = 1
		
		comp.transform = ((scalex, 0.0, 0.0, scaley, sx, sy))
		linecomponents.append(comp)

	return linecomponents



def LoopLines(thislayer, outlinedata):

	looppaths = []

	for path in outlinedata:

		direction = path[0]
		structure = path[1]
		nodelen = len(structure)
		minstep = 4
		maxstep = 10
		switch = True
		n = 0
		curve = GSPath()

		while n < nodelen:

			x1 = structure[n][0]
			y1 = structure[n][1]
			step = random.randrange(minstep, maxstep)

			if n+step>=nodelen-1:
				n = nodelen
				break

			# --- set node pos for main or end

			if n<nodelen-1:
				x2 = structure[n+step+1][0]
				y2 = structure[n+step+1][1]
				n+=step
			else: 
				x2 = structure[0][0]
				y2 = structure[0][1]

			a = atan2(y1-y2, x1-x2)
			a+=radians(90)

			if direction== Direction.ANTICLOCKWISE:
				pushdist = 1
			else:
				pushdist = -0.3

			linex = pushdist * cos(a)
			liney = pushdist * sin(a)
			linex_push = linex * 20
			liney_push = liney * 20

			#

			if switch==True:

				endx1 = x1+linex_push
				endy1 = y1+liney_push
				endx2 = x2+linex_push
				endy2 = y2+liney_push

				handle_len = distance([x1, y1], [x2, y2]) * 0.8
				handlex1 = endx1 + (linex*handle_len)
				handley1 = endy1 + (liney*handle_len)
				handlex2 = endx2 + (linex*handle_len)
				handley2 = endy2 + (liney*handle_len)

				curve.nodes.append(GSNode([x1, y1], type = GSLINE))
				curve.nodes.append(GSNode([endx1, endy1], type = GSLINE))
				curve.nodes.append(GSNode([handlex1, handley1], type = GSOFFCURVE))
				curve.nodes.append(GSNode([handlex2, handley2], type = GSOFFCURVE))
				curve.nodes.append(GSNode([endx2, endy2], type = GSCURVE))
				curve.nodes.append(GSNode([x2, y2], type = GSLINE))

			else:

				endx1 = x1-linex_push
				endy1 = y1-liney_push
				endx2 = x2-linex_push
				endy2 = y2-liney_push

				handle_len = distance([x1, y1], [x2, y2]) * 0.8
				handlex1 = endx1 - (linex*handle_len)
				handley1 = endy1 - (liney*handle_len)
				handlex2 = endx2 - (linex*handle_len)
				handley2 = endy2 - (liney*handle_len)

				curve.nodes.append(GSNode([x1, y1], type = GSLINE))
				curve.nodes.append(GSNode([endx1, endy1], type = GSLINE))
				curve.nodes.append(GSNode([handlex1, handley1], type = GSOFFCURVE))
				curve.nodes.append(GSNode([handlex2, handley2], type = GSOFFCURVE))
				curve.nodes.append(GSNode([endx2, endy2], type = GSCURVE))
				curve.nodes.append(GSNode([x2, y2], type = GSLINE))

			n+=1
			switch = not switch

		curve.closed = True
		looppaths.append(curve)

	return looppaths



def OutputLines():

	global line_vertical_comp, line_horizontal_comp
	line_vertical_comp = CreateLineComponent(font, "vertical", 8, "LineVerticalComponent")
	line_horizontal_comp = CreateLineComponent(font, "horizontal", 8, "LineHorizontalComponent")

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

		pathlist = ConvertPathsToSkeleton(thislayer.paths, 4)
		outlinedata = setGlyphCoords(pathlist)

		loopmask = LoopLines(thislayer, outlinedata)
		loopmasklist = ConvertPathsToSkeleton(loopmask, 20)
		outlinedata = setGlyphCoords(loopmasklist)

		AddAllPathsToLayer(loopmask, thislayer)

		try:
			startrect = AllPathBounds(thislayer)
			allrectangles = MakeRectangles([startrect], 8)
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
			print("Glyph (", glyph.name, ") failed to execute.")

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







