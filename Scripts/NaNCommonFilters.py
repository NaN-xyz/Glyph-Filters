from NaNGFGraphikshared import *
import random


def moonrocks(thislayer, outlinedata, iterations, shapetype = "blob", maxgap = 8, maxsize=250):
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
        circle = drawCircle(x, y, rad * 2, rad * 2)
        circlea = getGlyphCoords(ConvertPathsToSkeleton([circle], 10))
        circlecoords = circlea[0][1]

        if ShapeWithinOutlines(circlecoords, outlinedata):
            list_dots.append([x, y, rad])

    #print("Number of circles found:", len(list_dots))

    rocks = []
    for c in range(0, len(list_dots)):
        x, y, size = list_dots[c]
        if shapetype == "blob":
            circle = drawBlob(x, y, size * 2, 5, size > 15)
        else:
            circle = drawCircle(x, y, size * 2, size * 2)
        rocks.append(circle)

    return rocks

def spikes(thislayer, outlinedata, minpush, maxpush, minstep, maxstep, drawFunction):

    spikepaths = []

    for direction, structure in outlinedata:
        nodelen = len(structure)
        spike = GSPath()
        n = 0

        while n < nodelen:
            x1, y1 = structure[n]

            if direction==Direction.ANTICLOCKWISE:
                step = random.randrange(minstep, maxstep)
            else:
                step = random.randrange(minstep, maxstep/2)

            if n+step>=nodelen-1:
                break

            # --- set node pos for main or end
            if n<nodelen-1:
                x2, y2 = structure[n+step]
                n+=step
            else:
                x2, y2 = structure[0]

            a = atan2(y1-y2, x1-x2) + radians(90)

            midx, midy = x1 + ((x2-x1)/2), y1 + ((y2-y1)/2)

            pushdist = random.randrange(minpush, maxpush)

            linex, liney = MakeVector(pushdist, a)

            searchblack = DistanceToNextBlack(thislayer, [x1, y1], [x2, y2], outlinedata, 200)

            if direction==Direction.CLOCKWISE:
                linex*=0.7
                liney*=0.7
                pushdist*=0.7

            if searchblack is not None and searchblack < 200:
                    linex*=0.7
                    liney*=0.7
                    pushdist*=0.7

            midx += linex
            midy += liney

            drawFunction(spike, x1, y1, midx, midy, x2, y2, pushdist)

        spike.closed = True
        spikepaths.append(spike)
    return spikepaths


