#Graph Object

import operator

class graph(object):
    def __init__(self):
        self.gArray = [] # format: [r1[c1,c2],r2[c1,c2]...]
        self.cArray = [] # array of coordinates of the nodes
                         # format: [n1(x,y),n2(x,y),...]
        self.dArray = [] # array of disabled nodes
        self.userNodes = [] #array of letters set by user
        self.AlgorithmUsed = ""
        self.numNodes = 0
        self.startNode = None
        self.endNode = None

    def __str__(self):
        # convert gArray to string
        gString = ""
        for n in self.gArray:
            gString+="["
            for i in range(0,len(n)-1):
                gString+=str(n[i])
                gString+=","
            gString+=str(n[-1])
            gString+="]"
        cString = ""
        for n in self.cArray:
            cString+="["
            for i in range(0,len(n)-1):
                cString+=str(n[i])
                cString+=","
            cString+=str(n[-1])
            cString+="]"
        return "graph:" + gString + "\ncoords:" + cString

    def addNode(self,x,y):
        """adds a new node as position (x,y)"""
        #appends blanks to arrays
        self.gArray.append([None]*self.numNodes)
        self.cArray.append((x,y))
        self.userNodes.append(None)
        self.numNodes = self.numNodes+1
        for i in range(0,self.numNodes):
            self.gArray[i].append(None)
            
    def delNode(self,posX,y=None):
        """
        Removes a node.
        If 1 arg provided: by position
        If 2 args provided: by coordinate.
        """
        if y!=None:
            try:
                posX = self.CoordsGetIndex(posX,y)
            except:
                return False

        del self.gArray[posX]
        del self.cArray[posX]
        del self.userNodes[posX]
        self.numNodes = self.numNodes-1
        for i in range(0,self.numNodes):
            del self.gArray[i][posX]

    def setArc(self,posFrom,posTo,weight,directed=False):
        """Sets the weight of an arc"""
        self.gArray[posFrom][posTo] = weight
        if not directed:
            self.gArray[posTo][posFrom] = weight
    def getArc(self,posFrom,posTo):
        """returns the weight of an arc"""
        return self.gArray[posFrom][posTo]
    def delArc(self,posFrom,posTo):
        """Deletes an arc"""
        #Sets weight back to None
        self.gArray[posFrom][posTo] = None

    def getNumNodes(self):
        """returns the number of nodes in graph"""
        if self.numNodes == len(self.gArray):
            return self.numNodes
    def __len__(self):
        return self.numNodes

    def adjacent(self,posFrom,posTo):
        """returns true if there is an arc from posFrom to posTo"""
        return self.gArray[posFrom][posTo] != None

    def neighbors(self,pos):
        """returns tuple neighbors of the node pos."""
        neighbors = ()
        for i in range(0,self.numNodes):
            if self.gArray[pos][i] != None:
                neighbors = neighbors + (i,)
        return neighbors
    def revNeighbors(self,pos):
        """returns tuple neighbors of the node pos."""
        neighbors = ()
        for i in range(0,self.numNodes):
            if self.gArray[i][pos] != None:
                neighbors = neighbors + (i,)
        return neighbors

    def getOrder(self,pos):
        """Returns the order of a node"""
        return len(self.neighbors(pos))
    def isOdd(self,pos):
        """returns true if a node has odd order"""
        return self.getOrder(pos)%2 == 1
    def isEulerian(self):
        """
        Returns true if the graph is Eulerian.
        (i.e. there are no odd nodes)
        """
        #Loops through all nodes
        for node in range(0,self.numNodes):
            if self.isOdd(node)==True:
                return False
        return True
    
    def isSemiEulerian(self):
        """
        Returns true if the graph is semi-Eulerian.
        (i.e. there are 2 odd nodes)
        """
        oddCount = 0
        for node in range(0,self.numNodes):
            if self.isOdd(node)==True:
                oddCount += 1
        return oddCount==2


    def isDigraph(self):
        for i in range(0,self.numNodes):
            for j in range(0,self.numNodes):
                if self.getArc(i,j) != self.getArc(j,i):
                    return True
        return False

    def arcs(self,pos=None,direction=True):
        """
        Returns list of arcs in tuple format:
        (weight,(n1,n2))
        """
        arcs = ()
        if pos == None:
            for i in range(0,self.numNodes):
                for j in range(0,len(self.gArray[i])):
                    if self.gArray[i][j] != None:
                        arcs = arcs + ((self.gArray[i][j],(i,j)),)
        else:
            if direction:
                for j in range(0,len(self.gArray[pos])):
                    if self.gArray[pos][j] != None:
                        arcs = arcs + ((self.gArray[pos][j],(pos,j)),)
            else:
                    for j in range(0,len(self.gArray[pos])):
                        if self.gArray[pos][j] != None:
                            arcs = arcs + ((self.gArray[pos][j],(pos,j)),)
                        if self.gArray[j][pos] != None:
                            arcs = arcs + ((self.gArray[j][pos],(j,pos)),)
        return arcs

    #Coords
    def getCoords(self,pos):
        return self.cArray[pos]
    def setCoords(self,pos,x,y):
        self.cArray[pos] = (x,y)
    def CoordsGetIndex(self,x,y):
        try:
            return self.cArray.index((x,y))
        except:
            return False



    #letters
    def setUserNode(self,node,letter):
        if letter.isalpha():
            self.userNodes[node] = letter

    def delUserNode(self,node):
        self.userNodes[node] = None

    def isUserNode(self,testChar):
        return testChar in self.userNodes
    
    def isPosUserNode(self,testPos):
        return self.userNodes[testPos] != None


    def getLetter(self,pos):
        
        if self.userNodes.count(None) == len(self.userNodes):
            order = []
            for n in range(0,len(self.cArray)):
                order.append([n,self.cArray[n][0]+self.cArray[n][1]/2])
            order = sorted(order, key=operator.itemgetter(1))
            for i in range(0,len(order)):
                if order[i][0] == pos:
                    return chr(65+i)
        nodes = self.genNodes()                      
        return nodes[pos]
                    


    def letterGetPos(self,letter):
        if self.userNodes.count(None) == len(self.userNodes):
            order = []
            for n in range(0,len(self.cArray)):
                order.append([n,self.cArray[n][0]+self.cArray[n][1]/2])
            order = sorted(order, key=operator.itemgetter(1))
            
            return order[ord(letter)-65][0]

        nodes = self.genNodes()   
        return nodes.index(letter)

                    

    def genNodes(self):
        order = []
        for n in range(0,len(self.cArray)):
            order.append([n,self.cArray[n][0]+self.cArray[n][1]/2])
        order = sorted(order, key=operator.itemgetter(1))
        
        

        for n in range(0,len(order)):
            try:
                order[n][1] = ord(self.userNodes[order[n][0]])
            except:
                order[n][1] = self.userNodes[order[n][0]]


        offset = False
        
        for i in range(0,len(order)):
            if order[i][1] != None:
                if offset == False:
                     offset = order[i][1]-i
   

        if offset == False:
            offset = 65

        nodes = [None]*len(order)
        

        for i in range(0,len(order)):
            if order[i][1] != None:
                nodes[order[i][0]] = chr(order[i][1])
            else:
                letterCode = offset+i
                
                if letterCode > 90:
                    letterCode = (letterCode-90)+64
                if letterCode < 65:
                    letterCode = 90-(64-letterCode)
                
                while chr(letterCode) in self.userNodes or chr(letterCode) in nodes:
                    letterCode += 1
                    if letterCode > 90:
                        letterCode = (letterCode-90)+64
                    if letterCode < 65:
                        letterCode = 90-(64-letterCode)

                nodes[order[i][0]] = chr(letterCode)

        return nodes


    def getNodeLabels(self):
        letters = []
        for i in range(0,self.numNodes):
            letters.append(self.getLetter(i))
        return sorted(letters)


    def getStart(self):
        return self.startNode
    def setStart(self,start):
        self.startNode = start

    def getEnd(self):
        return self.endNode
    def setEnd(self,end):
        self.endNode = end

    def getNodeState(self,pos):
        if pos in self.dArray:
            return "disabled"
        else:
            return "normal"
    def getArcState(self,n1,n2):
        if (n1 in self.dArray) or (n2 in self.dArray):
            return "disabled"
        else:
            return "normal"
    def setNodeState(self,pos,state):
        if state == "normal":
            self.dArray.remove(pos)
        elif state == "disabled" and self.getNodeState(pos)=="normal":
            self.dArray.append(pos)




