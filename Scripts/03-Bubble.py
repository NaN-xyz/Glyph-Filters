#MenuTitle: 03. Bubble
# -*- coding: utf-8 -*-
__doc__="""
03. Bubble
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



# THE MAIN BUBBLE ACTION

def Bubble(thislayer, outlinedata, minpush, maxpush):

	for path in outlinedata:

		direction = path[0]
		structure = path[1]
		nodelen = len(structure)
		bubble = GSPath()
		n = 0

		while n < nodelen:

			x1 = structure[n][0]
			y1 = structure[n][1]
			minstep = 10
			maxstep = 40

			if direction=="False": maxstep=int(maxstep*0.5)
			step = random.randrange(minstep, maxstep)

			if n+step>=nodelen-1:
				n = nodelen
				break

			# --- set node pos for main or end

			if n<nodelen-1:
				x2 = structure[n+step][0]
				y2 = structure[n+step][1]
				n+=step
			else:
				x2 = structure[0][0]
				y2 = structure[0][1]

			#if distance([x1, y1], [x2, y2]) < 1:
			#	continue

			a = atan2(y1-y2, x1-x2)
			a += radians(90)
			pushdist = random.randrange(minpush, maxpush) 
			linex = pushdist * cos(a)
			liney = pushdist * sin(a)

			if direction=="False":
				linex*=0.5
				liney*=0.5

			# DRAW THE POINTS
			bubble.nodes.append(GSNode([x1+linex, y1+liney], type = GSOFFCURVE))
			bubble.nodes.append(GSNode([x2+linex, y2+liney], type = GSOFFCURVE))
			bubble.nodes.append(GSNode([x2, y2], type = GSCURVE))

		bubble.closed = True
		thislayer.paths.append(bubble)


def OutputBubble():

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
			minfur, maxfur = 20, 50
		if glyphsize=="M": 
			offset = -10
			minfur, maxfur = 40, 100
		if glyphsize=="L": 
			offset = -20
			minfur, maxfur = 60, 120

		if glyphsize=="S": offset = -5
		if glyphsize=="M": offset = -10
		if glyphsize=="L": offset = -20

		offsetpaths = saveOffsetPaths(thislayer, offset, offset, removeOverlap=False)
		pathlist = doAngularizzle(offsetpaths, 4)
		outlinedata = setGlyphCoords(pathlist)

		ClearPaths(thislayer)

		Bubble(thislayer, outlinedata, 60, 80)

		# ---

		thislayer.endChanges()

		# --- °°°°°°°

		endGlyphNaN(glyph)
		glyph.endUndo()


# =======

OutputBubble()

# =======

#OutputFur()
#OutputSpikes()

endFilterNaN(font)







