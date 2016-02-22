#Depth First Search

class dfs(object):
    def __init__(self,graph):
        self.graph = graph
        
    def nextStep(self,start=0):
        self.discovered = []
        self.stack = []
        self.stack.append(start)
        
        while len(self.stack) != 0:
            v = self.stack.pop()
            if v not in self.discovered:
                self.discovered.append(v)
                for w in self.graph.neighbors(v):
                    self.stack.append(w)
        return self.discovered

    def connected(self):
        return len(self.nextStep()) == self.graph.getNumNodes()

    def numConnectedComponants(self):
        foundNodes = []
        numComponants = 0
        for n in range(0,self.graph.getNumNodes()):
            if n not in foundNodes:
                numComponants += 1
                newComponant = self.nextStep(n)
                for i in newComponant:
                    foundNodes.append(i)
        return numComponants
        
    
