# Abstract out the differences between Glyphs 2, Glyphs 3 and glyphsLib
class Glyphs2:
    is_interactive = True

    @classmethod
    def clear_paths(cls, thislayer):
        thislayer.paths = []

    @classmethod
    def calculate_intersections(cls, layer, p1, p2, b):
        layer.calculateIntersectionsStartPoint_endPoint_decompose_(p1, p2, True)

    @classmethod
    def layer_bounds(cls, thislayer):
        x = int(thislayer.bounds.origin.x)
        y = int(thislayer.bounds.origin.y)
        w = int(thislayer.bounds.size.width)
        h = int(thislayer.bounds.size.height)
        return x, y, w, h

    @classmethod
    def path_bounds(cls, thispath):
        x = int(thispath.bounds.origin.x)
        y = int(thispath.bounds.origin.y)
        w = int(thispath.bounds.size.width)
        h = int(thispath.bounds.size.height)
        return x, y, w, h

    @classmethod
    def add_components(cls, layer, components):
        layer.components.extend(components)

    @classmethod
    def add_paths(cls, layer, paths):
        layer.paths.extend(paths)

    @classmethod
    def remove_overlap(cls, layer):
        layer.removeOverlap()
        return layer

    @classmethod
    def check_path_connections(cls, path):
        path.checkConnections()

    @classmethod
    def correct_path_direction(cls, layer):
        layer.correctPathDirection()

    @classmethod
    def remove_node(cls, path, node, keepshape=True):
        if keepshape:
            path.removeNodeCheckKeepShape_(node)
        else:
            path.removeNodeCheck_(node)

    @classmethod
    def remove_path_from_layer(cls, layer, path):
        layer.paths.remove(path)

    @classmethod
    def offset_layer(cls, layer, hoffset, voffset, make_stroke=False, position=0.5):
        try:
            import objc

            offsetCurveFilter = objc.lookUpClass("GlyphsFilterOffsetCurve")
            offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_(
                layer, hoffset, voffset, make_stroke, False, 0.5, None, None
            )
        except Exception as e:
            print("offset failed", e)

    @classmethod
    def selected_glyphs(cls, font):
        return [l.parent for l in font.selectedLayers]

    @classmethod
    def disable_updates(cls, font):
        font.disableUpdateInterface()

    @classmethod
    def enable_updates(cls, font):
        font.enableUpdateInterface()

    @classmethod
    def begin_undo(cls, glyph):
        glyph.beginUndo()

    @classmethod
    def end_undo(cls, glyph):
        glyph.endUndo()

    @classmethod
    def begin_layer_changes(cls, layer):
        layer.beginChanges()

    @classmethod
    def end_layer_changes(cls, layer):
        layer.endChanges()

    @classmethod
    def copy_layer(cls, layer):
        return layer.copy()

    @classmethod
    def cut_layer(cls, layer, pt1, pt2):
        layer.cut_between_points(pt1, pt2)

    @classmethod
    def clean_up_paths(cls, thislayer):
        thislayer.cleanUpPaths()


class Glyphs3(Glyphs2):
    @classmethod
    def clear_paths(cls, thislayer):
        thislayer.shapes = [x for x in thislayer.shapes if isinstance(x, GSComponent)]

    @classmethod
    def add_components(cls, layer, components):
        layer.shapes.extend(components)

    @classmethod
    def add_paths(cls, layer, paths):
        layer.shapes.extend(paths)

    @classmethod
    def remove_path_from_layer(cls, layer, path):
        layer.shapes.remove(path)

    @classmethod
    def offset_layer(cls, layer, hoffset, voffset, make_stroke=False, position=0.5):
        try:
            import objc
            from AppKit import NSButtLineCapStyle

            offsetCurveFilter = objc.lookUpClass("GlyphsFilterOffsetCurve")
            offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_capStyle_(
                Layer,
                hoffset,
                voffset,
                make_stroke,
                False,
                0.5,
                None,
                None,
                NSButtLineCapStyle,
            )
        except Exception as e:
            print("offset failed", e)


