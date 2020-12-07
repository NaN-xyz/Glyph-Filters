from GlyphsApp import *

from math import *
import random
import copy
import numpy as np
import matplotlib.path as mpltPath
from Foundation import NSMakePoint

from NaNGFConfig import *
from NaNGFAngularizzle import *
from NaNGFFitpath import *


# --------------------------------------------

def ClearPaths(thislayer):
	"""Removes all paths in a layer, leaving anchors and components in place"""
	thislayer.paths = []

def ShiftPath(path, variance, type):
	"""Shifts a path by a random amount in x, y or both directions."""
	shiftx = random.uniform(variance * -0.5, variance)
	shifty = random.uniform(variance * -0.5, variance)

	if type=="x":
		path.applyTransform((
								1, # x scale factor
								0, # x skew factor
								0, # y skew factor
								1, # y scale factor
								shiftx, # x position
								0  # y position
								))

	if type=="y":
		path.applyTransform((
								1, # x scale factor
								0, # x skew factor
								0, # y skew factor
								1, # y scale factor
								0, # x position
								shifty  # y position
								))

	if type=="xy":
		path.applyTransform((
								1, # x scale factor
								0, # x skew factor
								0, # y skew factor
								1, # y scale factor
								shiftx, # x position
								shifty  # y position
								))


def ChangeNodeStart(nodes):
	"""Cycles a node list so it starts at a random position."""
	cutpt = random.randrange(0, len(nodes))
	start = nodes[cutpt:]
	start.extend(nodes[0:cutpt])
	return start


def withinGlyphBlack(x, y, glyph):

	#if len(glyph)==0 : print "EMPTY GLYPH"

	paths_pos, paths_neg = [], []
	for p in glyph:
		direction = p[0]
		if direction == Direction.ANTICLOCKWISE: paths_pos.append(p)
		else: paths_neg.append(p)

	inside_pos, inside_neg = False, False

	for pospath in paths_pos:
		if (point_inside_polygon(x,y,pospath[1])): 
			inside_pos=True
			break

	if inside_pos==True:
		for negpath in paths_neg:
			if (point_inside_polygon(x,y,negpath[1])): 
				inside_neg=True
				break

	if inside_pos==True and inside_neg==False:
		return True # within glyph black
	else:
		return False # not

def withinLayerBlack(layer, x, y):
	if not layer.bounds:
		return
	definitelyOutside = NSMakePoint(layer.bounds.origin.x-1,y)
	pt = NSMakePoint(x,y)
	intersections = layer.calculateIntersectionsStartPoint_endPoint_decompose_(definitelyOutside, pt, True)
	return (len(intersections) % 2) == 1

def operateOnBlackAtInterval(layer, func, step_x, step_y=None):
	if step_y is None:
		step_y = step_x
	b = AllPathBounds(layer)
	ox, oy, w, h = int(b[0])+1, b[1]+1, b[2], b[3]
	results = []
	for y in range(oy, oy+h, step_y):
		for x in range(ox, ox+w, step_x):
			if not withinLayerBlack(layer, x, y):
				continue
			result = func(x,y,layer)
			if result is not None:
				results.extend(result)

	return results

def point_inside_polygon_faster(x,y,poly):

	inside = False

	path = mpltPath.Path(poly)
	numparray = np.array([[x,y]])
	#print numparray
	inside2 = path.contains_points(numparray)

	if inside2.all()==True: inside=True
	return inside


def point_inside_polygon(x,y,poly):

	n = len(poly)
	inside = False

	try:

		p1x,p1y = poly[0]
		for i in range(n+1):
			p2x,p2y = poly[i % n]
			if y > min(p1y,p2y):
				if y <= max(p1y,p2y):
					if x <= max(p1x,p2x):
						if p1y != p2y:
							xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
						if p1x == p2x or x <= xinters:
							inside = not inside
			p1x,p1y = p2x,p2y

		return inside

	except:

		return inside


def MakeVector(length, angle):
	return length * cos(angle), length * sin(angle)

def SumVectors(*args):
	return [
		sum([x[0] for x in args]),
		sum([x[1] for x in args])
	]

def NegateVector(pt):
	return [-pt[0], -pt[1]]

