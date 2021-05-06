# -*- coding: cp1252 -*-
#==============================================================================
# Graph Algorirthm Program
#==============================================================================


#------------------------------------------------------------------------------
# Import required modules
#   math:    provides link to the OS
#   random:  provides file handling
#   Tkinter: provides UI framework
#   tkk:     provides more UI widgets
#   pickle:  provides file packing / unpacking
#------------------------------------------------------------------------------
import math
import random
import sys
import os

from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox
from tkinter import *
from tkinter import  ttk
import pickle
import operator
import copy

#Import the parts of the program

from arcViewObj import *
from matrixViewObj import *

from graphObj import *

from kruskalObj import *
from primObj import *
from djikstraObj import *
from chinesePostmanObj import *
from nearestNObj import *
from lowerBoundObj import *

from dfsObj import *


#------------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------------
VERSION = "1.0.1"
PROGRAM_NAME = "GraphAlgori"
FILE_EXTENSION = ".grph"
RECENT_FILES_NAME = "recent.dat"
HELP_FILE = "help.pdf"
CONFIG_NAME = "config.dat"


#------------------------------------------------------------------------------
# Global variable declarations
#------------------------------------------------------------------------------

def globalVars():

    global coordClicked
    global newNode
    global shift
    global tempArcs
    global connected
    global myKruskal
    global myPrim
    global myDj
    global myNearestN
    global myLowerB
    global myCPostman


    coordClicked = None #variable holding index position of clicked node
    newNode = True
    shift = False
    tempArcs = [None,None,None]
    connected = None
    myKruskal=None
    myPrim=None
    myDj = None
    myNearestN = None
    myLowerB = None
    myCPostman = None

globalVars()

#------------------------------------------------------------------------------
# Class definitions (UI elements)
#   (other classes are defined in seperate files
#------------------------------------------------------------------------------


#Undo Redo
class UndoRedo(object):
    def __init__(self):
        self.undoStack = []
        self.redoStack = []
        self.stackLength = 5

    def lengthCheck(self):
        if len(self.undoStack) > self.stackLength:
            del self.undoStack[0]
        if len(self.redoStack) > self.stackLength:
            del self.redoStack[0]

    def undo(self,event=None):
        """Undoes actions"""
        #gets graph object from undo stack

        global myGraph
        if self.undoStack != []:
            theFile = pickle.dumps(myGraph)
            graph = pickle.loads(theFile)
            self.redoStack.append(graph)

            clear()
            myGraph = self.undoStack.pop()

            #redraw graph:
            for i in range(0,myGraph.getNumNodes()):
                drawNode(i)
                for j in myGraph.neighbors(i):
                    drawArc(i,j)
            #update other UI elements:
            myMatrixView.update(myGraph)
            myArcView.update(myGraph)
            self.lengthCheck()

    def redo(self,event=None):
        """redoes actions"""
        #gets graph object from redo stack
        global myGraph
        if self.redoStack != []:
            theFile = pickle.dumps(myGraph)
            graph = pickle.loads(theFile)
            self.undoStack.append(graph)
            clear()
            myGraph = self.redoStack.pop()
            #redraw graph:
            for i in range(0,myGraph.getNumNodes()):
                drawNode(i)
                for j in myGraph.neighbors(i):
                    drawArc(i,j)
            #update other UI elements:
            myMatrixView.update(myGraph)
            myArcView.update(myGraph)
            self.lengthCheck()

    def add(self):
        """adds a snapshot of the graph to undo stack"""
        theFile = pickle.dumps(myGraph)
        graph = pickle.loads(theFile)
        self.undoStack.append(graph)
        self.redoStack = []
        self.lengthCheck()

    def clear(self):
        self.undoStack = []
        self.redoStack = []



