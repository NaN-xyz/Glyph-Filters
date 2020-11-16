#MenuTitle: 19. Spray Paint
# -*- coding: utf-8 -*-
__doc__="""
19. Spray Paint
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFNoise import *
from noise import *

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
	currentglyph = Layer.parent
	templayer = Layer.copy()
	templayer.name = "tempoutline"
	currentglyph.layers.append(templayer)
	tmplayer_id = templayer.layerId
	doOffset(templayer, hoffset, voffset)
	if removeOverlap==True: templayer.removeOverlap()
	offsetpaths = templayer.paths
	del currentglyph.layers[tmplayer_id]
	return offsetpaths

# ================================================



# THE MAIN SPRAY PAINT ACTION

def Spray(thislayer, paths):

	for path in paths:

		glyph = thislayer.parent
		direction = path.direction

		# only round shape if over certain size (for small forms)
		if isPathSizeBelowThreshold(path,120,120):
			structure = path
		else:
			structure = RoundPath(path,"nodes")
			structure = convertToFitpath(structure, True)
		
		pathlist = doAngularizzle([structure], 7)
		outlinedata = setGlyphCoords(pathlist)

		if outlinedata:

			structure = outlinedata[0][1]
			outlinedata = setGlyphCoords(pathlist)
			structure = outlinedata[0][1]

			nodelen = len(structure)

			n = 0
			newpath = []

			noisescale = 0.01
			seed = random.randrange(0,100000)
			minshift, maxshift = 30, 90
			nstep = 0

			start_pushdist = 0
			last_pushdist = 0
			segwaylen = 40

			while n < nodelen:

				if n>0:
					prev=n-1
				else:
					prev=nodelen-1

				if n==nodelen-1:
					next=0
				else:
					next=n+1

				x_prev = structure[prev][0]
				y_prev = structure[prev][1]

				x_curr = structure[n][0]
				y_curr = structure[n][1]

				x_next = structure[next][0]
				y_next = structure[next][1]

				a1 = atan2(y_prev-y_next, x_prev-x_next)
				a2 = a1+radians(90)

				if n < nodelen-segwaylen:
					pushdist = pnoise1( (n+seed)*noisescale, 3) 
					pushdist = noiseMap( pushdist, minshift, maxshift )
					last_pushdist = pushdist

				else:
					pushdist = last_pushdist + ( ( start_pushdist-last_pushdist ) / segwaylen ) * (segwaylen-(nodelen-n)) 

				if n==0:
					start_pushdist = pushdist

				linex1 = pushdist * cos(a2)
				liney1 = pushdist * sin(a2)

				spikewidth = 4 

				linex2 = spikewidth * cos(a1)
				liney2 = spikewidth * sin(a1)

				newpath.extend( [
								[x_curr-linex2, y_curr-liney2], 
								[x_curr+linex2, y_curr+liney2],
								[x_curr+linex1, y_curr+liney1]]
								)
				n+=1

			np = drawSimplePath(newpath)
			thislayer.paths.append(np)



def OutputSpray():

	for glyph in selectedGlyphs:

		glyph.beginUndo()
		beginGlyphNaN(glyph)

		# --- °°°°°°°

		thislayer = font.glyphs[glyph.name].layers[0]
		thislayer.beginChanges()

		# ---

		glyphsize = glyphSize(glyph)
		
		if glyphsize=="S": offset = -5
		if glyphsize=="M": offset = -10
		if glyphsize=="L": offset = -20

		offsetpaths = saveOffsetPaths(thislayer, offset, offset, removeOverlap=False)
		pathlist = doAngularizzle(offsetpaths, 4)
		outlinedata = setGlyphCoords(pathlist)

		ClearPaths(thislayer)

		Spray(thislayer, pathlist)


		# ---

		thislayer.endChanges()

		# --- °°°°°°°

		endGlyphNaN(glyph)
		glyph.endUndo()


# =======

#cProfile.run("OutputSpray()")
OutputSpray()

# =======

#OutputFur()
#OutputSpikes()

endFilterNaN(font)