def LerpPoints(v1, v2, t):
	return [
	 	v1[0] * (1-t) + v2[0] * t,
	 	v1[1] * (1-t) + v2[1] * t
	]

def Midpoint(v1, v2):
	return LerpPoints(v1,v2,0.5)

def AllPathBoundsFromPathList(paths):
	templayer = GSLayer()
	AddAllPathsToLayer(paths, templayer)
	bounds = AllPathBounds(templayer)
	del templayer
	return bounds


def AllPathBounds(thislayer):

	x = int( thislayer.bounds.origin.x )
	y = int( thislayer.bounds.origin.y )
	w = int( thislayer.bounds.size.width )
	h = int( thislayer.bounds.size.height )

	if x==0 and y==0 and w==0 and h==0:
		return None
	else: 
		return [x,y,w,h]


#
#   SHAPES
#

def RoundPaths(paths, returntype):
	newpaths = []
	for p in paths:
		newpaths.append ( RoundPath( p, returntype ) )
	return newpaths

def RoundPath(path, returntype):

	outlinedata = getGlyphCoords(doAngularizzle([path], 2))[0][1]
	new_outline = outline
	nl = []

	switch = False

	for loop in range(0,12): # must be even number to maintain original shape

		nlen = len(new_outline)
		nl = []
		n = 0

		while n < nlen:

			if n==nlen-1:
				next = 0
			else:
				next = n+1

			node_next = new_outline[next]
			nl.append([node_next[0], node_next[1]])

			if switch==True:
				n+=4
			else:
				n+=8

		if switch==True:
			segmentsize=20
			switch = not switch
		else:
			segmentsize=3

		outlinedata = getGlyphCoords(doAngularizzle([drawSimplePath(nl)], segmentsize))

		try:
			new_outline = outlinedata[0][1]
		except:
			break

	if returntype=="nodes":
		return new_outline
	else:
		return path


def returnRoundedPaths(paths):

	roundedpathlist = []
	for p in paths:
		roundedpath = RoundPath(p, "nodes")
		roundedpath = convertToFitpath(roundedpath, True)
		roundedpathlist.append(roundedpath)
	return roundedpathlist


def clip(val, minimum, maximum):
	return min(max(val, minimum), maximum)

def convertToFitpath(nodelist, closed):

	addon = GSPath()

	# seems to be instances where empty nodelists are sent. 
	# workaround below with try/except sending empty path

	try:

		nodelist.append(nodelist[-1])
		pathlist = fitpath(nodelist, True)

		for segment in pathlist:
			pt = segment.getPoint()
			hin = segment.getHandleIn()
			hout = segment.getHandleOut()
			ptx, pty = pt.x, pt.y
			hinx, hiny = hin.x, hin.y
			houtx, houty = hout.x, hout.y

			# try and limit handle within max range (re fitpath bug)
			hinx = clip(hinx, -30, 30)
			hiny = clip(hiny, -30, 30)
			houtx = clip(houtx, -30, 30)
			houty = clip(houty, -30, 30)

			if s==0:
				addon.nodes.append(GSNode([ptx, pty], type = GSLINE))
				addon.nodes.append(GSNode([ptx+houtx, pty+houty], type = GSOFFCURVE))
			elif s>0 and s<len(pathlist)-1:
				addon.nodes.append(GSNode([ptx+hinx, pty+hiny], type = GSOFFCURVE))
				addon.nodes.append(GSNode([ptx, pty], type = GSCURVE))
				addon.nodes.append(GSNode([ptx+houtx, pty+houty], type = GSOFFCURVE))
			else:
				addon.nodes.append(GSNode([ptx+hinx, pty+hiny], type = GSOFFCURVE))
				addon.nodes.append(GSNode([ptx, pty], type = GSCURVE))
		
	except Exception as e:
		print("convertToFitpath failed", e)

	addon.closed = closed
	return addon


