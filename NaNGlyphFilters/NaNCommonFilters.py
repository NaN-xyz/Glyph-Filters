from NaNGFGraphikshared import AllPathBounds, withinGlyphBlack, drawCircle, ShapeWithinOutlines, drawBlob, MakeVector, DistanceToNextBlack
from NaNGlyphsEnvironment import GSPath
from NaNGFAngularizzle import Direction
import random
import math


def generate_circle_polygon(center, radius, segment_length):
	"""
	Generates a polygon of points on a circle.

	Parameters:
		center (tuple): The (x, y) coordinates of the circle's center.
		radius (float): The radius of the circle.
		segment_length (float): The desired length of each segment.

	Returns:
		list: A list of (x, y) tuples representing the points on the circle.
	"""
	# Calculate the circumference of the circle
	circumference = 2 * math.pi * radius

	# Determine the number of points
	num_points = math.ceil(circumference / segment_length)

	# Calculate the angle step between points
	angle_step = (2 * math.pi) / num_points

	# Generate the points
	points = []
	for i in range(num_points):
		angle = i * angle_step
		x = center[0] + radius * math.cos(angle)
		y = center[1] + radius * math.sin(angle)
		points.append((x, y))

	return points


def moonrocks(thislayer, outlinedata, iterations, shapetype="blob", maxgap=8, maxsize=250):
	list_dots = []
	b = AllPathBounds(thislayer)

	if b is None:
		return

	ox, oy, w, h = b

	for f in range(0, iterations):

		x = random.randrange(ox, ox + w)
		y = random.randrange(oy, oy + h)

		if not withinGlyphBlack(x, y, outlinedata):
			continue

		rad = random.randrange(10, maxsize)
		inside = True
		for n in range(0, len(list_dots)):
			nx, ny, nr = list_dots[n]
			dist = math.hypot(nx - x, ny - y)

			if dist < (nr + rad + maxgap):
				inside = False
				break

		if not inside:
			continue

		circlecoords2 = generate_circle_polygon((x, y), rad, 10)
		if ShapeWithinOutlines(circlecoords2, outlinedata):
			list_dots.append([x, y, rad])

	# print("Number of circles found:", len(list_dots))

	rocks = []
	for c in range(0, len(list_dots)):
		x, y, size = list_dots[c]
		if shapetype == "blob":
			circle = drawBlob(x, y, size * 2, 5, size > 15)
		else:
			circle = drawCircle(x, y, size * 2, size * 2)
		rocks.append(circle)

	return rocks


def spikes(outlinedata, minpush, maxpush, minstep, maxstep, drawFunction):

	spikepaths = []

	for direction, structure in outlinedata:
		nodelen = len(structure)
		spike = GSPath()
		n = 0

		while n < nodelen:
			x1, y1 = structure[n]

			if direction == Direction.ANTICLOCKWISE:
				step = random.randrange(minstep, maxstep)
			else:
				step = random.randrange(minstep, maxstep // 2)

			if n + step >= nodelen - 1:
				break

			# --- set node pos for main or end
			if n < nodelen - 1:
				x2, y2 = structure[n + step]
				n += step
			else:
				x2, y2 = structure[0]

			a = math.atan2(y1 - y2, x1 - x2) + math.radians(90)

			midx, midy = x1 + ((x2 - x1) / 2), y1 + ((y2 - y1) / 2)

			pushdist = random.randrange(minpush, maxpush)

			linex, liney = MakeVector(pushdist, a)
			searchblack = DistanceToNextBlack([x1, y1], [x2, y2], outlinedata, 200)
			if direction == Direction.CLOCKWISE:
				linex *= 0.7
				liney *= 0.7
				pushdist *= 0.7

			if searchblack is not None and searchblack < 200:
				linex *= 0.7
				liney *= 0.7
				pushdist *= 0.7

			midx += linex
			midy += liney
			# if searchblack:
			drawFunction(spike, x1, y1, midx, midy, x2, y2, pushdist)

		spike.closed = True
		spikepaths.append(spike)
	return spikepaths
