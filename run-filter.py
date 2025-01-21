import glyphsLib
import importlib
import argparse
import random
import sys
from glob import glob

parser = argparse.ArgumentParser(description='Filter a font file')
parser.add_argument(
	'--random-seed',
	metavar='INT',
	type=int,
	help='Random seed (for reproducibility)',
)

parser.add_argument(
	'input',
	metavar='GLYPHS',
	help='the Glyphs file'
)

parser.add_argument(
	'filter',
	metavar='FILTER',
	help='the filter to use'
)

args = parser.parse_args()

random.seed(args.random_seed)

base_path = "NaNGlyphFilters"
sys.path.append(base_path)
glyphsLib.Glyphs.font = glyphsLib.GSFont(args.input)
filter_script = args.filter

sys.modules['GlyphsApp'] = glyphsLib

try:
	i = importlib.import_module(filter_script)
except ModuleNotFoundError as e:
	modules = [x[len(base_path) + 1:-3] for x in sorted(glob(base_path + "/*.py")) if "/NaN" not in x]
	print("Couldn't find filter '%s'.\nTry one of: %s (%s)" % (filter_script, ", ".join(modules), e))
	sys.exit(1)

print("Saving...")
save_file = args.input.replace(".glyphs", "-" + filter_script + ".glyphs")
glyphsLib.Glyphs.font.save(save_file)
print("Saved on %s" % save_file)
