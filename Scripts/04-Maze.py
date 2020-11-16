#MenuTitle: 04. Maze
# -*- coding: utf-8 -*-
__doc__="""
04. Maze
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

def expandMonoline(Layer, noodleRadius ):
	try:
		offsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
		offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_( Layer, noodleRadius, noodleRadius, True, False, 0.5, None,None)
	except Exception as e:
		logToConsole( "expandMonoline: %s\n%s" % (str(e), traceback.format_exc()) )


# ===========================================================================


# Main Walker Function


def WalkerLoop(thislayer):

	walkerpaths = []

	while len(available_slots)>0:
		start = RandomStartPt()
		updateChecker(start[0], start[1])
		walks = Walker(thislayer, start)
		walkerpaths.extend(walks)

	return walkerpaths


def Walker(thislayer, start):

	go = True
	looklist = ["N","S","E","W"]
	startx, starty = start[0], start[1]
	walkpath = GSPath()
	
	sx, sy = startx, starty
	nx, ny = startx, starty

	startnode = GSNode([ox+(sx*unit), oy+(sy*unit)], type = GSLINE)
	walkpath.nodes.append( startnode )

	breakcounter=0
	lastdirection = ""
	nd, sd, ed, wd = False, False, False, False
	walkcontinue = True
	walkerpaths = []

	while walkcontinue==True:

		found = 0
		go = True

		direction = random.choice(looklist)
		if direction=="N": lastdirection="S"
		if direction=="S": lastdirection="N"
		if direction=="W": lastdirection="E"
		if direction=="E": lastdirection="W"

		if direction=="N" and direction!=lastdirection:
			lookx = sx
			looky = sy+1
			if isSlotFree(lookx, looky):
				updateChecker(lookx, looky)
				found=1
			else:
				go = False

		if direction=="S" and direction!=lastdirection:
			lookx = sx
			looky = sy-1
			if isSlotFree(lookx, looky):
				updateChecker(lookx, looky)
				found=1
			else:
				go = False

		if direction=="E" and direction!=lastdirection:
			lookx = sx+1
			looky = sy
			if isSlotFree(lookx, looky):
				updateChecker(lookx, looky)
				found=1
			else:
				go = False

		if direction=="W" and direction!=lastdirection:
			lookx = sx-1
			looky = sy
			if isSlotFree(lookx, looky):
				updateChecker(lookx, looky)
				found=1
			else:
				go = False

		if go==True:
			drawx, drawy = ox+(lookx*unit), oy+(looky*unit) 
			walkpath.nodes.append( GSNode([drawx, drawy], type = GSLINE) )
			sx = lookx
			sy = looky

		breakcounter+=1
		if breakcounter==1000:
			break

	if (len(walkpath.nodes))==1: walkpath.nodes.append(startnode)

	walkerpaths.append(walkpath)
	return walkerpaths



def SetAvailableSlots(thislayer, outlinedata):

	global available_slots
	global oy, ox

	for stepy in range(0, ysteps+3, 1):

		y = oy + (stepy*unit)

		for stepx in range(0, xsteps+3, 1):

			x = ox + (stepx*unit)
			shapepath = []
			nx = x+unit/2
			ny = y+unit/2
			shape = drawTriangle(nx, ny, 6, 6)
			shapepath.append(shape)

			nshape = doAngularizzle(shapepath, 10)
			nshape = setGlyphCoords(nshape)
			finalshape = nshape[0][1]
			
			if ShapeWithinOutlines(finalshape, outlinedata):
				setChecker(stepx, stepy, True)
				available_slots.append([stepx, stepy])
			else:
				setChecker(stepx, stepy, False)


def setChecker(xpos, ypos, checktype):

	global checker
	try:
		checker[ypos][xpos] = checktype
	except:
		pass

def updateChecker(xpos, ypos):

	global checker
	global available_slots

	try:
		checker[ypos][xpos] = False
	except:
		pass

	item = [xpos, ypos]
	if item in available_slots: 
		available_slots.remove(item)


def isSlotFree(xpos, ypos):

	global available_slots, checker

	free = True
	item = [xpos, ypos]

	if not item in available_slots: 
		free = False

	return free


def SetChecker(bounds):

	global xsteps, ysteps, checker, sizes, unit
	global ox, oy, ow, oh
	global available_slots

	available_slots = []
	ox = int(bounds[0])
	oy = int(bounds[1])
	ow = int(bounds[2])
	oh = int(bounds[3])

	ysteps = int ( math.floor ( oh / unit ) )
	xsteps = int ( math.floor ( ow / unit ) )
	checker = []

	for stepy in range(0, ysteps):
		xlist = []
		for stepx in range(0, xsteps):
			xlist.append(True)
		checker.append(xlist)


def RandomStartPt():
	return available_slots[ random.randrange(0, len(available_slots)) ]


def outputMaze(stepsize):

	global unit
	unit = stepsize

	for glyph in selectedGlyphs:

		glyph.beginUndo()
		beginGlyphNaN(glyph)

		# --- °°°°°°°

		thislayer = font.glyphs[glyph.name].layers[0]
		thislayer.beginChanges()

		# ---

		if ContainsPaths(thislayer):

			glyphsize = glyphSize(glyph)

			if glyphsize=="S": offset = 5
			if glyphsize=="M": offset = 10
			if glyphsize=="L": offset = 10

			offsetpaths = saveOffsetPaths(thislayer, offset, offset, removeOverlap=False)
			pathlist = doAngularizzle(offsetpaths, 4)
			outlinedata = setGlyphCoords(pathlist)

			bounds = AllPathBounds(thislayer)
			SetChecker(bounds)
			SetAvailableSlots(thislayer, outlinedata)

			ClearPaths(thislayer)

			walkpaths = WalkerLoop(thislayer)
			AddAllPathsToLayer(walkpaths, thislayer)
			
			expandMonoline(thislayer, 6)
			thislayer.removeOverlap()

		# ---

		thislayer.endChanges()

		# --- °°°°°°°

		endGlyphNaN(glyph)
		glyph.endUndo()



# =======

outputMaze(30)

# =======


endFilterNaN(font)