#Menus object
class Menus(Frame):
    """
    Creates menu bar and events
    """
    def __init__(self, parent):
        global myMatrixView,unRedo
        self.recentFiles = []
        self.parent = parent
        self.filePath = "Untitled"+FILE_EXTENSION
        parent.title(os.path.split(self.filePath)[-1][0:-len(FILE_EXTENSION)] + " - " + PROGRAM_NAME)

        Frame.__init__(self, parent)
        self.parent = parent
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        #FILE MENU
        fileMenu = Menu(menubar,tearoff=0)
        fileMenu.add_command(label="New",underline=0, command=self.newDoc, accelerator="Ctrl+N")
        fileMenu.add_command(label="Open",underline=0, command=self.openFileDialog, accelerator="Ctrl+O")

        self.recentMenu = Menu(fileMenu,tearoff=0)
        fileMenu.add_cascade(label="Recent Files",underline=0, menu=self.recentMenu)

        fileMenu.add_separator()
        fileMenu.add_command(label="Save",underline=0, command=self.saveFile, accelerator="Ctrl+S")
        fileMenu.add_command(label="Save As..",underline=5, command=self.saveAsFile, accelerator="Ctrl+Shift+S")

        fileMenu.add_separator()
        exportMenu = Menu(fileMenu,tearoff=0)
        exportMenu.add_command(label="Export Current Graph",underline=7, command=self.exportAs)
        exportMenu.add_command(label="Export Algorithm Sequence",underline=7, command=self.exportSequence)
        fileMenu.add_cascade(label="Export",underline=0, menu=exportMenu)
        fileMenu.add_separator()

        fileMenu.add_command(label="Exit",underline=1, command=self.onExit, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=fileMenu,underline=0)

        #EDIT MENU
        editMenu = Menu(menubar,tearoff=0)
        editMenu.add_command(label="Undo",underline=0,command=unRedo.undo, accelerator="Ctrl+Z")
        editMenu.add_command(label="Redo",underline=0,command=unRedo.redo, accelerator="Ctrl+Shift+Z")
        editMenu.add_separator()
        editMenu.add_command(label="Preferences",underline=0,command=self.preferences, accelerator="Ctrl+Shift+P")
        menubar.add_cascade(label="Edit", menu=editMenu,underline=0)

        #VIEW MENU
        viewMenu = Menu(menubar,tearoff=0)

        viewMenu.add_checkbutton(label="Matrix",underline=0,command=togMatrix,var=myMatrixView.visible,accelerator="Ctrl+M")
        viewMenu.add_checkbutton(label="Arcs",underline=0,command=togArcView,var=myArcView.visible, accelerator="Ctrl+A")
        self.orders = BooleanVar()
        viewMenu.add_checkbutton(label="Orders",underline=1,command=self.togOrders,var=self.orders, accelerator="Ctrl+R")
        viewMenu.add_separator()

        viewMenu.add_command(label="Graph Stats",underline=6,command=self.graphStats, accelerator="Ctrl+T")
        menubar.add_cascade(label="View", menu=viewMenu,underline=0)

        #HELP MENU
        helpMenu = Menu(menubar,tearoff=0)
        helpMenu.add_command(label="Help",underline=0,command=self.openHelp, accelerator="F1")
        helpMenu.add_separator()
        helpMenu.add_command(label="About",underline=0,command=self.about)

        menubar.add_cascade(label="Help", menu=helpMenu,underline=0)

        #KEYBOARD SHORTCUTS
        #   file menu
        self.bind_all("<Control-n>",self.newDoc)
        self.bind_all("<Control-o>",self.openFile)
        self.bind_all("<Control-s>",self.saveFile)
        self.bind_all("<Control-Shift-s>",self.saveAsFile)
        self.bind_all("<Control-q>",self.onExit)


        #   edit menu
        self.bind_all("<Control-z>",unRedo.undo)
        self.bind_all("<Control-Z>",unRedo.redo)
        self.bind_all("<Control-P>",self.preferences)

        #   view menu
        self.bind_all("<Control-m>",togMatrix)
        self.bind_all("<Control-a>",togArcView)
        self.bind_all("<Control-r>",self.togOrders)
        self.bind_all("<Control-t>",self.graphStats)

        #   help menu
        self.bind_all("<F1>",self.openHelp)

        root.protocol("WM_DELETE_WINDOW", self.onExit)
        self.updateRecents()

    def exportSequence(self,event=None):

        options = {}
        options['parent'] = self
        options['defaultextension'] = ".jpg"
        options['filetypes'] = [("Bitmap",(".bmp")),
                                ("GIF",(".gif")),
                                ("JPEG",(".jpg",".jpe",".jpeg")),
                                ("PDF",(".pdf")),
                                ("TIFF",(".tif",".tiff")),
                                ("PNG",(".png")) ]



        filePath = tkFileDialog.asksaveasfilename(**options) #creates file browseR
        if filePath != "":
            filePath = str(filePath)
            path = filePath[:filePath.index(".")]+"/"
            name = filePath.split("/")[-1]
            name = name[:name.index(".")]
            os.mkdir(path)
            global control
            finished = False
            i = 0
            while not finished:
                i+=1
                control.nextStep()
                self.exportImage(path+name+str(i)+filePath[filePath.index("."):])
                if control.algorithmVar.get() == "Kruskal's":
                    if myKruskal == None:
                        finished = True
                elif control.algorithmVar.get() == "Prim's":
                    if myPrim == None:
                        finished = True
                elif control.algorithmVar.get() == "Djikstra's":
                    if myDj == None:
                        finished = True
                elif control.algorithmVar.get() == "Chinese Postman":
                    if myCPostman == None:
                        finished = True
                elif control.algorithmVar.get() == "TSP- Nearest Neighbor":
                    if myNearestN == None:
                        finished = True
                elif control.algorithmVar.get() == "TSP - Lower Bound":
                    if myLowerB == None:
                        finished = True
                else:
                    finished = True





    def exportAs(self,event=None):
        #Set standard diologe options:
        options = {}
        options['parent'] = self
        options['defaultextension'] = ".jpg"
        options['filetypes'] = [("Bitmap",(".bmp")),
                                ("GIF",(".gif")),
                                ("JPEG",(".jpg",".jpe",".jpeg")),
                                ("PDF",(".pdf")),
                                ("TIFF",(".tif","tiff")),
                                ("PNG",(".png")) ]



        filename = tkFileDialog.asksaveasfilename(**options) #creates file browseR
        if filename != "":
            self.exportImage(filename)


    def exportImage(self,filename):
        if myGraph.getNumNodes() == 0:
            return

        global canvas
        from PIL import Image, ImageDraw,ImageFont

        #define color constants
        colors = {}
        colors["white"] = (255, 255, 255)
        colors["black"] = (0, 0, 0)
        colors["grey"] = (150, 150, 150)
        colors["green"] = (0, 255, 0)
        colors["red"] = (255, 0, 0)
        colors["#28D13B"] = (40, 209, 59)
        colors["orange"] = (255,165,0)

        #setup image
        rootWidth = int(self.parent.geometry().split('+')[0].split('x')[0])*2
        rootHeight = int(self.parent.geometry().split('+')[0].split('x')[1])*2
        size = (rootWidth,rootHeight)
        image = Image.new("RGB",size, colors["white"])
        draw = ImageDraw.Draw(image)


        #Draw the arcs
        for i in range(0,myGraph.getNumNodes()):
            for j in myGraph.neighbors(i):
                iC = list(myGraph.getCoords(i))
                iC[0] = iC[0]*2
                iC[1] = iC[1]*2
                jC = list(myGraph.getCoords(j))
                jC[0] = jC[0]*2
                jC[1] = jC[1]*2
                arcCol = canvas.itemcget("a"+"%02d" % (i)+"%02d" % (j), "fill")
                if arcCol != "":
                    if arcCol == "black":
                        draw.line((iC[0], iC[1], jC[0], jC[1]), fill=colors[arcCol])
                    else:
                        for w in range(0,5):
                            draw.line((iC[0]-w, iC[1], jC[0]-w, jC[1]), fill=colors[arcCol])
                            draw.line((iC[0], iC[1]-w, jC[0], jC[1]-w), fill=colors[arcCol])
                    rX = (iC[0]+jC[0])/2
                    rY = (iC[1]+jC[1])/2
                    draw.rectangle((rX-40,rY-20,rX+40,rY+20),fill=colors["black"])
                    weight = str(myGraph.getArc(i,j))
                    try:
                        tFont = ImageFont.load("timR18.pil")
                        draw.text((rX-len(weight)*6,rY-12),weight,fill=colors["white"],font=tFont)
                    except:
                        draw.text((rX-len(weight)*6,rY-12),weight,fill=colors["white"])



        minX = 9999999
        minY = 9999999
        maxX = 0
        maxY = 0

        #Draw the nodes
        for i in range(0,myGraph.getNumNodes()):
            iC = list(myGraph.getCoords(i))
            iC[0] = iC[0]*2
            iC[1] = iC[1]*2

            #Find top-left and bottom-right nodes
            if minX > iC[0]:
                minX = iC[0]
            if minY > iC[1]:
                minY = iC[1]
            if maxX < iC[0]:
                maxX = iC[0]
            if maxY < iC[1]:
                maxY = iC[1]
            nodeCol = canvas.itemcget("n"+"%02d" % (i), "outline")
            draw.ellipse((iC[0]-30,iC[1]-30,iC[0]+30,iC[1]+30),fill=colors[nodeCol])
            nodeCol = canvas.itemcget("n"+"%02d" % (i), "fill")
            draw.ellipse((iC[0]-27,iC[1]-27,iC[0]+27,iC[1]+27),fill=colors[nodeCol])
            try:
                draw.text((iC[0]+25,iC[1]+25),myGraph.getLetter(i),fill=colors["black"],font=tFont)
            except:
                draw.text((iC[0]+25,iC[1]+25),myGraph.getLetter(i),fill=colors["black"])



            if menu.orders.get():
                try:
                    draw.text((iC[0]+25,iC[1]-50),str(myGraph.getOrder(i)),fill=colors["black"],font=tFont)
                except:
                    draw.text((iC[0]+25,iC[1]-50),str(myGraph.getOrder(i)),fill=colors["black"])



        for d in canvas.find_withtag("dj"):
            i =  int(canvas.gettags(d)[1][-2:])
            iC = list(myGraph.getCoords(i))
            iC[0] = iC[0]*2
            iC[1] = iC[1]*2


            if canvas.gettags(d)[1][2] == "B":
                draw.rectangle((iC[0]+50,iC[1]+50,iC[0]+200,iC[1]+125),fill=colors["white"],outline=colors["black"])
                draw.line((iC[0]+125,iC[1]+50,iC[0]+125,iC[1]+90),fill=colors["black"])
                draw.line((iC[0]+50,iC[1]+90,iC[0]+200,iC[1]+90),fill=colors["black"])

            elif canvas.gettags(d)[1][2] == "O":
                draw.text((iC[0]+85,iC[1]+57),str(myDj.getNode(i).getOrderOfLbl()),fill=colors["black"],font=tFont)

            elif canvas.gettags(d)[1][2] == "P":
                draw.text((iC[0]+157,iC[1]+57),str(myDj.getNode(i).getPerminantLbl()),fill=colors["black"],font=tFont)

            elif canvas.gettags(d)[1][2] == "T":
                x = iC[0]+120-(len(myDj.getNode(i).getTempLbls())*9)

                #tempLbls
                tempLbls = myDj.getNode(i).getTempLbls()
                tempLbls = list(map(str,tempLbls))
                tempLbls = "  ".join(tempLbls)

                draw.text((x,iC[1]+93),str( tempLbls),fill=colors["black"],font=tFont)


        desc = control.myDescBox.canvas.itemcget(control.myDescBox.desc,"text")
        step = control.myDescBox.canvas.itemcget(control.myDescBox.step,"text")
        if desc != "Choose an algorithm to begin":
            draw.text((minX-90,minY-200),step,fill=colors["black"],font=tFont)
            draw.text((minX,minY-180),desc.split("\n")[0],fill=colors["black"],font=tFont)

            if len(desc.split("\n")) == 2:
                draw.text((minX,minY-150),desc.split("\n")[1],fill=colors["black"],font=tFont)

        #Crop and save image
        image = image.crop((minX-100,minY-200,maxX+300,maxY+200))
        image.save(filename)

    def togOrders(self,event=None):
        global myGraph
        if event != None:
            self.orders.set(not self.orders.get())
        for i in range(0,myGraph.getNumNodes()):
            drawNode(i)

    def new(self,event=None):
        """Creates new graph"""


        clear()
        unRedo.clear()
        self.filePath = "Untitled"+FILE_EXTENSION
        root.title(os.path.split(self.filePath)[-1][0:-len(FILE_EXTENSION)] + " - " + PROGRAM_NAME)

    def onExit(self,event=None):
        """
        Handles 'Do you want to save?' alert when window is closed
        """
        if "*" in root.title(): #If the graph has been changed
            #Create alert:
            answer = tkMessageBox.askyesnocancel("Save Changes", "Do you want to save your changes to "+os.path.split(self.filePath)[-1][0:-len(FILE_EXTENSION)]+"?")

            if answer == None: #"Cancel"
                return
            if answer: #"Yes"
                self.saveFile()

        #Close window:
        root.destroy()

    def openFileDialog(self,event=None):
        """Creates an 'open file dialoge'"""
        global FILE_EXTENSION
        options = {}
        options['parent'] = self
        try:
            global CONFIG_NAME
            theFile = open(CONFIG_NAME,'rb') #open connection
            options['initialdir'] = pickle.load(theFile)[0]
            if options['initialdir'] == "/examples":
                options['initialdir'] = "examples"
            theFile.close()
        except:
            options['initialdir'] = "examples"



        options['defaultextension'] = FILE_EXTENSION
        options['filetypes'] = [("graph files",FILE_EXTENSION)]
        self.filePath = tkFileDialog.askopenfilename(**options)
        self.openFile(self.filePath)

    def openFile(self,fileToOpen):
        """Opens the file: fileToOpen"""
        global myGraph,myMatrixView,myArcView,FILE_EXTENSION

        if fileToOpen != "": #if cancel not pressed

            if "*" in root.title(): #If the graph has been changed
                #Create alert:
                answer = tkMessageBox.askyesnocancel("Save Changes", "Do you want to save your changes to "+root.title()[1:-14]+"?")

                if answer: #"Yes"
                    self.saveFile()


            try:
                #attempt to open file
                theFile = open(fileToOpen,'rb') #open connection
                clear() #clear canvas
                myGraph = pickle.load(theFile)

                #redraw graph:
                for i in range(0,myGraph.getNumNodes()):
                    drawNode(i)
                    for j in myGraph.neighbors(i):
                        drawArc(i,j)
                #update other UI elements:
                myMatrixView.update(myGraph)
                myArcView.update(myGraph)

                control.algorithmVar.set(myGraph.AlgorithmUsed) #set algorithm to last used

                #change file path,title and close file
                self.filePath = fileToOpen
                root.title(os.path.split(fileToOpen)[-1][0:-len(FILE_EXTENSION)] + " - " + PROGRAM_NAME)
                theFile.close()
                self.addRecentFile(self.filePath)
            except:
                tkMessageBox.showwarning("Open file",
                                         "Cannot open this file:\n%s" % os.path.split(fileToOpen)[-1])
                self.newDoc()


    def saveAsFile(self,event=None):
        """Creates a 'save file' dialoge'"""
        global myGraph

        #Set standard diologe options:
        options = {}
        options['parent'] = self
        options['defaultextension'] = FILE_EXTENSION
        options['filetypes'] = [("graph files",FILE_EXTENSION)]
        options['initialfile'] = os.path.split(self.filePath)[-1][0:-len(FILE_EXTENSION)]

        #if not an existing file, go to it's location
        if self.filePath != "Untitled"+FILE_EXTENSION:
            options['initialdir'] = self.filePath

        self.filePath = tkFileDialog.asksaveasfilename(**options) #creates file browser
        self.save()

    def saveFile(self,event=None):
        """For 'Save' option"""

        #if file is not prev saved, open file brower
        if os.path.split(self.filePath)[-1][0:-len(FILE_EXTENSION)] == "Untitled":
            self.saveAsFile()
        else:
            self.save()

    def save(self):
        """uses pickle to save the graph"""
        if self.filePath != "":
            theFile = open(self.filePath,"wb")
            pickle.dump(myGraph,theFile)
            root.title(os.path.split(self.filePath)[-1][0:-len(FILE_EXTENSION)] + " - " + PROGRAM_NAME)
            theFile.close()
            self.addRecentFile(self.filePath)

    def onEdit(self):
        """Adds '*' when graph is changed"""
        root.title("*" + os.path.split(self.filePath)[-1][0:-len(FILE_EXTENSION)] + " - " + PROGRAM_NAME)
        unRedo.add()

    def graphStats(self,event=None):
        """Opens graph stats dialog by creating an aboutDialog object instance"""
        graphStatsDialog(self.parent)


    def about(self):
        """Opens about dialog by creating an aboutDialog object instance"""
        aboutDialog(self.parent)

    def preferences(self,event=None):
        """Opens about dialog by creating an prefDialog object instance"""
        prefDialog(self.parent)

    def newDoc(self,event=None):

        if "*" in root.title(): #If the graph has been changed
            #Create alert:
            answer = tkMessageBox.askyesnocancel("Save Changes", "Do you want to save your changes to "+os.path.split(self.filePath)[-1][0:-len(FILE_EXTENSION)]+"?")

            if answer == None: #"Cancel"
                return
            if answer: #"Yes"
                self.saveFile()

        clear()
        unRedo.clear()
        self.filePath = "Untitled"+FILE_EXTENSION
        root.title(os.path.split(self.filePath)[-1][0:-len(FILE_EXTENSION)] + " - " + PROGRAM_NAME)


    def addRecentFile(self,fileToAdd):
        """
        Adds a opened/saved file to the recent files list.
        This is stored using pickle
        """
        global RECENT_FILES_NAME


        theFile = open(RECENT_FILES_NAME,"wb") #opens conection

        if self.recentFiles == []:
            # if blank creates default blank strings
            self.recentFiles = ["","",""]
        if fileToAdd in self.recentFiles:
            #if already in list, delete existing
            del self.recentFiles[self.recentFiles.index(fileToAdd)]
        else:
            #else delete oldest item
            del self.recentFiles[0]

        self.recentFiles.append(fileToAdd)#appends new file

        #Save to file and update
        pickle.dump(self.recentFiles,theFile)
        theFile.close()
        self.updateRecents()

    def updateRecents(self):
        """ Updates recent files menu"""
        try:
            theFile = open(RECENT_FILES_NAME,"rb")
            if theFile != None:
                self.recentFiles = pickle.load(theFile)
            theFile.close()
            for i in range(0,3):
                self.recentMenu.delete(i)

            if self.recentFiles[2] != "":
                self.recentMenu.add_command(label=self.recentFiles[2],command=lambda:self.openFile(self.recentFiles[2]))
            if self.recentFiles[1] != "":
                self.recentMenu.add_command(label=self.recentFiles[1],command=lambda:self.openFile(self.recentFiles[1]))
            if self.recentFiles[0] != "":
                self.recentMenu.add_command(label=self.recentFiles[0],command=lambda:self.openFile(self.recentFiles[0]))

        except IOError:
            pass

    def openHelp(self,event=None):
        try:
            global CONFIG_NAME
            theFile = open(CONFIG_NAME,'rb') #open connection
            helpPath = pickle.load(theFile)[1]
            theFile.close()
        except:
            helpPath = "help.pdf"

        if os.path.isfile(helpPath):
            import webbrowser
            webbrowser.open(helpPath)
        else:
            tkMessageBox.showwarning("No Help File","The help file: "+helpPath+" cannot be found.")


