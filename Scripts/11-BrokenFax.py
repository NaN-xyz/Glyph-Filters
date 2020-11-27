#MenuTitle: 11. BrokenFax
# -*- coding: utf-8 -*-
__doc__="""
11. BrokenFax
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import *

def AngularSteps(thislayer, outlinedata, stepsize):
	allpaths = []
	size = stepsize
	originx = thislayer.bounds.origin.x

	for _,structure in outlinedata:
		nodelen = len(structure)
		bubble = GSPath()
		newpath = []

		for x1, y1 in structure:
			x2,y2 = int(x1/size) * size, int(y1/size) * size

			if len(newpath)>0:
				if x2!=newpath[-1][0] or y2!=newpath[-1][1]:
					newpath.append([x2,y2])
			else:
				newpath.append([x2,y2])

		allpaths.append(newpath)

	# shift
	# find lowest x in all paths
	lowestx = 99999
	for path in allpaths:
		xlow = findLowestX(path)
		if xlow<lowestx: 
			lowestx = xlow
	# adjust x in paths by lowestx
	for path in allpaths:
		for node in path:
			node[0] = node[0] + (originx - lowestx)
	# add all paths
	angularpaths = []
	for path in allpaths:
		simple = drawSimplePath(path)
		angularpaths.append(simple)

	return angularpaths


def findLowestX(nodes):
	lowestx = 99999
	for node in nodes:
		x = node[0]
		if x<lowestx:
			lowestx = x
	return lowestx


def Shapefit(thislayer, outlinedata):

	b = AllPathBounds(thislayer)

	if b is None:
		return

	ox, oy, w, h = b[0], b[1], b[2], b[3]
	sizes = returnSizes(random.randrange(3,5))
	newshapes = []
	allshapes = []

	for shapesize in sizes:

		for x in range(ox, ox+w, shapesize):

			for y in range(oy, oy+h, shapesize):

				shapepath = []
				shape = drawRectangle(x, y, shapesize, shapesize)
				shapepath.append(shape)
				nshape = doAngularizzle(shapepath, 10)
				nshape = setGlyphCoords(nshape)
				finalshape = nshape[0][1]
				rect = returnSquareShape(x, y, shapesize, shapesize)

				if ShapeWithinOutlines(finalshape, outlinedata):
					safe = True
					for n in range(0, len(allshapes)):
						if point_inside_polygon(x, y, allshapes[n]):
							safe = False
							break

					if safe:
						newshapes.append(shape)
						allshapes.append(rect)	

		return newshapes


def returnSizes(it):

	minsizes = [16, 24, 32, 48] #included 8
	minit = random.choice(minsizes)
	sizes = []
	sizes.append(random.choice(minsizes))
	for n in range(0, it): sizes.append(random.randrange(1,6)*minit)
	return sizes


def returnSquareShape(nx, ny, w, h):
	coord = [ [nx,ny], [nx,ny+h], [nx+w,ny+h], [nx+w,ny] ]
	return coord


class BrokenFax(NaNFilter):
	params = {
		"S": {"offset": -20, "stepsize": 50 },
		"M": {"offset": -20, "stepsize": 50 },
		"L": {"offset": -30, "stepsize": 50 },
	}

	def processLayer(self, thislayer, params):
		thislayer.removeOverlap()
		pathlist = doAngularizzle(thislayer.paths, params["stepsize"])
		outlinedata = setGlyphCoords(pathlist)
		ClearPaths(thislayer)

		angularpaths = AngularSteps(thislayer, outlinedata, params["stepsize"])
		AddAllPathsToLayer(angularpaths, thislayer)

		offsetpaths = saveOffsetPaths(thislayer, params["offset"], params["offset"], removeOverlap=True)
		pathlist = doAngularizzle(offsetpaths, 4)
		outlinedata = setGlyphCoords(pathlist)
		shapepaths = Shapefit(thislayer, outlinedata)
		AddAllPathsToLayer(shapepaths, thislayer)
		thislayer.removeOverlap()

BrokenFax()
