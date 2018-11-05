import inference
class Cell(object):
    def __init__(self, domain, coordRow, coordColumn, filled = False, num = None):
        self.domain = domain
        self.coordRow = coordRow
        self.coordColumn = coordColumn
        self.filled = filled
        self.num = num
        self.alldiff = [[],[],[]]

    def remove(self, val):
        if val in self.domain:
            self.domain.remove(val)
            return True
        return False

    def domain_size(self):
        return len(self.domain)
    
    def setConstraintVariable(self, t):
        alldiff = [[],[],[]]
        i = self.coordRow
        j = self.coordColumn
        for y in range(0,9):
            if not t[i][y].filled and y != self.coordColumn:
                alldiff[0].append(t[i][y])
            if not t[y][j].filled and y != self.coordRow:
                alldiff[1].append(t[y][j])
        
        i = i // 3
        j = j // 3
        
        for n in range(i * 3, i * 3 + 3):
            for m in range(j * 3, j * 3 + 3):
                if not t[n][m].filled and not (n == self.coordRow and m == self.coordColumn):
                   # print(n,m)
                    alldiff[2].append(t[n][m])
        self.alldiff = alldiff
        
    def getConstraintVariable(self, n = 3):
        if n == 3:
            return self.alldiff
        return self.alldiff[n]
    

class Table():
    def __init__(self, tableList):
        self.table = []
        self.backtrackings = 0
        self.tableList = tableList
        for i, x in enumerate(tableList):
            self.table.append([])
            for j, y in enumerate(x):
                if y == '0':
                    d = ['1','2','3','4','5','6','7','8','9']
                    self.table[i].append(Cell(d, i, j))
                else:
                    self.table[i].append(Cell([y], i ,j, True, y))
        self.setAlldiff()
        self.refreshDomain()
        
    def printT(self):
        for x in self.table:
            for y in x:
                if not y.filled:
                    print(str(y.domain) + ',',end='')
                else:
                    print(str(y.num) + ',',end='')
            print()
    def printTFormal(self):
        n = 1
        for x in self.table:
            
            for y in x:
                n = 5
                for d in y.domain:
                    print(d, end = '')
                    n -= 1
                print(" " * n, end = '')
                print(",", end = '')
            print()
                
            print()
    def writeFile(self):
        output = open('result.txt', 'a')
        output.write("--------------------solved------------------------\n")
        for x in self.table:
            for y in x:
                n = 2
                for d in y.domain:
                    output.write(d)
                    n -= 1
                output.write(" " * n)
                output.write(",")
            output.write('\n')
                
            output.write('\n')
    def refreshDomain(self):
        for x in self.table:
            for y in x:
                if not y.filled:
                    continue
                self.forwardChecking(y)
   #     self.printT()
    
    def forwardChecking(self,c):
        alldiff = c.getConstraintVariable()
        for x in alldiff:
            for y in x:
                y.remove(c.num)
                if y == []:
                    return False
        return True
    
    def setAlldiff(self):
        for x in self.table:
            for y in x:
                y.setConstraintVariable(self.table)
                
    def checkComplete(self):
        for x in self.table:
            for y in x:
                if y.filled:
                    continue
                else:
                    return False
                    break
        return True

def test(i , j):
    i = i // 3
    j = j // 3
    for n in range(i * 3, i * 3 + 3):
        for m in range(j * 3, j * 3 + 3):
            print((n,m))
'''
t = Table([
['2', '4', '0', '3', '0', '0', '0', '0', '0'],
['0', '0', '0', '5', '2', '0', '4', '0', '7'],
['0', '0', '0', '0', '4', '6', '0', '0', '8'],
['6', '1', '0', '7', '0', '0', '0', '8', '4'],
['0', '0', '9', '0', '6', '0', '5', '0', '0'],
['7', '3', '0', '0', '0', '5', '0', '6', '1'],
['1', '0', '0', '4', '7', '0', '0', '0', '0'],
['3', '0', '2', '0', '5', '1', '0', '0', '0'],
['0', '0', '0', '0', '0', '2', '0', '1', '9']
])
'''

'''
t = Table([
['0', '0', '3', '0', '1', '0', '0', '0', '8'],
['0', '0', '0', '4', '0', '0', '0', '3', '0'],
['8', '7', '0', '0', '0', '3', '0', '2', '0'],
['0', '1', '0', '0', '0', '9', '6', '0', '5'],
['3', '0', '0', '8', '6', '7', '0', '0', '2'],
['9', '0', '6', '5', '0', '0', '0', '4', '0'],
['0', '2', '0', '9', '0', '0', '0', '7', '4'],
['0', '9', '0', '0', '0', '6', '0', '0', '0'],
['5', '0', '0', '0', '7', '0', '1', '0', '0']
])
'''
'''
t = Table([
['1', '7', '0', '0', '0', '0', '0', '0', '6'],
['0', '0', '6', '0', '9', '0', '0', '4', '0'],
['3', '0', '0', '0', '7', '0', '0', '0', '0'],
['0', '0', '0', '9', '0', '0', '0', '3', '0'],
['0', '9', '4', '0', '2', '0', '8', '7', '0'],
['0', '3', '0', '0', '5', '0', '0', '0', '0'],
['0', '0', '0', '0', '6', '0', '0', '0', '1'],
['0', '8', '0', '0', '1', '0', '5', '0', '0'],
['5', '0', '0', '0', '0', '0', '0', '8', '2']
])

changed = True
while changed:
    changed = inference.nakedSingle(t)
    if not changed:
        changed = inference.hiddenSingle(t)
    if not changed:
        changed = inference.nakedPair(t)
print("*********************")
t.printT()
print("*********************")
inference.hiddenPair(t)
inference.nakedTriple(t)
t.printTFomal()
'''

