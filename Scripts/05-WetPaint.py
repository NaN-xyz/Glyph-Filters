#MenuTitle: 05. WetPaint
# -*- coding: utf-8 -*-
__doc__="""
05. WetPaint
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


def Drip(thislayer, outlinedata, maxdrip):

	# find drippable segments within path and store indices

	minsize = 0
	maxsize = maxdrip
	indices = []
	pathcount = 0
	degvariance = 40

	for path in outlinedata:

		direction = path[0]
		structure = path[1]
		nodelen = len(structure)
		index = []
		n=0
		index_start = -999
		index_end = -999

		# collect all possible drippable segments within certain angle

		while n < nodelen-1:

			x1 = structure[n][0]
			y1 = structure[n][1]
			x2 = structure[n+1][0]
			y2 = structure[n+1][1]
			a = atan2(y1-y2, x1-x2)
			deg = degrees(a)

			if abs(deg)>(180-degvariance) and abs(deg)<(180+degvariance):
				if index_start == -999:
					index_start = n
				else:
					index_end = n
			else:
				if index_start != -999:
					index.append( [ index_start, index_end ] )
				index_start = -999
			n+=1

		indices.append([ pathcount, index ])
		pathcount+=1

	

	# run through each drippable segment and do something


	for p in range(0, len(outlinedata)):

		direction = outlinedata[p][0]
		structure = outlinedata[p][1]
		nodelen = len(structure)
		n=0
		segs = indices[p][1]

		for seg in segs:

			index_start = seg[0]
			index_end = seg[1]

			seedx = random.randrange(0,100000)
			seedy = random.randrange(0,100000)
			noisescale = 0.01

			steps = float(index_end - index_start)
			steppos = 0

			for n in range(index_start, index_end):

				angle = 180/steps * steppos
				t = math.sin(math.radians(angle))
				adjust = 1

				x = structure[n][0]
				y = structure[n][1]

				if n < index_end:

					x2 = structure[n+1][0]
					y2 = structure[n+1][1]

					searchblack = DistanceToNextBlack(thislayer, [x, y], [x2, y2], outlinedata, searchlimit=200)
					#print searchblack

					if searchblack is not None:
						if searchblack < 200:
							adjust = 0.2

				# insert distance to next black checker here

				noiz = pnoise1( (n+seedx)*noisescale, 4) 
				size = noiseMap( noiz, minsize, maxsize )
				if direction=="False": size*=0.2
				size = t * abs(size) * adjust

				structure[n][1] = y - size

				steppos+=1


	# draw updated outline

	for path in outlinedata:

		#p = drawSimplePath(path[1])
		p = convertToFitpath(path[1], True)

		thislayer.paths.append(p)

# ----------------------------------------------------
# output controllers


def OutputDrip():

	for glyph in selectedGlyphs:
		
		beginGlyphNaN(glyph)
		glyph.beginUndo()

		# --- °°°°°°°

		thislayer = font.glyphs[glyph.name].layers[0]
		thislayer.beginChanges()

		# ---

		glyphsize = glyphSize(glyph)
		if glyphsize=="S": maxdrip, it = 150, 1
		if glyphsize=="M": maxdrip, it = 350, 2
		if glyphsize=="L": maxdrip, it = 400, 2

		for n in range(0, it):
			pathlist = doAngularizzle(thislayer.paths, 4) # small seg size = quicker
			outlinedata = setGlyphCoords(pathlist)
			Drip(thislayer, outlinedata, maxdrip)

		thislayer.removeOverlap()

		# ---

		thislayer.endChanges()

		# --- °°°°°°°

		endGlyphNaN(glyph)
		glyph.endUndo()


OutputDrip()



Font.enableUpdateInterface()

