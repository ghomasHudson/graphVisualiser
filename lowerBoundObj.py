import random
from tkinter import messagebox as tkMessageBox
import operator
from primObj import *
import pickle



class lowerB(object):
    def __init__(self,graph):
        theFile = pickle.dumps(graph)
        self.graph = pickle.loads(theFile)
        self.step = 1
        self.ChosenXArcs = []
        self.step1Sum = 0
        self.step2Sum = 0
        self.step3Sum = 0

        #STEP 1: Choose an arbitary node, X...
        if self.graph.getStart() != None:
            self.X = self.graph.getStart()
        else:
            self.X = random.randint(0,self.graph.getNumNodes()-1)

    def nextStep(self):
        if self.step==1:
            #...Find the total of the two smallest weights incident at X
            arcsOfX = self.graph.arcs(self.X,False)
            sortedArcs = sorted(arcsOfX, key=operator.itemgetter(0))
            self.step1Sum = sortedArcs[0][0] + sortedArcs[2][0]
            self.step+= 1
            self.ChosenXArcs = [sortedArcs[0],sortedArcs[2]]
            return (1,sortedArcs[0],sortedArcs[2],self.step1Sum)

        elif self.step==2:
            #STEP 2: Consider the network ignoring X. Find total weight of minimum connector
            delArcs = self.graph.arcs(self.X,False)
            self.graph.delNode(self.X)
            myPrims = prim(self.graph)
            minConnector = myPrims.doAll()
            for i in range(0,len(minConnector)):
                minConnector[i] = list(minConnector[i])
                minConnector[i][1] = list(minConnector[i][1])
                if minConnector[i][1][0]>= self.X:
                    minConnector[i][1][0]+=1
                if minConnector[i][1][1]>= self.X:
                    minConnector[i][1][1]+=1
                self.step2Sum+=minConnector[i][0]
            self.step+= 1
            return (2,delArcs,minConnector,self.step2Sum)
        elif self.step==3:
            #STEP 3: Sum of two totals is a lower bound
            self.step3Sum = self.step1Sum + self.step2Sum
            self.step+= 1
            return (3,self.ChosenXArcs,self.step1Sum,self.step2Sum,self.step3Sum)
        else:
            return [None]


    def getX(self):
        return self.X
