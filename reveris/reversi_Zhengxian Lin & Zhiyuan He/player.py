from random import randint,choice
from copy import deepcopy
import pickle
#from simulator import simulator
from math import log, sqrt
import time
class player(object):
    def __init__(self, chessType, agentType, minmax_depth = None, h = 'good', mcts_time = 8):
        self.agentType = agentType
        self.chessType = chessType
        self.domain = []
        self.minmax_depth = minmax_depth
        self.minmax_node = 0
        self.heuristic = h
        self.mcts_time = mcts_time
#        self.mcts_depth = 1
        self.mcts_c = sqrt(2)
        self.mcts_states = {}

    def playOne(self, chessboard):
 #       self.domain = []
        if len(self.domain) == 0:
            return None,None
        if self.agentType == 'random':
            return self.agent_random(chessboard)
        elif self.agentType == 'minmax' and self.minmax_depth is not None:
            self.minmax_node = 0
            return self.agent_minmax_alpha_beta(chessboard)
        elif self.agentType == 'mcts':
            return self.agent_mcts(chessboard)
    def selectHeuristic(self,chessboard):
        if self.heuristic == 'good':
            return self.goodHeuristic(chessboard)
        elif self.heuristic == 'simple':
            return self.simpleHeuristic(chessboard)
                
    def agent_random(self, chessboard):
 #       self.checkDomain(chessboard)
     
        return self.domain[randint(0, len(self.domain) - 1)]
    
    def agent_minmax_alpha_beta(self, chessboard):
 #       print("node:" + str(self.minmax_node))
        _, i, j = self.max_value(chessboard, 1, - float('inf'), float('inf'))
        if (i is None or j is None) and len(self.domain) != 0:
            
            return self.domain[randint(0, len(self.domain) - 1)]
 #       print("node:" + str(self.minmax_node))
        return i, j

    def max_value(self, chessboard, depth, a, b):
        self.minmax_node += 1
 #       print("max")
        if depth >= self.minmax_depth:
            return self.selectHeuristic(chessboard), None, None
        value = - float('inf')
        actions = self.getDomain(chessboard, self.chessType)
        if len(actions) == 0:
            return - float('inf'), None,None
        
 #       print(actions)
        maxI = None
        maxJ = None
        for i,j in actions:
            cb = deepcopy(chessboard)
            self.changeChess(cb, i, j,ct = self.chessType)
 #           self.printcb(cb)
            v,_,_ = self.min_value(cb, depth + 1, a, b)
            if v >= b:
                return v, i, j
            a = max(v,a)
            if v > value:
                value = v
                maxI = i
                maxJ = j
        
 #       print(value, maxI, maxJ)
        return value, maxI, maxJ
    
    def min_value(self, chessboard, depth, a, b):
        self.minmax_node += 1
 #       print("min")
        if depth > self.minmax_depth:
            return self.selectHeuristic(chessboard), None, None
        value = float('inf')
        
        minI = None
        minJ = None
        if self.chessType == 'x':
            ct = 'o'
        else:
            ct = 'x'
        actions = self.getDomain(chessboard, ct)
        if len(actions) == 0:
            return float('inf'), None,None
        
 #       print(actions)        
        for i,j in actions:
            cb = deepcopy(chessboard)
            self.changeChess(cb, i, j, ct = ct)
            v,_,_ = self.max_value(cb, depth + 1, a, b)
            if v <= a:
                return v, i, j
            b = min(v,b)
            if v < value :
                value = v
                minI = i
                minJ = j
            
        return value, minI, minJ
    
    def simpleHeuristic(self,chessboard):
        if self.chessType == 'o':
            ct = -1
        else:
            ct = 1
        value = 0
        for x in chessboard:
            for y in x:
                if y  is not None:
                    if y  == ct:
                        value += 1
                    else:
                        value -= 1
        return value
    
    def goodHeuristic(self,chessboard):
        l = len(chessboard)
        if self.chessType == 'o':
            ct = -1
        else:
            ct = 1
        value = 0
        for i,x in enumerate(chessboard):
            for j,y in enumerate(x):
 #              print( i,j)
                if y  is not None:
                    
                    if y  == ct:
                        value += 1
                        if  i == 0 or  i == l - 1:
                            value += 4
                        if j == 0 or j == l - 1:
                            value += 4
                        if ( i == 0 and j == 0) or ( i == l - 1 and j == 0) or ( i == 0 and j == l - 1) or ( i == l - 1 and j == l - 1):
 #                           print(1111111111)
                            value += 100
                    else:
                        value += 1
                        if  i == 0 or  i == l - 1:
                           value -= 4
                        if j == 0 or j == l - 1:
                           value -= 4
                        if ( i == 0 and j == 0) or ( i == l - 1 and j == 0) or ( i == 0 and j == l - 1) or ( i == l - 1 and j == l - 1):
 #                           print(22222222)
                            value -= 100
                        
        return value
  #      print("vlaue:" +  str(value))
    def printcb(self, cb):
        size = len(cb)
        numhorizon = ' ' + ''.join(['  ' + str(i) + ' ' for i in range(size)])
        print(numhorizon)
        horizon = ' ' + ''.join ([' ---' for i in range(size)])
        for i in range(size):
            vertical = str(i)
            for j in range(size):
                v = cb[i][j] 
          
                if v == 1:
                    v = ' x '
                elif v == -1:
                    v = ' o '
                elif v is None:
                    v = '   '
                vertical += '|' + v
            vertical += '|'
            print(horizon)
            print(vertical)
        print(horizon)
    def getDomain(self, chessboard, chessType):
        domain = []
        size = len(chessboard)
        ct = chessType
        def isAllowed(i,j):
            n = self.changeChess(chessboard, i, j, False, ct)
 #           print(n)
            if n == 0:
                return False
            else:
                return True
        for i in range(size):
            for j in range(size):
                if chessboard[i][j]  is None:
                    if isAllowed(i,j):
                        domain.append((i,j))
        return domain
    
    def checkDomain(self, chessboard):
        self.domain = []
        size = len(chessboard)
        def isAllowed(i,j):
            n = self.changeChess(chessboard, i, j, False)
 #           print(n)
            if n == 0:
                return False
            else:
                return True
        for i in range(size):
            for j in range(size):
                if chessboard[i][j]  is None:
                    if isAllowed(i,j):
                        self.domain.append((i, j))
        #print(self.domain)
    def changeChess(self, cb, i, j, isChange = True, ct = None):
        
        numOfChange = 0
        if ct is None:
            if self.chessType == 'o':
                chessType = -1
            else:
                chessType = 1
        else:
            if ct == 'o':
                chessType = -1
            elif ct == 'x':
                chessType = 1
        
        size = len(cb)
        if isChange:
            cb[i][j]  = chessType
        #row up
        if i - 1 > 0:
            for si in range(i - 1, -1, -1):
                if cb[si][j]  is None:
                    break
                if cb[si][j]  == chessType:
                    for ci in range(si + 1, i):
                        if cb[ci][j]  == chessType * -1:
                            numOfChange += 1
                            if isChange:
                                cb[ci][j]  = chessType
                        
                    break
        #row down             
        if i + 1 < size - 1:
            for si in range(i + 1, size):
                if cb[si][j]  is None:
                    break
                if cb[si][j]  == chessType:
                    for ci in range(i + 1, si):
                        if cb[ci][j]  == chessType * -1:
                            numOfChange += 1
                            if isChange:
                                cb[ci][j]  = chessType
                    break
        #colunm left               
        if j - 1 > 0:
            for sj in range(j - 1, -1, -1):
                if cb[i][sj]  is None:
                    break
                if cb[i][sj]  == chessType:
                    for cj in range(sj + 1, j):
                        if cb[i][cj]  == chessType * -1:
                            numOfChange += 1
                            if isChange:
                                cb[i][cj]  = chessType
                    break
        #colunm right        
        if j + 1 < size - 1:
            for sj in range(j + 1, size):
                if cb[i][sj]  is None:
                    break
                if cb[i][sj]  == chessType:
                    for cj in range(j + 1, sj):
                        if cb[i][cj]  == chessType * -1:
                            numOfChange += 1
                            if isChange:
                                cb[i][cj]  = chessType
                    break
        
        #diagonal leftup        
        if i - 1 > 0 and j - 1 > 0:
            minIJ = min(i, j)
            for sij in range(1, minIJ + 1):
                if cb[i - sij][j - sij]  is None:
                    break
                if cb[i - sij][j - sij]  == chessType:
                    for cij in range(1, sij + 1):
                        if cb[i - cij][j - cij]  == chessType * -1:
                            numOfChange += 1
                            if isChange:
                                cb[i - cij][j - cij]  = chessType
                    break
        #diagonal rightdown        
        if j + 1 < size - 1 and i + 1 < size:
            maxIJ = size - max(i, j)
            for sij in range(1, maxIJ):
                if cb[i + sij][j + sij]  is None:
                    break
                if cb[i + sij][j + sij]  == chessType:
                    for cij in range(1, sij + 1):
                        if cb[i + cij][j + cij]  == chessType * -1:
                            numOfChange += 1
                            if isChange:    
                                cb[i + cij][j + cij]  = chessType
                    break        

        #diagonal rightup       
        if i - 1 > 0 and j + 1 < size - 1:
            minIJ = min(i, size - j - 1)
            for sij in range(1, minIJ + 1):
                if cb[i - sij][j + sij]  is None:
                    break
                if cb[i - sij][j + sij]  == chessType:
                    for cij in range(1, sij + 1):
                        if cb[i - cij][j + cij]  == chessType * -1:
                            numOfChange += 1
                            if isChange:
                                cb[i - cij][j + cij]  = chessType
                    break
        #diagonal leftdown       
        if i + 1 < size and j - 1 > 0:
            maxIJ =  min(size - i - 1, j)
            for sij in range(1, maxIJ + 1):
                if cb[i + sij][j - sij]  is None:
                    break
                if cb[i + sij][j - sij]  == chessType:
                    for cij in range(1, sij + 1):
                        if cb[i + cij][j - cij]  == chessType * -1:
                            numOfChange += 1
                            if isChange:
                                cb[i + cij][j - cij]  = chessType
                    break 
 #       print(numOfChange)
        return numOfChange

    def agent_mcts(self, chessboard):
        actions = self.getDomain(chessboard, self.chessType)
        #expansion
        if len(actions) == 0:
            return None, None
        if len(actions) == 1:
            return actions[0]

        start = time.time()
        state = cbstate(chessboard,self.chessType)
        count = 0
        while time.time() - start < self.mcts_time:
            self.simulate(state,actions)
 #           count += 1
 #           print(count)