class aboutDialog(Toplevel):
    """creates the 'about' popup"""
    def __init__(self, parent):
        global PROGRAM_NAME,VERSION
        #Creates a box with the following properties:
        Toplevel.__init__(self, parent)
        self.resizable(0,0) #not resizable
        self.transient(parent) #minimizes with parent
        self.grab_set() #sets focus on self
        self.title("About")

        x = parent.winfo_rootx()
        y = parent.winfo_rooty()-40
        height = parent.winfo_height()
        width = parent.winfo_width()
        self.geometry("120x120+%d+%d" % (x+width/2-60,y+height/2-60))

        #Content:
        l1 = Label(self,text=PROGRAM_NAME,font=("Helvetica", 16))
        l1.pack()
        l2 = Label(self,text=chr(169)+" 2014 T. Hudson")
        l2.pack()
        l3 = Label(self,text="V"+VERSION)
        l3.pack()

        b1 = ttk.Button(self,text="Close",command=self.close)
        b1.focus_set()
        b1.pack(pady=10)


        #adds event bindings
        self.bind("<Return>",self.close)
        self.wait_window(self)

    def close(self,event=None):
        """destroy popup when closed button pressed"""
        self.destroy()

class graphStatsDialog(Toplevel):
    """creates the 'graph stats' popup"""
    def __init__(self, parent):
        global myGraph
        #Creates a box with the following properties:
        Toplevel.__init__(self, parent)
        self.resizable(0,0) #not resizable
        self.transient(parent) #minimizes with parent
        self.grab_set() #sets focus on self
        self.title("Stats")
        x = parent.winfo_rootx()
        y = parent.winfo_rooty()-40
        height = parent.winfo_height()
        width = parent.winfo_width()
        self.geometry("180x200+%d+%d" % (x+width/2-90,y+height/2-100))

        #Get Stats:
        if myGraph.isEulerian():
            l1 = Label(self,text="Eulerian")
        elif myGraph.isSemiEulerian():
            l1 = Label(self,text="Semi-Eulerian")
        else:
            l1 = Label(self,text="Non-Eulerian")

        myDfs = dfs(myGraph)
        if myDfs.connected():
            l2 = Label(self,text="Connected")
        else:
            l2 = Label(self,text="Non-Connected")


        l3 = Label(self,text=str(myGraph.getNumNodes()))

        arcsOrig = myGraph.arcs()
        arcs = []
        #remove duplicates (for non-directed arcs)
        for i in range(0,len(arcsOrig)):
            if (arcsOrig[i][0],(arcsOrig[i][1][1],arcsOrig[i][1][0])) not in arcs:
                arcs.append(arcsOrig[i])
        A = len(arcs)
        l4 = Label(self,text=str(A))

        R = A+2-myGraph.getNumNodes()
        l5 = Label(self,text=str(R))

        l6 = Label(self,text=str(myDfs.numConnectedComponants()))
        #Draw the layout
        headingFont = ("Arial",9,"bold")

        self.rowconfigure(0, weight=1)
        Label(self,text="Type:",font=headingFont).grid(column=0, row=1, sticky=(N,E))
        l1.grid(column=1, row=1, sticky=(N,W), pady=2)
        l2.grid(column=1, row=2, sticky=(N,W), pady=2)
        Label(self,text="Nodes:",font=headingFont).grid(column=0, row=3, sticky=(N,E))
        l3.grid(column=1, row=3, sticky=(N,W), pady=2)
        Label(self,text="Arcs:",font=headingFont).grid(column=0, row=4, sticky=(N,E))
        l4.grid(column=1, row=4, sticky=(N,W), pady=2)
        if myDfs.connected():
            Label(self,text="Regions:",font=headingFont).grid(column=0, row=5, sticky=(N,E))
            l5.grid(column=1, row=5, sticky=(N,W), pady=2)
        Label(self,text="   Connected\n Componants:",font=headingFont).grid(column=0, row=6, sticky=(N,E))
        #Label(self,text="Componants:",font=headingFont).grid(column=0, row=7, sticky=(N, W,E,S))
        l6.grid(column=1, row=6, sticky=(N,S,W),rowspan=2)

        b1 = ttk.Button(self,text="Close",command=self.close)
        b1.focus_set()
        b1.grid(column=0, row=8,columnspan=3, sticky=(N,W,E,S), padx=20, pady=10)

        #adds event bindings
        self.bind("<Return>",self.close)
        self.wait_window(self)

    def close(self,event=None):
        """destroy popup when closed button pressed"""
        self.destroy()

class prefDialog(Toplevel):
    """creates the 'preferences' popup"""
    def __init__(self, parent):
        #Creates a box with the following properties:
        Toplevel.__init__(self, parent)
        self.resizable(0,0) #not resizable
        self.transient(parent) #minimizes with parent
        self.grab_set() #sets focus on self


        self.title("Preferences")

        x = parent.winfo_rootx()
        y = parent.winfo_rooty()-40
        height = parent.winfo_height()
        width = parent.winfo_width()
        self.geometry("400x150+%d+%d" % (x+width/2-200,y+height/2-75))

        #Content:

        self.examplesPath = StringVar()
        self.helpPath = StringVar()

        try:
            global CONFIG_NAME
            theFile = open(CONFIG_NAME,'rb') #open connection
            paths = pickle.load(theFile)
            self.examplesPath.set(paths[0])
            self.helpPath.set(paths[1])
            theFile.close()
        except:
            self.helpPath.set("help.pdf")
            self.examplesPath.set("/examples")

        #Examples folder
        l2 = Label(self,text="Examples folder:")
        l2.grid(row=1, column=0,sticky="W")
        e2 = ttk.Entry(self,textvariable=self.examplesPath,width=50)
        e2.grid(row=2, column=0,columnspan=1,sticky="W")
        b2 = ttk.Button(self,text="Browse",command=self.browseExamples)
        b2.grid(row=2, column=1,columnspan=1,sticky="W",padx=10)

        #Help File
        l3 = Label(self,text="Help File:")
        l3.grid(row=3, column=0,columnspan=1,sticky="W",pady=(10,0))
        e3 = ttk.Entry(self,textvariable=self.helpPath,width=50)
        e3.grid(row=4, column=0,columnspan=1,sticky="W")
        b3 = ttk.Button(self,text="Browse",command=self.browseHelp)
        b3.grid(row=4, column=1,columnspan=1,sticky="W",padx=10)

        b1 = ttk.Button(self,text="Apply",command=self.close)
        b1.grid(row=5, column=0,columnspan=3,pady=20)
        b1.focus_set()

        #adds event bindings
        self.bind("<Return>",self.close)
        self.wait_window(self)



    def browseExamples(self):
        options = {}
        options['parent'] = self
        options['title'] = 'Choose examples directory'
        if self.examplesPath.get() != "":
            options['initialdir'] = self.examplesPath.get()
        path = tkFileDialog.askdirectory (**options)
        if path != "":
            self.examplesPath.set(path)

    def browseHelp(self):
        options = {}
        options['parent'] = self
        options['defaultextension'] = ".pdf"
        options['initialfile'] = self.helpPath.get()
        options['filetypes'] = [("Help Files",(".pdf",".html",".chm"))]
        path = tkFileDialog.askopenfilename(**options)
        if path != "":
            self.helpPath.set(path)


    def close(self,event=None):
        """destroy popup when closed button pressed"""

        global CONFIG_NAME

        theFile = open(CONFIG_NAME,"wb") #opens conection
        #Save to file

        data = [self.examplesPath.get(),self.helpPath.get()]
        if data[0] == "":
            data[0] = "/examples"
        if data[1] == "":
            data[1] = "help.pdf"

        pickle.dump(data,theFile)
        theFile.close()


        self.destroy()



#Controls Class
class controls:
    """Creates toolbar"""
    def __init__(self,parent):
        self.parent=parent
        self.controlsContainer = Frame(parent)
        self.playbackContainer = Frame(self.controlsContainer)


        #SCALE
        #setup style
        self.scaleVar = IntVar()
        w = ttk.Scale(self.playbackContainer,
                      from_=0, to=5,
                      orient=HORIZONTAL,
                      variable=self.scaleVar,
                      command=self.slideSnap)
        w.pack()

        lblFrame = Frame(self.playbackContainer)
        slow = Label(lblFrame,text="Slow")
        fast = Label(lblFrame,text="Fast")
        slow.pack(side=LEFT,expand=TRUE,padx=20)
        fast.pack(side=RIGHT,expand=TRUE,padx=20)
        lblFrame.pack(expand=TRUE)

        MainButton = ttk.Button(self.playbackContainer,text="Start",command=self.buttonPressed)
        MainButton.pack()

        self.algorithmVar = StringVar()
        self.algorithmVar.set("--Select Algorithm--")
        self.algorithm = ttk.Combobox(self.controlsContainer, textvariable=self.algorithmVar,state="readonly",takefocus=0)
        self.algorithm['values'] = ("--Select Algorithm--",
                                    "Prim's",
                                    "Kruskal's",
                                    "Djikstra's",
                                    "Chinese Postman",
                                    "TSP- Nearest Neighbor",
                                    "TSP - Lower Bound"
                                    #,"TSP - Tour Improvement",
                                    )
        self.algorithm.pack(side=LEFT)
        canvas.bind_all("<<ComboboxSelected>>", self.selectChange)
        self.playbackContainer.pack(side=LEFT,padx=100,pady=1)
        self.controlsContainer.grid(column=0, row=0, sticky=(N, W,E,S))

        self.myDescBox = descBox(self.controlsContainer)
        self.myDescBox.pack()

        self.timer = None



    def slideSnap(self,x=None):
        self.scaleVar.set(round(self.scaleVar.get()))


    def stepDone(self):
        if self.scaleVar.get() != 0:
            self.timer = canvas.after((5-self.scaleVar.get())*1000,self.nextStep)

    def buttonPressed(self):
        global canvas
        if self.algorithmVar.get() != "TSP - Tour Improvement" and self.scaleVar.get() != 0:
            reset()

        if self.timer != None:
            canvas.after_cancel(self.timer)
        self.nextStep()

    def nextStep(self):
        """Runs next step of selected algorithm"""
        global myGraph,control
        myDfs = dfs(myGraph)
        labelDeselected()
        if (myDfs.connected() and not myGraph.isDigraph()) or self.algorithmVar.get() == "--Select Algorithm--":
            if self.algorithmVar.get() == "--Select Algorithm--":
                reset()
            elif self.algorithmVar.get() == "Kruskal's":
                doKruskal()
                if myKruskal != None:
                    self.stepDone()
            elif self.algorithmVar.get() == "Prim's":
                doPrim()
                if myPrim != None:
                    self.stepDone()
            elif self.algorithmVar.get() == "Djikstra's":
                doDj()
                if myDj != None:
                    self.stepDone()
            elif self.algorithmVar.get() == "Chinese Postman":
                doCPostman()
                if myCPostman != None:
                    self.stepDone()
            elif self.algorithmVar.get() == "TSP- Nearest Neighbor":
                doNearestN()
                if myNearestN != None:
                    self.stepDone()
            elif self.algorithmVar.get() == "TSP - Lower Bound":
                doLowerB()
                if myLowerB != None:
                    self.stepDone()
            """elif self.algorithmVar.get() == "TSP - Tour Improvement":
                doTourImprov()
                if myTImprov != None:
                    self.stepDone()"""
        else:
            control.myDescBox.setText("WARNING",self.algorithmVar.get()+" can only be run on connected non-directed graphs")


    def selectChange(self,event=None):
        global myGraph
        myGraph.AlgorithmUsed = self.algorithmVar.get()
        myDfs = dfs(myGraph)
        if self.algorithmVar.get() == "--Select Algorithm--":
            self.myDescBox.setText("","Choose an algorithm to begin")
        elif self.algorithmVar.get() != "Djikstra's" and not myDfs.connected():
            self.myDescBox.setText(" WARNING","This algorithm only runs on connected graphs")
        elif myGraph.isDigraph():
            self.myDescBox.setText(" WARNING","This algorithm only runs on undirected graphs")
        else:
            self.myDescBox.setText("","Press Run to begin the Algorithm")


class StatusBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master,border=1, relief=RAISED)
        self.label = Label(self, anchor=W)
        self.label2 = Label(self, anchor=W)
        self.label.pack(side=LEFT)
        self.label2.pack(side=RIGHT)

    def setText(self, string):
        self.label.config(text=string)

    def setOrder(self,string):
        self.label2.config(text=string)

class descBox(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.canvas = Canvas(self, border=1, relief=SUNKEN, width=600,height=50,bg="#CCC")
        self.canvas.pack()
        self.step = self.canvas.create_text(5,5,font=("Arial",9,"bold"),text="STEP 1",anchor="nw")
        self.desc = self.canvas.create_text(300,25,text="")
        self.setText("","Choose an algorithm to begin")

    def setText(self,step,desc):
        self.canvas.itemconfig(self.step,text=step)
        if step == "ERROR" or step == " WARNING":
            self.canvas.itemconfig(self.step,fill="red")
        else:
            self.canvas.itemconfig(self.step,fill="black")

        self.canvas.itemconfig(self.desc,text=desc)





#------------------------------------------------------------------------------
# Canvas Functions
#------------------------------------------------------------------------------
def mouseClick(event):
    """
    Handles mouse clicks
        -Decides whether a node has been clicked on
    """
    global myGraph, mousedown,coordClicked

    if textOver()!=None: #If clicked on arc weight
        #select weight:
        labelDeselected()
        canvas.focus(textOver())
        canvas.select_from(textOver(), 0)
        canvas.select_to(textOver(), len(canvas.itemcget(textOver(),"text"))-1)
        coordClicked = None
    else:
        #deselect weight:
        labelDeselected()

        theNode = nodeOver(myGraph,event.x,event.y) #test if clicked on node
        if theNode == None:
            #if clicked on canvas, create a node
            addCoords(event)
        else:
            #else setup for arc drawing
            labelDeselected()
            coordClicked = theNode

    #Updates UI elements:
    menu.onEdit()
    myMatrixView.update()
    myArcView.update()

def nodeOver(graph,x,y):
    """
    Gets index of the node at pos (x,y).
    Returns None if no node is found.
    """
    found = False
    for i in range(0,graph.getNumNodes()): #interate through nodes
        coord = graph.getCoords(i)
        if (abs(x-coord[0]) <30) and (abs(y-coord[1]) <30): #compares mouse click to coords
            #if click within 30px of node center
            found = True
            return i #return node
        else:
            if i == (graph.getNumNodes()) and not found:
                #if didn't click on node
                return None

def textOver():
    """
    Gets index of the arc weight at pos (x,y).
    Returns None if no weight is found.
    """
    under = canvas.find_withtag("current")
    for i in under:
        tags = canvas.gettags(i)
        if "b" in tags or "w" in tags:
            return "w"+tags[1][1:]
        if "l" in tags:
            return "l"+tags[1][1:]
    return None


def updateStatus(event):
    global myGraph

    if nodeOver(myGraph,event.x,event.y) != None:
        bar.setText("Node "+myGraph.getLetter(nodeOver(myGraph,event.x,event.y))+": Shift-click to move")
        bar.setOrder("Order: "+str(myGraph.getOrder(nodeOver(myGraph,event.x,event.y))))
    else:
        bar.setText("For help, press F1")
        bar.setOrder("")



def addCoords(event,y=None):
    """adds new nodes to the list"""
    global  myGraph,coordClicked


    if y!=None:
        x = event
        coordClicked = None
    else:
        x = event.x
        y = event.y


    if myGraph.getNumNodes() == 0:
        global menu
        menu.onEdit()

    if coordClicked != None:

        node1 = myGraph.getCoords(coordClicked)
        if shift or abs(x-node1[0])<20 or abs(y-node1[1])<20:
            if abs(x-node1[0]) < abs(y-node1[1]):
                myGraph.addNode(node1[0],y)
            else:
                myGraph.addNode(x,node1[1])
        else:
            myGraph.addNode(x,y) #adds to graph object
    else:
        myGraph.addNode(x,y) #adds to graph object


    reset() #Clears all algorithms
    drawNode(myGraph.getNumNodes()-1) #draws the node
    coordClicked = myGraph.getNumNodes()-1 #sets node as clicked

def nodeMove(event):
    """moves node if selected"""
    global coordClicked,myGraph,newNode,shift
    if coordClicked != None: #if a node is selected

        if newNode == False:
            snapX = event.x
            snapY = event.y
            for n in myGraph.neighbors(coordClicked)+myGraph.revNeighbors(coordClicked):
                nCord = myGraph.getCoords(n)
                if abs(event.x-nCord[0])<20 or abs(event.y-nCord[1])<20:
                    if abs(event.x-nCord[0]) < abs(event.y-nCord[1]):
                        snapX = nCord[0]
                    else:
                        snapY = nCord[1]
            else:
                myGraph.setCoords(coordClicked,snapX,snapY)#update coords in graph obj
            drawNode(coordClicked) #redraw the node at new pos

        #redraws the arcs connected to the node:
        neigh = myGraph.neighbors(coordClicked)
        revNeighbors = myGraph.revNeighbors(coordClicked)
        for i in neigh:
            drawArc(coordClicked,i)
        for i in revNeighbors:
            drawArc(i,coordClicked)


def addArc(event):
    """Creates a new arc"""
    global coordClicked,myGraph,tempArcs,connected,newNode,shift
    if coordClicked != None and newNode: #if a node is selected
        #print shift

        node1 = myGraph.getCoords(coordClicked)

        if tempArcs == []:
            #if there is no temp arc, create one
            tempArcs[0] = canvas.create_line(node1[0],node1[1],event.x,event.y)
        else:
            #if there is then update it
            for i in tempArcs:
                canvas.delete(i) #deletes existing arcs

            theNode = nodeOver(myGraph,event.x,event.y)
            if theNode == None or theNode == coordClicked: #Stops self-loops TEMP

                if shift or abs(event.x-node1[0])<20 or abs(event.y-node1[1])<20:
                    #Snaps if close to vert/horz or if shift key pressed
                    for i in tempArcs:
                        canvas.delete(i) #deletes existing arcs
                    if abs(event.x-node1[0]) < abs(event.y-node1[1]):
                        tempArcs[0] = canvas.create_line(node1[0],node1[1],node1[0],event.y)
                    else:
                        tempArcs[0] = canvas.create_line(node1[0],node1[1],event.x,node1[1])
                else:
                    tempArcs[0] = canvas.create_line(node1[0],node1[1],event.x,event.y)
                connected = None
            else:
                #if between 2 different nodes...

                for i in tempArcs:
                    canvas.delete(i) #deletes existing arcs
                node2 = myGraph.getCoords(theNode)
                connected = theNode


                if myGraph.getArc(coordClicked,theNode) == None and myGraph.getArc(theNode,coordClicked) == None:
                    #straight arc
                    tempArcs[0] = canvas.create_line(node1[0],node1[1],node2[0],node2[1])
                else:
                    #For curved arcs

                    #draw the arc
                    tempArcs[0] = drawCurve(node1[0],node1[1],node2[0],node2[1],True)

                    #repeat for second arc
                    tempArcs[1] = drawCurve(node2[0],node2[1],node1[0],node1[1],False)

                    #cover existing line
                    tempArcs[2] = canvas.create_line(node1[0],node1[1],node2[0],node2[1],fill="white",width=4)
                    canvas.tag_raise("l")
                    canvas.tag_raise("b")
                    canvas.tag_raise("w")
    canvas.tag_raise("n")




def mouseUp(event):
    """
    Handles the event when the mouse button is relesed
    """
    global tempArcs,connected,coordClicked,myGraph,myMatrixView,myArcView,newNode

    newNode = True
    #Removes the tempArcs
    for i in tempArcs:
        canvas.delete(i)
    tempArcs = [None,None,None]

    if textOver()==None:
        randomW = random.randint(1,10)
        if connected != None:
            if myGraph.getArc(connected,coordClicked) == None and myGraph.getArc(coordClicked,connected) == None:
                #simple arc
                myGraph.setArc(coordClicked,connected,random.randint(1,10))
            else:
                #multiple arc

                randWeight = myGraph.getArc(connected,coordClicked)
                while randWeight == myGraph.getArc(connected,coordClicked ):
                    randWeight = random.randint(1,10)
                myGraph.setArc(coordClicked,connected,randWeight,True)

            drawArc(coordClicked,connected)
            textBox = "w" + "%02d" % (coordClicked) + "%02d" % (connected)
            canvas.focus(textBox)
            canvas.select_from(textBox, 0)
            canvas.select_to(textBox, len(canvas.itemcget(textBox,"text"))-1)
        elif nodeOver(myGraph,event.x,event.y) == None:
            #if not connecting 2 nodes, make a new node
            prev = coordClicked
            if coordClicked!=None:
                addCoords(event)

                myGraph.setArc(prev,myGraph.getNumNodes()-1,randomW)
                drawArc(prev,myGraph.getNumNodes()-1)
                textBox = "w" + "%02d" % (prev) + "%02d" % (myGraph.getNumNodes()-1)
                canvas.focus(textBox)
                canvas.select_from(textBox, 0)
                canvas.select_to(textBox, len(canvas.itemcget(textBox,"text"))-1)
        connected = None
        coordClicked = None

    myMatrixView.update()
    myArcView.update()
    control.selectChange()

def drawNode(pos):
    """
    Draws the graphical represantation of the node pos, in the graph object
    """
    global myGraph,canvas

    nOpt = {"fill":"grey",
            "activefill":"black",
            "disabledoutline":"grey",
            "state":myGraph.getNodeState(pos)
            }

    lOpt = {"disabledfill":"grey",
            "state":myGraph.getNodeState(pos)}

    strPos = "%02d" % (pos)

    coord = myGraph.getCoords(pos)
    letter = myGraph.getLetter(pos)
    #letter = pos #TEMP

    if canvas.find_withtag("n"+strPos) == ():

        t = canvas.create_oval(coord[0]+15, coord[1]+15, coord[0]-15, coord[1]-15,width=2,tags=("n","n"+strPos),**nOpt)
        canvas.create_text(coord[0]+20,coord[1]+20,text=letter,tags=("l","l"+strPos),**lOpt)
        o = canvas.create_text(coord[0]+20,coord[1]-20,text=str(myGraph.getOrder(pos)),tags=("o","o"+strPos),**lOpt)
        if not menu.orders.get():
            canvas.itemconfig(o,state=HIDDEN)

        if myGraph.isPosUserNode(pos):
            canvas.itemconfig("l"+strPos,font="Times 10 underline bold")
        else:
            canvas.itemconfig("l"+strPos,font="Times 10 normal")
    else:
        drawDj(pos)
        canvas.coords("n"+strPos, coord[0]+15, coord[1]+15, coord[0]-15, coord[1]-15)
        canvas.coords("l"+strPos,coord[0]+20, coord[1]+20)
        if myGraph.isPosUserNode(pos):
            canvas.itemconfig("l"+strPos,font="Times 10 underline bold")
        else:
            canvas.itemconfig("l"+strPos,font="Times 10 normal")

        canvas.coords("o"+strPos,coord[0]+20, coord[1]-20)
        canvas.itemconfig("o"+strPos,text=str(myGraph.getOrder(pos)))
        canvas.lift("o"+strPos)
        if not menu.orders.get():
            canvas.itemconfig("o"+strPos,state=HIDDEN)
        else:
            canvas.itemconfig("o"+strPos,state=NORMAL)

        canvas.itemconfig("l"+strPos,text=letter)

    #Change colour for start and end nodes
    if myGraph.getStart() == pos:
        canvas.itemconfig("n"+strPos,outline="#28D13B",state=myGraph.getNodeState(pos))
    elif myGraph.getEnd() == pos:
        canvas.itemconfig("n"+strPos,outline="red",state=myGraph.getNodeState(pos))
    else:
        canvas.itemconfig("n"+strPos,outline="black",state=myGraph.getNodeState(pos))



    #update labels
    for pos in range(0,myGraph.getNumNodes()):
        strPos = "%02d" % (pos)
        letter = myGraph.getLetter(pos)
        #letter = pos # temp
        canvas.itemconfig("l"+strPos,text=letter,state=myGraph.getNodeState(pos))



def drawArc(n1,n2):
    """
    Draws the graphical represantation of the arc between n1 and n2, in the graph object
    """
    global myGraph
    aOpt = {"disabledfill":"grey",
            "state":myGraph.getArcState(n1,n2)}

    bOpt = {"fill":"black",
            "disabledfill":"grey",
            "disabledoutline":"grey",
            "state":myGraph.getArcState(n1,n2)
            }

    wOpt = {"fill":"white"}


    strN1 = "%02d" % (n1)
    strN2 = "%02d" % (n2)


    #draws line representing edge

    node1 = myGraph.getCoords(n1)
    node2 = myGraph.getCoords(n2)
    midx = (node1[0]+node2[0])/2
    midy = (node1[1]+node2[1])/2

    if myGraph.getArc(n1,n2) == None:
        return

    if myGraph.getArc(n2,n1)==myGraph.getArc(n1,n2):
        #if -----NORMAL ARC-----

        """if canvas.find_withtag("a"+strN1+strN2) == ():
            # creates line if line doesn't already exist"""

        #delete existing arcs
        canvas.delete("a"+strN2+strN1)
        canvas.delete("w"+strN2+strN1)
        canvas.delete("b"+strN2+strN1)
        canvas.delete("a"+strN1+strN2)
        canvas.delete("w"+strN1+strN2)
        canvas.delete("b"+strN1+strN2)


        weight = myGraph.getArc(n1,n2) #gets weight
        canvas.create_line(node1[0],node1[1],node2[0],node2[1],tags=("a",("a"+strN1+strN2)),**aOpt)
        canvas.create_rectangle(midx-20,midy,midx+20,midy+20, tags=("b","b"+strN1+strN2),**bOpt)
        canvas.create_text(midx, midy+10, text=str(weight),tags=("w","w"+strN1+strN2),**wOpt)
        canvas.tag_lower("w"+strN1+strN2)
        canvas.tag_lower("b"+strN1+strN2)
        canvas.tag_lower("a"+strN1+strN2)
        """else:
            #adjust coords of existing arc
            canvas.itemconfig("a"+strN1+strN2,state=myGraph.getArcState(n1,n2))
            canvas.itemconfig("b"+strN1+strN2,state=myGraph.getArcState(n1,n2))
            canvas.itemconfig("w"+strN1+strN2,state=myGraph.getArcState(n1,n2))
            canvas.coords("a"+strN1+strN2,node1[0],node1[1],node2[0],node2[1])
            canvas.coords("b"+strN1+strN2,midx-20, midy+20,midx+20,midy+40)
            canvas.coords("w"+strN1+strN2,midx, midy+30)"""


    elif myGraph.getArc(n2,n1)!= None and myGraph.getArc(n1,n2) != None:
        #if ------MULTIPLE ARC------
        #delete existing arcs
        canvas.delete("a"+strN2+strN1)
        canvas.delete("w"+strN2+strN1)
        canvas.delete("b"+strN2+strN1)
        canvas.delete("a"+strN1+strN2)
        canvas.delete("w"+strN1+strN2)
        canvas.delete("b"+strN1+strN2)

        #draw and tag a new curve
        midX,midY,height,width = calcNormal(node1[0],node1[1],node2[0],node2[1])
        curve = drawCurve(node1[0],node1[1],node2[0],node2[1],True,aOpt)
        canvas.addtag_withtag("a",curve)
        canvas.addtag_withtag("a"+strN1+strN2,curve)

        #add a weight
        weight = myGraph.getArc(n1,n2) #gets weight
        x,y = calArcMid(node1[0],node1[1],node2[0],node2[1],True)
        w,h = point2(node1[0],node1[1],node2[0],node2[1])
        if node1[0]>= node2[0]:
            canvas.create_line(x,y,x+w,y+h,arrow=LAST,arrowshape=(10,10,10),width=0,tags=("a",("a"+strN2+strN1)))
        else:
            canvas.create_line(x,y,x+w,y+h,arrow=FIRST,arrowshape=(10,10,10),width=0,tags=("a",("a"+strN2+strN1)))
        canvas.create_rectangle(midX+width-20,midY+height+20,midX+width+20,midY+height+40, tags=("b","b"+strN1+strN2),**bOpt)
        canvas.create_text(midX+width, midY+height+30, text=str(weight),tags=("w","w"+strN1+strN2),**wOpt)

        #draw and tag second curve
        curve = drawCurve(node2[0],node2[1],node1[0],node1[1],False,aOpt)
        canvas.addtag_withtag("a",curve)
        canvas.addtag_withtag("a"+strN2+strN1,curve)

        #add a weight
        midX,midY,height,width = calcNormal(node1[0],node1[1],node2[0],node2[1])
        weight = myGraph.getArc(n2,n1) #gets weight
        x,y = calArcMid(node1[0],node1[1],node2[0],node2[1],False)
        w,h = point2(node1[0],node1[1],node2[0],node2[1])
        if node1[0]>= node2[0]:
            canvas.create_line(x,y,x+w,y+h,arrow=FIRST,arrowshape=(10,10,10),width=0,tags=("a",("a"+strN2+strN1)))
        else:
            canvas.create_line(x,y,x+w,y+h,arrow=LAST,arrowshape=(10,10,10),width=0,tags=("a",("a"+strN2+strN1)))

        canvas.create_rectangle(midX-width+20, midY-height-20,midX-width-20,midY-height-40,tags=("b","b"+strN2+strN1),**bOpt)
        canvas.create_text(midX-width, midY-height-30, text=str(weight),tags=("w","w"+strN2+strN1),**wOpt)


        canvas.tag_lower("w"+strN2+strN1)
        canvas.tag_lower("b"+strN2+strN1)
        canvas.tag_lower("a"+strN2+strN1)

        canvas.tag_lower("w"+strN1+strN2)
        canvas.tag_lower("b"+strN1+strN2)
        canvas.tag_lower("a"+strN1+strN2)

    elif myGraph.getArc(n2,n1)== None and myGraph.getArc(n1,n2) != None:
        #directed arc
        #delete existing arcs
        canvas.delete("a"+strN2+strN1)
        canvas.delete("w"+strN2+strN1)
        canvas.delete("b"+strN2+strN1)
        canvas.delete("a"+strN1+strN2)
        canvas.delete("w"+strN1+strN2)
        canvas.delete("b"+strN1+strN2)
        weight = myGraph.getArc(n1,n2) #gets weight
        canvas.create_line(midx,midy,node1[0],node1[1],tags=("a",("a"+strN1+strN2)),**aOpt)
        canvas.create_line(midx,midy,node2[0],node2[1],arrow=FIRST,arrowshape=(10,10,10),width=0,tags=("a",("a"+strN1+strN2)),**aOpt)
        canvas.create_rectangle(midx-20, midy+20,midx+20,midy+40,tags=("b","b"+strN1+strN2),**bOpt)
        canvas.create_text(midx, midy+30, text=str(weight),tags=("w","w"+strN1+strN2),**wOpt)
        #send to back
        canvas.tag_lower("w"+strN1+strN2)
        canvas.tag_lower("b"+strN1+strN2)
        canvas.tag_lower("a"+strN1+strN2)
    else:
        tkMessageBox.showwarning("Drawing","Arc drawing error")

    if menu.orders.get():
        drawNode(n1)
        drawNode(n2)

def calArcMid(x1,y1,x2,y2,up):
    L=25
    if y1==y2:
        y1+=10
    if x1==x2:
        x1+=5
    #Calculate midpoint between the nodes
    midX=(x1+x2)/float(2)
    midY=(y1+y2)/float(2)
    #Calculate gradient
    #if dy is 0, solve by setting gradient to 1
    m = 0-(x2-x1)/float(y2-y1)
    #calculate x and y of arc midpoint
    angle = math.atan(m)
    height = L*math.sin(angle)
    try:
        width = height/m
    except:
        width = height

    if up:
        return midX+width,midY+height
    else:
        return midX-width,midY-height

def point2(x1,y1,x2,y2):
    L=25
    if y1==y2:
        y1+=1
    if x1==x2:
        x1+=1
    m = calcGrad(x1,y1,x2,y2)
    angle = math.atan(m)
    height = L*math.sin(angle)
    try:
        width = height/m
    except:
        width = height
    return width/9,height/9


def calcGrad(x1,y1,x2,y2):
    try:
        return (y2-y1)/float(x2-x1)
    except:
        return 1


def calcNormal(x1,y1,x2,y2):
    L=50
    if y1==y2:
        y1+=10
    if x1==x2:
        x1+=5
    #Calculate midpoint between the nodes
    midX=(x1+x2)/float(2)
    midY=(y1+y2)/float(2)
    #Calculate gradient
    #if dy is 0, solve by setting gradient to 1
    m = 0-(x2-x1)/float(y2-y1)
    #calculate x and y of arc midpoint
    angle = math.atan(m)
    height = L*math.sin(angle)
    try:
        width = height/m
    except:
        width = height
    return midX,midY,height,width


def drawCurve(x1,y1,x2,y2,up,options={}):
    """
    Draws a curve between the 2 coords.
    Returns curve ID
    """
    if x1 == x2:
        x1+=1
    if y1 == y2:
        if up:
            up = False

    midX,midY,height,width = calcNormal(x1,y1,x2,y2)

    if up:
        #make array of points
        #           start                   mid
        points = [(x1, y1),(midX+width, midY+height)]
        #   end
        p = (x2,y2)
    else:
        points = [(x2, y2),(midX-width, midY-height)]
        p = (x1,y1)

    #draw the arc
    return canvas.create_line(points, p, smooth = True,**options)



def delNode(n1=None):
    """
    Deletes node in GUI and graph object.
    Also updates arc labels to accomadate
    """
    global myGraph,unRedo
    if n1 == None:
        global coordClicked
    else:
        coordClicked = n1

    reset()
    neigh = myGraph.neighbors(coordClicked)

    #deletes any arc lines connected to the deleted node

    strCoordClicked = "%02d" % (coordClicked)



    for n in neigh:
        strN = "%02d" % (n)
        canvas.delete("a"+strCoordClicked+strN)
        canvas.delete("b"+strCoordClicked+strN)
        canvas.delete("w"+strCoordClicked+strN)
    neigh = myGraph.revNeighbors(coordClicked)
    for n in neigh:
        strN = "%02d" % (n)
        canvas.delete("a"+strN+strCoordClicked)
        canvas.delete("b"+strN+strCoordClicked)
        canvas.delete("w"+strN+strCoordClicked)

    #deletes the node shape
    canvas.delete("n"+strCoordClicked)
    canvas.delete("l"+strCoordClicked)
    canvas.delete("o"+strCoordClicked)
    myGraph.delNode(coordClicked) #removes entry in graph obj

    #Adjusts node numbers to match array:
    #   All arcs connecting to a node with a higher index than the
    #   deleted node have their label decresed by one to match
    #   the array in the graph object
    for node in canvas.find_withtag("n"):
        if int(canvas.gettags(node)[1][1:]) > coordClicked:
            new =  "%02d" % (int(canvas.gettags(node)[1][1:])-1)
            canvas.addtag_withtag("n"+new, node)
            canvas.addtag_withtag("l"+new, "l"+canvas.gettags(node)[1][1:])
            canvas.addtag_withtag("o"+new, "o"+canvas.gettags(node)[1][1:])
            canvas.dtag("l"+new, "l"+canvas.gettags(node)[1][1:])
            canvas.dtag("o"+new, "o"+canvas.gettags(node)[1][1:])
            canvas.dtag(node,canvas.gettags(node)[1])

    #adjusts arc numbers
    #Fixed

    for arc in canvas.find_withtag("a"):
        theArc = canvas.gettags(arc)[1]
        new = theArc[1:]
        if int(new[0:2]) > coordClicked:
            new = ("%02d" % (int(new[0:2])-1))+new[2:4]
        if int(new[2:4]) > coordClicked:
            new = new[0:2]+("%02d" % (int(new[2:4])-1))
        if new != theArc[1:]:
            a = min(canvas.find_withtag(theArc))
            b = min(canvas.find_withtag("b"+theArc[1:]))
            w = min(canvas.find_withtag("w"+theArc[1:]))
            canvas.addtag_withtag("a"+new,a)
            canvas.addtag_withtag("b"+new,b)
            canvas.addtag_withtag("w"+new,w)
            canvas.dtag(b,"b"+theArc[1:])
            canvas.dtag(w,"w"+theArc[1:])
            canvas.dtag(a,theArc)

    #adjusts start/end nodes
    if myGraph.getStart() >= coordClicked:
        myGraph.setStart(myGraph.getStart()-1)
    if myGraph.getEnd() >= coordClicked:
        myGraph.setEnd(myGraph.getEnd()-1)

    myMatrixView.update()
    myArcView.update()


def delArc(n1,n2,both=False):
    """
    Deletes arc between n1 and n2
    if var both is set to true, arcs in both directiond are deleted
    """

    srtN1 = "%02d" % (n1)
    srtN2 = "%02d" % (n2)

    myGraph.delArc(n1,n2)#change matrix
    #remove GUI elements
    canvas.delete("a"+srtN1+srtN2)
    canvas.delete("b"+srtN1+srtN2)
    canvas.delete("w"+srtN1+srtN2)

    if both:
        myGraph.delArc(n2,n1)#change matrix
        #remove GUI elements
        canvas.delete("a"+srtN2+srtN1)
        canvas.delete("b"+srtN2+srtN1)
        canvas.delete("w"+srtN2+srtN1)
    else:
        drawArc(n2,n1)

    myMatrixView.update()
    myArcView.update()


def popup(event):
    """Creates context menu at mouse position"""
    global myGraph,coordClicked
    if nodeOver(myGraph,event.x,event.y) != None:
        #popup node menu
        coordClicked = nodeOver(myGraph,event.x,event.y)
        isStart = BooleanVar()
        isStart.set(myGraph.getStart() == coordClicked)
        isEnd = BooleanVar()
        isEnd.set(myGraph.getEnd() == coordClicked)
        isDisabled = BooleanVar()
        isDisabled.set(myGraph.getNodeState(coordClicked) == "disabled")

        popNodeMenu = Menu(root, tearoff=0)
        popNodeMenu.add_command(label="Delete", command=delNode)
        popNodeMenu.add_separator()
        popNodeMenu.add_checkbutton(label="Start", command=setStart,var=isStart)#PROBLEM: Need to change to checkbutton
        popNodeMenu.add_checkbutton(label="End", command=setEnd,var=isEnd)
        popNodeMenu.add_separator()
        popNodeMenu.add_checkbutton(label="Disabled",command=disabledClicked,var=isDisabled)
        popNodeMenu.post(event.x_root, event.y_root)

    elif canvas.find_overlapping(event.x-5,event.y-5,event.x+5,event.y+5) != ():
        tag = canvas.gettags(canvas.find_overlapping(event.x-5,event.y-5,event.x+5,event.y+5)[0])[1]
        if tag[0] in ["w","b","a"]:
            tag = [int(tag[1:3]),int(tag[3:5])]
            popArcMenu = Menu(root, tearoff=0)
            popArcMenu.add_command(label="Delete", command=lambda:delArc(tag[0],tag[1],myGraph.getArc(tag[0],tag[1]) == myGraph.getArc(tag[1],tag[0])))
            popArcMenu.post(event.x_root,event.y_root)
    else:
        popCanvasMenu = Menu(root, tearoff=0)
        popCanvasMenu.add_command(label="Clear Algorithm", command=reset)
        popCanvasMenu.add_command(label="Clear Screen", command=clear)
        popCanvasMenu.post(event.x_root,event.y_root)


def keypress(event):
    """handles typing"""
    global myGraph,canvas, shift
    shift = (event.keysym[:5] == "Shift")
    textBox = canvas.focus()
    if textBox:
        if canvas.gettags(textBox)[0] == "l":
            #If a node label
            labelKeypress(event,textBox)
        else:
            weightKeypress(event,textBox)

def weightKeypress(event,textBox):
    nodes = (int(canvas.gettags(textBox)[1][1:3]),
         int(canvas.gettags(textBox)[1][3:5]))
    insert = canvas.index(textBox, INSERT) #gets cursor index
    if event.char.isdigit() or event.char== ".": #accept digits only
        if canvas.tk.call(canvas._w, 'select', 'item'):
            #if selected replace contents
            canvas.dchars(textBox, SEL_FIRST, SEL_LAST)
            canvas.select_clear()
            canvas.insert(textBox, "insert", event.char)
            current = myGraph.getArc(nodes[0],nodes[1])
        elif len(canvas.itemcget(textBox,"text").split(".")[0])<3 and  len(canvas.itemcget(textBox,"text").split(".")[-1])<3:

            #append a digit (limited to 2 digit numbers)
            if event.char != "." or (event.char == "." and "." not in canvas.itemcget(textBox,"text")):
                canvas.insert(textBox, "insert", event.char)
                current = myGraph.getArc(nodes[0],nodes[1])
                labelDeselected(False)

    elif event.keysym == "BackSpace":
        if canvas.tk.call(canvas._w, 'select', 'item'):
            #if label selected, clear it
            canvas.dchars(textBox, SEL_FIRST, SEL_LAST)
            canvas.select_clear()
            current = myGraph.getArc(nodes[0],nodes[1])
        else:
            if insert > 0: #if not already blank
                canvas.dchars(textBox, insert-1, insert)
                current = myGraph.getArc(nodes[0],nodes[1])

def labelKeypress(event,textBox):
    node = int(canvas.gettags(textBox)[1][1:])

    insert = canvas.index(textBox, INSERT) #gets cursor index

    if event.char.isalpha() and not myGraph.isUserNode(event.char): #accept letters only
        if canvas.tk.call(canvas._w, 'select', 'item'):
            #if selected replace contents
            canvas.dchars(textBox, SEL_FIRST, SEL_LAST)
            canvas.select_clear()
            canvas.insert(textBox, "insert", event.char.upper())
            myGraph.setUserNode(node,canvas.itemcget(textBox,"text"))
            #current = myGraph.getArc(nodes[0],nodes[1])
        elif len(canvas.itemcget(textBox,"text"))<1:
            #append a digit (limited to 1 letter)
                labelDeselected(False)

    elif event.keysym == "BackSpace":
        canvas.itemconfig(textBox,font="Times 10 normal")
        myGraph.delUserNode(node)
        canvas.dchars(textBox, SEL_FIRST, SEL_LAST)
        canvas.select_clear()


    for i in range(0,myGraph.getNumNodes()):
        drawNode(i)



def labelDeselected(clear=True):
    """
    Deselects text box and updates matrix
    also removes arc if set to 0 or blank
    """
    textBox = canvas.focus()

    if textBox != "":

        value =  canvas.itemcget(textBox,"text")

        if not canvas.gettags(textBox)[0] == "l":
            #if an arc weight

            nodes = (int(canvas.gettags(textBox)[1][1:3]),
                     int(canvas.gettags(textBox)[1][3:]))



            if value not in ["","0"]:
                if "." in value:
                    try:
                        value = float(value.strip(' "'))
                    except:
                        #If invalid weight entered:
                        #Perform a fix
                        first = True
                        newValue = ""
                        for s in value:
                            if s != ".":
                                newValue += s
                            if s == "." and first:
                                newValue += s
                                first = False
                        canvas.itemconfig(textBox,text=newValue)
                        control.myDescBox.setText("ERROR","Invalid decimal "+value+". Has been corrected")

                else:
                    value = int(value)
                if myGraph.getArc(nodes[0],nodes[1])== myGraph.getArc(nodes[1],nodes[0]):
                    myGraph.setArc(int(nodes[0]),int(nodes[1]),value)
                else:
                    myGraph.setArc(int(nodes[0]),int(nodes[1]),value,True)
            else:
                delArc(nodes[0],nodes[1],myGraph.getArc(nodes[0],nodes[1]) == myGraph.getArc(nodes[1],nodes[0]))
    if clear != False:
        canvas.focus("")
        canvas.select_clear()
    myMatrixView.update()
    myArcView.update()

def togMatrix(event=None):
    if myMatrixView.isShown():
        myMatrixView.hide()
    else:
        myMatrixView.show()

def togArcView(event=None):
    if myArcView.isShown():
        myArcView.hide()
    else:
        myArcView.show()

def setStart():
    global coordClicked
    old = myGraph.getStart()
    if myGraph.getStart() == coordClicked:
        myGraph.setStart(None)
    else:
        myGraph.setStart(coordClicked)
        if myGraph.getEnd() == coordClicked:
            drawNode(myGraph.getEnd())
            myGraph.setEnd(None)
    drawNode(coordClicked)
    if old != None:
        drawNode(old)

def setEnd():
    global coordClicked,myGraph
    old = myGraph.getEnd()
    if myGraph.getEnd() == coordClicked:
        myGraph.setEnd(None)
    else:
        myGraph.setEnd(coordClicked)
        if myGraph.getStart() == coordClicked:
            drawNode(myGraph.getStart())
            myGraph.setStart(None)
    if old != None:
        drawNode(old)
    drawNode(coordClicked)

def disabledClicked():
    global coordClicked,myGraph
    if myGraph.getNodeState(coordClicked) == "normal":
        myGraph.setNodeState(coordClicked,"disabled")
    else:
        myGraph.setNodeState(coordClicked,"normal")

    for j in range(0,2):
        drawNode(coordClicked) #redraw the node at new pos
        #redraws the arcs connected to the node:
        neigh = myGraph.neighbors(coordClicked)
        revNeighbors = myGraph.revNeighbors(coordClicked)
        for i in neigh:
            drawArc(coordClicked,i)
        for i in revNeighbors:
            drawArc(i,coordClicked)


def resize(event=None):
    myMatrixView.resize()
    myArcView.resize()

#------------------------------------------------------------------------------
# Step Algorithms
#------------------------------------------------------------------------------

def doKruskal(event=None):
    global myGraph,myKruskal,myArcView
    if myKruskal==None:
        reset()
        myKruskal = kruskal(myGraph)
    kResult= myKruskal.nextStep()
    if kResult[0] != "3":
        if kResult[1]:
            if len(kResult[2]) == 1:
                control.myDescBox.setText("STEP 1","Choose the arc of least weight ("+myGraph.getLetter(kResult[0][1][0])+myGraph.getLetter(kResult[0][1][1])+").")
            else:
                control.myDescBox.setText("STEP 2","Choose from those arcs remaining the arc of least weight\nwhich does not form a cycle with already chosen arcs ("+myGraph.getLetter(kResult[0][1][0])+myGraph.getLetter(kResult[0][1][1])+").")
            arcCol(myGraph,kResult[0][1][0],kResult[0][1][1],"green")
            arcCol(myGraph,kResult[0][1][1],kResult[0][1][0],"green")
        else:
            control.myDescBox.setText("STEP 2","Arc "+myGraph.getLetter(kResult[0][1][0])+myGraph.getLetter(kResult[0][1][1])+" rejected as it forms a cycle with already chosen arcs.")
            arcCol(myGraph,kResult[0][1][0],kResult[0][1][1],"red")
            arcCol(myGraph,kResult[0][1][1],kResult[0][1][0],"red")
    else:
        control.myDescBox.setText("STEP 3","Repeat Step 2 until n-1 arcs have been chosen.\nThe minimum spanning tree has weight "+str(kResult[1])+" units.")
        myKruskal=None
    myArcView.update()

def doPrim(event=None):
    global myGraph,myPrim,myMatrixView,control

    if myPrim==None:
        myMatrixView.clearPrim()
        reset()
        myPrim = prim(myGraph)
        nodeCol(myGraph,myPrim.getStartNode(),"green")
    pResult= myPrim.nextStep()


    if isinstance(pResult,int):
        nodeCol(myGraph,pResult,"green") #update canvas

        #update matrix
        myMatrixView.circleNode(pResult)
        myMatrixView.horizontalLine(pResult)

        control.myDescBox.setText("STEP 1"," Select any node ("+myGraph.getLetter(pResult) + ") to be the first node of T.")
    elif pResult[0] != "3":
        arcCol(myGraph,pResult[1][0],pResult[1][1],"green")
        nodeCol(myGraph,pResult[1][1],"green")
        myMatrixView.circleNode(pResult[1][1])
        myMatrixView.circleWeight(pResult[1][1],pResult[1][0])
        myMatrixView.horizontalLine(pResult[1][1])

        control.myDescBox.setText("STEP 2","Consider the arcs which connect nodes in T to nodes outside T.\nPick the one with minimum weight ("
                                +myGraph.getLetter(pResult[1][0])+myGraph.getLetter(pResult[1][1])
                                +"). Add this arc and the extra node ("
                                +myGraph.getLetter(pResult[1][1])
                                +") to T.")

    else:
        control.myDescBox.setText("STEP 3","Repeat Step 2 until T contains every node of the graph.\n"
                                  +"The minimum spanning tree has weight "+str(pResult[1])+" units.")
        myPrim=None

def doDj(event=None):
    global myGraph,myDj
    if myDj==None:
        reset()
        myDj = djikstra(myGraph)
    changedNode = myDj.nextStep()
    if changedNode[1] == "1":
        resetCols(myGraph)
        #Redraw start and ends to update if they weren't specified.
        drawNode(changedNode[0])
        canvas.itemconfig("n"+"%02d" % (myGraph.getEnd()),outline="red")
        drawDj(changedNode[0])
        nodeCol(myGraph,changedNode[0],"green")
        control.myDescBox.setText("STEP 1","Label the start node with zero and box this label.")
    elif changedNode[1] == "2":
        drawDj(changedNode[0])
        nodeCol(myGraph,changedNode[0],"orange")
        control.myDescBox.setText("STEP 2","Consider each node, Y connected to the most recently boxed node, X.\n"
                                  +"Temperarily label it with: (the perminant label of X) + XY.")
    elif changedNode[1] == "3":
        resetCols(myGraph)
        drawDj(changedNode[0])
        nodeCol(myGraph,changedNode[0],"green")
        control.myDescBox.setText("STEP 3","Choose the least of all the temporary labels of the network ("
                                  +myGraph.getLetter(changedNode[0])+")."
                                  +"\nMake this label permanent by boxing it")
    elif changedNode[3] == "4":
        drawDj(changedNode[0])
        resetCols(myGraph)
        nodeCol(myGraph,changedNode[0],"green")
        for arc in changedNode[1]:
            arcCol(myGraph,arc[0],arc[1],"green")
        control.myDescBox.setText("STEP 5","Go backwards through the network, retracing the path of shortest length\nfrom the destination node to the start node."
                                  +"    Weight: "+str(changedNode[2])+".")
    else:
        #reset()
        myDj = None

def drawDj(node=None):
    """
    Draws a djikstra working out box next to the node specified.
    """
    if myDj != None and node!=None:
        #Constants
        BOX_OFFSET = 25
        BOXWIDTH = 100
        BOXHEIGHT = 50

        coords =  myGraph.getCoords(node)
        coords = list(coords)
        coords[0] = coords[0]+BOX_OFFSET
        coords[1] = coords[1]+BOX_OFFSET
        x = coords[0]+BOXWIDTH/2-(len(myDj.getNode(node).getTempLbls())/2)

        #tempLbls
        tempLbls = myDj.getNode(node).getTempLbls()
        tempLbls = list(map(str,tempLbls))
        tempLbls = "  ".join(tempLbls)


        strNode = "%02d" % (node)

        if canvas.find_withtag("djB"+strNode) == (): #if box doesnt exist:
            #draw box
            canvas.create_rectangle(coords[0],coords[1],coords[0]+BOXWIDTH,coords[1]+BOXHEIGHT,fill="white",tags=("dj","djB"+strNode))
            canvas.create_line(coords[0],coords[1]+BOXHEIGHT/2,coords[0]+BOXWIDTH,coords[1]+BOXHEIGHT/2,tags=("dj","djL1"+strNode))
            canvas.create_line(coords[0]+BOXWIDTH/2,coords[1],coords[0]+BOXWIDTH/2,coords[1]+BOXHEIGHT/2,tags=("dj","djL2"+strNode))
            #draw text
            canvas.create_text(coords[0]+BOXWIDTH*0.25,coords[1]+BOXHEIGHT*0.25,text=myDj.getNode(node).getOrderOfLbl(),tags=("dj","djOLb"+strNode))
            canvas.create_text(coords[0]+BOXWIDTH*0.75,coords[1]+BOXHEIGHT*0.25,text=myDj.getNode(node).getPerminantLbl(),tags=("dj","djPLb"+strNode))
            canvas.create_text(x,coords[1]+BOXHEIGHT*0.75,text=tempLbls,tags=("dj","djTLb"+strNode))
        else:
            #Move box and update labels
            canvas.coords("djB"+strNode,coords[0],coords[1],coords[0]+BOXWIDTH,coords[1]+BOXHEIGHT)
            canvas.coords("djL1"+strNode,coords[0],coords[1]+BOXHEIGHT/2,coords[0]+BOXWIDTH,coords[1]+BOXHEIGHT/2)
            canvas.coords("djL2"+strNode,coords[0]+BOXWIDTH/2,coords[1],coords[0]+BOXWIDTH/2,coords[1]+BOXHEIGHT/2)

            canvas.coords("djOLb"+strNode,coords[0]+BOXWIDTH*0.25,coords[1]+BOXHEIGHT*0.25)
            canvas.itemconfig("djOLb"+strNode,text=myDj.getNode(node).getOrderOfLbl())
            canvas.coords("djPLb"+strNode,coords[0]+BOXWIDTH*0.75,coords[1]+BOXHEIGHT*0.25)
            canvas.itemconfig("djPLb"+strNode,text=myDj.getNode(node).getPerminantLbl())
            canvas.coords("djTLb"+strNode,x,coords[1]+BOXHEIGHT*0.75)
            canvas.itemconfig("djTLb"+strNode,text=tempLbls)

    else:
        canvas.delete("dj")

def doCPostman():
    global myGraph,myCPostman,canvas
    if myCPostman==None:
        reset()
        myCPostman = cPostman(myGraph)

    cpResult= myCPostman.nextStep()

    if cpResult == None:
        myCPostman=None
        resetCols(graph)
        canvas.delete("cp")
    elif cpResult[0] == "1":
        nodes = list(cpResult[1])
        resetCols(graph)
        for n in range(0,len(nodes)):
            nodeCol(myGraph,nodes[n],"green")
            nodes[n] = myGraph.getLetter(nodes[n])
        nodes = sorted(nodes)
        if len(nodes)!= 0:
            control.myDescBox.setText("STEP 1","Find all the nodes of odd order."
                                      +"\nThe odd nodes are "+", ".join(nodes)+".")
        else:
            control.myDescBox.setText("STEP 1","Find all the nodes of odd order."
                                      +"\nThere are no odd nodes.")
    elif cpResult[0] == "2":
        for arc in myGraph.arcs():
            canvas.itemconfig("a"+"%02d" % (arc[1][0])+"%02d" % (arc[1][1]),fill="black",width=1)
            canvas.itemconfig("a"+"%02d" % (arc[1][1])+"%02d" % (arc[1][0]),fill="black",width=1)
        for a in cpResult[2]:
            arcCol(myGraph,a[0],a[1],"green")
        control.myDescBox.setText("STEP 2","For each pair of nodes find the connecting path of minimum weight.\n"
                                  +"Weight of path connecting "+ myGraph.getLetter(cpResult[1][0])+myGraph.getLetter(cpResult[1][1]) + " is "+ str(cpResult[3]))

    elif cpResult[0] == "3":
        for arc in myGraph.arcs():
            canvas.itemconfig("a"+"%02d" % (arc[1][0])+"%02d" % (arc[1][1]),fill="black",width=1)
            canvas.itemconfig("a"+"%02d" % (arc[1][1])+"%02d" % (arc[1][0]),fill="black",width=1)
        for path in cpResult[1]:
            for a in path:
                arcCol(myGraph,a[0],a[1],"green")
        control.myDescBox.setText("STEP 3","Pair up all the odd nodes so that the sum of the weights of the connecting paths is minimised.")

    elif cpResult[0] == "4":
        for arc in myGraph.arcs():
            canvas.itemconfig("a"+"%02d" % (arc[1][0])+"%02d" % (arc[1][1]),fill="black",width=1)
            canvas.itemconfig("a"+"%02d" % (arc[1][1])+"%02d" % (arc[1][0]),fill="black",width=1)
        for path in cpResult[1]:
            for a in path:
                curve = drawCurve(myGraph.getCoords(a[0])[0],myGraph.getCoords(a[0])[1],myGraph.getCoords(a[1])[0],myGraph.getCoords(a[1])[1],True)
                canvas.addtag_withtag("cp",curve)
        canvas.lower("cp")
        control.myDescBox.setText("STEP 4","In the original graph, duplicate the minimum weight paths found in step 3.")
    elif cpResult[0] == "5":
        for arc in canvas.find_withtag("a"):
            canvas.itemconfig(arc,fill="green",width=3)
        for arc in canvas.find_withtag("cp"):
            canvas.itemconfig(arc,fill="green",width=3)
        control.myDescBox.setText("STEP 5","Find a trail containing every arc for the new (Eulerian) graph.")
    else:
        canvas.delete("cp")
        myCPostman=None
        resetCols(graph)

def doNearestN():
    global myGraph,myNearestN
    if myNearestN==None:
        reset()
        myNearestN = nearestN(myGraph)
        control.myDescBox.setText("STEP 1","Choose any starting node ("+myGraph.getLetter(myNearestN.getStartNode())+").")
        nodeCol(myGraph,myNearestN.getStartNode(),"green")
        myMatrixView.circleNode(myNearestN.getStartNode())

    else:
        nResult= myNearestN.nextStep()
        if nResult[0] == "error":
            warnings = ["All of the neighbors of the current node have already been added",
                        "There is no arc joining the first to the last node."]
            control.myDescBox.setText("ERROR",warnings[nResult[1]-1])
            myNearestN=None
            return

        if nResult[0] != None:
            arcCol(myGraph,nResult[1][1][0],nResult[1][1][1],"green")
            nodeCol(myGraph,nResult[1][1][1],"green")
            if nResult[0] == 2:
                control.myDescBox.setText("STEP 2","Consider the arcs which join the previous chosen node to not-yet-chosen nodes.\n"
                                          +"Pick one with the minimum weight. Add this arc ("
                                          + myGraph.getLetter(nResult[1][1][0])+myGraph.getLetter(nResult[1][1][1])
                                          +") and the new node ("
                                          +myGraph.getLetter(nResult[1][1][1])
                                          +"), to the cycle.")
                myMatrixView.circleNode(nResult[1][1][1])
                myMatrixView.circleWeight(nResult[1][1][1],nResult[1][1][0])
                myMatrixView.horizontalLine(nResult[1][1][1])
            else:
                control.myDescBox.setText("STEP 3 & 4","Repeat step 2 until all arcs have been chosen."+"Then add the arc that joins the\n"
                                          +"last-chosen node to the first-chosen node ("
                                          + myGraph.getLetter(nResult[1][1][0])+myGraph.getLetter(nResult[1][1][1])
                                          +"). Weight: "+ str(nResult[2]))
                myMatrixView.circleWeight(nResult[1][1][1],nResult[1][1][0])
                myMatrixView.horizontalLine(nResult[1][1][1])
        else:
            myNearestN=None
            resetCols(graph)

def doLowerB():
    global myGraph,myLowerB
    if myLowerB==None:
        reset()
        myLowerB = lowerB(copy.copy(myGraph))
        nodeCol(myGraph,myLowerB.getX(),"green")
        control.myDescBox.setText("STEP 1","Choose an arbitrary node, say "+myGraph.getLetter(myLowerB.getX())+".")
        return
    cResult= myLowerB.nextStep()
    if cResult[0] == 1:
        arcCol(myGraph,cResult[1][1][0],cResult[1][1][1],"green")
        arcCol(myGraph,cResult[2][1][0],cResult[2][1][1],"green")
        control.myDescBox.setText("STEP 1","Find the total of the two smallest weights of arcs incedent at "
                                  +myGraph.getLetter(myLowerB.getX())
                                  +" = "
                                  +str(cResult[3])
                                  +".")
    elif cResult[0] == 2:
        nodeCol(myGraph,myLowerB.getX(),"grey",DISABLED)

        for i in cResult[1]:
            arcCol(myGraph,i[1][0],i[1][1],"grey",DISABLED)
        for i in cResult[2]:
            arcCol(myGraph,i[1][0],i[1][1],"green")
        control.myDescBox.setText("STEP 2","Consider the arc formed by ignoring "+myGraph.getLetter(myLowerB.getX())
                                  +" and all arcs incident to "+myGraph.getLetter(myLowerB.getX())+"."
                                  +"\nFind the total weight for the minimum connector for this network = "
                                  + str(cResult[3]))
    elif cResult[0] == 3:
        arcCol(myGraph,cResult[1][0][1][0],cResult[1][0][1][1],"green")
        arcCol(myGraph,cResult[1][1][1][0],cResult[1][1][1][1],"green")
        nodeCol(myGraph,myLowerB.getX(),"grey",NORMAL)
        control.myDescBox.setText("STEP 3","The sum of the two totals, "+str(cResult[2])+"+"+str(cResult[3])+"="+str(cResult[4])+", is a lower bound.")
    else:
        myLowerB=None
        resetCols(graph)


"""
def doTourImprov():
    global myGraph,myTImprov,myNearestN
    if myTImprov==None:
        if myNearestN == None:
            control.myDescBox.setText("Error","Nearest neighbor must be run first")
            return
        tour = myNearestN.nextStep()[1]
        tour.insert(0,None)
        myTImprov = tourImprov(myGraph,tour)
        control.myDescBox.setText("STEP 1","Let i=1")
        return
    tiResult= myTImprov.nextStep()
    if tiResult[0] == "2":
        control.myDescBox.setText("STEP 2","Compare d(Vi,Vi+2) + d(Vi+1,Vi+3)\n i.e. Distance between "
                                            +myGraph.getLetter(tiResult[1])
                                            +myGraph.getLetter(tiResult[1]+2)
                                            +" + Distance between "
                                            +myGraph.getLetter(tiResult[1]+1)
                                            +myGraph.getLetter(tiResult[1]+3)
                                            +" ("+str(tiResult[4])+" + "+str(tiResult[5])+" = "+str(tiResult[4]+tiResult[5])+").")
        resetCols(graph)
        arcCol(myGraph,tiResult[2][0],tiResult[2][1],"green")
        arcCol(myGraph,tiResult[3][0],tiResult[3][1],"green")
    if tiResult[0] == "2.1":
        control.myDescBox.setText("STEP 2","d(Vi, Vi+2) + d(Vi+1,Vi+3)  is not less than d(Vi, Vi+1) + d(Vi+2, Vi+3)\n"
                                    + "i.e. "+str(tiResult[3]) +" is not < " + str(tiResult[4])+".")
    if tiResult[0] == "3":
        control.myDescBox.setText("STEP 3","Replace i by i+1.\ni is now "+str(tiResult[1]))
    if tiResult[0] == "4":
        if tiResult[1] == True:
            control.myDescBox.setText("STEP 4","i <= n so go back to Step 2")
        else:
            control.myDescBox.setText("STEP 4","i > n")
"""
#------------------------------------------------------------------------------
# General algorirthm procedures
#------------------------------------------------------------------------------

def reset(event=None):
    """resets algorithms"""
    global myGraph,myKruskal,myPrim,myDj,myNearestN,myLowerB,myCPostman
    global myMatrixView,myArcView
    #Clears object instances:
    myPrim=None
    myKruskal=None
    myCPostman = None
    drawDj()
    myDj = None
    myNearestN = None
    myLowerB = None
    control.selectChange()
    myMatrixView.clearPrim()
    resetColsOnly(myGraph) #resets arc and node colours


def clear(event=None):
    """clears canvas"""
    global myGraph
    global canvas
    global myKruskal,myPrim,myMatrixView,myArcView

    reset()
    myGraph = graph()

    #reinitializes matrix:
    if myMatrixView.isShown()==True:
        canvas.delete("matrix")
        myMatrixView = matrixView(root,canvas,myGraph,NORMAL)
    else:
        canvas.delete("matrix")
        myMatrixView = matrixView(root,canvas,myGraph,HIDDEN)

    #reinitializes arcs:
    if myArcView.isShown()==True:
        canvas.delete("arcView")
        myArcView = arcView(root,canvas,myGraph,NORMAL)
    else:
        canvas.delete("arcView")
        myArcView = arcView(root,canvas,myGraph,HIDDEN)

    #deletes all canvas items:
    canvas.delete("a")
    canvas.delete("b")
    canvas.delete("o")
    canvas.delete("w")
    canvas.delete("n")
    canvas.delete("l")
    canvas.delete("cp")

    globalVars()


def resetCols(graph):
    """Sets all colors to defaults"""
    for arc in canvas.find_withtag("a"):
        canvas.itemconfig(arc,fill="black",width=1,state=NORMAL)
    for arc in canvas.find_withtag("b"):
        canvas.itemconfig(arc,state=NORMAL)
    for arc in canvas.find_withtag("w"):
        canvas.itemconfig(arc,state=NORMAL)

    for node in canvas.find_withtag("n"):
        canvas.itemconfig(node,fill="grey",state=NORMAL)


def resetColsOnly(graph):
    """Sets all colors to defaults"""
    for arc in canvas.find_withtag("a"):
        canvas.itemconfig(arc,fill="black",width=1)
    for arc in canvas.find_withtag("b"):
        canvas.itemconfig(arc)
    for arc in canvas.find_withtag("w"):
        canvas.itemconfig(arc)
    for node in canvas.find_withtag("n"):
        canvas.itemconfig(node,fill="grey")


def arcCol(graph,n1,n2,col,state=NORMAL):
    """changes colour of arcs"""

    srtN1 = "%02d" % (n1)
    srtN2 = "%02d" % (n2)

    #as bidirectional arcs are treated as one, arc colour is changed for both
    canvas.itemconfig("a"+srtN1+srtN2,fill=col,width=3,state=state)
    canvas.itemconfig("a"+srtN2+srtN1,fill=col,width=3,state=state)

    canvas.itemconfig("w"+srtN1+srtN2,state=state)
    canvas.itemconfig("w"+srtN2+srtN1,state=state)
    canvas.itemconfig("b"+srtN1+srtN2,state=state)
    canvas.itemconfig("b"+srtN2+srtN1,state=state)

def nodeCol(graph,pos,col,state=NORMAL):
    """changes colour of nodes"""
    if pos != None:
        strPos = "%02d" % (pos)
    else:
        strPos = str(pos)
    canvas.itemconfig("n"+strPos,fill=col,state=state)



#------------------------------------------------------------------------------
# Main Code
#------------------------------------------------------------------------------
myGraph = graph()


#initializes Tkinter window
root = Tk()
root.title(PROGRAM_NAME)#title bar
root.minsize(640,480)#sets minimum size for window


#initializes gridding
root.columnconfigure(0, weight=1)


#Attempt to maxamize:
try:
    root.wm_state('zoomed')
except:
    None


#setup rows in grid:
root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=1)




