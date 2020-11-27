#MenuTitle: 13 Burned
# -*- coding: utf-8 -*-
__doc__="""
13. Burned
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFSpacePartition import *
from NaNGFNoise import *
from NaNFilter import NaNFilter


def SortCollageSpace(thislayer, outlinedata, outlinedata2, gridsize, bounds):

	final_in_triangles = []
	in_triangles = []
	out_triangles = []
	edge_triangles = []

	isogrid = makeIsometricGrid(bounds, gridsize)
	isogrid = RandomiseIsoPoints(isogrid, gridsize)
	alltriangles = IsoGridToTriangles(isogrid)

	# Return triangles within and without
	in_out_triangles = returnTriangleTypes(alltriangles, outlinedata)
	in_triangles = in_out_triangles[0]
	out_triangles = in_out_triangles[1]

	#edge_triangles = StickTrianglesToOutline(out_triangles, outlinedata)
	edge_triangles = ReturnOutlineOverlappingTriangles(out_triangles, outlinedata)	

	final_in_triangles.extend(in_triangles)
	final_in_triangles.extend(edge_triangles)

	# for triangle in edge_triangles:
	# 	tricoords = SimplifyTriangleList(triangle)
	# 	if ShapeWithinOutlines(tricoords, outlinedata2): final_in_triangles.append(triangle)

	return TrianglesListToPaths(edge_triangles)

	

# ---------



def ApplyBurn(thislayer, groups):

	for g in groups:

		if len(g)>2:

			templayer = GSLayer()
			for path in g:
				tp = path
				templayer.paths.append(tp)
				thislayer.paths.append(tp)
			templayer.removeOverlap()

			for p in templayer.paths: 
				
				nodelen = len(p.nodes)

def returnRoundedPaths(paths):

	roundedpathlist = []
	for p in paths:
		roundedpath = RoundPath(p, "nodes")
		try: 
			roundedpath = convertToFitpath(roundedpath, True)
			roundedpathlist.append(roundedpath)
		except:
			pass
	return roundedpathlist


class Burn(NaNFilter):
	params = {
		"S": { "offset": 0, "gridsize": 40 },
		"M": { "offset": 4, "gridsize": 45 },
		"L": { "offset": 4, "gridsize": 50 },
	}

	def processLayer(self, thislayer, params):
		pathlist = doAngularizzle(thislayer.paths, 20)
		outlinedata = setGlyphCoords(pathlist)
		bounds = AllPathBounds(thislayer)
		
		offsetpaths = self.saveOffsetPaths(thislayer, params["offset"], params["offset"], removeOverlap=True)
		pathlist2 = doAngularizzle(offsetpaths, 4)
		outlinedata2 = setGlyphCoords(pathlist2)
		bounds2 = AllPathBoundsFromPathList(pathlist2)

		ClearPaths(thislayer)

		newtris = SortCollageSpace(thislayer, outlinedata, outlinedata2, params["gridsize"], bounds)
		maxchain = random.randrange(200,400)
		groups = BreakUpSpace(thislayer, outlinedata, newtris, params["gridsize"], maxchain)
		ApplyBurn(thislayer, groups)
		#AddAllPathsToLayer(edgetris, thislayer)

		thislayer.removeOverlap()
		roundedpathlist = returnRoundedPaths(thislayer.paths)
		ClearPaths(thislayer)
		AddAllPathsToLayer(roundedpathlist, thislayer)

Burn()
