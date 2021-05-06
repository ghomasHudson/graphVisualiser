from tkinter import *

class matrixView(object):
    """
    Draws the matrix representation of the graph. E.g:
        A    B    C
    -----------------
    A |       1    2
      |
    B |  1         3
      |
    C |  2    3
    """
    def __init__(self,parent,parentCanvas,graph,visibility):
        self.graph = graph
        self.canvasTag = "matrix"
        self.parentCanvas = parentCanvas
        self.visible = BooleanVar() #Variable to control menu checkbox
        if visibility == NORMAL:
            self.visible.set(True)
        else:
            self.visible.set(False)

        self.matrixCanvas = Canvas(parent,bg="grey",width=0,height=0)
        parentCanvas.create_window(parentCanvas.winfo_width(),0,anchor=NE,window=self.matrixCanvas,tag=self.canvasTag)
        parentCanvas.itemconfigure(self.canvasTag,state=visibility)
        self.matrixCanvas.bind("<Button-1>", self.mouseClick)
        self.update()

    def show(self):
        """Displays the matrix view"""
        self.parentCanvas.itemconfigure(self.canvasTag,state=NORMAL)
        self.visible.set(True)
    def hide(self):
        """Hides the matrix view"""
        self.parentCanvas.itemconfigure(self.canvasTag,state=HIDDEN)
        self.visible.set(False)
    def isShown(self):
        """Returns a boolean value of whether the matrix is currently visable"""
        return self.parentCanvas.itemcget(self.canvasTag,"state") == NORMAL
    def resize(self,event=None):
        """Moves the matrix view when the window is resized"""
        self.parentCanvas.coords(self.canvasTag,self.parentCanvas.winfo_width(),0)

    def circleNode(self,node):
        n1 = ord(self.graph.getLetter(node))-65
        self.matrixCanvas.create_oval(n1*50+65,15,n1*50+85,35,width=2,tag="nodeCircle")

    def circleWeight(self,n1,n2):
        n1 = ord(self.graph.getLetter(n1))-65
        n2 = ord(self.graph.getLetter(n2))-65
        self.matrixCanvas.create_oval(n2*50+65,n1*50+65,n2*50+85,n1*50+85,width=2,tag="weightCircle")


    def horizontalLine(self,n1):
        n1 = ord(self.graph.getLetter(n1))-65
        nodes = self.graph.getNumNodes()
        self.matrixCanvas.create_line(50,n1*50+75,(nodes+1)*50,n1*50+75,width=1.5,tag="hrzLine")

    def clearPrim(self):
        self.matrixCanvas.delete("nodeCircle")
        self.matrixCanvas.delete("weightCircle")
        self.matrixCanvas.delete("hrzLine")

    def update(self,graph=None):
        """Refreshes the matrix"""
        if graph != None:
            self.graph = graph
        #PROBLEM: letters aren't in same order as node!!
        self.matrixCanvas.delete("matrixNode")
        self.matrixCanvas.delete("matrixTblLine")
        self.matrixCanvas.delete("matrixWeight")
        self.matrixCanvas.delete("matrixLbl")
        arcs = self.graph.arcs()
        nodes = self.graph.getNumNodes()


        self.matrixCanvas.configure(width=(nodes+1)*50,height=(nodes+1)*50)
        self.matrixCanvas.create_line(0,50,(nodes+1)*50,50,tag="matrixTblLine")
        self.matrixCanvas.create_line(50,0,50,(nodes+1)*50,tag="matrixTblLine")
        self.matrixCanvas.create_text(((nodes+1)*50)/2+25,10,tag="matrixLbl")


        for node in range(0,nodes):
            self.matrixCanvas.create_text(node*50+75,25,text=self.graph.getNodeLabels()[node],tag="matrixNode")
            self.matrixCanvas.create_text(25,node*50+75,text=self.graph.getNodeLabels()[node],tag="matrixNode")
            for node2 in range(0,nodes):
                n1 = self.graph.letterGetPos(self.graph.getNodeLabels()[node])
                n2 = self.graph.letterGetPos(self.graph.getNodeLabels()[node2])
                weight = self.graph.getArc(n2,n1)
                if weight==None:
                    weight=chr(8210)
                self.matrixCanvas.create_text(node2*50+75,node*50+75,text=weight,tag="matrixWeight")

    def mouseClick(self,event):
        """Handles event when the matrix is clicked"""
        self.hide()