def drawBlob(nx, ny, maxrad, maxpoints, rounded):

	#print nx, ny, maxrad, maxpoints
	addon = GSPath()
	sides = 360 / maxpoints
	points = []

	rotation = random.randrange(0,90)

	for n in range(0, maxpoints):

		a = sides * n + rotation
		rad = math.radians(a)
		pushpointlen = random.randrange( int(maxrad*0.5), maxrad) / 2
		cx, cy = MakeVector(pushpointlen, rad)
		points.append([nx+cx, ny+cy])


	for n in range(0, len(points)):
		thisPt = points[n]
		nextPt = points[(n+1) % len(points)]
		cx1, cy1 = thisPt
		cx2, cy2 = nextPt

		pushdist = distance(thisPt, nextPt) / 2

		a1 = math.atan2(ny-cy2, nx-cx2) + math.radians(90)
		a2 = math.atan2(ny-cy1, nx-cx1) + math.radians(90)
		linex1, liney1 = MakeVector(pushdist, a1)
		linex2, liney2 = MakeVector(pushdist, a2)

		if rounded==True:
			addon.nodes.append(GSNode([cx1-linex2, cy1-liney2], type = GSOFFCURVE))
			addon.nodes.append(GSNode([cx2+linex1, cy2+liney1], type = GSOFFCURVE))
			addon.nodes.append(GSNode(nextPt, type = GSCURVE))
		else:
			addon.nodes.append(GSNode(nextPt, type = GSLINE))

	addon.closed = True
	#thislayer.paths.append(addon)
	return addon


def drawSidedPolygon(nx, ny, maxlen, maxpoints):

	#print nx, ny, maxlen, maxpoints
	addon = GSPath()

	sides = 360 / maxpoints

	for n in range(0, maxpoints):

		a = sides * n + 90
		cx, cy = MakeVector(maxlen/2, math.radians(a))

		newnode = GSNode()
		newnode.type = GSLINE
		newnode.position = ( nx + cx, ny + cy)
		addon.nodes.append( newnode )

	addon.closed = True
	#thislayer.paths.append(addon)
	return addon


def drawSpeck(nx, ny, maxrad, maxpoints):

	#print nx, ny, maxrad, maxpoints
	addon = GSPath()

	sides = 360 / maxpoints
	rotation = random.randrange(0,360)

	mr = random.randrange(0, maxrad)

	points = random.randrange(3, maxpoints)

	for n in range(0, points):

		a = sides * n + rotation
		rad = math.radians(a)
		cx = nx + (maxrad/2) * cos(rad)
		cy = ny + (maxrad/2) * sin(rad)

		newnode = GSNode()
		newnode.type = GSLINE
		newnode.position = ( cx, cy)
		addon.nodes.append( newnode )

	addon.closed = True
	#thislayer.paths.append(addon)
	return addon


def drawCircle(nx, ny, w, h):

	#thislayer = f.selectedLayers[0]
	#coord = [ [nx-(w/2),ny], [nx,ny+(h/2)], [nx+(w/2),ny], [nx,ny-(w/2)] ]
	addon = GSPath()

	addon.nodes.append(GSNode([nx-(w/2),ny], type = GSCURVE))
	addon.nodes.append(GSNode([nx-(w/2),ny+(h/4)], type = GSOFFCURVE))

	addon.nodes.append(GSNode([nx-(w/4),ny+(h/2)], type = GSOFFCURVE))
	addon.nodes.append(GSNode([nx,ny+(h/2)], type = GSCURVE))
	addon.nodes.append(GSNode([nx+(w/4),ny+(h/2)], type = GSOFFCURVE))

	addon.nodes.append(GSNode([nx+(w/2),ny+(h/4)], type = GSOFFCURVE))
	addon.nodes.append(GSNode([nx+(w/2),ny], type = GSCURVE))
	addon.nodes.append(GSNode([nx+(w/2),ny-(h/4)], type = GSOFFCURVE))

	addon.nodes.append(GSNode([nx+(w/4),ny-(h/2)], type = GSOFFCURVE))
	addon.nodes.append(GSNode([nx,ny-(h/2)], type = GSCURVE))
	addon.nodes.append(GSNode([nx-(w/4),ny-(h/2)], type = GSOFFCURVE))

	addon.nodes.append(GSNode([nx-(w/2),ny-(h/4)], type = GSOFFCURVE))
	#addon.nodes.append(GSNode([nx-(w/2),ny], type = GSCURVE))

	addon.closed = True
	if addon.direction==1: addon.reverse()

	return addon


def drawDiamond(nx, ny, w, h):
	return drawSimplePath([
		(nx-(w/2),ny),
		(nx,ny+(h/2)),
		(nx+(w/2),ny),
		(nx,ny-(w/2))
	], correctDirection=True)

