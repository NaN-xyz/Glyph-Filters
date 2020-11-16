import GlyphsApp
from noise import *
import math, random
from NaNGFFitpath import *



def noiseMap(noise, min, max):
	multiplier = 1
	return min + ( (max-min)*noise*multiplier )



def NoiseOutline(thislayer, outlinedata):

	#
	#
	#   Need to modulate intensity of noise added 
	#   from beginning to end so there is a smooth transition.
	#
	#

	noisepaths = []

	for path in outlinedata:

		direction = path[0]
		structure = path[1]

		nodelen = len(structure)

		noisescale = 0.03
		seedx = random.randrange(0,100000)
		seedy = random.randrange(0,100000)
		minsize = 0
		maxsize = 20

		n = 0

		newpath = []

		while n < nodelen:

			# x_noiz = abs ( snoise2( (n+seedy)*noisescale,(n+seedx)*noisescale, 4) )
			x_noiz = pnoise1( (n+seedx)*noisescale, 3) 
			x_size = noiseMap( x_noiz, minsize, maxsize )

			y_noiz = pnoise1( ((1000+n)+seedy)*noisescale, 3) 
			y_size = noiseMap( y_noiz, minsize, maxsize )

			#print x_noiz #, x_size, y_size

			xadjust = 0 + x_size
			yadjust = 0 + y_size

			# xadjust = 0 - (maxsize/2) + x_size
			# yadjust = 0 - (maxsize/2) + y_size

			x = structure[n][0] + xadjust
			y = structure[n][1] + yadjust

			#print x, y
			newpath.append([x,y])

			n+=1

		#p = drawSimplePath(newpath)

		p = convertToFitpath(newpath, True)
		noisepaths.append(p) 
		#thislayer.paths.append(p)

	return noisepaths


