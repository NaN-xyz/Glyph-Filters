import GlyphsApp
from noise import *
import math, random
from NaNGFFitpath import *
import NaNGFGraphikshared

def noiseMap(noise, min, max):
	multiplier = 1
	return min + ( (max-min)*noise*multiplier )



def NoiseOutline(thislayer, outlinedata, noisevars=[0.03, 0, 20]):

	#
	#
	#   Need to modulate intensity of noise added 
	#   from beginning to end so there is a smooth transition.
	#
	#

	noisepaths = []

	for direction, structure in outlinedata:

		nodelen = len(structure)

		seedx = random.randrange(0,100000)
		seedy = random.randrange(0,100000)
		noisescale, minsize, maxsize = noisevars[0], noisevars[1], noisevars[2] 

		n = 0
		newpath = []

		while n < nodelen:

			x_noiz = pnoise1( (n+seedx)*noisescale, 3) 
			x_size = noiseMap( x_noiz, minsize, maxsize )

			y_noiz = pnoise1( ((1000+n)+seedy)*noisescale, 3) 
			y_size = noiseMap( y_noiz, minsize, maxsize )

			xadjust = 0 + x_size
			yadjust = 0 + y_size

			x = structure[n][0] + xadjust
			y = structure[n][1] + yadjust
			newpath.append([x,y])

			n+=1

		p = convertToFitpath(newpath, True)
		noisepaths.append(p) 

	return noisepaths



