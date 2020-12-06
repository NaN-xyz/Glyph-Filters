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


def roughenLines(lines, depth):

    newlines = []
    stepsize = 15
    noisescale = 0.01
    seedx = random.randrange(0,100000)
    seedy = random.randrange(0,100000)
    minshift = 0
    maxshift = 3
    nstep = 0

    for l1, l2 in lines:

        for n in range(0, len(l1)):

            x1, y1 = l1[n][0], l1[n][1]
            x2, y2 = l2[n][0], l2[n][1]

            newline = []
            stepnum = math.floor( depth / stepsize ) 
            stepsize_x = (x2-x1) / stepnum
            stepsize_y = (y2-y1) / stepnum
            newx, newy = x1, y1
            step = 0

            while step < stepnum+1:

                x_noiz = pnoise1( (nstep+seedx)*noisescale, 3) 
                rx = noiseMap( x_noiz, minshift, maxshift )

                y_noiz = pnoise1( ((1000+nstep)+seedy)*noisescale, 3) 
                ry = noiseMap( y_noiz, minshift, maxshift )

                rx2 = random.randrange(-2,2)
                ry2 = random.randrange(-2,2)

                newline.append([newx, newy])
                newx += stepsize_x + rx + rx2
                newy += stepsize_y + ry + ry2

                step+=1
                nstep+=1

            newlines.append(newline)

    return newlines

