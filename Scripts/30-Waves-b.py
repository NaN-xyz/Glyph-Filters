#MenuTitle: 30. Waves b
# -*- coding: utf-8 -*-
# __doc__="""
# 30. Waves b
# """

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *

# COMMON
font = Glyphs.font
selectedGlyphs = beginFilterNaN(font)


# ====== OFFSET LAYER CONTROLS ================== 

def doOffset( Layer, hoffset, voffset ):
	try:
		offsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
		offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_( Layer, hoffset, voffset, False, False, 0.5, None,None)
	except Exception as e:
		print("offset failed")

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



# THE MAIN NOISE WAVE FUNCTION ACTION

def NoiseWaves(thislayer, outlinedata, b, minsize, maxsize):

	noisescale = 0.002
	yshift = maxsize/4

	if b is not None:

		tx = b[0]
		ty = b[1]
		tw = b[2]
		th = b[3]

		seedx = random.randrange(0,100000)
		seedy = random.randrange(0,100000)

		waves = []
		searchstep=2

		for y in range(ty, ty+th, 20):

			lines = []
			wave = []

			for x in range(tx, tx+tw + 40, searchstep):

				if withinGlyphBlack(x, y, outlinedata):

					noiz = abs ( snoise2( (y+seedy)*noisescale,(x+seedx)*noisescale, 4) )
					size = noiseMap( noiz, minsize, maxsize )
					wave.append([x, y+size-yshift])
				
				else:

					if len(wave)>4:

						lines.append(wave)
						del wave
						wave = []

			if len(lines)>0:
				waves.append(lines)

		wavepaths = []

		wavepaths = convertToWavePaths(waves)

		# wavepaths = []
		# # draw the wave data in to paths

		# for w in range(0, len(waves)-1, 2): #step 2

		# 	lines1 = waves[w]
		# 	lines2 = waves[w+1]

		# 	if len(lines1) == len(lines2):

		# 		for l in range(0, len(waves[w])):

		# 			wav = waves[w][l]
		# 			wav2 = waves[w+1][l]
		# 			wav2 = wav2[::-1]

		# 			p = []

		# 			p.extend(wav+wav2)
		# 			np = convertToFitpath(p, True)
		# 			wavepaths.append(np)

		return wavepaths
		

def convertToWavePaths(waves):

	wavepaths = []

	for w in range(0, len(waves)-1, 2): #step 2

		lines1 = waves[w]
		lines2 = waves[w+1]

		if len(lines1) == len(lines2):

			for l in range(0, len(waves[w])):

				wav = waves[w][l]
				wav2 = reversed(waves[w+1][l])

				p = GSPath()
				for n in wav: p.nodes.append(GSNode([n[0], n[1]], type = GSLINE))
				for n in wav2: p.nodes.append(GSNode([n[0], n[1]], type = GSLINE))

		if len(lines1)==1 and len(lines2)==2:

			try:

				wav = waves[w][0]
				wav2a = waves[w+1][0]
				wav2b = waves[w+1][1]
				#print wav, wav2a, wav2b

				wavlen = len(wav)
				wav2alen = len(wav2a)
				wav2blen = len(wav2a)

				#if wavlen>(wav2alen+wav2blen):

				new_wave1top = wav [ 0 : wav2alen ]

				p = GSPath()
				for n in wav: p.nodes.append(GSNode([n[0], n[1]], type = GSLINE))
				for n in reversed(wav2b): p.nodes.append(GSNode([n[0], n[1]], type = GSLINE))
				p.nodes.append(GSNode([ wav[wavlen/2][0], wav[wavlen/2][1] ], type = GSLINE))
				for n in reversed(wav2a): p.nodes.append(GSNode([n[0], n[1]], type = GSLINE))

			except:

				pass


		if len(lines1)==2 and len(lines2)==1:

			try:

				wav = waves[w+1][0]
				wav2a = waves[w+0][0]
				wav2b = waves[w+0][1]

				wavlen = len(wav)
				wav2alen = len(wav2a)
				wav2blen = len(wav2a)
				new_wave1top = wav [ 0 : wav2alen ]

				p = GSPath()
				for n in reversed(wav2b): p.nodes.append(GSNode([n[0], n[1]], type = GSLINE))
				p.nodes.append(GSNode([ wav[wav2alen][0], wav[wav2alen][1] ], type = GSLINE))
				for n in reversed(wav2a): p.nodes.append(GSNode([n[0], n[1]], type = GSLINE))
				for n in wav: p.nodes.append(GSNode([n[0], n[1]], type = GSLINE))

			except:

				pass

		try:
			if p!=None:
				p.closed = True
				if p.direction==1: p.reverse()
				wavepaths.append(p)
		except:
			pass


	return wavepaths


def OutputWaves(minsize, maxsize):

	for glyph in selectedGlyphs:

		glyph.beginUndo()
		beginGlyphNaN(glyph)

		# --- °°°°°°°

		thislayer = font.glyphs[glyph.name].layers[0]
		thislayer.beginChanges()

		# ---
		
		glyphsize = glyphSize(glyph)

		if glyphsize=="S": 
			offset = -4 
			iterations = 0
		if glyphsize=="M": 
			offset = -4
			iterations = 0
		if glyphsize=="L": 
			offset = -4
			iterations = 0

		# ----

		offsetpaths = saveOffsetPaths(thislayer, 0, 0, removeOverlap=True)
		pathlist = doAngularizzle(offsetpaths, 20)
		bounds = AllPathBoundsFromPathList(pathlist)
		outlinedata = getGlyphCoords(pathlist)

		wavepaths = NoiseWaves(thislayer, outlinedata, bounds, minsize, maxsize)
		ClearPaths(thislayer)
		#rockpaths = MoonRocks(thislayer, outlinedata, iterations, maxgap, shapetype)
		
		wavepaths = ConvertPathlistDirection(wavepaths, -1)
		AddAllPathsToLayer(wavepaths, thislayer)

		# ---

		thislayer.endChanges()

		# --- °°°°°°°

		endGlyphNaN(glyph)
		glyph.endUndo()


# =======

OutputWaves(40, 200)

# =======

#OutputFur()
#OutputSpikes()

endFilterNaN(font)







