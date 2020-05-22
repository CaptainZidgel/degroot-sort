# Degroot Sort
# I import like this instead of From X Import Y because it creates cleaner, more readable code. Bonus readability for people not familiar with a specific library. Also it's Lua convention and I'm a Lua gamer.
import os
import struct
import io
import json
import re
import vserv
from sys import *

aliases = {}
def load_aliases():
	try:
		with open("Aliases.json", "r") as a:
			a = a.read()
			aliases = json.loads(a)
			for alias in aliases['plain']:
				a = aliases['plain'][alias]
				aliases[alias] = set(a)	
		x = input("Do you want to add a server alias group for Valve servers? (y/n)\n>")
		if x == 'y' and not 'valve' in aliases['plain']:
			print("OK. Processing valve servers.")
			aliases['plain']['valve'] = vserv.unfurl_relays()
	except FileNotFoundError:
		print("No alias file found. Place 'Aliases.json' in the same folder you're running this form.")

#Search a directory for files
def searchdir(_dir):
	files = [f for f in os.listdir(_dir) if os.path.isfile(os.path.join(_dir, f)) if os.path.splitext(f)[1] == ".dem" if os.path.getsize(os.path.join(_dir, f)) >= 1072] #This is called list comprehension. I'm looping over a directory and using if statements to determine what goes inside the list.
	#I am saying: Add `f` to the list, where f is the iter object in the loop that: searches directory given. Only do this if f meets these conditions: Is a file, is .dem type, and is at least the minimum size for a demo header.	
	return files	# a list of file NAMES

#unfurl (unpack) a specific file
def unfurl(path):
	with open(path, "rb") as input:
		data = input.read(1072)				#unpack requires the buffer be the same size as the format you give it to unpack, so I'm reading only what I need here.
	demo_keys = ['header', 'demoproto', 'netproto', 'servername', 'clientname', 'map', 'game', 'time', 'ticks', 'frames', 'signon'] #a list of keys for later use. this isnt global because its zipped up.
	try:
		d = dict(zip(demo_keys, struct.unpack('8sii260s260s260s260sfiii', data)))	#create a dictionary from the zipping of demo_keys and the result of unpack. zip pairs As and Bs together: zip((A, B), (A, B)) => (A, A), (B, B)
																	#8s             i    i    260s 260s 260s 260s   f      i    i    i    #I don't think this formatting will stick on other editors lol
																	#8-byte string, int, int, 260 byte string (x4), float, int, int, int  #These should be aligned but probably aren't lol
	except:
		return "Bad file"

	for key, value in d.items():
		if type(value) == bytes:	#if binary string
			d[key] = value.decode().rstrip('\x00')	#decode into utf-8 and strip null bytes at the end

	d['servername'] = d['servername'].replace(":", "@")	#can't have : in filenames in windows
	#these two statements truncate our path to just the filename, then assign the key date with the first 7 chars of the file name.
	ym = os.path.basename(path)
	d['date'] = ym[:7] #store the date in the dictionary. This is a slice: slices are string/array/other-compatible-object[start:stop]
	d['name'] = ym

	#determine what servergroup a demo is in
	try:
		for group in aliases['plain']:
			g = set(aliases['plain'][group])
			if d['servername'].replace("@", ":") in g or d['servername'].split("@")[0] in g:
				d['sgroup'] = group
		for rule in aliases['regex']:
			if re.fullmatch(aliases['regex'][rule], d['servername'].replace("@", ":")):
				d['sgroup'] = rule
		if 'sgroup' not in d:
				d['sgroup'] = "other"
	except KeyError:
		d['sgroup'] = "NOGROUP"
		#"Error processing aliases. This is expected behavior if you don't have an Aliases.json file"

	#depending on what you use as a demo recorder and how you configurate it, events are stored in different ways. The in game recorder stores JSON files.
	try:
		with open(path.replace(".dem", ".json")) as f:
			e = json.loads(f.read())['events']
			if len(e) > 0:
				d['eventful'] = "eventful"
			else:
				d['eventful'] = "not-eventful"
	except FileNotFoundError:
		d['eventful'] = "no-event-info"
	
	return d

#unfurl every demo in the directory given.
def unfurl_dir(path):
	files = searchdir(path)
	files_o = []
	for f in files:
		files_o.append(unfurl(os.path.join(path, f)))
	return files_o

#turn a prototype matrix into a real matrix string
def assemble_matrix(prototype, demo):
	#matrix = [demo[a] for a in prototype]
	matrix = []
	for item in prototype:
		if item == "sag" or item == "sag*":
			matrix.append(demo['sgroup'])
			if item == "sag*" and demo['sgroup'] == "other":
				matrix.append(demo['servername'])
		else:
			matrix.append(demo[item])
	matrix = os.sep.join(matrix)
	print(matrix, demo["name"])
	return matrix

#make dirs recursively, move file. path = root folder, demo = actual file 
def move(path, matrix, demo):
	target = os.path.join(path, matrix)
	j_p = demo['name'].replace(".dem", ".json")
	os.renames(os.path.join(path, demo['name']), os.path.join(target, demo['name']))	#move the demo
	try:
		os.renames(os.path.join(path, j_p), os.path.join(target, j_p))	#move the JSON
	except FileNotFoundError:
		print("Can't find JSON")

#move everything inside to the root
def flatten(path, to):
	print("Flattening", path)
	for root, subdir, files in os.walk(path):
		for filename in files:
			if os.path.splitext(filename)[1] == ".dem" or os.path.splitext(filename)[1] == ".json":
				os.renames(os.path.join(root, filename), os.path.join(to, filename))
