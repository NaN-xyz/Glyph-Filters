from NaNGlyphsEnvironment import glyphsEnvironment as G
import time

__all__ = [
	"beginFilterNaN",
	"beginGlyphNaN",
	"endGlyphNaN",
	"endFilterNaN",
	"glyphSize",
	"NANGFSET",
]
# Misc settings

NANGFSET = {
	"highlight_glyph": True,  # colour label the processed glyph
	"highlight_col": 1,  # colour label # for orange
	"show_time": G.is_interactive,  # show the time to process each glyph as well as total
	"show_console": G.is_interactive,  # show macro and console window
	"debug": True,  # LNP debug tool
	"smallest_path": 7,  # Smallest permissable path width and height on clean-up
	"smallest_seg": 5,  # Smallest permissable segment length on clean-up
}

global start_time

# SET UP COMMON STUFF


def beginFilterNaN(font):
	global start_time
	selectedGlyphs = G.selected_glyphs(font)
	selectedGlyphs = filterGSGlyphList(selectedGlyphs)
	# print selectedGlyphs

	G.disable_updates(font)
	if NANGFSET["show_time"]:
		start_time = time.time()
	if NANGFSET["show_console"]:
		from GlyphsApp import Glyphs

		Glyphs.showMacroWindow()
		Glyphs.clearLog()
	return selectedGlyphs


def endFilterNaN(font):
	G.enable_updates(font)
	if NANGFSET["show_time"]:
		show_total_time(start_time)


def beginGlyphNaN(glyph):
	global glyph_start_time, glyphsize
	glyphsize = glyphSize(glyph)

	if NANGFSET["show_time"]:
		glyph_start_time = time.time()
	if NANGFSET["debug"]:
		print("starting glyph: " + glyph.name)
		print("glyph size: " + glyphsize)


def endGlyphNaN(glyph):
	if NANGFSET["show_time"]:
		show_glyph_time(glyph_start_time, glyph.name)
	if NANGFSET["highlight_glyph"]:
		glyph.color = NANGFSET["highlight_col"]
	print("-\n")

	# print out approximate time for entire glyphset


# SHOW INDIVIDUAL GLYPH PROCESSING TIME


def show_glyph_time(start_time, glyph):
	print(
		"Processing time for glyph("
		+ glyph
		+ "): "
		+ str(round(time.time() - start_time, 4))
		+ " seconds"
	)


# SHOW TOTAL PROCESSING TIME


def show_total_time(start_time):
	print(
		"-\nTotal processing time: "
		+ str(round(time.time() - start_time, 4))
		+ " seconds, "
		+ str(round((time.time() - start_time) / 60, 4))
		+ " minutes"
	)
	print("---\n")


# RETURN A SIZE (L, M, S) IN ORDER REFINE LEVEL OF REDRAW
def glyphSize(glyph):
	cat = glyph.category
	subcat = glyph.subCategory
	nc = ""

	# decide glyph size based on category
	if cat == "Letter":
		if subcat == "Uppercase":
			nc = "L"
		else:
			nc = "M"
	elif cat == "Number":
		if subcat == "Decimal Digit":
			nc = "L"
		elif subcat == "Small":
			nc = "S"
		else:
			nc = "L"
	elif cat == "Mark":
		nc = "S"
	elif cat == "Symbol":
		if subcat == "Currency":
			nc = "L"
		elif subcat == "Math":
			nc = "M"
		else:
			nc = "L"
	elif cat == "Punctuation":
		nc = "M"
	else:
		nc = "M"

	return nc


def filterGSGlyphList(selectedG):
	"""Return a list of unique GSGlyph objects, skipping those which cannot
	be processed."""
	newlist = []
	seen = {}
	for g in selectedG:
		if g.name is None or g.category == "Separator" or g.name in seen:
			continue
		font = g.parent
		if not ContainsPaths(font.glyphs[g.name].layers[0]):
			continue
		newlist.append(g)
		seen[g.name] = True
	return newlist


def ContainsPaths(thislayer):
	return len(thislayer.paths) > 0