#Intialises canvas
canvas = Canvas(root,bg="white")
canvas.grid(column=0, row=1, sticky=(N, W,E,S))

canvas.config(insertbackground="white")

#adds matrix view
myMatrixView = matrixView(root,canvas,myGraph,HIDDEN)
myArcView = arcView(root,canvas,myGraph,HIDDEN)

#creates undoRedo manager
unRedo = UndoRedo()


#add menus:
menu = Menus(root)
control = controls(root)

#add status bar
bar = StatusBar(root)
bar.grid(column=0, row=2, sticky=(N, W,E,S))
bar.setText("For help, press F1")





def nnF(event=None):
    global newNode

    newNode = False
    mouseClick(event)

def press(event=None):
    global shift
    shift = False

def tab(event=None):
    """Highlights next weight when tab pressed"""
    global canvas
    tags = list(canvas.find_withtag("w"))
    if canvas.focus() != "":
        new =  tags[(tags.index(int(canvas.focus()))+1)% len(tags)]
    else:
        new  = tags[0]
    canvas.focus(new)
    canvas.select_from(canvas.focus(), 0)
    canvas.select_to(canvas.focus(), len(canvas.itemcget(canvas.focus(),"text"))-1)


#adds event bindings
canvas.bind("<Button-1>", mouseClick)
canvas.bind("<ButtonRelease-1>", mouseUp)
canvas.bind("<B1-Motion>", addArc)
canvas.bind("<Motion>", updateStatus)
canvas.bind("<Shift-B1-Motion>", nodeMove,add='+')
canvas.bind("<Shift-B1-Motion>", addArc,add='+')
canvas.bind("<Shift-Button-1>", nnF,mouseClick)
canvas.bind_all("<KeyRelease>", press)
canvas.bind("<Button-3>", popup)
canvas.bind_all("<Key>", keypress)
canvas.bind("<Configure>", resize)
canvas.bind_all("<Return>", labelDeselected)
canvas.bind_all("<Tab>", tab)

#canvas.bind_all("<ErrorToMakeMyLifeEasy>", tab) #TEMP

#begins GUI
root.mainloop()
