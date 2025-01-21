import random
# import time
# import traceback
from NaNGFConfig import NANGFSET, beginFilterNaN, beginGlyphNaN, endFilterNaN, endGlyphNaN, glyphSize
from NaNGFGraphikshared import SnapToGrid, ClearPaths
from NaNGFSpacePartition import IsoGridToTriangles, RandomiseIsoPoints, ReturnOutlineOverlappingTriangles, StickTrianglesToOutline, TrianglesListToPaths, makeIsometricGrid, returnTriangleTypes
from NaNGlyphsEnvironment import OFFCURVE, GSLayer, Glyphs
# from Foundation import NSClassFromString
from NaNGlyphsEnvironment import glyphsEnvironment as G

try:
	import tqdm

	progress = tqdm.tqdm
except:
	progress = list


class NaNFilter:
	def __init__(self):
		self.font = Glyphs.font
		selectedGlyphs = beginFilterNaN(self.font)
		self.setup()
		for glyph in progress(selectedGlyphs):
			self.processGlyph(glyph)
		endFilterNaN(self.font)

	def setup(self):
		pass

	def processGlyph(self, glyph):

		G.begin_undo(glyph)
		try:
			beginGlyphNaN(glyph)
			old_state = random.getstate()
			for thislayer in list(glyph.layers):  # Don't use a proxy!
				# Use the same random seed for each layer, else we're in trouble
				random.setstate(old_state)
				G.begin_layer_changes(thislayer)
				# thislayer.correctPathDirection()
				if hasattr(self, "params"):
					params = self.params[glyphSize(glyph)]
				else:
					params = None
				self.processLayer(thislayer, params)
				G.end_layer_changes(thislayer)
			endGlyphNaN(glyph)
		except:
			import traceback
			print(traceback.format_exc())
		finally:
			G.end_undo(glyph)

	def processLayer(self, layer, params):
		raise NotImplementedError

	def doOffset(self, Layer, hoffset, voffset):
		G.offset_layer(Layer, hoffset, voffset)

	def saveOffsetPaths(self, Layer, hoffset, voffset, removeOverlap):
		# glyph = Layer.parent
		templayer = G.copy_layer(Layer)
		templayer.name = "tempoutline"
		self.doOffset(templayer, hoffset, voffset)
		if removeOverlap:
			G.remove_overlap(templayer)
		# templayer.correctPathDirection() # doesn't seem to work when placed here
		offsetpaths = list(templayer.paths)
		ClearPaths(templayer)  # to trigger setting path.parent = None
		return offsetpaths

	def expandMonoline(self, Layer, noodleRadius):
		G.offset_layer(Layer, noodleRadius, noodleRadius, make_stroke=True)
		G.correct_path_direction(Layer)

	def expandMonolineFromPathlist(self, Paths, noodleRadius):
		Layer = GSLayer()
		for p in Paths:
			Layer.paths.append(p)
		G.offset_layer(Layer, noodleRadius, noodleRadius, make_stroke=True)
		G.correct_path_direction(Layer)
		return Layer.paths

	def SortCollageSpace(self, thislayer, outlinedata, gridsize, bounds, action, randomize=False, snap=False):
		isogrid = makeIsometricGrid(bounds, gridsize)
		if randomize:
			isogrid = RandomiseIsoPoints(isogrid, gridsize)
		if snap:
			isogrid = SnapToGrid(isogrid, gridsize)
		alltriangles = IsoGridToTriangles(isogrid)

		# Return triangles within and without
		in_triangles, out_triangles = returnTriangleTypes(alltriangles, outlinedata)

		if action == "stick":
			edge_triangles = StickTrianglesToOutline(out_triangles, outlinedata)
			return TrianglesListToPaths(in_triangles + edge_triangles)
		elif action == "overlap":
			edge_triangles = ReturnOutlineOverlappingTriangles(out_triangles, outlinedata)
			# Just return the edges
			return TrianglesListToPaths(edge_triangles)
		else:
			raise NotImplementedError

	def CleanOutlines(self, thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False):
		if remSmallPaths:
			self.removeSmallPaths(thislayer, NANGFSET["smallest_path"])
		if remSmallSegments:
			self.removeSmallSegments(thislayer, NANGFSET["smallest_seg"], keepshape)
		if remStrayPoints:
			self.removeOpenPaths(thislayer)
		if remOpenPaths:
			self.removeStrayPoints(thislayer)  # see note for why this & above

	def removeSmallPaths(self, layer, maxdim):
		for p in reversed(layer.paths):
			w, h = p.bounds.size.width, p.bounds.size.height
			if w < maxdim and h < maxdim:
				G.remove_path_from_layer(layer, p)

	# based on
	# https://github.com/mekkablue/Glyphs-Scripts/blob/master/Paths/Remove%20Short%20Segments.py
	def removeSmallSegments(self, thisLayer, maxseg, keepshape):
		for thisPath in thisLayer.paths:
			count = len(thisPath.nodes)
			for i in range(count - 1, -1, -1):
				thisNode = thisPath.nodes[i]
				prevNode = thisPath.nodes[(i % count) - 1]
				if prevNode.type != OFFCURVE and thisNode.type != OFFCURVE:
					xDistance = thisNode.position.x - prevNode.position.x
					yDistance = thisNode.position.y - prevNode.position.y
					if abs(xDistance) < maxseg and abs(yDistance) < maxseg:
						G.remove_node(thisPath, thisNode, keepshape=keepshape)

	def removeStrayPoints(self, thislayer):
		for p in reversed(thislayer.paths):
			if len(p.nodes) < 3:
				G.remove_path_from_layer(thislayer, p)

	def removeOpenPaths(self, thislayer):
		pass
		# deleteing the segments seems to leave paths that are open but still have closed==True
		# for p in reversed(thislayer.paths):
		# 	if p.closed==False: thislayer.paths.remove(p)