def drawRectangle(nx, ny, w, h):
	return drawSimplePath([
		(nx-(w/2),ny-(h/2)),
		(nx-(w/2),ny+(h/2)),
		(nx+(w/2),ny+(h/2)),
		(nx+(w/2),ny-(h/2))
	], correctDirection=True)

def drawTriangle(nx, ny, w, h):
	return drawSimplePath([
		[nx-(w/2),ny-(h/2)],
		[nx+(w/2),ny-(h/2)],
		[nx,ny+(h/2)]
	], correctDirection=True)

def drawSimplePath(nodes, correctDirection=False, closed=True):

	addon = GSPath()
	for xy in nodes:
		newnode = GSNode()
		newnode.type = GSLINE
		newnode.position = (xy[0], xy[1])
		addon.nodes.append( newnode )
	addon.closed = closed
	#thislayer.paths.append(addon)
	if correctDirection and addon.direction==1: addon.reverse()

	return addon



# def Fill_Halftone(thislayer, maskshape, shapetype):

# 	allshapes = []

# 	t = shape
# 	shapelist = PathToNodeList(t)

# 	x = int (t.bounds.origin.x)
# 	y = int (t.bounds.origin.y)
# 	w = int (t.bounds.size.width)
# 	h = int (t.bounds.size.height)

# 	grid = 13
# 	#size = random.randrange(12, 24)
# 	size = 8

# 	for row in range(y, y+h, grid):

# 		for col in range(x, x+w, grid):

# 			if point_inside_polygon(col, row, shapelist):

# 				nx = math.floor(col/grid) * grid
# 				ny = math.floor(row/grid) * grid

# 				if row%2==0:
# 					adjust = grid/2
# 				else:
# 					adjust = 0

# 				c = drawCircle(nx+adjust, ny, size, size)
# 				#thislayer.paths.append(c)
# 				allshapes.append(c)

# 		size+=0.1

# 	return allshapes


def Fill_Drawlines(thislayer, path, direction, gap, linecomponents):

	#print "fill lines", thislayer, path, bounds, direction

	bounds = path.bounds
	line_vertical_comp, line_horizontal_comp = linecomponents[0], linecomponents[1]

	x = int( bounds.origin.x )
	y = int( bounds.origin.y )
	w = int( bounds.size.width )
	h = int( bounds.size.height )

	pathlist = doAngularizzle([path], 10)
	outlinedata = getGlyphCoords(pathlist)
	outlinedata = outlinedata[0][1]
	
	tilecoords = [[x,y], [x,y+h], [x+w,y+h], [x+w,y]]
	lines = []

	checkgap = 2

	xstart, ystart = None, None
	xend, yend = None, None

	if direction=="horizontal":
		for y2 in range(y, y+h+gap, gap):
			newline = []
			for x2 in range(x, x+w, checkgap):
				if point_inside_polygon(x2, y2, outlinedata):
					if xstart==None and ystart==None:
						xstart = x2
						ystart = y2
					else:
						xend = x2
						yend = y2
				else:
					if xstart!=None and xend!=None:
						newline = [[xstart, ystart],[xend, yend]]
						lines.append( newline )
						xstart, ystart = None, None
						xend, yend = None, None
			y2 = 0

	if direction=="vertical":
		for x2 in range(x, x+w+gap, gap):
			newline = []
			for y2 in range(y, y+h, checkgap):
				if point_inside_polygon(x2, y2, outlinedata):
					if xstart==None and ystart==None:
						xstart = x2
						ystart = y2
					else:
						xend = x2
						yend = y2
				else:
					if xstart!=None and xend!=None:
						newline = [[xstart, ystart],[xend, yend]]
						lines.append( newline )
						xstart, ystart = None, None
						xend, yend = None, None
			x2 = 0

	linecomponents = []

	for l in lines:
		sx, sy = l[0][0], l[0][1]
		ex, ey = l[-1][0], l[-1][1]
		comp = returnLineComponent([sx,sy], [ex,ey], direction, [line_vertical_comp,line_horizontal_comp], 100)
		linecomponents.append(comp)

	return linecomponents


