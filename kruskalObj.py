class kruskal(object):
    def __init__(self,graph):
        self.graph=graph
        self.sortedArcs = []
        self.minimumConnectorNodes = []
        self.minimumConnector = []
    def nextStep(self):
        if self.sortedArcs == []:
            self.sortedArcs = self.sortArcs()
        if len(self.minimumConnector)>=self.graph.getNumNodes()-1:
            weight = 0
            for i in self.minimumConnector:
                weight += i[0]
            return ("3",weight)
        else:
            arc = self.sortedArcs.pop(0)
            self.minimumConnector.append(arc)
            if self.hasCycle(self.minimumConnector):
                self.minimumConnector.pop()
                return (arc,False,self.minimumConnector)
            else:
                if arc[1][0] not in self.minimumConnectorNodes:
                    self.minimumConnectorNodes.append(arc[1][0])
                if arc[1][1] not in self.minimumConnectorNodes:
                    self.minimumConnectorNodes.append(arc[1][1])
                return (arc,True,self.minimumConnector)
    def sortArcs(self):
        sortedArcs = []
        sortedArcsOrig =  sorted(self.graph.arcs())
        for i in range(0,len(sortedArcsOrig)):
            if (sortedArcsOrig[i][0],(sortedArcsOrig[i][1][1],sortedArcsOrig[i][1][0])) not in sortedArcs:
                sortedArcs.append(sortedArcsOrig[i])
        return sortedArcs
                                 


    def hasCycle(self,path):
        color = {}
        pred = {}
        nodes = []
        oldPath = path
        path = []
        for i in oldPath:
            path.append(i)
            path.append((i[0],(i[1][1],i[1][0])))
        for i in path:
            for j in range(0,2):
                if i[1][j] not in nodes:
                    nodes.append(i[1][j])
        for u in nodes:
            color[u] = "w"
            pred[u] = None
        #time = 0
        for u in nodes:
            if color[u] == "w":
                boolean = self.dfs(u,path,color,pred)
                if boolean:
                    return True
                
    def dfs(self,u,path,color,pred):
        color[u] = "g"
        adjacent = []
        for i in path:
            if i[1][0] == u:
                adjacent.append(i[1][1])
            if i[1][1] == u:
                adjacent.append(i[1][0])
        for v in adjacent:
            if color[v] == "g" and pred[u]!=v:
                return True
            if color[v] == "w":
                pred[v] = u
                self.dfs(v,path,color,pred)
        color[u] = "b"
        return False
