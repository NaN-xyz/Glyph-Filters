from NaNGFGraphikshared import *
import traceback
import GlyphsApp
from Foundation import NSClassFromString
from NaNGFSpacePartition import *

class NaNFilter:
    def __init__(self):
        self.font = Glyphs.font
        selectedGlyphs = beginFilterNaN(self.font)
        self.setup()
        for glyph in selectedGlyphs:
            self.processGlyph(glyph)
        endFilterNaN(self.font)

    def setup(self):
        pass

    def processGlyph(self, glyph):
        glyph.beginUndo()
        beginGlyphNaN(glyph)

        thislayer = self.font.glyphs[glyph.name].layers[0]
        thislayer.beginChanges()
        #thislayer.correctPathDirection()
        if hasattr(self, "params"):
            params = self.params[glyphSize(glyph)]
        else:
            params = None
        self.processLayer(thislayer, params)

        self.removeSmallPaths(thislayer, NANGFSET["smallest_path"])
        self.removeSmallSegments(thislayer, NANGFSET["smallest_seg"], False)
        self.removeOpenPaths(thislayer)
        self.removeStrayPoints(thislayer) # see note for why this & above

        thislayer.endChanges()
        endGlyphNaN(glyph)
        glyph.endUndo()

    def processLayer(self, layer, params):
        raise NotImplementedError

    def doOffset(self, Layer, hoffset, voffset):
        try:
            offsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
            offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_(
                Layer, hoffset, voffset, False, False, 0.5, None, None
            )
        except Exception as e:
            print("offset failed")

    def saveOffsetPaths(self, Layer, hoffset, voffset, removeOverlap):
        templayer = Layer.copy()
        templayer.name = "tempoutline"
        currentglyph = Layer.parent
        currentglyph.layers.append(templayer)
        tmplayer_id = templayer.layerId
        self.doOffset(templayer, hoffset, voffset)
        if removeOverlap:
            templayer.removeOverlap()
        #templayer.correctPathDirection() # doesn't seem to work when placed here
        offsetpaths = templayer.paths
        del currentglyph.layers[tmplayer_id]
        return offsetpaths

    def expandMonoline(self, Layer, noodleRadius):
        try:
            offsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
            offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_( Layer, noodleRadius, noodleRadius, True, False, 0.5, None,None)
            Layer.correctPathDirection()
        except Exception as e:
            print(( "expandMonoline: %s\n%s" % (str(e), traceback.format_exc()) ))

    def expandMonolineFromPathlist(self, Paths, noodleRadius):
        Layer = GSLayer()
        for p in Paths: Layer.paths.append(p)
        try:
            offsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
            offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_( Layer, noodleRadius, noodleRadius, True, False, 0.5, None,None)
            Layer.correctPathDirection()
            monopaths = Layer.paths
            del Layer
            return monopaths
        except Exception as e:
            print(( "expandMonoline: %s\n%s" % (str(e), traceback.format_exc()) ))

    def SortCollageSpace(self, thislayer, outlinedata, outlinedata2, gridsize, bounds, action, randomize = False, snap=False):
        isogrid = makeIsometricGrid(bounds, gridsize)
        if randomize:
            isogrid = RandomiseIsoPoints(isogrid, gridsize)
        if snap:
            isogrid = SnapToGrid(isogrid, gridsize)
        alltriangles = IsoGridToTriangles(isogrid)

        # Return triangles within and without
        in_triangles, out_triangles = returnTriangleTypes(alltriangles, outlinedata)

        if action == "stick":
            edge_triangles = StickTrianglesToOutline(out_triangles, outlinedata)
            return TrianglesListToPaths(in_triangles + edge_triangles)
        elif action == "overlap":
            edge_triangles = ReturnOutlineOverlappingTriangles(out_triangles, outlinedata)
            # Just return the edges
            return TrianglesListToPaths(edge_triangles)
        else:
            raise NotImplementedError

    def removeSmallPaths(self, layer, maxdim):
        for p in reversed(layer.paths):
            w, h = p.bounds.size.width, p.bounds.size.height
            if w<maxdim and h<maxdim:
                layer.paths.remove(p)

    # https://github.com/mekkablue/Glyphs-Scripts/blob/master/Paths/Remove%20Short%20Segments.py         
    def removeSmallSegments(self, thisLayer, maxseg, keepshape):
        for thisPath in thisLayer.paths:
            for i in range(len(thisPath.nodes))[::-1]:
                thisNode = thisPath.nodes[i]
                prevNode = thisNode.prevNode
                if prevNode.type != OFFCURVE and thisNode.type != OFFCURVE:
                    xDistance = thisNode.x-prevNode.x
                    yDistance = thisNode.y-prevNode.y
                    if abs(xDistance) < maxseg and abs(yDistance) < maxseg:
                        if keepshape:
                            thisPath.removeNodeCheckKeepShape_( thisNode )
                        else:
                            thisPath.removeNodeCheck_( thisNode )

    def removeStrayPoints(self, thislayer):
        for p in reversed(thislayer.paths):
            if len(p.nodes)<3: thislayer.paths.remove(p)

    def removeOpenPaths(self, thislayer):
        pass
        # deleteing the segments seems to leave paths that are open but still have closed==True
        # for p in reversed(thislayer.paths):
        #     if p.closed==False: thislayer.paths.remove(p)

