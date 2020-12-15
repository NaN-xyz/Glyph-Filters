#MenuTitle: Broken Fax
# -*- coding: utf-8 -*-
__doc__="""
Broken Fax
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import *

class BrokenFax(NaNFilter):
	params = {
		"S": {"offset": -20, "stepsize": 50 },
		"M": {"offset": -20, "stepsize": 50 },
		"L": {"offset": -30, "stepsize": 50 },
	}

	def processLayer(self, thislayer, params):
		thislayer.removeOverlap()
		pathlist = ConvertPathsToSkeleton(thislayer.paths, params["stepsize"])
		outlinedata = setGlyphCoords(pathlist)
		ClearPaths(thislayer)

		allpaths = []
		size = params["stepsize"]
		offset = params["offset"]
		originx = thislayer.bounds.origin.x

		for _,structure in outlinedata:
			newpath = []

			for x1, y1 in structure:
				x2,y2 = int(x1/size) * size, int(y1/size) * size

				if len(newpath)>0:
					if x2!=newpath[-1][0] or y2!=newpath[-1][1]:
						newpath.append([x2,y2])
				else:
					newpath.append([x2,y2])

			allpaths.append(newpath)

		# shift and find lowest x in all paths
		lowestx = min([
			min([ node[0] for node in path]) # Min x in path
		for path in allpaths])

		# adjust x in paths by lowestx
		for path in allpaths:
			for node in path:
				node[0] = node[0] + (originx - lowestx)

		angularpaths = [ drawSimplePath(path) for path in allpaths]
		AddAllPathsToLayer(angularpaths, thislayer)
		thislayer.removeOverlap()

		offsetpaths = saveOffsetPaths(thislayer, offset, offset, removeOverlap=True)
		pathlist = ConvertPathsToSkeleton(offsetpaths, 4)
		outlinedata = setGlyphCoords(pathlist)

		glitchpaths = self.Shapefit(thislayer, outlinedata)
		glitchopaths = ConvertPathlistDirection(glitchpaths,1)
		AddAllPathsToLayer(glitchpaths, thislayer)

		self.CleanOutlines(thislayer, remSmallPaths=False, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)

	def Shapefit(self, thislayer, outlinedata):

		b = AllPathBounds(thislayer)
		if b is not None:
			ox, oy, w, h = b[0], b[1], b[2], b[3]
			sizes = self.returnSizes(random.randrange(3,5))
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
						rect = self.returnSquareShape(x, y, shapesize, shapesize)

						if ShapeWithinOutlines(finalshape, outlinedata):
							safe = True
							for n in range(0, len(allshapes)):
								if point_inside_polygon(x, y, allshapes[n]):
									safe = False
									break
							if safe==True:		
								newshapes.append(shape)
								allshapes.append(rect)	
			return newshapes

	def returnSizes(self, it):

		minsizes = [16, 24, 32, 48] #included 8
		minit = random.choice(minsizes)
		sizes = []
		sizes.append(random.choice(minsizes))
		for n in range(0, it): sizes.append(random.randrange(1,6)*minit)
		return sizes

	def returnSquareShape(self, nx, ny, w, h):
		coord = [ [nx,ny], [nx,ny+h], [nx+w,ny+h], [nx+w,ny] ]
		return coord


BrokenFax()
