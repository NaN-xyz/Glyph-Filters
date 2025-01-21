
import random
from NaNGFGraphikshared import convertToFitpath

try:
	from noise import pnoise1

except:
	def grad1(hash, x):
		grad = 1.0 + (hash & 7)
		if (hash & 8):
			grad = -1  # Copilot says this should be -grad and I think it's right
		return grad * x

	def lerp(a, b, x):
		return (a + x * (b - a))

	def _noise1(x, repeat, base):
		PERM = [151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53, 194, 233, 7, 225, 140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23, 190, 6, 148, 247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32, 57, 177, 33, 88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27, 166, 77, 146, 158, 231, 83, 111, 229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244, 102, 143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169, 200, 196, 135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64, 52, 217, 226, 250, 124, 123, 5, 202, 38, 147, 118, 126, 255, 82, 85, 212, 207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42, 223, 183, 170, 213, 119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9, 129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104, 218, 246, 97, 228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241, 81, 51, 145, 235, 249, 14, 239, 107, 49, 192, 214, 31, 181, 199, 106, 157, 184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205, 93, 222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180]
		fx = 0.0
		i = int(int(x) % repeat)
		ii = int((i + 1) % repeat)
		i = (i & 255) + base
		ii = (ii & 255) + base

		x -= int(x)
		fx = x * x * x * (x * (x * 6 - 15) + 10)

		return lerp(fx, grad1(PERM[i], x), grad1(PERM[ii], x - 1)) * 0.4

	def pnoise1(x, octaves):
		repeat = 1024
		persistence = 0.5
		lacunarity = 2.0
		base = 0
		total = 0
		freq = 1
		pmax = 0
		amp = 1
		while octaves > 0:
			total += _noise1(x * freq, repeat * freq, base) * amp
			pmax += amp
			freq *= lacunarity
			amp *= persistence
			octaves -= 1
		return total / pmax


def noiseMap(noise, min, max):
	multiplier = 1
	return min + ((max - min) * noise * multiplier)


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

		seedx = random.randrange(0, 100000)
		seedy = random.randrange(0, 100000)
		noisescale, minsize, maxsize = noisevars[0], noisevars[1], noisevars[2]

		n = 0
		newpath = []

		while n < nodelen:

			x_noiz = pnoise1((n + seedx) * noisescale, 3)
			x_size = noiseMap(x_noiz, minsize, maxsize)

			y_noiz = pnoise1(((1000 + n) + seedy) * noisescale, 3)
			y_size = noiseMap(y_noiz, minsize, maxsize)

			xadjust = 0 + x_size
			yadjust = 0 + y_size

			x = structure[n][0] + xadjust
			y = structure[n][1] + yadjust
			newpath.append([x, y])

			n += 1

		p = convertToFitpath(newpath, True)
		noisepaths.append(p)

	return noisepaths
