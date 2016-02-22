import random

class prim(object):
    def __init__(self,graph):
        self.graph = graph

        self.startNode = None
        self.minimumConnector = []
    def nextStep(self):
        if self.startNode == None:
            if self.graph.getStart() != None:
                self.startNode = self.graph.getStart()
            else:
                self.startNode = random.randint(0,self.graph.getNumNodes()-1)
            self.minimumConnectorNodes = [self.getStartNode()]
            return self.startNode

        if len(self.minimumConnectorNodes) <= self.graph.getNumNodes()-1:
            minArc = [float(1e3000),[float(1e3000),float(1e3000)]]
            for node in self.minimumConnectorNodes:
                for arc in self.graph.arcs(node,False):
                    if (arc[0] < minArc[0]) and (arc[1][1] not in self.minimumConnectorNodes):
                        minArc = arc
                    if (arc[0] < minArc[0]) and (arc[1][0] not in self.minimumConnectorNodes):
                        minArc = arc
            self.minimumConnector.append(minArc)
            if minArc[1][1] not in self.minimumConnectorNodes:
                self.minimumConnectorNodes.append(minArc[1][1])
            else:
                self.minimumConnectorNodes.append(minArc[1][0])
            return minArc
        else:
            weight = 0
            for i in self.minimumConnector:
                weight += i[0]
            return ("3",weight)
    def doAll(self):
        "Run the whole algorithm"
        result = []
        connector = []
        result = self.nextStep()
        result = self.nextStep()
        connector.append(result)
        while result[0] != "3": #Wait till returns None
            result = self.nextStep()
            connector.append(result)
        return connector[:-1]

    def getStartNode(self):
        return self.startNode
