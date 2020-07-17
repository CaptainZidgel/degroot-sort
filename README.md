# Sort Demo Files
You provide the .dem files, program provides the folders.

## Dependencies
Almost all dependencies are standard library. Use the latest version of Python 3. Works on at least 3.6:  \
The only external dependency is tkinter(3), if you wish to use `ui.py`, but `cli.py` is much better.

## Usage
### Sorting
Please note this could render files unusable on other platforms depending on how Python handles their binary files (but when do you move demos to other platforms, anyway?) \
Windows: Open the .exe OR execute `python ui.py` or `python cli.py` (on Linux, use `python3` or whatever you have python3 installed under) \
Select a source directory: This will be the source of your files and where your files are organized.  \
The program will ask you to write a long template string (called a "Matrix") for assembling your folders. It is read left to right and separated by spaces. Options:  \
`servername` This is not the title of the server, it is the hostname and port you use to connect.  \
`clientname` This is your in game name. I do not know if this is recorded at the start of recording or the end.  \
`map` The map name  \
`day` YYYY-MM-DD  \
`month` YYYY-MM  \
`year` YYYY  \
`eventful` If there are events. Currently only supports in-game option of a separate json for each dem. What counts as an event is configured in game or with ds_mark.  \
`sag` Use server aliasing - Anything with no alias will be stored in `other/_rest_of_matrix` \
`sag*` Use server aliasing - Anything with no alias will be stored in `other/servername/_rest_of_matrix`  \
Click the submit button to format. On Unix, you can use `ls -R` to quickly see your new folders.

### Server Aliasing
Create an `Aliases.json` file. Place it wherever your installation is (sibling with the exe or python scripts). Syntax:
```json
{
	"regex": {
		"group_name": "regex_string"
	},
	"plain": {
		"group_name": [
			"ip:port1",
			"ip:port2",
		]
	}
}
```
I haven't tested it without using both groups, but if you don't want plain just leave whatever it is as `"plain": {}` and it should be fine.  \
If you wish to create a server alias group for Valve servers, you will need a NetworkDatagramConfig.json file. Same dir as everything else. If you are interested and need a link, please raise an issue.

### Flatten, Probe, Index
flatten will move every json and dem file from their subfolders back to the source folder, deleting any folder left empty.  \
probe will print out select information on every single demo file in a directory, be careful as this could be a lot if you have a giant demo folder.  
index will create a txt file that contains a visual tree of your source folder. Example:  
```
root\
--DIR1\
----DIRA\
------A			#this is a file
----DIRB\
------B			#this is a file
--DIR2\
----DIRC\
------C			#this is a file
----DIRD\
------D			#this is a file
```