# MenuTitle: Distressed
# -*- coding: utf-8 -*-
__doc__ = """
Distressed
"""

from GlyphsApp import Glyphs, GSLayer
from NaNGFGraphikshared import ShiftPath, AllPathBounds, ClearPaths
from NaNGFAngularizzle import ConvertPathsToSkeleton, setGlyphCoords
from NaNGFSpacePartition import makeIsometricGrid, RandomiseIsoPoints, IsoGridToTriangles, returnTriangleTypes, StickTrianglesToOutline, TrianglesListToPaths, BreakUpSpace
from NaNGlyphsEnvironment import glyphsEnvironment as G
from NaNGFConfig import beginFilterNaN, beginGlyphNaN, endGlyphNaN, endFilterNaN, glyphSize
import random

# COMMON
font = Glyphs.font
selectedGlyphs = beginFilterNaN(font)


# ====== OFFSET LAYER CONTROLS ==================

def saveOffsetPaths(Layer, hoffset, voffset, removeOverlap):
	templayer = G.copy_layer(Layer)
	templayer.name = "tempoutline"
	currentglyph = Layer.parent
	currentglyph.layers.append(templayer)
	tmplayer_id = templayer.layerId
	G.offset_layer(templayer, hoffset, voffset)
	if removeOverlap:
		templayer.removeOverlap()
	offsetpaths = templayer.paths
	del currentglyph.layers[tmplayer_id]
	return offsetpaths

# ================================================


def SortCollageSpace(thislayer, outlinedata, outlinedata2, gridsize, bounds):

	final_in_triangles = []
	in_triangles = []
	out_triangles = []
	edge_triangles = []

	isogrid = makeIsometricGrid(bounds, gridsize)
	isogrid = RandomiseIsoPoints(isogrid, gridsize)
	alltriangles = IsoGridToTriangles(isogrid)

	in_out_triangles = returnTriangleTypes(alltriangles, outlinedata)
	in_triangles = in_out_triangles[0]
	out_triangles = in_out_triangles[1]

	edge_triangles = StickTrianglesToOutline(out_triangles, outlinedata)
	# edge_triangles = ReturnOutlineOverlappingTriangles(out_triangles, outlinedata)

	final_in_triangles.extend(in_triangles)
	final_in_triangles.extend(edge_triangles)

	# for triangle in edge_triangles:
	# 	tricoords = SimplifyTriangleList(triangle)
	# 	if ShapeWithinOutlines(tricoords, outlinedata2): final_in_triangles.append(triangle)

	return TrianglesListToPaths(final_in_triangles)


# ---------


def ApplyBurn(thislayer, groups):

	for g in groups:

		if len(g) > 2:

			shiftmax = random.randrange(1, 50)
			shiftype = random.choice(["x", "y", "xy"])

			templayer = GSLayer()
			G.add_paths(templayer, g)
			templayer.removeOverlap()

			for p in templayer.paths:
				ShiftPath(p, shiftmax, shiftype)
				G.add_paths(thislayer, [p])
				# nodelen = len(p.nodes)


def OutputTopography():

	for glyph in selectedGlyphs:

		glyph.beginUndo()
		beginGlyphNaN(glyph)

		# --- °°°°°°°

		thislayer = font.glyphs[glyph.name].layers[0]
		thislayer.beginChanges()

		# ---

		glyphsize = glyphSize(glyph)

		if glyphsize == "S":
			offset = 0
			gridsize = 30
		if glyphsize == "M":
			offset = 4
			gridsize = 30
		if glyphsize == "L":
			offset = 4
			gridsize = 30

		# ----

		pathlist = ConvertPathsToSkeleton(thislayer.paths, 20)
		outlinedata = setGlyphCoords(pathlist)
		bounds = AllPathBounds(thislayer)

		offsetpaths = saveOffsetPaths(thislayer, offset, offset, removeOverlap=True)
		pathlist2 = ConvertPathsToSkeleton(offsetpaths, 4)
		outlinedata2 = setGlyphCoords(pathlist2)
		# bounds2 = AllPathBoundsFromPathList(pathlist2)

		ClearPaths(thislayer)

		newtris = SortCollageSpace(thislayer, outlinedata, outlinedata2, gridsize, bounds)
		maxchain = random.randrange(30, 60)
		groups = BreakUpSpace(thislayer, outlinedata, newtris, gridsize, maxchain)
		ApplyBurn(thislayer, groups)
		# AddAllPathsToLayer(edgetris, thislayer)
		# thislayer.removeOverlap()

		# ---

		thislayer.endChanges()

		# --- °°°°°°°

		endGlyphNaN(glyph)
		glyph.endUndo()


# =======

OutputTopography()

# =======

# OutputFur()
# OutputSpikes()

endFilterNaN(font)
