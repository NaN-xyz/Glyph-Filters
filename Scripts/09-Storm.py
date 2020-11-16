#MenuTitle: 09. Storm
# -*- coding: utf-8 -*-
__doc__="""
09. Storm
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


def drawStorm(thislayer, outlinedata, step, minsize, maxsize, stormcomponent):

	b = AllPathBounds(thislayer)
	ox, oy, w, h = int(b[0])+1, b[1]+1, b[2], b[3]
	stormpaths = []

	freq = 0.005
	noiseseed = random.randrange(0,100000)
	n=0

	for y in range(oy, oy+h, step):
		for x in range(ox, ox+h, step):
			if withinGlyphBlack(x, y, outlinedata):
				noiz = snoise2(x*freq, y*freq, 3)
				size = noiseMap( noiz, minsize, maxsize )
				if size>4:
					stormcomp = GSComponent(stormcomponent)
					scale = (float(1)/maxsize)*size
					stormcomp.transform = ((scale, 0.0, 0.0, scale, x, y))
					thislayer.components.append(stormcomp)
				n+=1

	return stormpaths

# ----------------------------------------------------
# output controllers


def OutputStorm():

	global stormcomponent

	gridsize, minsize, maxsize = 25, 20, 60
	stormcomponent = CreateShapeComponent(font, maxsize, maxsize, "circle", "StormShape")

	for glyph in selectedGlyphs:
		
		beginGlyphNaN(glyph)
		glyph.beginUndo()

		# --- °°°°°°°

		thislayer = font.glyphs[glyph.name].layers[0]
		thislayer.beginChanges()

		# ---

		glyphsize = glyphSize(glyph)
		pathlist = doAngularizzle(thislayer.paths, 4)
		outlinedata = setGlyphCoords(pathlist)

		stormpaths = drawStorm(thislayer, outlinedata, gridsize, minsize, maxsize, stormcomponent)

		ClearPaths(thislayer)
		AddAllPathsToLayer(stormpaths, thislayer)

		# ---

		thislayer.endChanges()

		# --- °°°°°°°

		endGlyphNaN(glyph)
		glyph.endUndo()


OutputStorm()



Font.enableUpdateInterface()

