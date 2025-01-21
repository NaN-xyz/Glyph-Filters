from NaNGFGraphikshared import pathCenterPoint, withinGlyphBlack, drawSimplePath
import math
import random


# strip out colour list item [2]
def SimplifyTriangleList(triangle):
	newtri = []
	for node in triangle:
		newtri.append([node[0], node[1]])
	return newtri


def PathToNodeList(path):
	np = []
	for node in path.nodes:
		np.append([node.position.x, node.position.y])
	return np


def ReturnNearestPath(px, py, searchlist, variance, centers=None):

	newx = 0
	newy = 0
	dist = 9999999
	cid = 9999999
	px += random.randrange(variance * -1, variance)
	py += random.randrange(variance * -1, variance)

	for item in range(0, len(searchlist)):
		cl = searchlist[item]
		if centers:
			center = centers[item]
		else:
			center = pathCenterPoint(cl)
		nx = center[0]
		ny = center[1]
		testdist = math.hypot(px - nx, py - ny)

		if testdist < dist:
			newx = nx
			newy = ny
			cid = item
			dist = testdist

	return [newx, newy, dist, cid]


def ReturnNearestPoint(px, py, outlinedata):

	newx = 0
	newy = 0
	dist = 9999999

	for path in outlinedata:
		outline = path[1]
		for node in outline:
			nx = node[0]
			ny = node[1]
			testdist = math.hypot(px - nx, py - ny)
			if testdist < dist:
				newx = nx
				newy = ny
				dist = testdist

	return [newx, newy]


def makeIsometricGrid(bounds, gridsize):

	mx = bounds[0]
	my = bounds[1]
	w = bounds[2]
	h = bounds[3]

	cols = int(math.ceil(w / float(gridsize)))
	rows = int(math.ceil(h / float(gridsize)))
	lines = []
	# alltriangles = []
	mx -= gridsize
	my -= gridsize

	for y in range(0, rows + 2):
		line = []
		for x in range(0, cols + 2):
			ny = my + (y * gridsize)
			if y % 2 == 0:
				nx = mx + (x * gridsize)
			else:
				nx = mx + (x * gridsize + (gridsize / 2))
			line.append([nx, ny])
		lines.append(line)

	return lines


def returnTriangleTypes(alltriangles, outlinedata):

	in_triangles = []
	out_triangles = []  # including overlaps

	for triangle in alltriangles:

		p1, p2, p3 = triangle[0], triangle[1], triangle[2]

		if withinGlyphBlack(p1[0], p1[1], outlinedata) or withinGlyphBlack(p2[0], p2[1], outlinedata) or withinGlyphBlack(p3[0], p3[1], outlinedata):
			if withinGlyphBlack(p1[0], p1[1], outlinedata) and withinGlyphBlack(p2[0], p2[1], outlinedata) and withinGlyphBlack(p3[0], p3[1], outlinedata):
				in_triangles.append(triangle)
			else:
				out_triangles.append(triangle)

	return [in_triangles, out_triangles]


def StickTrianglesToOutline(out_triangles, outlinedata):

	edge_triangles = []

	for triangle in out_triangles:

		tri = []

		for node in triangle:
			px = node[0]
			py = node[1]
			if not withinGlyphBlack(px, py, outlinedata):
				newnode = ReturnNearestPoint(px, py, outlinedata)
				tri.append([newnode[0], newnode[1], node[2]])
			else:
				tri.append([px, py, node[2]])

		edge_triangles.append(tri)

	edge_triangles = RemoveTrianglesWithCentroidInWhite(edge_triangles, outlinedata)

	return edge_triangles


def RemoveTrianglesWithCentroidInWhite(edge_triangles, outlinedata):

	nedge = []

	for tri in edge_triangles:

		ax, ay = tri[0][0], tri[0][1]
		bx, by = tri[1][0], tri[1][1]
		cx, cy = tri[2][0], tri[2][1]

		centroidx = (ax + bx + cx) / 3
		centroidy = (ay + by + cy) / 3

		if withinGlyphBlack(centroidx, centroidy, outlinedata):
			nedge.append(tri)

	return nedge


