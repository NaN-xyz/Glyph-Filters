from NaNGFGraphikshared import *


def moonrocks(thislayer, outlinedata, iterations, shapetype = "blob", maxgap = 8):
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

        rad = random.randrange(10, 250)
        inside = True
        for n in range(0, len(list_dots)):
            nx, ny, nr = list_dots[n]
            dist = math.hypot(nx - x, ny - y)  # alt method

            if dist < (nr + rad + maxgap):
                inside = False
                break

        if not inside:
            continue
        circle = drawCircle(x, y, rad * 2, rad * 2)
        circlea = setGlyphCoords(doAngularizzle([circle], 10))
        circlecoords = circlea[0][1]

        if ShapeWithinOutlines(circlecoords, outlinedata):
            list_dots.append([x, y, rad])

    print("Number of circles found:", len(list_dots))

    rocks = []
    for c in range(0, len(list_dots)):
        x, y, size = list_dots[c]
        if shapetype == "blob":
            circle = drawBlob(x, y, size * 2, 5, True)
        else:
            circle = drawCircle(x, y, size * 2, size * 2)
        rocks.append(circle)

    rocks = ConvertPathlistDirection(rocks, 1)
    AddAllPathsToLayer(rocks, thislayer)
