from copy import deepcopy
class Tower(object):
    def __init__(self, a):
        self.pegs = []
        self.parent = None
        self.numberOfDisks = 0
        for i in range(0, 3):
            self.pegs.append([])
            self.pegs[i] = a[i]
            for j in a[i]:
                self.numberOfDisks += 1
        
    def move(self, originalState, originalPeg, targetPeg):
        newState = deepcopy(originalState)
        newState.parent = self
        newState.pegs[targetPeg].append(newState.pegs[originalPeg][-1])
        del newState.pegs[originalPeg][-1]
        return newState

    def expand(self):
        children = []
        for x in range(0, 3):
            if self.pegs[x]:
                for y in range(0, 3):
                    if x == y:
                        continue
                    children.append(self.move(self, x, y))
        return children
        
    def goalStateCheck(self):
        goalPeg = []
        for i in range(self.numberOfDisks - 1, -1, -1):
            goalPeg.append(i)
        if self.pegs[0] == goalPeg:
            return True
        return False

    def sameCheck(self, targetState):
        if targetState.pegs[0] == self.pegs[0] and targetState.pegs[1] == self.pegs[1] and targetState.pegs[2] == self.pegs[2]:
            return True
        return False

