#MenuTitle: 29. Speckled Dirt
# -*- coding: utf-8 -*-
__doc__="""
29. Speckled Dirt
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFNoise import *

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


def AddDirt(thislayer, outlinedata, bounds):

	start = defineStartXY(bounds, outlinedata)

	startx = start[0]
	starty = start[1]
	walklen = 10000

	noisescale = 0.05
	seedx = random.randrange(0,100000)
	seedy = random.randrange(0,100000)
	maxstep = 50
	minsize = 0
	maxsize = 6

	sx = startx
	sy = starty

	dirt = []

	for n in range(0, walklen):

		x_noiz = pnoise1( (n+seedx)*noisescale, 3) 
		rx = noiseMap( x_noiz, minsize, maxsize )

		y_noiz = pnoise1( ((1000+n)+seedy)*noisescale, 3) 
		ry = noiseMap( y_noiz, minsize, maxsize )

		nx = sx + rx
		ny = sy + ry

		if withinGlyphBlack(nx, ny, outlinedata):

			r = random.randrange(0,10)

			if r==2:

				size = random.randrange(6,18)
				#speck = drawTriangle(nx, ny, size, size)
				speck = drawSpeck(nx, ny, size, 6)
				dirt.append(speck)
				sx = nx
				sy = ny

	return dirt





# ----------------------------------------------------
# output controllers



def OutputNoiseOutline():

	for glyph in selectedGlyphs:

		beginGlyphNaN(glyph)
		glyph.beginUndo()

		# --- °°°°°°°

		thislayer = font.glyphs[glyph.name].layers[0]
		thislayer.beginChanges()

		# --

		glyphsize = glyphSize(glyph)

		pathlist = doAngularizzle(thislayer.paths, 4)
		outlinedata = setGlyphCoords(pathlist)

		ClearPaths(thislayer)

		noisepaths = NoiseOutline(thislayer, outlinedata)

		AddAllPathsToLayer(noisepaths, thislayer)

		# add specks of dirt --

		# thislayer = font.glyphs[glyph.name].layers[0]
		# tmpid = saveOutlinePaths(thislayer, -15, -15)
		# tmplayer = glyph.layers[tmpid]
		# pathlist = doAngularizzle(tmplayer.paths, 20)
		# outlinedata = setGlyphCoords(pathlist)

		# bounds = AllPathBounds(tmplayer)
		# del tmplayer
		# dirt = AddDirt(thislayer, outlinedata, bounds)

		# templayer = GSLayer()
		# templayer.name = "dirt"
		# currentglyph = thislayer.parent
		# currentglyph.layers.append(templayer)
		# tmplayer_id = templayer.layerId
		# tmplayer = glyph.layers[tmplayer_id]

		# for path in dirt: templayer.paths.append(path)

		# templayer.removeOverlap()

		# # convert below in to function that returns only positive paths

		# for path in tmplayer.paths: 
		# 	#print path
		# 	if path.direction == -1:
		# 		path.reverse()
		# 	thislayer.paths.append(path)

		# del glyph.layers[tmplayer_id]

		# ---

		thislayer.endChanges()

		# --- °°°°°°°

		endGlyphNaN(glyph)
		glyph.endUndo()


OutputNoiseOutline()



Font.enableUpdateInterface()

