from NaNGlyphsEnvironment import GSNode, GSPath, GSLINE
import math


__all__ = [
	"getListOfPoints", "ConvertPathsToLineSegments", "StripDetail", "RemoveDuplicatePts",
	"GetPoint", "CreatePointList", "CreateDistList", "FindPosInDistList", "ListToPath",
	"PointToPointSteps", "ReturnNodesAlongPath", "Direction"
]


class Direction():
	ANTICLOCKWISE = -1
	CLOCKWISE = 1


STEPNUM = 130
STEPSIZE = 1.0 / STEPNUM  # !impt


def getListOfPoints(pathlist):

	listOfPoints = []

	for path in pathlist:
		thispath = [[node.position.x, node.position.y] for node in path.nodes]
		listOfPoints.append([path.direction, thispath])

	return listOfPoints


def ConvertPathsToLineSegments(pathlist, segs):
	if len(pathlist) == 0:
		return []

	ang = ReturnNodesAlongPath(pathlist, segs)

	if ang is None:
		print("Returned no nodes along path")
		return []

	newpaths = []
	for _, isclosed, pts in ang:
		newpaths.append(ListToPath(pts, isclosed))

	return newpaths


def StripDetail(pathlist, segsize):

	newList = list()

	for path in pathlist:
		newnodes = list()
		length, isclosed, nodelist = path
		prevX, prevY = nodelist[0]

		for thisX, thisY in nodelist[1:]:
			dist = math.hypot(thisX - prevX, thisY - prevY)

			if dist < segsize:
				continue

			newnodes.append([prevX, prevY])
			prevX = thisX
			prevY = thisY

		nl = [length, isclosed, newnodes]
		newList.append(nl)

	return newList


# Remove any duplicate points from list
def RemoveDuplicatePts(ptlist):
	ptl = []
	for i in ptlist:
		if i not in ptl:
			ptl.append(i)

	ptl.append(ptlist[-1])
	return ptl


# the main return t postion on curve script p0, 1, 2, 3 is segment
def GetPoint(p0, p1, p2, p3, t):

	ax = lerp([p0[0], p1[0]], t)
	ay = lerp([p0[1], p1[1]], t)
	bx = lerp([p1[0], p2[0]], t)
	by = lerp([p1[1], p2[1]], t)
	cx = lerp([p2[0], p3[0]], t)
	cy = lerp([p2[1], p3[1]], t)
	dx = lerp([ax, bx], t)
	dy = lerp([ay, by], t)
	ex = lerp([bx, cx], t)
	ey = lerp([by, cy], t)

	pointx = lerp([dx, ex], t)
	pointy = lerp([dy, ey], t)

	calc = [pointx, pointy]
	return calc


# Put all the xy coords of linear t GetPoint() increments in list
def CreatePointList(p0, p1, p2, p3):
	pl = list()
	for i in range(0, STEPNUM):
		pl.append(GetPoint(p0, p1, p2, p3, float(i) / STEPNUM))
	return pl


def lerp(v, d):
	return v[0] * (1 - d) + v[1] * d


# create distance look up list from pointlist so we can determine a % position along spine
# each item represents cumulative distances from beginning of segments
def CreateDistList(pointlist):

	lookup = [0]
	totallength = 0

	for tp in range(0, len(pointlist) - 1):
		p1x, p1y = pointlist[tp]
		p2x, p2y = pointlist[tp + 1]
		totallength += math.hypot(p2x - p1x, p2y - p1y)
		lookup.append(totallength)

	return lookup


# find at which index the desired length matches to determine nearest t step value
# return new precise t value between the two indexes desiredlen falls
def FindPosInDistList(lookup, newlen):  # newlen = length along curve

	for s in range(0, len(lookup) - 1):

		b1 = lookup[s]
		b2 = lookup[s + 1]

		if b1 <= newlen <= b2:
			if b1 == 0:
				newt = 0
			else:
				proportion = (newlen - b1) / (b2 - b1)
				newt = (s * STEPSIZE) + (STEPSIZE * proportion)
			return (newt)


# Draw new angular path from list
def ListToPath(ptlist, isopen):
	np = GSPath()

	if len(ptlist) <= 2:
		return np
	if isopen:
		del ptlist[-1]

	for pt in ptlist:
		newnode = GSNode()
		newnode.type = GSLINE
		newnode.position = (pt[0], pt[1])
		np.nodes.append(newnode)
	np.closed = isopen  # XXX
	return np


def PointToPointSteps(tp0, tp1, spacebetween):
	if tp0 == tp1:
		return []

	tmplist = list()
	n1x, n1y = tp0
	n2x, n2y = tp1

	dist = math.hypot(n2x - n1x, n2y - n1y)

	currentx = n1x
	currenty = n1y

	psteps = int(math.ceil(dist / spacebetween))

	stepx = (n2x - n1x) / psteps
	stepy = (n2y - n1y) / psteps

	for n in range(psteps):
		tmplist.append([currentx, currenty])
		currentx += stepx
		currenty += stepy

	return tmplist


# returns nodes along a curve at intervals of space between
def ReturnNodesAlongPath(GlyphStartPaths, spacebetween):

	allPaths = list()
	for path in GlyphStartPaths:

		pathTotalLength = 0
		allpointslist = []

		for segment in path.segments:
			# if straight segment
			if len(segment) == 2:
				tp0 = (segment[0].x, segment[0].y)
				tp1 = (segment[1].x, segment[1].y)

				pathTotalLength += math.hypot(tp1[0] - tp0[0], tp1[1] - tp0[1])
				allpointslist.extend(PointToPointSteps(tp0, tp1, spacebetween))

			# if bezier curve segment
			else:
				tp0 = (segment[0].x, segment[0].y)
				tp1 = (segment[1].x, segment[1].y)
				tp2 = (segment[2].x, segment[2].y)
				tp3 = (segment[3].x, segment[3].y)

				pointlist = CreatePointList(tp0, tp1, tp2, tp3)
				lookup = CreateDistList(pointlist)
				totallength = lookup[-1]
				pathTotalLength += totallength

				# check that the distance of curve segment is at least as big as spacebetween jump
				if totallength > spacebetween:
					steps = int(math.floor(totallength / spacebetween))
					stepinc = totallength / steps
					dlen = 0  # distance to check in list of distances

					for s in range(0, steps + 1):

						if s == 0:
							newt = 0
						elif s == steps:
							newt = 1
						else:
							newt = FindPosInDistList(lookup, dlen)

						calc = GetPoint(tp0, tp1, tp2, tp3, newt)
						allpointslist.append(calc)
						dlen += stepinc
				else:
					allpointslist.extend([tp0, tp3])

		if allpointslist:
			allpointslist = RemoveDuplicatePts(allpointslist)
			pathdata = [pathTotalLength, path.closed, allpointslist]
			allPaths.append(pathdata)

	return allPaths
