# MenuTitle: SeaCamouflage
# -*- coding: utf-8 -*-
__doc__ = """
SeaCamouflage
"""

import math
from NaNFilter import NaNFilter
import random
from noise import snoise2
from math import sin, cos, degrees, radians
from NaNGFAngularizzle import ConvertPathsToLineSegments, getListOfPoints
from NaNGFGraphikshared import AddPaths, AllPathBounds, ClearPaths, ShiftAllPaths, point_inside_polygon, RoundPaths
from NaNGFNoise import noiseMap
from NaNGlyphsEnvironment import glyphsEnvironment as G
from NaNGlyphsEnvironment import GSPath, GSNode, GSLINE


class SeaCamouflage(NaNFilter):

	params = {
		"S": {"iterations": 0},
		"M": {"iterations": 4},
		"L": {"iterations": 5},
	}

	def processLayer(self, thislayer, params):
		iterations = params["iterations"]
		self.SliceGlyph(thislayer, iterations)
		ShiftAllPaths(thislayer.paths, 10, "xy")
		stripepaths = list(thislayer.paths)
		ClearPaths(thislayer)
		stripepaths = returnAllStripePaths(stripepaths)

		newPaths = []
		for stripes in stripepaths:
			if stripes is not None:
				for stripe in stripes:
					stripe.applyTransform((1, 0, 0, 1, 0, -30))
					newPaths.append(stripe)
		AddPaths(newPaths, thislayer)
		self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=False, remStrayPoints=True, remOpenPaths=True, keepshape=False)

	def processLayerSmall(self, thislayer):
		G.remove_overlap(thislayer)
		roundedpathlist = RoundPaths(thislayer.paths)
		ClearPaths(thislayer)
		AddPaths(roundedpathlist, thislayer)

	def SliceGlyph(self, thislayer, iterations):

		b = AllPathBounds(thislayer)
		ox, oy, w, h = b[0], b[1], b[2], b[3]
		cx, cy = ox + (w / 2), oy + (h / 2)
		angle = random.randrange(0, 360)

		if cy > cx:
			rad1 = cy * 3
			rad2 = rad1 * -1
		else:
			rad1 = cx * 3
			rad2 = rad1 * -1

		for n in range(0, iterations):
			angle += random.randrange(40, 120)
			angle2 = angle  # + random.randrange(0, 30)
			cx2 = cx + random.randrange(w * -1, w)
			cy2 = cy + random.randrange(h * -1, h)
			cutx1, cuty1 = cx2 + (rad1 * cos(angle)), cy2 + (rad1 * sin(angle))
			cutx2, cuty2 = cx2 + (rad2 * cos(angle2)), cy2 + (rad2 * sin(angle2))
			G.cut_layer(thislayer, (cutx1, cuty1), (cutx2, cuty2))


def returnAllStripePaths(paths):
	allpaths = []
	for p in paths:
		allpaths.append(StripePath(p))
	return allpaths


