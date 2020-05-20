import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import dsort as degroot
import os

#Assemble a root window
root = tk.Tk()
root.title = "Degroot Sort"
root.geometry("900x900")
root.resizable(0, 0)

frame1 = ttk.Frame(root)
frame1.grid(column=0, row=0, padx=10, pady=10)

src = tk.StringVar()
src.set("No directory selected")
dest = tk.StringVar()
dest.set = src.get()

#IDK lol
style = ttk.Style()

#file dialog
def setsrc():
	src.set(tk.filedialog.askdirectory())
	if dest.get() == "No directory selected":
		dest.set(src.get())

def setdest():
	dest.set(tk.filedialog.askdirectory())

#A button to set the source folder, and a label that relays that information back tot he user.
setsrc = ttk.Button(root, text="Choose Source Directory", command=setsrc)
setsrc.grid(column=1, row=1, in_ = frame1)

showsrc = ttk.Label(root, textvariable=src)
showsrc.grid(column=2, row=1, padx=25, in_ = frame1)

#Orderability - I am mentally incapable of creating some sort of fancy, intuitive drag and drop UI - it will be far easier for me and the user to just have a text box.
m_label = ttk.Label(root, wraplength=800, text="Write your pattern here. Pattern must be keywords, separated by spaces. Example:\nclientname map servername\nThis will create directories like: source/tavish/ctf_2fort/127.0.0.1")
m_label.grid(column=1, row=2, columnspan=15, in_ = frame1, pady=(25, 0))
write_matrix = ttk.Entry(root, width=100)
write_matrix.grid(column=1, row=3, columnspan=15, pady=10, in_ = frame1)
option_label = ttk.Label(root, text="Options:\nservername\nclientname\nmap\ndate [yyyy-mm, requires your files are appropriately named]\neventful [are there recorded events?]\n\nAdvanced options:\nsag [Server Alias Groups]\nsag* [SAG: store 'other' servers in other/servername]")
option_label.grid(column=0, row=4, rowspan=4)

m_rule = {"servername", "clientname", "map", "date", "game", "demproto", "netproto", "eventful", "sag", "sag*"}	#A set of options you could use
def verify_matrix():
	m = write_matrix.get()
	m = set(m.split())
	if m <= m_rule:						#if m is a subset of m_rule
		return True
	else:
		return False

def execute_unfurl():
	if verify_matrix() == True:
		files = degroot.unfurl_dir(src.get())
		for f in files:
			m = degroot.assemble_matrix(write_matrix.get().split(), f)
			degroot.move(src.get(), m, f)				
		print("Finished sorting!")
	else:
		print("Error")
		
def probe_dir(dir):
	f = degroot.unfurl_dir(dir)
	for d in f:
		print("{} s: {} <- {} | {}, {}, len: secs {}, ticks {} name: {}".format(d['name'], d['sgroup'], d['servername'], d['eventful'], d['map'], d['time'], d['ticks'], d['clientname']))
		print("\n")
	print("Finished probe")
		
submit = ttk.Button(root, text="Submit", command=execute_unfurl)
submit.grid(column=0, row=10, pady=15)

flatten = ttk.Button(root, text="Flatten source directory", command=lambda: degroot.flatten(src.get(), src.get()))
flatten.grid(column=0, row=11, pady=15)

probe = ttk.Button(root, text="Probe directory", command=lambda: probe_dir(src.get()))
probe.grid(column=0, row=12)

root.mainloop()