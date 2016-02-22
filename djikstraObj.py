import uuid
import random

class djikstra(object):
    def __init__(self,graph):
        self.graph = graph
        self.djNodes = []
        self.X = None
        self.nextOrder = 2
        self.neighborIndex = 1
        self.neighbors = []
        self.D = 0

        if self.graph.getStart() == None and self.graph.getEnd() == None:
            self.graph.setStart(random.randint(0,self.graph.getNumNodes()-1))
            while self.graph.getEnd() == None or self.graph.getStart()==self.graph.getEnd():
                self.graph.setEnd(random.randint(0,self.graph.getNumNodes()-1))
        elif self.graph.getStart() == None:
            self.graph.setStart(random.randint(0,self.graph.getNumNodes()-1))
        elif self.graph.getEnd() == None:
            self.graph.setEnd(random.randint(0,self.graph.getNumNodes()-1))


        self.startNode = self.graph.getStart()
        self.endNode = self.graph.getEnd()

        #Add Blank Nodes
        for i in range(0,self.graph.getNumNodes()):
            self.djNodes.append(djNode(self.graph,i))


    def getNode(self,pos):
        return self.djNodes[pos]

    def nextStep(self):
        if self.X == "True":
            return [None,None,None,None]
        if self.X == None:
            #STEP 1: label start node...
            self.X = self.startNode
            self.djNodes[self.X].addTempLbl(0)
            self.djNodes[self.X].setOrderOfLbl(1)
            self.djNodes[self.X].setPerminantLbl()
            neighborsTup = self.graph.neighbors(self.X)
            self.neighbors = list(neighborsTup)
            self.neighborIndex = 0
            return [self.X,"1"]

        #remove permenent Lbls
        neighbors2 = []
        for i in range(0,len(self.neighbors)):
            if self.djNodes[self.neighbors[i]].getPerminantLbl() == "":
                #if not got a perm lbl
                neighbors2.append(self.neighbors[i])
        self.neighbors = neighbors2

        if  self.neighborIndex < len(self.neighbors):
            #STEP 2: Consider Each node connected to X...
            n = self.neighbors[self.neighborIndex]
            self.D = self.djNodes[self.X].getPerminantLbl()
            #New temp lbl:
            newDistance = self.D+self.graph.getArc(self.X,n)
            self.djNodes[n].addTempLbl(newDistance)

            self.neighborIndex += 1
            return [n,"2"]

        if self.neighborIndex == len(self.neighbors):
            #STEP 3: Choose the least temp Lbl...
            minNode = None
            for n in range(0,len(self.djNodes)): #loop through all nodes
                if self.djNodes[n].getPerminantLbl()=="": #if not labeled
                    if minNode != None:
                        #if not the first node tested...
                        if self.djNodes[n].getMinTempLbl() != False:
                            if self.djNodes[minNode].getMinTempLbl() > self.djNodes[n].getMinTempLbl():
                                #if temp lbl less than current lowest
                                minNode = n
                    elif self.djNodes[n].getMinTempLbl() != False:
                        minNode = n

            #Give node with lowest temp lbl a perminant lbl
            self.X = minNode
            self.djNodes[self.X].setPerminantLbl()
            self.djNodes[self.X].setOrderOfLbl(self.nextOrder)
            self.nextOrder += 1
            neighborsTup = self.graph.neighbors(self.X)
            self.neighbors = list(neighborsTup)
            self.neighborIndex = 0
            if self.X != self.endNode:
                return [self.X,"3"]

        if self.X == self.endNode:
            arcs = []
            weight = 0
            while self.X != self.startNode:
                n = self.graph.neighbors(self.X)
                for neigh in n:
                    if self.djNodes[neigh].getPerminantLbl() != "":
                        if (self.djNodes[self.X].getPerminantLbl()-self.djNodes[neigh].getPerminantLbl())==self.graph.getArc(neigh,self.X):
                           arcs.append((neigh,self.X))
                           weight += self.graph.getArc(neigh,self.X)
                           self.X = neigh
                           break
            self.X = "True"
            return [self.endNode,arcs,weight,"4"]



    def doAll(self,start,end):
        self.startNode = start
        self.endNode = end
        output = [None,"1"]

        while len(output)!= 4:
            output = self.nextStep()
        return output[1:]




class djNode(object):
    """Stores Djikstra data about a node"""
    def __init__(self,graph,node):
        self.graph = graph
        self.node = node

        self.orderOfLbl = ""
        self.perminantLbl  = ""
        self.tempLbl = []
        self.ID = uuid.uuid4()

    #Standard methods
    def __len__(self):
        return len(self.tempLbl)
    def __str__(self):
        return "ORDER: "+str(self.orderOfLbl)+" | PERM: "+str(self.perminantLbl) +"\nTEMP: " + str(self.tempLbl)
    def getOrderOfLbl(self):
        return self.orderOfLbl
    def getPerminantLbl(self):
        return self.perminantLbl
    def getTempLbls(self):
        return self.tempLbl
    def getMinTempLbl(self):
        if self.tempLbl == []:
            return False
        return min(self.tempLbl)
        return True
    def setOrderOfLbl(self,order):
        self.orderOfLbl = int(order)
    def setPerminantLbl(self):
        if self.tempLbl == []:
            return False
        self.perminantLbl = min(self.tempLbl)
    def addTempLbl(self,tempLbl):
        if self.tempLbl != []:
            if tempLbl < min(self.tempLbl):
                if int(tempLbl) == float(tempLbl):
                    tempLbl = int(tempLbl)
                else:
                    tempLbl = float(tempLbl)
                self.tempLbl.append(tempLbl)
        else:
            if int(tempLbl) == float(tempLbl):
                tempLbl = int(tempLbl)
            else:
                tempLbl = float(tempLbl)
            self.tempLbl.append(tempLbl)