def StripePath(path):

	bounds = path.bounds
	tx = int(bounds.origin.x)
	ty = int(bounds.origin.y)
	tw = int(bounds.size.width)
	th = int(bounds.size.height)

	if tw > 40 and th > 40:

		noisescale = 0.002
		# x_max, y_max = 10, 10
		minsize, maxsize = 20, 60
		seedx, seedy = random.randrange(0, 100000), random.randrange(0, 100000)
		outline = getListOfPoints(ConvertPathsToLineSegments([path], 10))[0][1]
		wavepaths, waves = [], []

		if random.choice([1, 0]) == 0:
			angle = radians(random.randrange(1, 89))
		else:
			angle = radians(random.randrange(91, 170))

		minstepx, minstepy = 10, random.randrange(3, 40)
		mingap = random.randrange(5, 15)

		a = int(degrees(angle))
		tmpstepy = minstepy

		if a > 0 and a < 89:
			direction = 1
			startx, starty = tx, ty + th
			endx = 1000
			stepx = minstepx
			theta = 180 - 90 - (degrees(angle))
			hypot = tw / sin(angle)
			oppos = sin(radians(theta)) * hypot
			hypot2 = th / sin(radians(theta))
			pushx = stepx * cos(angle)
			pushy = stepx * sin(angle)
			a2 = angle
			starty = ty + th + oppos

		if a > 89 and a < 180:
			direction = 0
			startx, starty = tx + tw, ty + th
			endx = -1000
			stepx = minstepx * -1
			a2 = 180 - (degrees(angle))
			theta = 180 - 90 - (a2)
			hypot = tw / sin(radians(a2))
			oppos = sin(radians(theta)) * hypot
			hypot2 = th / sin(radians(theta))
			pushx = stepx * cos(angle) * -1
			pushy = stepx * sin(angle) * -1
			starty = ty + th + oppos

		break_counter_x = 0
		loop_counter = 0
		y = starty

		searchlen = hypot + hypot2
		step = 0
		steps = abs(math.floor(searchlen / tmpstepy) + 1)
		steplen = searchlen / steps

		if direction == 0:
			steplen *= -1

		searchangle = angle + radians(-90)
		gapcounter = 0
		# gap = mingap

		while step < steps + 1:

			gapx = mingap * cos(searchangle)
			gapy = mingap * sin(searchangle)

			if direction == 0:
				gapx *= -1
				gapy *= -1

			lines, wave = [], []

			if step % 2 == 0:
				gapcounter += 1

			nx = startx + (step * ((steplen) * cos(searchangle)))
			nx2 = nx + (gapx * gapcounter)
			ny = starty + (step * ((steplen) * sin(searchangle)))
			ny2 = ny + (gapy * gapcounter)

			for x in range(startx, endx + stepx, stepx):

				nx2 -= pushx
				ny2 -= pushy

				if point_inside_polygon(nx2, ny2, outline):
					noiz = abs(snoise2((y + seedy) * noisescale, (x + seedx) * noisescale, 4))
					size = noiseMap(noiz, minsize, maxsize)
					wave.append([nx2, ny2 + size])
				else:
					if len(wave) > 4:
						lines.append(wave)
						del wave
						wave = []
					if break_counter_x == 100:
						break_counter_x = 0
						continue
					else:
						break_counter_x += 1
				loop_counter += 1

			if len(lines) > 0:
				waves.append(lines)

			step += 1

		# draw the waves
		for w in range(0, len(waves) - 1, 2):

			lines1 = waves[w]
			lines2 = waves[w + 1]

			if len(lines1) == len(lines2):
				for l in range(0, len(waves[w])):
					wav = waves[w][l]
					wav2 = reversed(waves[w + 1][l])
					p = GSPath()
					for n in wav:
						p.nodes.append(GSNode([n[0], n[1]], type=GSLINE))
					for n in wav2:
						p.nodes.append(GSNode([n[0], n[1]], type=GSLINE))

			if len(lines1) == 1 and len(lines2) == 2:
				try:
					wav = waves[w][0]
					wav2a = waves[w + 1][0]
					wav2b = waves[w + 1][1]
					wavlen = len(wav)
					wav2alen = len(wav2a)
					# wav2blen = len(wav2a)
					# new_wave1top = wav[0: wav2alen]

					p = GSPath()
					for n in wav:
						p.nodes.append(GSNode([n[0], n[1]], type=GSLINE))
					for n in reversed(wav2b):
						p.nodes.append(GSNode([n[0], n[1]], type=GSLINE))
					p.nodes.append(GSNode([wav[wavlen / 2][0], wav[wavlen / 2][1]], type=GSLINE))
					for n in reversed(wav2a):
						p.nodes.append(GSNode([n[0], n[1]], type=GSLINE))
				except:
					pass

			if len(lines1) == 2 and len(lines2) == 1:
				try:
					wav = waves[w + 1][0]
					wav2a = waves[w + 0][0]
					wav2b = waves[w + 0][1]
					wavlen = len(wav)
					wav2alen = len(wav2a)
					# wav2blen = len(wav2a)
					# new_wave1top = wav [ 0 : wav2alen ]
					p = GSPath()
					for n in reversed(wav2b):
						p.nodes.append(GSNode([n[0], n[1]], type=GSLINE))
					p.nodes.append(GSNode([wav[wav2alen][0], wav[wav2alen][1]], type=GSLINE))
					for n in reversed(wav2a):
						p.nodes.append(GSNode([n[0], n[1]], type=GSLINE))
					for n in wav:
						p.nodes.append(GSNode([n[0], n[1]], type=GSLINE))
				except:
					pass
			try:
				if p is not None:
					p.closed = True
					if p.direction == 1:
						p.reverse()
					wavepaths.append(p)
			except:
				pass

		return wavepaths
	else:
		return None


SeaCamouflage()
