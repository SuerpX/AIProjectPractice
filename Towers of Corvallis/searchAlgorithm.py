from nodeState import *
from tower import *
import copy
import time

def AStar(problem, NMax, isUsingAdmiH):
    #problem is the initState of Tower
    #NMax is the max number of nodes
    #isUsingAdmiH is the BOOL to control use which h (admissible or not)

    #showedNodes is the set of Nodes which have showed
    #notVisitedNodes is the set of Nodes which have not been visited
    #numOfNodes records the number of Nodes have showed
    timeStart = time.process_time()
    
    showedNodes = []
    notVisitedNodes = []
    initialNode = nodeState(None, Tower(problem), isUsingAdmiH)
    showedNodes.append(initialNode)
    notVisitedNodes.append(initialNode)
    #Calculate(initialNode, isUsingAdmiH)
    numOfNodes = 1
    goalState = None
    hCalculationTime = initialNode.heristicTime
    
    while numOfNodes <= NMax and len(notVisitedNodes) > 0 :
        #currentState et smallest f(n) state
        currentState = notVisitedNodes[0]
        for state in notVisitedNodes:
            if state.FN() < currentState.FN():
                currentState = state
        #check if currentState is goal state
        if currentState.tower.goalStateCheck():
            goalState = currentState
            break

        numOfNodes += 1
        childrenTower = currentState.tower.expand()
        childrenNode = []
        for ct in childrenTower:
           #print(ct.pegs[0],ct.pegs[1],ct.pegs[2])
            ns = nodeState(currentState, ct, isUsingAdmiH)
            childrenNode.append(ns)
            hCalculationTime += ns.heristicTime
            #print(childrenNode[-1].FN())
            #print("")
        
        for child in childrenNode:
            repetitiveState = False
            for targetState in showedNodes:
                if child.tower.sameCheck(targetState.tower):
                    minDepth = min(child.depth, targetState.depth)
                    if minDepth == child.depth:
                        targetState.parent = currentState
                        targetState.depth = currentState.depth + 1
                    repetitiveState = True
                    break
            if not repetitiveState:
                showedNodes.append(child)
                notVisitedNodes.append(child)

        notVisitedNodes.remove(currentState)
        
    totalSearchTime = time.process_time() - timeStart
    if goalState:
        if isUsingAdmiH:
            typeOfH = "Adimissible"
        else:
            typeOfH = "NonAdimissible"
        print("----------------------------A*----------------------------")
        print("The length of solution:          " + str(goalState.depth + 1))
        print("The number of nodes expanded:    " + str(len(showedNodes)))
        print("The total CPU time of heuristic: " + str(hCalculationTime))
        print("The total CPU time of A*:        " + str(totalSearchTime))
        print("The type of heuristic:           " + str(typeOfH))
        print("-----------path-----------")
        path = []
        gs = copy.deepcopy(goalState)
        while gs != None:
            path.append([gs.tower.pegs[0]] + [gs.tower.pegs[1]] + [gs.tower.pegs[2]])
            gs = gs.parent
        i = 0
        for x in reversed(path):
            i += 1
            print(str(i) + ": " + str(x))
        print("--------------------------")

    print()