def FillHalftoneShape(thislayer, maskshape, shapetype):

	allshapes = []

	t = maskshape
	shapelist = PathToNodeList(t)
	x = int (t.bounds.origin.x)
	y = int (t.bounds.origin.y)
	w = int (t.bounds.size.width)
	h = int (t.bounds.size.height)

	grid = 13
	size = random.randrange(12, 24)

	for col in range(x, x+w, grid):

		for row in range(y, y+h, grid):

			if point_inside_polygon(col, row, shapelist):

				nx = math.floor(col/grid) * grid
				ny = math.floor(row/grid) * grid

				if shapetype=="triangle":
					c = drawTriangle(nx, ny, size, size)
				if shapetype=="circle":
					c = drawCircle(nx, ny, size, size)

				#thislayer.paths.append(c)
				allshapes.append(c)

		size+=0.3

	return allshapes





# MUST CHANGE NAME


def Split(rectangle, axis):

	splitrectangles = []
	rect = rectangle
	rectx = rect[0]
	recty = rect[1]
	rectw = rect[2]
	recth = rect[3]
	percentage = 0.5

	if (axis=="x"):
		minh = int(recth*percentage)
		rh1 = random.randrange(minh, recth+1) # was previous randrange
		splitrectangles.append( [ rectx, recty, rectw, rh1 ] )
		splitrectangles.append( [ rectx, recty+rh1, rectw, recth-rh1 ] )
	if (axis=="y"):
		minw = int(rectw*percentage)
		rw1 = random.randrange(minw, rectw+1)
		splitrectangles.append( [ rectx, recty, rw1, recth ] )
		splitrectangles.append( [ rectx+rw1, recty, rectw-rw1, recth ] )

	return splitrectangles


def MakeRectangles(startrect, it):
	if it==0:
		return startrect

	collections = []

	rectangles = startrect
	counter=0
	axis="y"

	while counter<it:

		collection = []

		for n in range(0, len(rectangles)):
			if axis=="y": axis = "x"
			else: axis = "y"
			collection.extend(Split( rectangles[n], axis ))

		rectangles = collection
		collections.append(collection)
		counter+=1

	return collections[-1]


# def drawAllRectangles(allrectangles, thislayer):

# 	#print "number of allrectangles", len(allrectangles) 

# 	for n in range(0, len(allrectangles)):

# 		rect = allrectangles[n]
# 		rectx = rect[0]
# 		recty = rect[1]
# 		rectw = rect[2]
# 		recth = rect[3]

# 		drawRectangle( rectx, recty, rectw, recth, thislayer )


def returnRandomNodeinPaths(outlinedata):

	glyph = outlinedata

	allnodes = []

	for p in range(0, len(glyph)):
		path = glyph[p][1]
		for n in range(0, len(path)):
			allnodes.append(path[n])

	node = allnodes [ random.randrange(0, len(allnodes)) ]

	return node


def defineStartXY(thislayer, outlinedata):
	#ox, oy, ow, oh = p.bounds.origin.x, p.bounds.origin.y, p.bounds.size.width, p.bounds.size.height
 
	b = AllPathBounds(thislayer)
	ox, oy, w, h = b[0], b[1], b[2], b[3]
 
	inside = False
	breakcounter = 0
	while breakcounter<200: 
		rx = random.randrange(ox, ox+w)
		ry = random.randrange(oy, oy+h)
		if withinGlyphBlack(rx, ry, outlinedata):
			return [rx, ry]
		breakcounter+=1

	# #node = returnRandomNodeinPaths(glyph)

	# inside = False

	# #thislayer = f.selectedLayers[0]
	# #width = thislayer.width
	# #height = thislayer.height

	# originx = rect[0]
	# originy = rect[1]
	# ow = rect[2]
	# oh = rect[3]
	# newrect = [ [originx, originy], [originx, originy+oh], [originx+ow, originy+oh], [originx+ow, originy]  ]
 	
	# #print "define start xy"
	# #print path_origin_x, path_origin_x, path_size_width
 
	# counter=0
	# while inside==False:
 
	# 	rx = random.randrange(int(originx), int(originx + ow))
	# 	ry = random.randrange(int(originy), int(originy + oh))
 
	# 	# rx = node[0]
	# 	# ry = node[1]
 
	# 	#inside1 = point_inside_polygon(rx, ry, glyph)
	# 	inside1 = withinGlyphBlack(rx, ry, glyph)					#checks not in glyph negative counters
	# 	inside2 = point_inside_polygon(rx, ry, newrect)		#basic point in path check
 
	# 	if inside1 and inside2:
	# 		inside=True
 		
	# 	if counter==20:
	# 		#print "----"
	# 		#print "could not find startXY"
	# 		#print "----"
	# 		return
	# 		break
 
	# 	counter+=1
 
	# return[rx, ry]
 

