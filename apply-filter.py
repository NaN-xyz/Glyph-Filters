from glyphsLib import *
import importlib
import re
import os
import sys

sys.path.append("./Scripts/")
Glyphs.font = GSFont(sys.argv[1])
filter_script = sys.argv[2].replace("/", ".").replace(".py","")

print(filter_script)
i = importlib.import_module(filter_script)

m = re.match(r'^(?:Scripts/)?(.*)[-\.].*.py', sys.argv[2])
if not m:
	raise Exception("Don't recognise that filter")
script_number = m[1]
save_file = sys.argv[1].replace(".glyphs", "-"+script_number+".glyphs")
Glyphs.font.save(save_file)
print("Saved on %s" % save_file)
