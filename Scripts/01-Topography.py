#MenuTitle: 01. Topography
# -*- coding: utf-8 -*-
__doc__="""
01. Topography
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFSpacePartition import *

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


def SortCollageSpace(thislayer, outlinedata, outlinedata2, gridsize, bounds):

	final_in_triangles = []
	in_triangles = []
	out_triangles = []
	edge_triangles = []

	isogrid = makeIsometricGrid(bounds, gridsize)
	alltriangles = IsoGridToTriangles(isogrid)

	# Return triangles within and without
	in_out_triangles = returnTriangleTypes(alltriangles, outlinedata)
	in_triangles = in_out_triangles[0]
	out_triangles = in_out_triangles[1]

	edge_triangles = StickTrianglesToOutline(out_triangles, outlinedata)
	#edge_triangles = ReturnOutlineOverlappingTriangles(out_triangles, outlinedata)	

	final_in_triangles.extend(in_triangles)
	final_in_triangles.extend(edge_triangles)

	# for triangle in edge_triangles:
	# 	tricoords = SimplifyTriangleList(triangle)
	# 	if ShapeWithinOutlines(tricoords, outlinedata2): final_in_triangles.append(triangle)

	return TrianglesListToPaths(final_in_triangles)

	

# ---------


def ApplyCollageGraphixxx(thislayer, groups, drawtype):

	for g in groups:

		if len(g)>2:

			templayer = GSLayer()
			for path in g:
				tp = path
				templayer.paths.append(tp)
			templayer.removeOverlap()

			for p in templayer.paths: 
				
				nodelen = len(p.nodes)

				if nodelen>4:

					try:
						roundedpath = RoundPath(p, "nodes")
						roundedpath = convertToFitpath(roundedpath, True)
						pathlist = doAngularizzle([roundedpath],80)
						outlinedata = setGlyphCoords(pathlist)

						try:
							if drawtype=="vertical" or drawtype=="horizontal":
								all_lines = Fill_Drawlines(thislayer, roundedpath, drawtype, 15, linecomponents)
								AddAllComponentsToLayer(all_lines, thislayer)

							if drawtype=="blob":
								# disallow small blobs
								rw = roundedpath.bounds.size.width
								rh = roundedpath.bounds.size.height
								if (rw>30 and rh>30) and (rw<200 or rh<200): thislayer.paths.append(roundedpath)

						except:
							pass

					except:
						pass
				else:
					pass


			del templayer


def OutputTopography():

	global line_vertical_comp, line_horizontal_comp, linecomponents
	
	linecomponents = []
	line_vertical_comp = CreateLineComponent(font, "vertical", 6, "LineVerticalComponent")
	line_horizontal_comp = CreateLineComponent(font, "horizontal", 6, "LineHorizontalComponent")
	linecomponents.extend([line_vertical_comp, line_horizontal_comp])
	print linecomponents

	for glyph in selectedGlyphs:

		glyph.beginUndo()
		beginGlyphNaN(glyph)

		# --- °°°°°°°

		thislayer = font.glyphs[glyph.name].layers[0]
		thislayer.beginChanges()

		# ---
		
		glyphsize = glyphSize(glyph)

		if glyphsize=="S": 
			offset = 0
			gridsize = 10
		if glyphsize=="M": 
			offset = 4
			gridsize = 30
		if glyphsize=="L": 
			offset = 4
			gridsize = 40

		# ----


		if glyphsize!="S":

			pathlist = doAngularizzle(thislayer.paths, 20)
			outlinedata = setGlyphCoords(pathlist)
			bounds = AllPathBounds(thislayer)
			
			offsetpaths = saveOffsetPaths(thislayer, offset, offset, removeOverlap=True)
			pathlist2 = doAngularizzle(offsetpaths, 4)
			outlinedata2 = setGlyphCoords(pathlist2)
			bounds2 = AllPathBoundsFromPathList(pathlist2)

			ClearPaths(thislayer)

			newtris = SortCollageSpace(thislayer, outlinedata, outlinedata2, gridsize, bounds)
			maxchain = random.randrange(200,400)
			groups = BreakUpSpace(thislayer, outlinedata, newtris, gridsize, maxchain)
			ApplyCollageGraphixxx(thislayer, groups, "vertical")

			newtris = SortCollageSpace(thislayer, outlinedata, outlinedata2, gridsize, bounds)
			maxchain = random.randrange(200,400)
			groups = BreakUpSpace(thislayer, outlinedata, newtris, gridsize, maxchain)
			ApplyCollageGraphixxx(thislayer, groups, "horizontal")

			newtris = SortCollageSpace(thislayer, outlinedata, outlinedata2, gridsize, bounds)
			maxchain = random.randrange(70,100)
			groups = BreakUpSpace(thislayer, outlinedata, newtris, gridsize, maxchain)
			ApplyCollageGraphixxx(thislayer, groups, "blob")

		else:

			thislayer.removeOverlap()
			roundedpathlist = returnRoundedPaths(thislayer.paths)
			ClearPaths(thislayer)
			AddAllPathsToLayer(roundedpathlist, thislayer)

		# ---

		thislayer.endChanges()

		# --- °°°°°°°

		endGlyphNaN(glyph)
		glyph.endUndo()


# =======

OutputTopography()

# =======

#OutputFur()
#OutputSpikes()

endFilterNaN(font)