def ShapeWithinOutlines(shape, glyph):
	within = True
	for node in shape:
		nx = node[0]
		ny = node[1]
		if withinGlyphBlack(nx, ny, glyph)==False:
			within=False
			break
	return within


def DistanceToNextBlack(thislayer, p1, p2, outlinedata, searchlimit):

	x1, x2 = p1[0], p2[0]
	y1, y2 = p1[1], p2[1]

	midx = x1 + ((x2-x1)/2)
	midy = y1 + ((y2-y1)/2)

	a = atan2(y1-y2, x1-x2)
	a += radians(90)

	pushdist = 10

	stepx = pushdist * cos(a)
	stepy = pushdist * sin(a)

	newx = midx
	newy = midy

	for step in range(0, int(searchlimit/pushdist)):
		newx += stepx
		newy += stepy
		if withinGlyphBlack(newx, newy, outlinedata):
			#return distance([midx, midy], [newx, newy])
			return distance([midx, midy], [newx, newy])
			break

	return None


def isPathSizeBelowThreshold(path, maxw, maxh):
	bounds = path.bounds
	if bounds.size.width<maxw and bounds.size.height<maxh:
		return True
	else:
		return False


def isLayerSizeBelowThreshold(thislayer, maxw, maxh):
	bounds = thislayer.bounds
	if bounds.size.width<maxw and bounds.size.height<maxh:
		return True
	else:
		return False


def AddAllComponentsToLayer(components, thislayer):
	try:
			thislayer.components.extend(components)
	except:
		print("Couldn't add components to layer", thislayer)


def AddAllPathsToLayer(paths, thislayer):
	try:
			thislayer.paths.extend(paths)
	except:
		print("Couldn't add all paths to layer", thislayer)


def ConvertPathlistDirection(paths, direction):
	try:
		newpaths = []
		for p in paths:
			if p.direction != direction:
				p.reverse()
			newpaths.append(p)
		return newpaths
	except:
		print("Couldn't change direction of all paths")


def ContainsPaths(thislayer):
	if len(thislayer.paths)>0:
		return True
	else:
		return False


def pathCenterPoint(path):
	bounds = path.bounds
	x = bounds.origin.x
	y = bounds.origin.y
	w = bounds.size.width
	h = bounds.size.height
	return [x+(w/2),y+(h/2)]


def CreateShapeComponent(font, sizex, sizey, shapetype, shapename):

	if font.glyphs[shapename]: del font.glyphs[shapename]
	ng = GSGlyph()
	ng.name = shapename
	ng.category = "Mark"
	ng.export = True
	font.glyphs.append(ng)
	layer = font.glyphs[ng.name].layers[0]
	layer.width = 0

	# add speck, blob, perhaps even a line?
	if shapetype=="circle":
		shape = drawCircle(0, 0, sizex, sizey)
	elif shapetype=="diamond":
		shape = drawDiamond(0, 0, sizex, sizey)
	elif shapetype=="rectangle":
		shape = drawRectangle(0, 0, sizex, sizey)
	elif shapetype=="triangle":
		shape = drawTriangle(0, 0, sizex, sizey)
	else: 
		shape = drawDiamond(0, 0, sizex, sizey)

	layer.paths.append(shape)
	return ng


def CreateAllShapeComponents(font, sizex, sizey):
	return [
		CreateShapeComponent(font, sizex, sizey, shape, shape[0].upper()+shape[1:]+"Shape") for shape in ["circle", "diamond", "rectangle", "triangle"]
	]


