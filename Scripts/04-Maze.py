#MenuTitle: 04. Maze
# -*- coding: utf-8 -*-
__doc__="""
04. Maze
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNFilter import NaNFilter


class Maze(NaNFilter):
	params = {
		"S": { "offset": 5 },
		"M": { "offset": 10 },
		"L": { "offset": 10 },
	}

	def setup(self):
		self.unit = 30

	def processLayer(self, thislayer, params):
		offset = params["offset"]
		if ContainsPaths(thislayer):
			offsetpaths = self.saveOffsetPaths(thislayer, offset, offset, removeOverlap=False)
			pathlist = doAngularizzle(offsetpaths, 4)
			outlinedata = setGlyphCoords(pathlist)

			bounds = AllPathBounds(thislayer)
			self.setupChecker(bounds)
			self.setAvailableSlots(thislayer, outlinedata)

			ClearPaths(thislayer)

			walkpaths = self.walkerLoop(thislayer)
			AddAllPathsToLayer(walkpaths, thislayer)
			
			self.expandMonoline(thislayer, 6)
			thislayer.removeOverlap()

	def setupChecker(self, bounds):
		self.available_slots = []
		self.ox, self.oy, self.ow, self.oh = bounds
		self.ysteps = self.oh // self.unit
		self.xsteps = self.ow // self.unit
		self.checker = []

		for stepy in range(0, self.ysteps+3):
			xlist = []
			for stepx in range(0, self.xsteps+3):
				xlist.append(True)
			self.checker.append(xlist)


	def setAvailableSlots(self, thislayer, outlinedata):
		for stepy in range(0, self.ysteps+3, 1):

			y = self.oy + (stepy*self.unit)

			for stepx in range(0, self.xsteps+3, 1):

				x = self.ox + (stepx*self.unit)
				shapepath = []
				nx = x+self.unit/2
				ny = y+self.unit/2
				shape = drawTriangle(nx, ny, 6, 6)
				shapepath.append(shape)

				nshape = doAngularizzle(shapepath, 10)
				nshape = setGlyphCoords(nshape)
				finalshape = nshape[0][1]
				
				if ShapeWithinOutlines(finalshape, outlinedata):
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

		while len(self.available_slots)>0:
			start = self.random.choice(self.available_slots)
			self.updateChecker(start[0], start[1])
			walks = self.walker(thislayer, start)
			walkerpaths.extend(walks)

		return walkerpaths

	def walker(self, thislayer, start):
		looklist = ["N","S","E","W"]
		startx, starty = start[0], start[1]
		walkpath = GSPath()
		
		sx, sy = startx, starty
		nx, ny = startx, starty

		startnode = GSNode([self.ox+(sx*self.unit), self.oy+(sy*self.unit)], type = GSLINE)
		walkpath.nodes.append( startnode )

		breakcounter=0
		walkcontinue = True
		walkerpaths = []

		while walkcontinue==True:
			direction = random.choice(looklist)
			movements = { "N": (0,1), "S": (0,-1), "E": (1,0), "W": (-1,0) }
			lookx = sx + movements[direction][0]
			looky = sy + movements[direction][1]
			if [lookx, looky] in self.available_slots:
				self.updateChecker(lookx, looky)
				drawx, drawy = self.ox+(lookx*self.unit), self.oy+(looky*self.unit) 
				walkpath.nodes.append( GSNode([drawx, drawy], type = GSLINE) )
				sx = lookx
				sy = looky

			breakcounter+=1
			if breakcounter==1000:
				break

		if (len(walkpath.nodes))==1: walkpath.nodes.append(startnode)

		walkerpaths.append(walkpath)
		return walkerpaths

Maze()

