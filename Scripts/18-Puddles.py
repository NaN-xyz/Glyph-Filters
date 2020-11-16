#MenuTitle: 18. Puddles
# -*- coding: utf-8 -*-
__doc__="""
18. Puddles
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
import copy

# COMMON TO ALL SCRIPTS
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


def drawToenail(p1, p2, thickness):

	p1x, p1y = p1[0], p1[1]
	p2x, p2y = p2[0], p2[1]

	dist =  distance([p1x, p1y],[p2x, p2y])
	curvedist = dist * 0.3

	midx = p1x + ( (p2x-p1x) / 2)
	midy = p1y + ( (p2y-p1y) / 2)

	a1 = atan2(p1y-p2y, p1x-p2x)
	a2 = a1 - radians(90)
	a3 = a2 - radians(20)
	a4 = a2 + radians(20)

	pushx1 = (curvedist + (thickness/2)) * cos(a2)
	pushy1 = (curvedist + (thickness/2)) * sin(a2)

	pushx2 = (curvedist - (thickness/2)) * cos(a2)
	pushy2 = (curvedist - (thickness/2)) * sin(a2)

	hlen = dist*0.15
	mlen = (dist*0.21)
	handlex1 = mlen * cos(a1)
	handley1 = mlen * sin(a1)

	handlex2 = mlen * cos(a3)
	handley2 = mlen * sin(a3)
	handlex2b = mlen * cos(a3 - radians(20))
	handley2b = mlen * sin(a3 - radians(20))

	handlex3 = mlen * cos(a4)
	handley3 = mlen * sin(a4)
	handlex3b = mlen * cos(a4 + radians(20))
	handley3b = mlen * sin(a4 + radians(20))

	handlex4 = (mlen*0.8) * cos(a1)
	handley4 = (mlen*0.8) * sin(a1)

	# draw path

	nail = GSPath()
	nail.nodes.append( GSNode( [p1x, p1y] , type=GSLINE) )

	nail.nodes.append( GSNode( [p1x+handlex2, p1y+handley2] , type=GSOFFCURVE) )
	nail.nodes.append( GSNode( [midx+pushx1+handlex1, midy+pushy1+handley1] , type=GSOFFCURVE) )
	node = GSNode( [midx+pushx1, midy+pushy1] , type=GSCURVE)
	node.toggleConnection()
	nail.nodes.append(node)

	nail.nodes.append( GSNode( [midx+pushx1-handlex1, midy+pushy1-handley1] , type=GSOFFCURVE) )
	nail.nodes.append( GSNode( [p2x+handlex3, p2y+handley3] , type=GSOFFCURVE) )
	nail.nodes.append( GSNode( [p2x, p2y] , type=GSCURVE) )

	nail.nodes.append( GSNode( [p2x+handlex3b, p2y+handley3b] , type=GSOFFCURVE) )
	nail.nodes.append( GSNode( [midx+pushx2-handlex4, midy+pushy2-handley4] , type=GSOFFCURVE) )
	node = GSNode( [midx+pushx2, midy+pushy2] , type=GSCURVE) 
	node.toggleConnection()
	nail.nodes.append(node)

	nail.nodes.append( GSNode( [midx+pushx2+handlex4, midy+pushy2+handley4] , type=GSOFFCURVE) )
	nail.nodes.append( GSNode( [p1x+handlex2b, p1y+handley2b] , type=GSOFFCURVE) )
	nail.nodes.append( GSNode( [p1x, p1y] , type=GSCURVE) )

	nail.closed = True

	return nail


def Toenail(thislayer, outlinedata, min_nail, max_nail, gap, thickness):

	for path in outlinedata:

		direction = path[0]
		structure = path[1]

		if len(structure)!=0:

			structure = ChangeNodeStart(copy.copy(structure))
			nodelen = len(structure)
			n = 0

			while n < nodelen:

				x1 = structure[n][0]
				y1 = structure[n][1]

				step = random.randrange(min_nail, max_nail)

				if n+step >= nodelen-1:
					x2 = structure[0][0]
					y2 = structure[0][1]
					n = nodelen
				else:
					if n<nodelen-1:
						x2 = structure[n+step][0]
						y2 = structure[n+step][1]
						n += step + gap               # <------------------------------------------- !!!
					else:
						x2 = structure[0][0]
						y2 = structure[0][1]

				variance = random.randrange(0,10)
				toenail = drawToenail([x2, y2], [x1, y1], thickness)
				thislayer.paths.append(toenail)




def OutputToenail():

	for glyph in selectedGlyphs:

		glyph.beginUndo()
		beginGlyphNaN(glyph)

		# --- °°°°°°°

		thislayer = font.glyphs[glyph.name].layers[0]
		thislayer.beginChanges()

		# ---

		glyphsize = glyphSize(glyph)

		# add variations for glyph size here

		pathlist = doAngularizzle(thislayer.paths, 4)
		outlinedata2 = setGlyphCoords(pathlist)

		offsetpaths = saveOffsetPaths(thislayer, -40, -40, removeOverlap=False)
		pathlist = doAngularizzle(offsetpaths, 4)
		outlinedata = setGlyphCoords(pathlist)

		offsetpaths = saveOffsetPaths(thislayer, 20, 20, removeOverlap=True)
		pathlist = doAngularizzle(offsetpaths, 4)
		outlinedata3 = setGlyphCoords(pathlist)

		offsetpaths = saveOffsetPaths(thislayer, 60, 60, removeOverlap=True)
		pathlist = doAngularizzle(offsetpaths, 4)
		outlinedata4 = setGlyphCoords(pathlist)

		ClearPaths(thislayer) 


		Toenail(thislayer, outlinedata, 30, 50, gap=4, thickness=25)
		Toenail(thislayer, outlinedata3, 40, 60, gap=100, thickness=20)
		Toenail(thislayer, outlinedata4, 50, 70, gap=100, thickness=10)

		thislayer.removeOverlap()

		# ---

		thislayer.endChanges()

		# --- °°°°°°°

		endGlyphNaN(glyph)
		glyph.endUndo()

# =======

OutputToenail()

# =======

endFilterNaN(font)

