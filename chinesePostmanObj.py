from djikstraObj import *
from dfsObj import *
import pickle


class cPostman(object):
    def __init__(self,graph):
        self.graph = graph
        self.oddNodes = []
        self.fromIndex = 0
        self.toIndex = 0

        self.step = 1

    def nextStep(self):
        if self.step == 1:
            #STEP 1
            for node in range(0,self.graph.getNumNodes()):
                if self.graph.isOdd(node):
                    self.oddNodes.append(node)
            self.step += 1
            if len(self.oddNodes) == 0:
                self.step = 5
            return ("1",self.oddNodes)

        elif self.step == 2:
            #STEP 2
            if self.fromIndex == self.toIndex:
                self.toIndex += 1
            node1 = self.oddNodes[self.fromIndex]
            node2 = self.oddNodes[self.toIndex]

            if self.graph.adjacent(node1,node2):
                output = ("2",(node1,node2),[(node1,node2)],self.graph.getArc(node1,node2))
            else:
                myDj = djikstra(self.graph)
                path = myDj.doAll(node1,node2)
                myDj = None
                output = ("2",(node1,node2),path[0],path[1])

            self.toIndex += 1
            if self.toIndex == len(self.oddNodes):
                self.fromIndex += 1
                self.toIndex = self.fromIndex

            if self.fromIndex == len(self.oddNodes)-1:
                self.step += 1

            return output

        elif self.step == 3 or self.step == 4:
            #STEP 3 Pair up all the odd nodes so the sum...
            #STEP 4 Duplicate paths...
            pairArray = []
            for x in self.get_pairs(set(self.oddNodes)):
                pairArray.append(x)

            highestIndex = None
            highestTotal = float(1e3000)

            for combination in range(0,len(pairArray)):
                combTotal = 0
                for pair in pairArray[combination]:
                    if self.graph.adjacent(pair[0],pair[1]):
                        combTotal += self.graph.getArc(pair[0],pair[1])
                    else:
                        myDj = djikstra(self.graph)
                        path = myDj.doAll(pair[0],pair[1])
                        myDj = None
                        combTotal += path[1]
                if combTotal < highestTotal:
                    highestTotal = combTotal
                    highestIndex = combination

            self.paths = []
            for pair in pairArray[highestIndex]:
                myDj = djikstra(self.graph)
                path = myDj.doAll(pair[0],pair[1])
                myDj = None
                self.paths.append(path[0])
            self.step +=1
            return(str(self.step-1),self.paths)

        elif self.step == 5:
            start = self.graph.getStart()
            #print self.getPath(self.paths,start)
            self.step +=1
            return ("5")


    def get_pairs(self,s):
        #FOUND THIS CODE
        #http://stackoverflow.com/questions/5360220/how-to-split-a-list-into-pairs-in-all-possible-ways
        if not s: yield []
        else:
            i = min(s)
            for j in s - set([i]):
               for r in self.get_pairs(s - set([i, j])):
                   yield [(i, j)] + r



    def getPath(self,dArcs,v):

        #Copy graph
        theFile = pickle.dumps(self.graph)
        self.graph = pickle.loads(theFile)


        #reformat duplicated arcs
        duplicatedArcs = []

        for i in dArcs:
            for j in i:
                duplicatedArcs.append(j)






        #STEP 1: Choose any vertex v of G and set current vertex equal to v and current trail equal to the empty sequence of edges.

        current = v
        trail = []


        while len(trail) < len(self.graph.arcs()):
            #STEP 2: Select any edge e incident with the current vertex but choosing a bridge only if there is no alternative.
            neighbors = list(self.graph.neighbors(current))
            for n in duplicatedArcs:
                if n[0] == current:
                    neighbors.append(n[1])
                elif n[1] == current:
                    neighbors.append(n[0])


            #Test if an arc is a bridge
            bridge = True
            while bridge:
                n = neighbors.pop()
                self.graph.delArc(current,n)
                if self.graph.getArc(current,n) == self.graph.getArc(n,current):
                    self.graph.delArc(n,current)
                myDfs = dfs(self.graph)
                bridge = not myDfs.connected()

            e = [current,n]

            #STEP 3: Add e to the current trail and set the current vertex equal to the vertex at the ?other end? of e. [If e is a loop, the current vertex will not move.]
            trail.append(e)
            current = n

            #STEP 4: Delete e from the graph. Delete any isolated vertices
            if (e[0],e[1]) not in duplicatedArcs and (e[1],e[0]) not in duplicatedArcs:
                self.graph.delArc(e[0],e[1])
                self.graph.delArc(e[1],e[0])

            else:
                if (e[0],e[1]) in duplicatedArcs:
                    duplicatedArcs.remove((e[0],e[1]))
                if (e[1],e[0]) in duplicatedArcs:
                    duplicatedArcs.remove((e[1],e[0]))


            current = n
        return trail