def ReturnOutlineOverlappingTriangles(out_triangles, outlinedata):

	edge_triangles = []

	for triangle in out_triangles:

		# tri = []

		for node in triangle:
			px = node[0]
			py = node[1]
			if not withinGlyphBlack(px, py, outlinedata):
				edge_triangles.append(triangle)
				# tripath = drawSimplePath(triangle)
				break

	return edge_triangles


def TrianglesListToPaths(triangle_list):
	newtris = []
	for triangle in triangle_list:
		newshape = drawSimplePath(triangle)
		newtris.append(newshape)
	return newtris


def BreakUpSpace(thislayer, looptriangles, gridsize, maxchain):

	groups = []
	group = []
	current_tri_id = random.randrange(0, len(looptriangles))
	counter, chaincounter = 0, 0
	variance = gridsize + 2
	centers = [pathCenterPoint(p) for p in looptriangles]

	while len(looptriangles) > 0:

		current_tri = looptriangles[current_tri_id]
		center = centers[current_tri_id]
		x = center[0]
		y = center[1]
		looptriangles.pop(current_tri_id)
		centers.pop(current_tri_id)
		next_tri = ReturnNearestPath(x, y, looptriangles, variance, centers=centers)

		# nx = next_tri[0]
		# ny = next_tri[1]
		dist = next_tri[2]
		nid = next_tri[3]

		if dist < 270 and chaincounter < maxchain:
			current_tri_id = nid
			group.append(current_tri)
			# temp_tri = looptriangles[nid]
			chaincounter += 1
		else:
			chaincounter = 0
			current_tri_id = nid
			group.append(current_tri)
			groups.append(group)
			del group
			group = []

		counter += 1

	return groups


def IsoGridToTriangles(lines):

	alltriangles = []

	for n in range(0, len(lines) - 1):
		line = lines[n]
		line2 = lines[n + 1]
		for s in range(len(line) - 1):

			line1_nx1 = line[s][0]
			line1_ny1 = line[s][1]
			line1_nx2 = line[s + 1][0]
			line1_ny2 = line[s + 1][1]
			line2_nx1 = line2[s][0]
			line2_ny1 = line2[s][1]
			line2_nx2 = line2[s + 1][0]
			line2_ny2 = line2[s + 1][1]
			line2_nx3 = line2[s - 1][0]
			line2_ny3 = line2[s - 1][1]
			tri1, tri2 = [], []
			# colour switch
			if n % 2 == 0:
				if s % 2 == 0:
					col1 = "black"
					col2 = "white"
			else:
				if s % 2 == 0:
					col1 = "white"
					col2 = "black"

			if n % 2 == 0:
				tri1.append([line1_nx1, line1_ny1, col1])
				tri1.append([line2_nx1, line2_ny1, col1])
				tri1.append([line1_nx2, line1_ny2, col1])
				alltriangles.append(tri1)
				if s > 0:
					tri2.append([line1_nx1, line1_ny1, col2])
					tri2.append([line2_nx1, line2_ny1, col2])
					tri2.append([line2_nx3, line2_ny3, col2])
					alltriangles.append(tri2)
			else:
				tri1.append([line1_nx1, line1_ny1, col1])
				tri1.append([line2_nx1, line2_ny1, col1])
				tri1.append([line2_nx2, line2_ny2, col1])
				tri2.append([line1_nx1, line1_ny1, col2])
				tri2.append([line2_nx2, line2_ny2, col2])
				tri2.append([line1_nx2, line1_ny2, col2])
				alltriangles.append(tri1)
				alltriangles.append(tri2)

	return alltriangles


def RandomiseIsoPoints(lines, gridsize):

	maxmove = int(gridsize / 3)
	# noisescale = 4
	# seedx = random.randrange(0, 100000)
	# seedy = random.randrange(0, 100000)
	# minshift = 0
	# maxshift = gridsize*1.2
	nstep = 0

	for n in range(0, len(lines)):
		line = lines[n]
		for l in range(0, len(line)):

			x = lines[n][l][0]
			y = lines[n][l][1]

			rx = random.randrange(maxmove * -1, maxmove)
			ry = random.randrange(maxmove * -1, maxmove)

			lines[n][l][0] = x + rx
			lines[n][l][1] = y + ry

			nstep += 8

	return lines
