# MenuTitle: Zebra
# -*- coding: utf-8 -*-
__doc__ = """
Zebra
"""

# from GlyphsApp import Glyphs
from NaNGFGraphikshared import withinGlyphBlack, convertToFitpath, AllPathBounds, ClearPaths, ConvertPathlistDirection, AddPaths
from NaNFilter import NaNFilter
import random
from NaNGlyphsEnvironment import glyphsEnvironment as G
# from NaNGFNoise import noiseMap

try:
	from itertools import izip
except ImportError:
	izip = zip


# Note that this is *not* the same as the pairwise recipe in the itertools page
def pairs(iterable):
	"s -> (s0, s1), (s2, s3), (s4, s5), ..."
	a = iter(iterable)
	return izip(a, a)


# THE MAIN NOISE WAVE FUNCTION ACTION


def NoiseWaves(outlinedata, b, minsize, maxsize):

	# noisescale = 0.002
	yshift = maxsize / 4

	if b is None:
		print("No bounds")
		return []

	tx, ty, tw, th = b
	# seedx = random.randrange(0, 100000)
	# seedy = random.randrange(0, 100000)

	waves = []
	searchstep = 20
	step = 11

	for y in range(ty, ty + th, step):
		lines = []
		wave = []

		for x in range(tx, tx + tw + 40, searchstep):
			if withinGlyphBlack(x, y, outlinedata):
				# size = noiseMap(random.random(), minsize, maxsize)
				size = random.random() * (maxsize - minsize) + minsize
				wave.append([x, y + size - yshift])
			elif len(wave) > 4:
				lines.append(wave)
				wave = []

		if lines:
			waves.append(lines)

	wavepaths = []
	# draw the wave data in to paths

	for lines1, lines2 in pairs(waves):
		if len(lines1) != len(lines2):
			continue

		for wav, wav2 in zip(lines1, lines2):
			np = convertToFitpath(wav + list(reversed(wav2)), True)
			wavepaths.append(np)

	return wavepaths


class Zebra(NaNFilter):
	minsize, maxsize = 1, 10

	def processLayer(self, thislayer, params):
		bounds = AllPathBounds(thislayer)

		outlinedata = G.outline_data_for_hit_testing(thislayer)

		wavepaths = NoiseWaves(outlinedata, bounds, self.minsize, self.maxsize)

		ClearPaths(thislayer)
		wavepaths = ConvertPathlistDirection(wavepaths, -1)

		shifty = -20
		for path in wavepaths:
			path.applyTransform((1, 0.0, 0.0, 1, 0, shifty))

		AddPaths(wavepaths, thislayer)


Zebra()
