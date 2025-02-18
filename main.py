#!/usr/bin/env python3

#The code above makes it easier to load the python code in Linux and other Unixes. It won't affect it running in Windows

#These bring in the 'tkinter' modules needed to make the gui parts of the program
import tkinter as tk
from tkinter import *
import tkinter.messagebox as tkMessageBox
import subprocess

#The code below makes a window that'll ask the user for which file to open/create
openWindow = tk.Tk()
openWindow.title('Open File')
openWindow.geometry("560x50")

FileName = ""

def OpenFileGUI():
	#This makes the variable "FileName" global & makes it the place (if defined) & the name of the file
	try:
		getFileName = subprocess.check_output(["yad", "--file-selection", "--title=Select a file to open", "--window-icon=/home/bluecool1734/Python Concepts/PyText Editor Icon.png", "--width=1000", "--height=630"],
										universal_newlines=True)
		getFileName = getFileName[:-1]
		global FileName
		FileName = str(getFileName)
		OpenFile()
	except(FileNotFoundError):
		tkMessageBox.showinfo("GUI Not Working", "Make sure the program yad is properly installed for the GUI to work. For now, use the text box option.")
	except(subprocess.CalledProcessError):
		tkMessageBox.showinfo("No File Selected", "You have not selected a file. Please select one or exit the program.")

def OpenFileTextbox():
	#This makes the variable "FileName" global & makes it the place (if defined) & the name of the file
	global FileName
	FileName = openBox.get()
	OpenFile()

def OpenFile(): #Function used to open the file the user typed in
	#The if & else statement sees if the name typed is nothing & tells user to type in a name. Otherwise, it goes on
	global FileName
	if FileName == "":
		tkMessageBox.showinfo("File Warning", "Please type in a name for a file")
	else:
		#This checks to see if the file already exists, otherwise it'll say that it'll create the file
		try:
			open(FileName, "r+")
		except (FileNotFoundError):
			tkMessageBox.showinfo("File Warning", "File doesn't exist. Will create text file '" + FileName + "'")
			open(FileName, "x")
		#This makes the window removed & allow it to move on to the text editor window
		openWindow.destroy()

#The following code below adds the elements for "openWindow"
openFileText = Label(openWindow, text="File: ")
openFileText.pack(side = "left")

openBox = Entry(openWindow, bd=2, bg="gray99")
openBox.pack(side = "left")

openFileGUIButton = tk.Button(openWindow, text="Open file (GUI)", command=OpenFileGUI)
openFileGUIButton.pack(side = "right")

openFileButton = tk.Button(openWindow, text="Open/Create file (textbox)", command=OpenFileTextbox)
openFileButton.pack(side = "left")


#Additional settings for "openWindow"
openWindow.eval('tk::PlaceWindow . center')

#If the icon for the program is found, it'll show. Otherwise, it'll say that the icon can't be found
try:
	openWindow.iconphoto(True, tk.PhotoImage(file='PyText Editor Icon.png'))
except:
	tkMessageBox.showinfo("Icon Warning", "Couldn't find icon for this application. Will be using the default icon.")

#Allows the window to stay open until closed
openWindow.mainloop()



#The code below makes a window for the text editor
mainWindow = tk.Tk()
try:
	mainWindow.title(FileName + ' - PyText Editor')
except (NameError):
	exit()
mainWindow.geometry("800x486")


#Sets the side for the text editor's buttons 
buttonSides = "left"

#Sets the text shown when pressing the "Help" button
HelpText = "\nButtons:\nHelp - Shows help\nClear - Clears all text in the text file\nBefore - Goes back to version of text file before starting program\nUndo Last Change - Undo last change in a text file\n"

#If the name of the file given is '', then it'll exit the program. Otherwise it'll save the contents of the file 
try:
	with open(FileName) as f:
		PrevText = f.read()
		UndoText = f.read()
		CurrText = f.read()
except (FileNotFoundError):
	exit()

# Saves text from the user to the document ()
def SaveText():
	global UndoText
	with open(FileName) as f:
		UndoText = f.read()
	with open(FileName, "w") as f:
		f.write(TextBox.get("1.0", 'end-1c'))

# Clears all text in the document ()
def ClearText():
	global UndoText
	with open(FileName) as f:
		UndoText = f.read()
	TextBox.delete(1.0, "end")
	CurrText = TextBox.get("1.0", 'end-1c')
	with open(FileName, "w") as f:
		f.write(CurrText)

# Goes to the previous saved version of the document ()
def BeforeText():
	global UndoText
	with open(FileName) as f:
		UndoText = f.read()
	TextBox.delete(1.0, 'end-1c')
	with open(FileName, "w") as f:
		f.write(PrevText)
	TextBox.insert('end-1c', PrevText)

# Goes back a previous change ()
def UndoTextFunction():
	global UndoText
	TextBox.delete(1.0, "end")
	TextBox.insert('end-1c', UndoText)
	with open(FileName) as f:
		f.write(UndoText)

# Shows what each button does
def Help():
	global HelpText
	tkMessageBox.showinfo("Help", HelpText)


TextFileName = Label(mainWindow, text=("File: " + FileName))
TextFileName.pack(side = "top")

scrollbarX = tk.Scrollbar(mainWindow, orient=tk.HORIZONTAL, bg="gray25")
scrollbarY = tk.Scrollbar(mainWindow, orient=tk.VERTICAL, bg="gray25")

TextBox = Text(mainWindow, bd=2, bg="gray99", wrap="none", yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
scrollbarY.pack(side = "right", fill="y")
TextBox.pack(fill = "both")

scrollbarX.pack(side = "top", fill="x")

TextBox.insert("end", str(dir(tk.Scrollbar)))

scrollbarX.config(command=TextBox.xview)
scrollbarY.config(command=TextBox.yview)

TextBox.delete("1.0", "end")

with open(FileName) as f:
	TextBox.insert("end", f.read())


SaveButton = tk.Button(mainWindow, text="Save", command=SaveText)
SaveButton.pack(side = buttonSides)

ClearButton = tk.Button(mainWindow, text="Clear", command=ClearText)
ClearButton.pack(side = buttonSides)

BeforeButton = tk.Button(mainWindow, text="Before", command=BeforeText)
BeforeButton.pack(side = buttonSides)

UndoButton = tk.Button(mainWindow, text="Undo Last Change", command=UndoTextFunction)
UndoButton.pack(side = buttonSides)

HelpButton = tk.Button(mainWindow, text="Help", command=Help)
HelpButton.pack(side = buttonSides)

#Additional settings for "mainWindow"
mainWindow.eval('tk::PlaceWindow . center')

#Allows the window to stay open until closed
mainWindow.mainloop()
