import random
import tkMessageBox

class nearestN(object):
    def __init__(self,graph):
        self.graph=graph
        #STEP 1: Choose any starting node
        if self.graph.getStart() != None:
            self.startNode = self.graph.getStart()
        else:
            self.startNode = random.randint(0,self.graph.getNumNodes()-1)
        self.minimumConnectorNodes = [self.getStartNode()]
        self.minimumConnector = []
    def nextStep(self):
        if len(self.minimumConnectorNodes) <= self.graph.getNumNodes()-1:
            minArc = [float(1e3000),[float(1e3000),float(1e3000)]]
            node = self.minimumConnectorNodes[-1]

            #STEP 2: Consider the arcs which join to the previously chosen one...
            for arc in self.graph.arcs(node,False):
                #...pick arc with minimum weight
                if (arc[0] < minArc[0]) and (arc[1][1] not in self.minimumConnectorNodes):
                    minArc = arc
                if (arc[0] < minArc[0]) and (arc[1][0] not in self.minimumConnectorNodes):
                    minArc = arc

            if minArc == [float(1e3000),[float(1e3000),float(1e3000)]]:
                return ["error",1]

            self.minimumConnector.append(minArc)
            if minArc[1][1] not in self.minimumConnectorNodes:
                self.minimumConnectorNodes.append(minArc[1][1])
            else:
                self.minimumConnectorNodes.append(minArc[1][0])
            return (2,minArc)
        elif self.minimumConnectorNodes[-1] != self.startNode:
            #STEP 4: Then add the arc that joins the last-chosen node to the first one.
            minArc = (self.graph.getArc(self.minimumConnectorNodes[-1],self.startNode),(self.minimumConnectorNodes[-1],self.startNode))
            weight = 0
            for i in self.minimumConnector:
                weight+=i[0]
            if minArc[0] != None:
                self.minimumConnector.append(minArc)
                self.minimumConnectorNodes.append(minArc[1][1])
                weight+=minArc[0]
                return (4,minArc,weight)
            else:

                return ["error",2]
        else:
            return [None,self.minimumConnectorNodes]
    def getStartNode(self):
        return self.startNode
