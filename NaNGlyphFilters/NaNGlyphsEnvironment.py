# Abstract out the differences between Glyphs 2, Glyphs 3 and glyphsLib
class Glyphs2:
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
        self.layer.paths.remove(path)

    @classmethod
    def offset_layer(cls, layer, hoffset, voffset, make_stroke=False, position=0.5):
        try:
            import objc

            offsetCurveFilter = objc.lookUpClass("GlyphsFilterOffsetCurve")
            offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_(
                Layer, hoffset, voffset, make_stroke, False, 0.5, None, None
            )
        except Exception as e:
            print("offset failed", e)


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
        self.layer.shapes.remove(path)

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
    def remove_overlap(cls, layer):
        raise NotImplementedError

    def calculate_intersections(cls, layer):
        raise NotImplementedError

    @classmethod
    def check_path_connections(cls, path):
        raise NotImplementedError

    @classmethod
    def offset_layer(cls, layer, hoffset, voffset, position=0.5):
        raise NotImplementedError


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
