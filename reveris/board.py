#from cell import cell
from copy import deepcopy
from tkinter import PhotoImage
class board(object):
    def __init__(self, size, canvas = None, currentPlayer = 'o', isPrint = True):
        self.chessboard = []
        self.size = size
        self.currentPlayer = 'o'
        self.currentChess = []
        self.currentPlayerDomain = []
        self.canvas = canvas
        self.isPrint = isPrint
        self.forceEnd = False
        self.endNum = 0
        for i in range(size):
            self.chessboard.append([])
            for j in range(size):
                self.chessboard[i].append(None)
        '''               
        for i in range(size):
            for j in range(size):
                print(self.chessboard[i][j].row, self.chessboard[i][j].colunm)
        '''
        # 1 is black(x), -1 is white(o)
        m = size // 2
        self.chessboard[m - 1][m - 1] = 1
        self.chessboard[m][m] = 1
        self.chessboard[m - 1][m] = -1
        self.chessboard[m][m - 1] = -1

        if canvas is not None:
            self.initCanvas(canvas)
            self.drawBoard()
            
    def printBoard(self):
        numhorizon = ' ' + ''.join(['  ' + str(i) + ' ' for i in range(self.size)])
        print(numhorizon)
        horizon = ' ' + ''.join ([' ---' for i in range(self.size)])
        for i in range(self.size):
            vertical = str(i)
            for j in range(self.size):
                v = self.chessboard[i][j]
          
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

    def playOne(self, i, j, player):
        if i is None or j is None:
            self.endNum += 1
            if self.endNum == 2:
                self.forceEnd = True
            if self.isPrint:
                print("Can not move!!")
            self.changePlayer()
            return True
        if i < 0 or j < 0 or i >= self.size or j >= self.size:
            if self.isPrint:
                print("wrong play, try again")
            return False
        cb = deepcopy(self.chessboard)
        if cb[i][j] is not None:
            if self.isPrint:
                print("has chesspiece")
            return False

        if player == 'o':
            self.endNum = 0
            cb[i][j] = -1
            numOfChange = self.changeChess(cb, i, j)
            if self.isPrint:
                print(numOfChange)
            if numOfChange != 0:
                self.chessboard = deepcopy(cb)
                self.changePlayer()
                if self.canvas is not None:
                    self.drawBoard()
                return numOfChange
            else:
                if self.isPrint:
                    print("wrong play, try again")
                return False
        elif player == 'x':
            self.endNum = 0
            cb[i][j]  = 1
            numOfChange = self.changeChess(cb, i, j)
            if numOfChange != 0:
                self.chessboard = deepcopy(cb)
                self.changePlayer()
                if self.canvas is not None:
                    self.drawBoard()
                return numOfChange
            else:
                if self.isPrint:
                    print("wrong play, try again")
                return False
        if self.isPrint:
            print("error step")
        return False

    def changePlayer(self):
        if self.currentPlayer == 'o':
            self.currentPlayer = 'x'
        else:
            self.currentPlayer = 'o'
    def changeChess(self, cb, i, j):
        numOfChange = 0
        chessType = cb[i][j] 

        #row up
        if i - 1 > 0:
            for si in range(i - 1, -1, -1):
                if cb[si][j]  is None:
                    break
                if cb[si][j]  == chessType:
                    for ci in range(si + 1, i):
                        if cb[ci][j]  == chessType * -1:
                            numOfChange += 1
                            cb[ci][j]  = chessType
                        
                    break
        #row down             
        if i + 1 < self.size - 1:
            for si in range(i + 1, self.size):
                if cb[si][j]  is None:
                    break
                if cb[si][j]  == chessType:
                    for ci in range(i + 1, si):
                        if cb[ci][j]  == chessType * -1:
                            numOfChange += 1
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
                            cb[i][cj]  = chessType
                    break
        #colunm right        
        if j + 1 < self.size - 1:
            for sj in range(j + 1, self.size):
                if cb[i][sj]  is None:
                    break
                if cb[i][sj]  == chessType:
                    for cj in range(j + 1, sj):
                        if cb[i][cj]  == chessType * -1:
                            numOfChange += 1
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
                            cb[i - cij][j - cij]  = chessType
                    break
        #diagonal rightdown        
        if j + 1 < self.size - 1 and i + 1 < self.size:
            maxIJ = self.size - max(i, j)
            for sij in range(1, maxIJ):
                if cb[i + sij][j + sij]  is None:
                    break
                if cb[i + sij][j + sij]  == chessType:
                    for cij in range(1, sij + 1):
                        if cb[i + cij][j + cij]  == chessType * -1:
                            numOfChange += 1
                            cb[i + cij][j + cij]  = chessType
                    break        

        #diagonal rightup       
        if i - 1 > 0 and j + 1 < self.size - 1:
            minIJ = min(i, self.size - j - 1)
            for sij in range(1, minIJ + 1):
                if cb[i - sij][j + sij]  is None:
                    break
                if cb[i - sij][j + sij]  == chessType:
                    for cij in range(1, sij + 1):
                        if cb[i - cij][j + cij]  == chessType * -1:
                            numOfChange += 1
                            cb[i - cij][j + cij]  = chessType
                    break
        #diagonal leftdown       
        if i + 1 < self.size and j - 1 > 0:
            maxIJ =  min(self.size - i - 1, j)
            for sij in range(1, maxIJ + 1):
                if cb[i + sij][j - sij]  is None:
                    break
                if cb[i + sij][j - sij]  == chessType:
                    for cij in range(1, sij + 1):
                        if cb[i + cij][j - cij]  == chessType * -1:
                            numOfChange += 1
                            cb[i + cij][j - cij]  = chessType
                    break 
 #       print(numOfChange)
        return numOfChange

    def isEnd(self):
        numOfo = 0
        numOfx = 0
        for x in self.chessboard:
            for y in x:
                if y  == -1:
                    numOfo += 1
                elif y  == 1:
                    numOfx += 1
        if self.isPrint:
            print('o:' + str(numOfo), 'x:' + str(numOfx))
        if numOfo == 0:
            return 'x'
        if numOfx == 0:
            return 'o'
        
        if numOfo + numOfx == self.size * self.size or self.forceEnd:
            if numOfo == numOfx:
                return 'a draw'
            if numOfo > numOfx:
                return 'o'
            else:
                return 'x'
        return False

    def initCanvas(self, canvas):
        c = 'A'
        canvas.create_rectangle(60, 60, (self.size + 1) * 60, (self.size + 1) * 60)
        for i in range(self.size):
            
            canvas.create_text(60 * (i + 2) - 30,30,text = c)
            canvas.create_text(30,60 * (i + 2) - 30,text = str(i + 1))
            
            canvas.create_line(60 * (i + 1),60 , 60 * (i + 1),(self.size + 1) * 60)
            canvas.create_line(60, 60 * (i + 1), (self.size + 1) * 60,60 * (i + 1))
            c = chr(ord(c) + 1)
            
        canvas.create_text((self.size - 1) * 60 + 20,60 * (self.size + 2) - 30, text = 'Current Player:')
        '''
        leftx = 50 + 15
        lefty = 60 * (self.size + 1) + 15
        rightx = 110 - 15
        righty = 60 * (self.size + 2) - 15
        canvas.create_oval(leftx, lefty, rightx, righty, outline = 'white', fill = 'white')
        '''
    def drawBoard(self):
        for x in self.currentChess:
            self.canvas.delete(x)
        self.currentChess = []
        if self.currentPlayer == 'o':
            color = 'white'
        else:
            color = 'black'
        leftx = (self.size - 1) * 60 + 70 + 15
        lefty = 60 * (self.size + 1) + 15
        rightx = (self.size - 1) * 60 + 130 - 15
        righty = 60 * (self.size + 2) - 15
        self.currentChess.append(self.canvas.create_oval(leftx, lefty, rightx, righty, outline = color, fill = color))
        
        for i in range(self.size):
            for j in range(self.size):
                if self.chessboard[j][i]  is not None:
                    leftx = (i + 1) * 60 + 10
                    lefty = (j + 1) * 60 + 10
                    rightx = (i + 2) * 60 - 10
                    righty = (j + 2) * 60 - 10
                    
                    if self.chessboard[j][i]  == -1:
                        color = 'white'
                    elif self.chessboard[j][i]  == 1:
                        color = 'black'
                    item = self.canvas.create_oval(leftx, lefty, rightx, righty, outline = color, fill = color)
                    self.currentChess.append(item)
        self.canvas.update()
        return
    def prepareBoard(self,domain):
        for x in self.currentPlayerDomain:
            self.canvas.delete(x)
        self.currentPlayerDomain = []
        for j,i in domain:
            leftx = (i + 1) * 60 + 20
            lefty = (j + 1) * 60 + 20
            rightx = (i + 2) * 60 - 20
            righty = (j + 2) * 60 - 20
            item = self.canvas.create_oval(leftx, lefty, rightx, righty, outline = 'gray', fill = 'gray')
            self.currentPlayerDomain.append(item)
        self.canvas.update()

'''
b = board(8)
#print(b.playOne(5, 3, 'o'))

b.printBoard()

print(b.playOne(5, 4, 'x'))
b.printBoard()
print(b.playOne(4, 2, 'x'))
b.printBoard()
print(b.playOne(5, 5, 'o'))
b.printBoard()
print(b.playOne(4, 5, 'x'))
b.printBoard()
print(b.playOne(3, 2, 'o'))
b.printBoard()
print(b.playOne(2, 5, 'o'))
b.printBoard()
'''

        
#start(16)
