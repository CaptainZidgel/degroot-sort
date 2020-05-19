# Sort Demo Files
I created this for my own uses and it now works. If I were to try and keep going to make this a user friendly, useful utility, I would go crazy and the code would spiral into spaghetti.
I do not intend to support this any more - except for potentially supporting new event storage types.
I do not recommend using this unless you really understand what you're doing.

## Dependencies
Almost all dependencies are standard library (use python3):  \
`io, sys, re, json, struct, os`  \
The exception is:  \
tkinter - If you wish to use the UI. But if you mess around with the code enough, it won't be hard to ignore ui.py and write this as a command line tool.  \
vserv (included) - If you wish to parse a json file of valve server ranges (not included) into an alias group, you'll need this, but you can delete it with no consequences. Code has contingencies to avoid erroring if you remove this.

## File requirements
See Usage.

## Usage
Please note this will erase file metadata like created/last-modified but considering a good demo has the date in the name this shouldn't be a problem (and when do you modify demos, anyway?)  \
Please note this could render files unusable on other platforms depending on how Python handles their binary files (but when do you move demos to other platforms, anyway?) \
`$ python3 ui.py`  \
Select a source directory: This will be the source of your files and where your files are organized.  \
The UI will ask you to write a long template string (called a "Matrix") for assembling your folders. It is read left to read and separated by spaces. Options:  \
`servername` This is not the title of the server, it is the hostname and port you use to connect.  \
`clientname` This is your in game name. I do not know if this is recorded at the start of recording or the end.  \
`map` The map name  \
`date` Technically, this is just the first 7 characters of the filename: This is because my demos are all recorded as `YYYY-MM_day_hour_something_something`, this can be configured in game.  \
`eventful` If there are events. Currently only supports in-game option of a separate json for each dem. What counts as an event is configured in game.  \
`sag` Use server aliasing - Anything with no alias will be stored in `other/_rest_of_matrix` \
`sag*` Use server aliasing - Anything with no alias will be stored in `other/servername/_rest_of_matrix`  \
Click the submit button to format. On Unix, you can use `ls -R` to quickly see your new folders.  \
The library/UI also features an option called flatten - it will move every json and dem file from their subfolders back to the source folder, deleting any folder left empty.

## Server Aliasing
Create an `Aliases.json` file. Place it wherever your installation is. Syntax:
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
I haven't tested it without using both groups, but if you don't want plain just leave whatever it is as `"plain": {}` and it should be fine.

