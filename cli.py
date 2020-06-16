import dsort as degroot
import index
import vserv
import os

src = input("Write path to your directory.\n>")
if not os.path.isdir(src):
	print("Bad directory.")
	exit()
src = os.path.abspath(src)

def getMethod():
	method = input("What do you want to do with this directory? (Sort/Flatten/Probe/Index/Help)\n>")
	m = method.lower()
	if m == "sort" or m == "s":
		return 's'
	elif m == "flatten" or m == "f":
		return 'f'
	elif m == "probe" or m == "p":
		return 'p'
	elif m == "index" or m == "i":
		return 'i'
	elif m == "help" or m == "h":
		print("""
SORT 		=> Place demos into folders based on your own designed tree
FLATTEN => Move all files from subdirs into root dir
PROBE 	=> Get quick information on files in dir
INDEX 	=> Output a .txt file with a formatted file tree (see your tree at a glance)
					""")
	else:
		print("Unknown method '{}'. Try: sort flatten probe index (OR: s f p i)".format(m))
		return getMethod()

m = getMethod()
print("Method is:", m)

rules = {"servername", "clientname", "map", "date", "game", "demproto", "netproto", "eventful", "sag", "sag*"}	

if m == "f":
	degroot.flatten(src, src)
elif m == "p":
	degroot.aliases = degroot.load_aliases(True)
	f = degroot.unfurl_dir(src)
	for d in f:
		print("{} s: {} <- {} | {}, {}, len: secs {}, ticks {} name: {}\n".format(d['name'], d['sgroup'], d['servername'], d['eventful'], d['map'], d['time'], d['ticks'], d['clientname']))
	print("Finished probe")	
elif m == "s":
	print("""
Now comes the part where you enter your sort string. 
This contains the ways you want to sort your folder. 
It is read left to right, each keyword separated by a space.
Your options are:
map - The map
date - The first 7 chars of the file name - that's because all my demos are named YYYY-MM
servername - The hostname+port you connect to (not the server title)
clientname - Your username
eventful - If there are events - this is based on .json files that match to each .dem, created by the in game recorder.
sag - [advanced] Use a server alias group. Others are placed in folder "other" and sorting continues to the next keyword.
sag* - [advanced] Use a server alias group. Others are placed in folder "other/servername" and sorting continues to the next keyword.
	""")
	keywords = input("Enter your keywords now (one line)\n>")
	keywordset = set(keywords.split())	#we must distinguish the keyword LIST from the keyword SET because one is ordered and one is not.
	if keywordset <= rules:	#if keywordset is a subset of rules
		print("Keywords accepted, beginning sort...")
		if "sag" in keywordset or "sag*" in keywordset:
			degroot.aliases = degroot.load_aliases()
		files = degroot.unfurl_dir(src)
		for f in files:
			matrix = degroot.assemble_matrix(keywords.split(), f)
			degroot.move(src, matrix, f)
		print("Finished sorting.")
	else:
		print("Error: Unknown keyword")
elif m == "i":
	print("This will output a dg_index.txt file to your current directory, overwriting any previous edition that might exist.")
	yn = input("Continue? (y/n)")
	if yn.lower() == "y":
		ignore = input("Hide JSON files from the index? (y/n)")
		if ignore.lower() == "y":
			ignore = {".json"}
		else:
			ignore = {}
		print("Creating Index...")
		index.createIndex(src, ignore)
else:
	print("This shouldn't have happened. What did you DO? m = ", m)
	exit()
_ = input("You can press enter to close this program now.")
