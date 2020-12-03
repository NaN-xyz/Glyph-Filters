import glyphsLib
from Scripts.NaNGFAngularizzle import doAngularizzle
import pytest
import math


rubik = glyphsLib.GSFont("Source/Rubik.glyphs")
pathlist = rubik.glyphs["O"].layers[1].paths

def test_angularizzle():
	newpaths = doAngularizzle(pathlist, 5)
	assert(len(newpaths) == 2)
	assert(len(newpaths[0].nodes) == 454)
	assert(len(newpaths[1].nodes) == 162)
	assert(math.isclose(newpaths[0].nodes[3].position[0], 386.096111247388))
	assert(math.isclose(newpaths[1].nodes[10].position[1], 200.38488745054002))
