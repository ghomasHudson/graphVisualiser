from Tkinter import *
from matrixViewObj import *

class arcView(matrixView):
    """
    Displays a list of the arcs in the graph in assending order. E.g:

    AB  10
    AC  9
    CB  8
    
    Inherits from matrixView
    """
    def __init__(self,parent,parentCanvas,graph,visibility):
        self.graph = graph
        self.canvasTag = "arcView"
        self.parentCanvas = parentCanvas
        self.visible = BooleanVar()
        if visibility == NORMAL:
            self.visible.set(True)
        else:
            self.visible.set(False)
            
        
        self.arcCanvas = Canvas(parent,bg="grey",width=100,height=100)
        parentCanvas.create_window(parentCanvas.winfo_width(),parentCanvas.winfo_height(),anchor=SE,window=self.arcCanvas,tag=self.canvasTag)
        parentCanvas.itemconfigure(self.canvasTag,state=visibility)
        self.arcCanvas.bind("<Button-1>", self.mouseClick)
        self.update()
        
    def resize(self,event=None):
        """Moves the arc view when the window is resized"""
        self.parentCanvas.coords(self.canvasTag,self.parentCanvas.winfo_width(),self.parentCanvas.winfo_height())
        
    def update(self,graph=None):
        """Refreshes the arcs"""
        global canvas
        if graph != None:
            self.graph = graph
            
        self.arcCanvas.delete(ALL) #Clears canvas
        self.arcCanvas.create_text(50,20,text="Arcs") #title
        
        #get list of sorted arcs
        sortedArcs = []
        sortedArcsOrig =  sorted(self.graph.arcs())

        #remove duplicates (for non-directed arcs)
        for i in range(0,len(sortedArcsOrig)):
            if (sortedArcsOrig[i][0],(sortedArcsOrig[i][1][1],sortedArcsOrig[i][1][0])) not in sortedArcs:
                sortedArcs.append(sortedArcsOrig[i])

        self.arcCanvas.configure(width=100,height=((len(sortedArcs)+2)*20)) #change height

        #draw arc in form: AB 10
        for i in range(0,len(sortedArcs)):
            arc = sortedArcs[i]
            n1 = self.graph.getLetter(arc[1][0])
            n2 = self.graph.getLetter(arc[1][1])
            weight = arc[0]
            arcString = n1+n2+" "*10+str(weight)
            arcTag = "%02d" % (arc[1][0])+"%02d" % (arc[1][1])
            arcColor = self.parentCanvas.itemcget("a"+arcTag, "fill")
            if arcColor == "":
                arcColor = self.parentCanvas.itemcget("a"+"%02d" % (arc[1][1])+"%02d" % (arc[1][0]), "fill")
            self.arcCanvas.create_text(50,(i+2)*20,text=arcString,tag=arcTag,fill=arcColor)
 