#TESTING
if __name__ == "__main__":
    print "TESTING"
    myGraph = graph()
    print "1.BLANK GRAPH"
    print myGraph
    print
    print "2.ADD A NODE"
    print "(adds 2 nodes at (1,2) and (3,4))"
    myGraph.addNode(1,2)
    myGraph.addNode(3,4)
    print myGraph
    print
    print "3.DELETE A NODE"
    print "3.1. by index:"
    myGraph.delNode(1)
    print myGraph
    print "3.2. by coords:"
    myGraph.delNode(1,2)
    print
    print "4.SET AN ARC"
    myGraph = graph()
    myGraph.addNode(1,2)
    myGraph.addNode(3,4)
    myGraph.setArc(0,1,9)
    print "4.1",myGraph.gArray[0][1] == 9 and myGraph.gArray[1][0] == 9
    myGraph = graph()
    myGraph.addNode(1,2)
    myGraph.addNode(3,4)
    myGraph.setArc(0,1,9,True)
    print "4.2",myGraph.gArray[0][1] == 9 and not myGraph.gArray[1][0] == 9

    print "5.GET COORDS"
    myGraph = graph()
    myGraph.addNode(1,2)
    myGraph.addNode(3,4)

    print "Coords of node 0:",myGraph.getCoords(0)
    print "Node index at coords (3,4):",myGraph.CoordsGetIndex(3,4)
    print "No node at points (9,9), returns false:",myGraph.CoordsGetIndex(9,9)

    print "6 RETURN LETTER"
    myGraph = graph()
    myGraph.addNode(3,4)
    myGraph.addNode(1,2)
    print "Letter of node 0:",myGraph.getLetter(0)
    print "Index of node 'A':",myGraph.letterGetPos("A")

    print "7.NUMBER OF NODES"
    myGraph = graph()
    myGraph.addNode(3,4)
    myGraph.addNode(1,2)
    print myGraph.getNumNodes()
