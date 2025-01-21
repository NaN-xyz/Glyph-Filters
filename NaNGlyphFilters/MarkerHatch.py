# MenuTitle: Marker Hatch
# -*- coding: utf-8 -*-
__doc__ = """
Marker Hatch
"""

import random
from NaNGFAngularizzle import ConvertPathsToLineSegments, getListOfPoints
from NaNGFGraphikshared import AddPaths, AllPathBounds, ClearPaths, drawSimplePath, point_inside_polygon, retractHandles, RoundPaths
from NaNGlyphsEnvironment import glyphsEnvironment as G
from NaNGFConfig import glyphSize
from NaNFilter import NaNFilter
from math import cos, radians, sin


class Shatter(NaNFilter):

	params = {
		"S": {"offset": 20, "sliceheight": 5},
		"M": {"offset": 0, "sliceheight": 10},
		"L": {"offset": 0, "sliceheight": 10}
	}
	sliceheight = 10
	angle = 45

	def setup(self):
		pass

	def processLayer(self, thislayer, params):
		if glyphSize(thislayer.parent) == "S":
			self.processLayerSmall(thislayer, params)
		else:
			self.processLayerLarge(thislayer, params)

	def processLayerSmall(self, thislayer, params):
		paths = list(thislayer.paths)
		rounded = RoundPaths(paths)
		ClearPaths(thislayer)
		AddPaths(rounded, thislayer)
		# retractHandles(thislayer)
		self.doclean(thislayer)

	def processLayerLarge(self, thislayer, params):

		sliceheight = params["sliceheight"]
		G.remove_overlap(thislayer)
		bounds = AllPathBounds(thislayer)

		spaths = self.returnSlicedPaths(thislayer, sliceheight, bounds)

		ClearPaths(thislayer)

		n = 1
		maxshift = 20
		for sh, row in spaths:
			for p in row:
				if n % 2 == 0:
					d = random.randrange(0, maxshift)
				else:
					d = random.randrange(maxshift * -1, 0)
				self.shufflePaths(row, d)
			n += 1
			rounded = RoundPaths(row)
			AddPaths(rounded, thislayer)

		retractHandles(thislayer)
		self.doclean(thislayer)

	def doclean(self, thislayer):
		self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)

	def shufflePaths(self, row, d):
		shiftx = d * cos(radians(self.angle))
		shifty = d * sin(radians(self.angle))
		for path in row:
			path.applyTransform((
				1,  # x scale factor
				0,  # x skew factor
				0,  # y skew factor
				1,  # y scale factor
				shiftx,  # x position
				shifty   # y position
			))

	def returnSlicedPaths(self, thislayer, sliceheight, bounds):

		slicedpaths = []
		ox, oy, w, h = bounds[0], bounds[1], bounds[2], bounds[3]
		# starty = oy
		y = oy
		dist = thislayer.width * 3
		sh = 0

		# angle = self.angle + random.randrange(-5, 5)

		while y < oy + h + dist:

			rowpaths = []
			tmplayer = G.copy_layer(thislayer)

			shiftx = dist * cos(radians(self.angle))
			shifty = dist * sin(radians(self.angle))

			cutax1, cutay1 = ox - 1, y - dist - sh
			cutax2, cutay2 = ox + 1 + shiftx, y - sh + shifty
			cutbx1, cutby1 = ox - 1, y - dist
			cutbx2, cutby2 = ox + 1 + shiftx, y + shifty
			# c = drawCircle(cutax1-20, cutay1, 20, 20)
			# thislayer.paths.append(c)

			buff = 15  # increase top+bottom margin of container
			slicepoly = [[cutax1 - 2, cutay1 - buff], [cutax2 + 2, cutay2 - buff], [cutbx2 + 2, cutby2 + buff], [cutbx1 - 2, cutby1 + buff]]
			slicepath = drawSimplePath(slicepoly)
			slicedata = getListOfPoints(ConvertPathsToLineSegments([slicepath], 20))[0][1]
			# thislayer.paths.append(slicepath)

			G.cut_layer(tmplayer, (cutax1, cutay1), (cutax2, cutay2))
			G.cut_layer(tmplayer, (cutbx1, cutby1), (cutbx2, cutby2))

			for path in tmplayer.paths:
				try:
					pathdata = getListOfPoints(ConvertPathsToLineSegments([path], 20))[0][1]
					if self.WithinSlice(pathdata, slicedata):
						rowpaths.append(path)
				except:
					pass
			ClearPaths(tmplayer)  # to trigger path.parent = None
			del tmplayer
			sh = sliceheight * random.randrange(1, 20)
			y += sh  # +sliceheight
			slicedpaths.append([sh, rowpaths])

		return slicedpaths

	def WithinSlice(self, shape, glyph):
		for nx, ny in shape:
			if not point_inside_polygon(nx, ny, glyph):
				return False
		return True


Shatter()
