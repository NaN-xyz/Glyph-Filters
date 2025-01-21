# MenuTitle: Maze
# -*- coding: utf-8 -*-
__doc__ = """
Maze
"""

from NaNGFConfig import ContainsPaths
from NaNGFGraphikshared import AddPaths, AllPathBounds, ClearPaths, ShapeWithinOutlines, drawTrianglePoints
from NaNGlyphsEnvironment import GSNode, GSLINE, GSPath
from NaNFilter import NaNFilter
from NaNGlyphsEnvironment import glyphsEnvironment as G
import random


class Maze(NaNFilter):
	params = {
		"S": {"offset": 5},
		"M": {"offset": 10},
		"L": {"offset": 10},
	}

	def setup(self):
		self.unit = 30

	def processLayer(self, thislayer, params):
		offset = params["offset"]
		if ContainsPaths(thislayer):
			offsetpaths = self.saveOffsetPaths(
				thislayer, offset, offset, removeOverlap=False
			)

			outlinedata = G.outline_data_for_hit_testing(offsetpaths)

			bounds = AllPathBounds(thislayer)
			self.setupChecker(bounds)
			self.setAvailableSlots(thislayer, outlinedata)

			ClearPaths(thislayer)

			walkpaths = self.walkerLoop(thislayer)
			AddPaths(walkpaths, thislayer)

			self.expandMonoline(thislayer, 6)
			G.remove_overlap(thislayer)
			self.CleanOutlines(thislayer, remSmallPaths=False, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)

	def setupChecker(self, bounds):
		self.available_slots = []
		self.ox, self.oy, self.ow, self.oh = bounds
		self.ysteps = self.oh // self.unit
		self.xsteps = self.ow // self.unit
		self.checker = []

		for stepy in range(0, self.ysteps + 3):
			xlist = []
			for stepx in range(0, self.xsteps + 3):
				xlist.append(True)
			self.checker.append(xlist)

	def setAvailableSlots(self, thislayer, outlinedata):
		for stepy in range(0, self.ysteps + 3, 1):

			y = self.oy + (stepy * self.unit)

			for stepx in range(0, self.xsteps + 3, 1):

				x = self.ox + (stepx * self.unit)
				nx, ny = x + self.unit / 2, y + self.unit / 2
				trianglePoints = drawTrianglePoints(nx, ny, 6, 6)
				if ShapeWithinOutlines(trianglePoints, outlinedata):
					self.checker[stepy][stepx] = True
					self.available_slots.append([stepx, stepy])
				else:
					self.checker[stepy][stepx] = False

	def updateChecker(self, xpos, ypos):
		self.checker[ypos][xpos] = False

		item = [xpos, ypos]
		if item in self.available_slots:
			self.available_slots.remove(item)

	def walkerLoop(self, thislayer):
		walkerpaths = []

		while len(self.available_slots) > 0:
			start = random.choice(self.available_slots)
			self.updateChecker(start[0], start[1])
			walks = self.walker(thislayer, start)
			walkerpaths.extend(walks)

		return walkerpaths

	def walker(self, thislayer, start):
		movements = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
		walkpath = GSPath()
		walkpath.closed = False
		sx, sy = start

		startnode = GSNode(
			[self.ox + (sx * self.unit), self.oy + (sy * self.unit)], type=GSLINE
		)
		walkpath.nodes.append(startnode)

		breakcounter = 0
		walkerpaths = []

		while breakcounter < 1000:
			dx, dy = random.choice(list(movements.values()))
			lookx, looky = sx + dx, sy + dy
			if [lookx, looky] in self.available_slots:
				self.updateChecker(lookx, looky)
				drawx, drawy = self.ox + (lookx * self.unit), self.oy + (
					looky * self.unit
				)
				walkpath.nodes.append(GSNode([drawx, drawy], type=GSLINE))
				sx, sy = lookx, looky

			breakcounter += 1

		if (len(walkpath.nodes)) == 1:
			walkpath.nodes.append(startnode)

		walkerpaths.append(walkpath)
		return walkerpaths


Maze()
