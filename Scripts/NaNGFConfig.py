from GlyphsApp import *
import random
from NaNGFGraphikshared import *
from math import *
import time
import cProfile

# Misc settings

NANGFSET = {
  "highlight_glyph": True,		# colour label the processed glyph
  "highlight_col": 1,			# colour label # for orange
  "show_time": True,			# show the time to process each glyph as well as total
  "show_console": True,			# show macro and console window
  "debug": True					# LNP debug tool
}

global start_time

# SET UP COMMON STUFF

def beginFilterNaN(font):

	global start_time
	selectedGlyphs = [ l.parent for l in font.selectedLayers ] 
	selectedGlyphs = processSelectedGlyphs(selectedGlyphs)
	#print selectedGlyphs

	font.disableUpdateInterface()
	if NANGFSET["show_time"]==True: start_time = time.time()
	if NANGFSET["show_console"]==True: 
		Glyphs.showMacroWindow()
		Glyphs.clearLog()
	return selectedGlyphs

def endFilterNaN(font):
	font.enableUpdateInterface()
	if NANGFSET["show_time"]==True: show_total_time(start_time)

def beginGlyphNaN(glyph):

	global glyph_start_time, glyphsize
	glyphsize=glyphSize(glyph)

	if NANGFSET["show_time"]==True: glyph_start_time = time.time()
	if NANGFSET["debug"]==True: 
		print "starting glyph: " + glyph.name
		print "glyph size: " + glyphsize

def endGlyphNaN(glyph):

	if NANGFSET["show_time"]==True: show_glyph_time(glyph_start_time, glyph.name)
	if NANGFSET["highlight_glyph"]==True: glyph.color = NANGFSET["highlight_col"]
	print "-\n"

	# print out approximate time for entire glyphset

# SHOW INDIVIDUAL GLYPH PROCESSING TIME

def show_glyph_time(start_time, glyph):
	print "Processing time for glyph( " + glyph + " ): " + str(round(time.time()-start_time,4)) + " seconds"

# SHOW TOTAL PROCESSING TIME

def show_total_time(start_time):
	print "-\nTotal processing time: " + str(round(time.time()-start_time,4)) + " seconds, " + str(round((time.time()-start_time )/60,4)) + " minutes"
	print "---\n"


# RETURN A SIZE (L, M, S) IN ORDER REFINE LEVEL OF REDRAW
def glyphSize(glyph):

	cat =  glyph.category
	subcat = glyph.subCategory
	nc = ""

	# decide glyph size based on category
	if cat=="Letter":
		if subcat=="Uppercase": nc = "L"
		else: nc = "M"
	elif cat=="Number":
		if subcat=="Decimal Digit": nc = "L"
		elif subcat=="Small": nc = "S"
		else: nc = "L"
	elif cat=="Mark": nc = "S"
	elif cat=="Symbol": 
		if subcat=="Currency": nc = "L"
		elif subcat=="Math": nc = "M"
		else: nc = "L"
	elif cat=="Punctuation": nc = "M"
	else: nc = "M"

	return nc


def processSelectedGlyphs(selectedG):

	newlist = []
	for g in selectedG:
		if g.name is not None: 
			if g.category != "Separator":
				font = g.parent
				if ContainsPaths(font.glyphs[g.name].layers[0]):
					newlist.append(g)

	return unique_list(newlist)


def unique_list(lst):

    # for order preserving
    def func_ord_preserve(x):
        return x

    set_seen = {}
    lst_result = []

    for item in lst:
        lst_marker_item = func_ord_preserve(item)

        if lst_marker_item in set_seen:
            continue

        set_seen[lst_marker_item] = 1
        lst_result.append(item)

    return lst_result

def ContainsPaths(thislayer):
	if len(thislayer.paths)>0: return True
	else: return False