#            print(time.time() - start)
#        print(count)
        bestV = -1
#        for sss in self.mcts_states:
 #           print(sss, self.mcts_states[sss])
        states = []

        bestPlays = -1
        bestWins = -1
        bestI = -1
        bestJ = -1
        for i,j in actions:
            cb = deepcopy(chessboard)
            self.changeChess(cb, i, j,self.chessType)
            s = cbstate(cb,self.chessType)
            
 #           states.append(s)
            if s.getHashString() in self.mcts_states:
                wins,plays = self.mcts_states[s.getHashString()]
     #           print("{:.2%}".format(wins / plays),plays)
                if plays > bestPlays:
                    bestPlays = plays
                    bestWins = wins
                    bestI = i
                    bestJ = j
                elif plays == bestPlays:
                    if wins > bestWins:
                        bestPlays = plays
                        bestWins = wins
                        bestI = i
                        bestJ = j
 #       print("best: {:.2%}".format( bestWins / bestPlays ), bestPlays) 
        return bestI, bestJ
        
        '''
        for i,j in actions:
            cb = deepcopy(chessboard)
            self.changeChess(cb, i, j,self.chessType)
 #           if cbstate(cb,self.chessType).getHashString() in self.mcts_states:
 #               print(111111)
            s = cbstate(cb,self.chessType)
            states.append(s)
 #           print(s.getHashString())
            ratio = self.mcts_states[s.getHashString()]
            print("{:.2%}".format(ratio[0] / ratio[1]))
        '''
        '''
        return self.chooseBestAction(states)
        '''
        '''
        bestS = self.chooseBestS(states)
        for i,s in enumerate(states):
            if s == bestS:
                ratio = self.mcts_states[s.getHashString()]
                print("best: {:.2%}".format( ratio[0] / ratio[1] ))
                return actions[i]
        '''
 #       return bestI,bestJ
        
    def simulate(self,state, actions):
        expand = True
        ct = self.chessType
        visitedSelf = set()
        vistiedOppo = set()
        #simulate
        stopNum = 0
        goon = True
        while goon:
            states = []
            if len(actions) == 0:
                stopNum += 1
                if stopNum == 2:
                    goon = False
            else:
                stopNum = 0
            
            #expandation
                for i,j in actions:
                    childcb = deepcopy(state.getcb())
                    self.changeChess(childcb, i, j,ct = ct)
                    states.append(cbstate(childcb,ct))
                #selection
     #           if len(states) > 0:
                unexplored = self.checkUnexplored(states)
                if len(unexplored) == 0:
                    state = self.chooseBestS(states)
                else:
                    state = choice(unexplored)
     #           print(unexplored)
     #           else:
                if ct == self.chessType:
                        visitedSelf.add(state.getHashString())
                        if expand:
                            if state.getHashString() not in self.mcts_states:
                                expand = False
                                self.mcts_states[state.getHashString()] = [0,0]
            if ct == 'o':
                ct = 'x'
            else:
                ct = 'o'
            #print(state)
            #expandation
            actions = self.getDomain(state.getcb(), ct)
        #backpropagation
        self.backpropagation(visitedSelf, self.isWinner(state.getcb()))
    
    def isWinner(self, chessboard):
        selfN = 0
        oppoN = 0
        if self.chessType == 'o':
            ct = -1
        else:
            ct = 1
        for x in chessboard:
            for y in x:
                if y  is not None:
                    if y  == ct:
                        selfN += 1
                    else:
                        oppoN += 1
 #       print(selfN,oppoN)
        if selfN > oppoN:
            return True
        return False
    def backpropagation(self, vs, isWin):
        for s in vs:
            if s in self.mcts_states:
                self.mcts_states[s][1] += 1
                if isWin:
                    self.mcts_states[s][0] += 1
        '''
        for s in vo:
            if s in self.mcts_states:
                self.mcts_states[s][1] += 1
                if not isWin:
                    self.mcts_states[s][0] += 1
        '''
                
    def chooseBestS(self, states):
        #UCB calculation
        sumplays = 0
        for s in states:
            sumplays += self.mcts_states[s.getHashString()][1]
       # print(sumplays)
        bestV = -1
        for s in states:
            numOfWin = self.mcts_states[s.getHashString()][0]
            numOfPlays = self.mcts_states[s.getHashString()][1]

            v = numOfWin / numOfPlays + self.mcts_c * sqrt(log(sumplays) / numOfPlays)
            if v > bestV:
                bestV = v
                bestS = s
        return bestS
        
    def checkUnexplored(self,states):
        ue = []
 #       print(states)
        for s in states:
            if s.getHashString() not in self.mcts_states:
                ue.append(s)
        return ue
    