class GlyphsLib(Glyphs2):
    is_interactive = False

    @classmethod
    def remove_overlap(cls, layer):
        from pathops import union
        import ufoLib2
        from glyphsLib.builder import UFOBuilder, GlyphsBuilder
        ufo_glyph = ufoLib2.objects.Glyph()
        UFOBuilder(Glyphs.font).to_ufo_paths(ufo_glyph, layer)
        contours = list(ufo_glyph)
        ufo_glyph.clearContours()
        pen = ufo_glyph.getPen()
        union(contours, pen)
        layer.paths = []
        GlyphsBuilder(ufos=[ufoLib2.objects.Font()]).to_glyphs_paths(ufo_glyph, layer)
        return layer

    @classmethod
    def calculate_intersections(cls, layer, p1, p2, b):
        raise NotImplementedError

    @classmethod
    def check_path_connections(cls, path):
        raise NotImplementedError

    @classmethod
    def offset_layer(cls, layer, hoffset, voffset, position=0.5, make_stroke=False):
        import ufostroker
        import ufoLib2
        from glyphsLib.builder import UFOBuilder, GlyphsBuilder
        class MyUFOBuilder(UFOBuilder):
            def _is_vertical(self):
                return False
        if hoffset == 0 and voffset == 0:
            return
        ufo_glyph = ufoLib2.objects.Glyph()
        MyUFOBuilder(Glyphs.font).to_ufo_paths(ufo_glyph, layer)
        ufostroker.constant_width_stroke(ufo_glyph, width=hoffset*2, remove_internal=(not make_stroke), jointype="round")
        layer.paths = []
        # Sometimes a degenerate path is produced
        ufo_glyph.contours = [ x for x in ufo_glyph.contours if len(x) > 2]
        GlyphsBuilder(ufos=[ufoLib2.objects.Font()]).to_glyphs_paths(ufo_glyph, layer)
        for p in layer.paths:
            p.nodes = list(reversed(p.nodes))

    @classmethod
    def remove_node(cls, path, node, keepshape=True):
        if keepshape:
            raise NotImplementedError
        else:
            path.nodes.remove(node)

    @classmethod
    def selected_glyphs(cls, font):
        return font.glyphs

    @classmethod
    def disable_updates(cls, font):
        pass

    @classmethod
    def enable_updates(cls, font):
        pass

    @classmethod
    def begin_undo(cls, glyph):
        pass

    @classmethod
    def end_undo(cls, glyph):
        pass

    @classmethod
    def begin_layer_changes(cls, layer):
        pass

    @classmethod
    def end_layer_changes(cls, layer):
        pass

    @classmethod
    def copy_layer(cls, layer):
        import copy

        oldparent = layer.parent
        layer.parent = None
        newlayer = copy.deepcopy(layer)
        newlayer.parent = layer.parent = oldparent
        return newlayer

    @classmethod
    def check_path_connections(cls, path):
        for ix, n in enumerate(path.nodes):
            if n.type != "curve":
                continue
            if not (path.nodes[ix-1].type == "offcurve" and path.nodes[ix+1].type == "offcurve"):
                continue
            import IPython;IPython.embed()

    @classmethod
    def correct_path_direction(cls, layer):
        for p in layer.paths:
            # XXX
            pass

    @classmethod
    def cut_layer(cls, layer, pt1, pt2):
        raise NotImplementedError

    @classmethod
    def clean_up_paths(cls, thislayer):
        pass

# Now, let's find out where we are.
try:
    from GlyphsApp import *

    # We're glyphs, which one?
    if Glyphs.versionString[0] == "3":
        glyphsEnvironment = Glyphs3
    else:
        glyphsEnvironment = Glyphs2
except Exception as e:
    glyphsEnvironment = GlyphsLib
