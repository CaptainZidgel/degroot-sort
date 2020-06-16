import os

def defineBranch(path):	#The goal is to create a neat, readable "branch" to show file trees.
	b = path.split(os.sep)#The default os.path.split: A/B/C -> ["A/B", "C"]. Using .split(os.sep): A/B/C -> ["A", "B", "C"]. Useful for measuring the depth of a file.
	s = ""
	for i in range(len(b)-1):	#For the folders in the filepath, ignore the actual file.
		s = s + "--"						#Double -- for cushioning.
	t = s + "--"							#t is the branch but with an extra length to accomodate the child file placed on it.
	s = s + b[-1]							#Add the file previously provided to the end of the branch
	return {"branch": s, "nbranch": t}

def createIndex(path, ignore={".json"}):
	path = os.path.split(path)[1]	#dsort passes an absolute path, but that would create very long branches.
	f = open("dg_index.txt", "w")

	for root, subdir, files in os.walk(path, topdown=True):
		branch = defineBranch(root)
		f.write(branch["branch"]+"\\\n")
		for filename in files:
			ext = os.path.splitext(filename)[1]
			if not ext in ignore:
				f.write(branch["nbranch"]+filename+"\n")

	f.close()
	return
