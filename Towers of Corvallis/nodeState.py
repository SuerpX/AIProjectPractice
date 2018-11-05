import tower
import time

class nodeState(object):
    def __init__(self, parentNode, tower, isUsingAdmiH):
        self.parent = parentNode
        self.admissibleHeuristic = None
        self.notAdmissibleHeuristic = None
        self.tower = tower
        if parentNode != None:
            self.depth = parentNode.depth + 1
        else:
            self.depth = 0
        self.heuristic = float('inf')
        self.heristicTime = 0
        if isUsingAdmiH:
            self.heristicTime = self.admissibleH()
        else:
            self.heristicTime = self.notAdmissibleH()

    def admissibleH(self):
        # For the admissible heuristic function, we relax the problem by removing the constraint that we can only remove the top disk
        # keep the constraint that can not remove the bottommost of B and C peg directly
        timeStart = time.process_time()
        h = 0

        numOfDisks = self.tower.numberOfDisks
        k = 0
        for i in self.tower.pegs[0]:
            if i == numOfDisks - 1:
                k += 1
                numOfDisks -= 1
            else:
                break
            
        h = (len(self.tower.pegs[0]) - k) * 2 + len(self.tower.pegs[1]) + len(self.tower.pegs[2])

        k = 0
        if len(self.tower.pegs[1]) > 1:
            last = self.tower.pegs[1][0]
            for i in self.tower.pegs[1]:
                if last > i:
                    break
                else:
                    last = i
                    k += 1
                    #print(k, i)
                    
            h += (len(self.tower.pegs[1]) - k)
            
        k = 0
        if len(self.tower.pegs[2]) > 1:
            last = self.tower.pegs[2][0]
            for i in self.tower.pegs[2]:
                if last > i:
                    break
                else:
                    k += 1
                    last = i
                    #print(k, i)
            h += (len(self.tower.pegs[2]) - k)
            
        self.heuristic = h
        #print(h)
        timeComsuption = time.process_time() - timeStart
        return timeComsuption
        
    def notAdmissibleH(self):
        
        timeStart = time.process_time()

        h = 0

        numOfDisks = self.tower.numberOfDisks
        k = 0
        for i in self.tower.pegs[0]:
            if i == numOfDisks - 1:
                k += 1
                numOfDisks -= 1
            else:
                break
            
        h = (len(self.tower.pegs[0]) - k) * 2 + len(self.tower.pegs[1]) + len(self.tower.pegs[2])

        k = 0
        if len(self.tower.pegs[1]) > 1:
            last = self.tower.pegs[1][0]
            for i in self.tower.pegs[1]:
                if last > i:
                    h += (len(self.tower.pegs[1]) - k)
                last = i
                k += 1
                    #print(k, i)
            
        k = 0
        if len(self.tower.pegs[2]) > 1:
            last = self.tower.pegs[2][0]
            for i in self.tower.pegs[2]:
                if last > i:
                    h += (len(self.tower.pegs[2]) - k)
                k += 1
                last = i
                    #print(k, i)
            
            
        self.heuristic = h
        #print(h)

        timeComsuption = time.process_time() - timeStart
        return timeComsuption
        '''
        # For the non-admissible heuristic function, we relax the problem by removing the constraint that we can only remove the top disk
        # Then we pick the smallest disk form A and put it in B, do this until all disk in A is removed to B, then we just need to put back to A
        # For the state which there are disks not only on A but also on other pegs, we just need to put them together to A.
        h = 0
        # First put all disk in other pegs to A.
        for i in self.tower.pegs[1]:
            h += 1
        for i in self.tower.pegs[2]:
            h += 1
        #After put all disk in A, we need find the smallest and move it to another disk, then repeat until all disk in A are moved to another peg
        #Then put them back one by one. So for all disks are moved twice.
        h += self.tower.numberOfDisks * 2

        self.heuristic = h
        '''
        
        '''
        h = len(self.tower.pegs[2]) * 3 + len(self.tower.pegs[1]) * 3 + len(self.tower.pegs[0]) * 2
        self.heuristic = h
        
        '''
        '''
        h = 0
        numOfDisks = self.tower.numberOfDisks
        k = 0
        for i in self.tower.pegs[0]:
            if i == numOfDisks - 1:
                k += 1
                numOfDisks -= 1
            else:
                break
        #print(list(range(self.tower.numberOfDisks - 1, -1, -1)))
        
        for i in range(self.tower.numberOfDisks - k - 1, -1, -1):
            #print(i)
            findA = False
            kA = 0
            for j in self.tower.pegs[0]:
                kA += 1
                #print(i,j)
                if i == j:
                    findA = True
                    break
            if findA:
                #print(i)
                #print(len(self.tower.pegs[0]), kA)
                #if len(self.tower.pegs[0]) == i + kA:
#                    continue
                h += len(self.tower.pegs[0]) - kA + 2
                
            else:
                kB = 0
                findB = False
                for j in self.tower.pegs[1]:
                    kB += 1
                    if i == j:
                        findB = True
                        break
                if findB:
                    h += len(self.tower.pegs[1]) - kB + 1
                else :
                    kC = 0
                    
                    findC = False
                    for j in self.tower.pegs[2]:
                        kC += 1
                        if i == j:
                            findC = True
                            break
                    if findC:
                        h += len(self.tower.pegs[2]) - kC + 1
        self.heuristic = h
        #print(h)
        
        '''
        '''
        cost = 0
        goalPeg = self.tower.pegs[0]
        pegSize = len(goalPeg)

        isInOrder = True
        for i in range(0, pegSize):
            expectedDisc = self.tower.numberOfDisks - i -1

            # cost += 2*abs(goalPeg[i] - expectedDisc)

            isInOrder = isInOrder and (goalPeg[i] == expectedDisc)
            if not isInOrder:
                cost += 2 + abs(goalPeg[i] - expectedDisc)


        for thisPeg in self.tower.pegs:
            if not thisPeg == goalPeg:
                for i in range(0, len(thisPeg)):
                    for j in range(i, len(thisPeg)):
                        dP = thisPeg[i] - thisPeg[j]
                        if dP > 0:
                            cost += dP
                        cost += 1

        #print(1)

        self.heuristic = cost
        
        #print(cost)
        '''                    
                


    def FN(self):
        #print(self.heuristic + self.depth)
        return self.heuristic + self.depth

    

nodeState(None, tower.Tower([[2,3,1,0],[],[]]),False)
