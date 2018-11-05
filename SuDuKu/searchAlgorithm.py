import inference
from table import *
from copy import *
'''
def backtracking(t, isUsingMCV = False):
    constraintPropagation(t)
    while not t.checkComplete():
        backtrackings = t.backtrackings
        if not isUsingMCV:
            isBreak = False
            for x in t.table:
                if isBreak:
                    break
                for y in x:
                    if y.filled:
                        continue
                    if isBreak:
                        break
                    for d in y.domain:
                        if isBreak:
                            break
                        if backtrackings > 0:
                            backtrackings -= 1
                            continue
                        else:
                            tchild = deepcopy(t)
                            tchild.parent = t
                            i = y.coordRow
                            j = y.coordColumn
                            tchild.table[i][j].filled = True
                            tchild.table[i][j].num = d
                            isSuccess1 = tchild.forwardChecking(tchild.table[i][j])
                            isSuccess2 = constraintPropagation(tchild)
                            if isSuccess1 and isSuccess2:
                                t = tchild
                                isBreak = True
                            else:
                                t.backtrackings += 1
                                isBreak = True
        else:
            i, j = mostConstrainedVariable(t)
    t.writeFile()
'''
step = 0
nOfback = -1
def backtracking(t, isUsingMCV = False, rule = 0, s = False):
    global step
    global nOfback
    if s:
        step = 0
        nOfback = -1
    
    if step > 1000:
        if s:
            return False, nOfback
        return False
    if t.checkComplete():
        return t
    nOfback += 1
    v = selectunassignedVariable(t, isUsingMCV)
    for value in v.domain:
        step += 1
        if step > 1000:
            if s:
                return False, nOfback
            return False
        tCopy = deepcopy(t)
        i = v.coordRow
        j = v.coordColumn
        tCopy.table[i][j].filled = True
        tCopy.table[i][j].num = value
        isSuccess1 = tCopy.forwardChecking(tCopy.table[i][j])
        if rule > 0:
            isSuccess2 = constraintPropagation(tCopy, rule)
        else:
            isSuccess2 = True
        if isSuccess1 and isSuccess2:
            result = backtracking(tCopy, isUsingMCV, rule)
        else:
            continue
        if result:
            if s:
                return result,nOfback
            
            return result
    if s:
        return False, nOfback
    return False
      
def selectunassignedVariable(t, isUsingMCV):
    if isUsingMCV:
        return mostConstrainedVariable(t)
    else:
        for x in t.table:
            for y in x:
                if not y.filled:
                    return y
def b(t, rule):
    constraintPropagation(t,rule)
    if t.checkComplete():
        return True
    return False

def constraintPropagation(t, rule):
    changed = True
    while changed:
        changed = inference.nakedSingle(t)
        if not changed:
            changed = inference.hiddenSingle(t)
        if not changed and rule > 1:
            changed = inference.nakedPair(t)
        if not changed and rule > 1:
            changed = inference.hiddenPair(t)
        if not changed and rule > 2:
            changed = inference.nakedTriple(t)
        if not changed and rule > 2:
            changed = inference.hiddenTriple(t)
            
    for x in t.table:
        for y in x:
            if not y.filled and len(y.domain) == 0:
                return False
    return True

def mostConstrainedVariable(table):
    t = table.table
    minL = float('inf')
    for x in t:
        for y in x:
            if not y.filled:
                if len(y.domain) < minL:
                    minL = len(y.domain)
                    minV = y
    return minV

t = Table([
['0', '0', '0', '9', '0', '0', '0', '1', '0'],
['1', '0', '0', '0', '8', '0', '0', '0', '0'],
['0', '9', '0', '0', '0', '6', '2', '0', '0'],
['0', '1', '5', '0', '0', '3', '9', '0', '0'],
['0', '0', '7', '0', '9', '0', '8', '0', '0'],
['0', '0', '9', '6', '0', '0', '5', '2', '0'],
['0', '0', '2', '5', '0', '0', '0', '7', '0'],
['0', '0', '0', '0', '1', '0', '0', '0', '6'],
['0', '8', '0', '0', '0', '9', '0', '5', '0'],
])
t = backtracking(t, True, 3)
t.printTFormal()

'''
backtracking(Table([
['0', '0', '8', '0', '7', '0', '1', '0', '0'],
['0', '0', '0', '0', '0', '0', '0', '2', '0'],
['5', '0', '0', '4', '0', '0', '8', '0', '0'],
['0', '9', '0', '0', '0', '8', '5', '0', '4'],
['0', '0', '0', '1', '0', '4', '0', '0', '0'],
['8', '0', '3', '5', '0', '0', '0', '6', '0'],
['0', '0', '7', '0', '0', '3', '0', '0', '9'],
['0', '3', '0', '0', '0', '0', '0', '0', '0'],
['0', '0', '1', '0', '2', '0', '6', '0', '0'],
]))
'''
'''
b(Table([
['2', '0', '0', '0', '0', '6', '0', '5', '0'],
['3', '0', '0', '0', '9', '0', '0', '0', '2'],
['0', '0', '1', '0', '0', '0', '0', '0', '0'],
['5', '6', '0', '2', '0', '0', '4', '0', '0'],
['0', '0', '0', '6', '0', '3', '0', '0', '0'],
['0', '0', '7', '0', '0', '5', '0', '2', '8'],
['0', '0', '0', '0', '0', '0', '8', '0', '0'],
['7', '0', '0', '0', '1', '0', '0', '0', '3'],
['0', '4', '0', '8', '0', '0', '0', '0', '9'],
]))
'''