def beamSearch(problem, NMax, isUsingAdmiH, beamWidth):
    timeStart = time.process_time()
    
    showedNodes = []
    notVisitedNodes = []
    initialNode = nodeState(None, Tower(problem), isUsingAdmiH)
    showedNodes.append(initialNode)
    notVisitedNodes.append(initialNode)
    numOfNodes = 1
    goalState = None

    hCalculationTime = initialNode.heristicTime
    
    while len(showedNodes) <= NMax and len(notVisitedNodes) > 0:
        #currentState et smallest f(n) state
        currentState = notVisitedNodes[0]
        for state in notVisitedNodes:
            if state.FN() < currentState.FN():
                currentState = state
        #check if currentState is goal state
        if currentState.tower.goalStateCheck():
            goalState = currentState
            break

        numOfNodes += 1
        childrenTower = currentState.tower.expand()
        childrenNode = []
        for ct in childrenTower:
           #print(ct.pegs[0],ct.pegs[1],ct.pegs[2])
            ns = nodeState(currentState, ct, isUsingAdmiH)
            childrenNode.append(ns)
            hCalculationTime += ns.heristicTime
            #print(childrenNode[-1].FN())
            #print("")
        notVisitedNodes.remove(currentState)
        for child in childrenNode:
            repetitiveState = False
            for targetState in showedNodes:
                if child.tower.sameCheck(targetState.tower):
                    minDepth = min(child.depth, targetState.depth)
                    if minDepth == child.depth:
                        targetState.parent = currentState
                        targetState.depth = currentState.depth + 1
                    repetitiveState = True
                    break
            if not repetitiveState:
                showedNodes.append(child)
                max = 0
                i = 0
                if len(notVisitedNodes) == beamWidth:
                    for nvn in notVisitedNodes:
                        if nvn.FN() > notVisitedNodes[max].FN():
                            max = i
                        i += 1
                    if notVisitedNodes[max].FN() > child.FN():
                        notVisitedNodes[max] = child
                else:
                    notVisitedNodes.append(child)
    if not goalState:
        goalState = currentState
    totalSearchTime = time.process_time() - timeStart
    if isUsingAdmiH:
        typeOfH = "Adimissible"
    else:
        typeOfH = "NonAdimissible"
    output = open(typeOfH + '/' + 'solution_bs' + str(beamWidth) + '_' + str(len(problem[0])) + 'disks' + '.txt', 'a')
    '''
    print("----------------------------Beam Search----------------------------")
    print("The beam width:                  " + str(beamWidth))
    print("The length of solution:          " + str(goalState.depth + 1))
    print("The number of nodes expanded:    " + str(len(showedNodes)))
    print("The total CPU time of heuristic: " + str(hCalculationTime))
    print("The total CPU time of A*:        " + str(totalSearchTime))
    print("The type of heuristic:           " + str(typeOfH))
    '''
    output.write("The beam width:                  " + str(beamWidth) + '\n')
    output.write("The length of solution:          " + str(goalState.depth + 1) + '\n')
    output.write("The number of nodes expanded:    " + str(len(showedNodes)) + '\n')
    output.write("The total CPU time of heuristic: " + str(hCalculationTime) + '\n')
    output.write("The total CPU time of A*:        " + str(totalSearchTime) + '\n')
    output.write("The type of heuristic:           " + str(typeOfH) + '\n')
        
    #print("-----------path-----------")
    output.write("-----------path-----------" + '\n')
    path = []
    gs = copy.deepcopy(goalState)
    while gs != None:
        path.append([gs.tower.pegs[0]] + [gs.tower.pegs[1]] + [gs.tower.pegs[2]])
        gs = gs.parent
    i = 0
    for x in reversed(path):
        i += 1
        #print(str(i) + ": " + str(x))
        output.write(str(i) + ": " + str(x) + '\n')
    #print("--------------------------")
    output.write("--------------------------\n\n")
    output.close()


    #print()
            
'''
AStar([[5,7,3,0,2,4,1,6],[],[]],float('inf'),False)
AStar([[5,7,3,0,2,4,1,6],[],[]],float('inf'),True)
'''
'''
a = [
    [2,3,4,1,0],
    [3,6,8,5,7,0,1,2,4],
    [4,0,2,1,3],
    [2,1,4,0,3],
    [0,1,3,4,2],
    [0,3,4,1,2],
    [3,0,1,4,2],
    [0,4,1,2,3],
    [3,4,2,1,0],
    [1,0,3,2,4],
    [0,4,2,1,3],
    [0,1,2,4,3],
    [3,2,0,1,4],
    [1,4,0,2,3],
    [1,0,3,4,2],
    [2,0,3,1,4],
    [1,2,0,3,4],
    [4,0,1,3,2],
    [1,2,3,4,0],
    [1,2,0,4,3],
    [4,3,1,0,2],
    ]
for i in a:
    beamSearch(Tower([i, [], []]), float('inf'), False, 100)


    '''

    