class cbstate(object):
    def __init__(self, cb, ct):
        self.cb = deepcopy(cb)
        self.ct = ct
 #       for i in cb:
#            print(cb)
        self.s = tuple([tuple(cb[i]) for i in range(8)])
 #       self.s = str(cb)
#        print(self.s)
        
    def getcb(self):
        return self.cb
    def getHashString(self):
        return self.s
    '''
    def stringize(self, chessboard):
        if self.ct == 'o':
            ct = -1
        else:
            ct = 1
        s = ''
        for x in chessboard:
            for y in x:
                if y  is None:
                    s += '0'
                elif y  == ct:
                    s += '1'
                elif y  == ct * -1:
                    s += '2'
        return s
    '''
"""
    def agent_mcts1(self,chessboard):
        fr = open('dataFile','rb')
        self.mctsData = pickle.load(fr)
        '''
        '''
        actions = self.getDomain(chessboard, self.chessType)
        if len(actions) == 0:
            return None, None
        maxI = -1
        maxJ = -1
        maxV = -1
        for i,j in actions:
            cb = deepcopy(chessboard)
            self.changeChess(cb, i, j,ct = self.chessType)
            '''
            '''
            s = self.stringize(cb)
 #           s = s[::-1]
            '''
            '''
 #           print(self.mctsData['0000000000000000000100000001100000012000000000000000000000000000'])
            
            if s in self.mctsData:
                #print(111111111111111111111111111111)
                v = self.mctsData[s][0] / self.mctsData[s][1] * self.goodHeuristic(chessboard)
            
                if maxV < v:
                        maxV = v
                        maxI = i
                        maxJ = j
    
        if maxI != -1:
 #           print(11111111111111)
            return maxI, maxJ
        else:
            for i,j in actions:
                cb = deepcopy(chessboard)
                self.changeChess(cb, i, j,ct = self.chessType)
                if self.chessType == 'o':
                    ct = 'x'
                else:
                    ct = 'o'
                sim = simulator(cb, None,ct)
                v = sim.simulate()
                v = v[0] / v[1]
                if maxV < v:
                        maxV = v
                        maxI = i
                        maxJ = j
            del sim
            sim = None
            del sim
        return maxI, maxJ
            
        
        def self_agent_mcts_helper(i,j,chessboard)
            if len(ac
            actions = self.getDomain(chessboard, self.chessType)
            if len(actions) == 0:
            maxI = -1
            maxJ = -1
            maxV = -1
            maxCB = None
            for i,j in actions:
                cb = deepcopy(chessboard)
                self.changeChess(cb, i, j,ct = self.chessType)
                s = self.stringize(cb)
                
                if s in self.mctsData:
                    v = self.mctsData[s]
                    if maxV < v:
                        maxV = v
                        maxI = i
                        maxJ = j
                        maxCB = cb
                        
            if maxI != -1:
                return oppo_agent_mcts_helper(maxI, maxJ, maxCB)
            else:
                cb = deepcopy(chessboard)
                i, j = actions[randint(0, len(actions) - 1)]
                self.changeChess(cb, i, j,ct = self.chessType)
                return oppo_agent_mcts_helper(i, j, cb)
                
        def oppo_agent_mcts_helper(i,j,chessboard):
            if self.chessType = 'o':
                ct = 'x'
            else:
                ct = o
            actions = self.getDomain(chessboard, ct)
            if len(actions) == 0:
                return i,j
            maxI = -1
            maxJ = -1
            maxV = -1
            maxCB = None
            for i,j in actions:
                cb = deepcopy(chessboard)
                self.changeChess(cb, i, j,ct = ct)
                s = self.stringize(cb)
                
                if s in self.mctsData:
                    v = self.mctsData[s]
                    if maxV < 1 - v:
                        maxV = 1 - v
                        maxI = i
                        maxJ = j
                        maxCB = cb
                        
            if maxI != -1:
                return oppo_agent_mcts_helper(maxI, maxJ, maxCB)
            else:
                cb = deepcopy(chessboard)
                i, j = actions[randint(0, len(actions) - 1)]
                self.changeChess(cb, i, j,ct = self.chessType)
                return oppo_agent_mcts_helper(i, j, cb)
            
            
    def agent_mcts2(self,chessboard):
        fr = open('dataFile','rb')
        self.mctsData = pickle.load(fr)
        #mcts_depth = 3

        actions = self.getDomain(chessboard, self.chessType)
        if len(actions) == 0:
            return None, None
        maxI = -1
        maxJ = -1
        maxV = -1
        for i,j in actions:
            cb = deepcopy(chessboard)
            self.changeChess(cb, i, j,ct = self.chessType)
            s = self.stringize(cb)
            if s in self.mctsData:
                v = self.mctsData[s][0] / self.mctsData[s][1] * self.goodHeuristic(chessboard)
            else:
                fz, fm = self.oppo_value(cb,0)
                v = fz / fm
            if maxV < v:
                    maxV = v
                    maxI = i
                    maxJ = j
        return maxI, maxJ
        
    
    def self_value(self, chessboard, depth):
        if depth >= self.mcts_depth:
            sim = simulator(chessboard, self.mctsData,self.chessType)
            v = sim.simulate()
#            print(v[0],v[1])
            return v[0],v[1]
        maxCB = []
        value = - 1
        actions = self.getDomain(chessboard, self.chessType)
        l = len(actions)
        if l == 0:
            return 0,1
        
        sumOfFz = 0
        sumOfFm = 0
        for i,j in actions:
            cb = deepcopy(chessboard)
            self.changeChess(cb, i, j,ct = self.chessType)
            if len(maxCB) < 3:
                maxCB.append((self.goodHeuristic(cb),i,j,cb))
            else:
                if self.goodHeuristic(cb) > maxCB[0][0]:
                    maxCB[0] = (self.goodHeuristic(cb),i,j,cb)
                    maxCB = sorted(maxCB)
                    
 #           fz,fm = self.oppo_value(cb, depth + 1)
            sumOfFz += fz
            sumOfFm += fm

        for _, i, j, cb in maxCB:
            fz,fm = self.oppo_value(cb, depth + 1)
            sumOfFz += fz
            sumOfFm += fm
        return sumOfFz,sumOfFm
            
            
        return sumOfFz, sumOfFm
    
    def oppo_value(self, chessboard, depth):
        if self.chessType == 'x':
            ct = 'o'
        else:
            ct = 'x'
        if depth >= self.mcts_depth:
            sim = simulator(chessboard, self.mctsData,ct)
            v = sim.simulate()
 #           print(v[0],v[1])
            return 1 - v[0],v[1]
        minCB = []
        value = - 1
        actions = self.getDomain(chessboard, self.chessType)
        l = len(actions)
        if l == 0:
            return 1,1

        sumOfFz = 0
        sumOfFm = 0
        for i,j in actions:
            cb = deepcopy(chessboard)
            self.changeChess(cb, i, j,ct = ct)
            if len(maxCB) < 3:
                maxCB.append((self.goodHeuristic(cb),i,j,cb))
            else:
                if self.goodHeuristic(cb) > minCB[2][0]:
                    minCB[0] = (self.goodHeuristic(cb),i,j,cb)
                    minCB = sorted(minCB)
                    
            fz,fm = self.self_value(cb, depth + 1)
            sumOfFz += fz
            sumOfFm += fm
            
        return sumOfFm - sumOfFz, sumOfFm
    
    def stringize(self, chessboard):
        self.chessType
        if self.chessType == 'o':
            ct = -1
        else:
            ct = 1
        s = ''
        for x in chessboard:
            for y in x:
                if y  is None:
                    s += '0'
                elif y  == ct:
                    s += '1'
                elif y  == ct * -1:
                    s += '2'
        return s
    """

#p = player('w', 'random')