def CreateLineComponent(font, direction, size, shapename):

	if font.glyphs[shapename]: del font.glyphs[shapename]
	ng = GSGlyph()
	ng.name = shapename
	ng.category = "Mark"
	ng.export = True
	font.glyphs.append(ng)
	layer = font.glyphs[ng.name].layers[0]
	layer.width = 0

	#line = GSPath()
	if direction=="vertical": line = drawRectangle(0,50,size,100)
	if direction=="horizontal": line = drawRectangle(50,0,100,size)

	layer.paths.append(line)

	return ng


def returnLineComponent(p1, p2, direction, component_glyphs_vh, source_component_len):

	sx, sy = p1[0], p1[1]
	ex, ey = p2[0], p2[1]
	dist = distance([sx,sy],[ex,ey])

	linev = component_glyphs_vh[0]
	lineh = component_glyphs_vh[1]

	if direction=="vertical": 
		comp = GSComponent(linev)
		scaley = (float(1)/source_component_len)*dist
		scalex = 1
	else: 
		comp = GSComponent(lineh)
		scaley = 1
		scalex = (float(1)/source_component_len)*dist

	comp.transform = ((scalex, 0.0, 0.0, scaley, sx, sy))
	return comp


# shadow functions

def DoShadow(thislayer, outlinedata, shadangle, depth, shadowtype):

    shadowpaths = []

    for direction, structure in outlinedata:

        nodelen = len(structure)
        stepnum = depth
        n = 0
        lines, line1, line2 = [], [], []

        while n < nodelen+1:

            if n==nodelen: thisnode=0
            else: thisnode=n

            x1 = structure[thisnode][0]
            y1 = structure[thisnode][1]

            rad = math.radians(shadangle)
            x2 = x1 + depth * math.cos(rad)
            y2 = y1 + depth * math.sin(rad)

            xtest = x1 + 1 * math.cos(rad)
            ytest = y1 + 1 * math.sin(rad)

            if not withinGlyphBlack(xtest, ytest, outlinedata):
                # search for length of line within max
                stepsize_x = (x2-x1) / stepnum
                stepsize_y = (y2-y1) / stepnum
                newx, newy = x1, y1
                step = 0
                while step < stepnum+1:
                    newx += stepsize_x
                    newy += stepsize_y
                    if withinGlyphBlack(newx, newy, outlinedata):
                        break
                    step+=1
                line1.append([x1, y1])
                line2.append([newx, newy])
            else:
                if len(line1)>2 and len(line2)>2:
                    lines.append([line1, line2])
                    line1, line2 = [], []
            n+=1

        if len(line1)>2 and len(line2)>2:
            lines.append([line1, line2])
            line1, line2 = [], []

        if shadowtype=="paths":
            shadowpaths.extend( CreateShadowPaths(thislayer, lines) )
        if shadowtype=="lines":
            shadowpaths.extend( CreateShadowLines(thislayer, lines, depth) )

    return shadowpaths


def CreateShadowLines(thislayer, lines, depth):

    newlines = roughenLines(lines, depth)
    newpaths = []
    for line in newlines:
        nl = []
        for node in line:
            x = node[0]
            y = node[1]
            nl.append([x,y])
        p = drawSimplePath(nl, False, False)
        newpaths.append(p)
    return newpaths


def CreateShadowPaths(thislayer, lines):

    #print "Number of shadow sections: ", len(lines)
    newpaths = []
    for l in lines:
        newline = []
        l1 = l[0]
        l2 = l[1]
        l2.reverse()
        for node in l1: newline.append(node)
        for node in l2: newline.append(node)
        p = drawSimplePath(newline)
        newpaths.append(p)
    return newpaths


def removeOverlapPathlist(paths):
	Layer = GSLayer()
	for p in paths: Layer.paths.append(p)
	Layer.removeOverlap()
	newpaths = Layer.paths
	del Layer
	return newpaths

# MekkaBlue
def retractHandles(thisLayer):
	for thisPath in thisLayer.paths:
		for x in reversed( range( len( thisPath.nodes ))):
			thisNode = thisPath.nodes[x]
			if thisNode.type == GSOFFCURVE:
				del thisPath.nodes[x]
			else:
				thisNode.type = GSLINE
		
		thisPath.checkConnections()

def SnapToGrid(lines, gridsize):
	for line in lines:
		for pt in line:
			pt[1] = int(pt[1]/gridsize)*gridsize

	return lines
