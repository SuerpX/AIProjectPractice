#import graphics
#import threading
from board import *
from tkinter import *
from player import *
from copy import deepcopy
import time
#import time

def startCmd(size ,currentPlayer = 'o'):
    
    b = board(size)
    while True:
        b.printBoard()
        resEnd = b.isEnd()
        if resEnd:
            print("The winner is: " + str(resEnd))
            break
        
        if currentPlayer == 'o':
            s = 'o'
        else:
            s = 'x'
        print("current player is " + s)
        s = input("row and column:")
        i = s[0]
        j = s[2]
 #       print(i,j)
        res = b.playOne(int(i),int(j), currentPlayer)

        if not res:
            print("wrong play, try again")
        else:
            
            if currentPlayer == 'o':
                currentPlayer = 'x'
            else:
                currentPlayer = 'o'


def startWin(size, player1 = 'human', player2 = 'human', minmax_depth1 = None, minmax_depth2 = None, h1 = 'good', h2 = 'good', time1 = 5, time2 = 5):
    tk = Tk()
    width = 60 * (size + 2)
    height = 60 * (size + 2)
    canvas = Canvas(tk, width = width,height = height)
    canvas.pack()
    background_image = PhotoImage(file = "timg.gif", master = canvas, width = width, height = height)
    canvas.create_image(0,0,anchor="nw",image=background_image)
 #   canvas.wm_attributes('-alpha', 0.3)
    
 #   canvas.grid()

 #   image = Image.open("timg.jpg")  
#    im = ImageTk.PhotoImage(image)  
  
#    canvas.create_image(300,50,image = im)
    b = board(size, canvas)
    playero = player('o', player1,minmax_depth1,h1,time1)
    playerx = player('x', player2,minmax_depth2,h2,time2)
    currentPlayer = playero
    btnIsStart = True
 #   print(currentPlayer.agentType)


 
    
    def preparePlayer():
        print("----------")
        print(currentPlayer.agentType,currentPlayer.chessType)
        currentPlayer.checkDomain(b.chessboard)
 #       print(currentPlayer.domain)
        b.prepareBoard(currentPlayer.domain)
        
        if len(currentPlayer.domain) != 0:
            b.prepareBoard(currentPlayer.domain)
        else:
            b.playOne(None,None, b.currentPlayer)
            changePlayer()
        
        
    def changePlayer():
        nonlocal currentPlayer
        if currentPlayer == playerx:
            currentPlayer = playero
        else:
            currentPlayer = playerx
        preparePlayer()
    #    changePlayer()
 #   print(currentPlayer.agentType)
    def humanPlay(event):
        print(event.x,event.y)
        pi = event.y // 60 - 1
        pj = event.x // 60 - 1
        
        playOne(pi,pj)
        
    def buttonEvent():
        preparePlayer()
        nonlocal btnIsStart
        if player1 == 'human' or player2 == 'human':
           btn.config(state = "disable")
           btnIsStart = False
           startGame()
        else:
            if btnIsStart:
                btn.config(text = "stop")
                btnIsStart = False
                startGame()
            else:
                btn.config(text = "start")
                btnIsStart = True
        
    def startGame():
#        btn.config(state = "disable")
        run()

    def run():
        if not btnIsStart:
            nonlocal currentPlayer
            if currentPlayer.agentType == 'human':
                canvas.bind('<Button-1>',humanPlay)
                
                '''
                if currentPlayer == playerx:
                    currentPlayer = playero
                else:
                    currentPlayer = playerx
                '''
            else:
                canvas.unbind('<Button-1>')
                cb = deepcopy(b.chessboard)
     #          print(currentPlayer.playOne(cb))
                pi,pj = currentPlayer.playOne(cb)
#                print(pi,pj)
     #           print(pi,pj)
                playOne(pi,pj)
                



    def playOne(i,j):
        print(i, j)
        isPlay = True
        isPlay = b.playOne(i,j, b.currentPlayer)
        if isPlay:
            resEnd = b.isEnd()
            if resEnd:
                if resEnd == 'o':
                    winner = playero
                    chessType = 'White'
                else:
                    winner = playerx
                    chessType = 'Black'
    #            print("The winner is: " + str(resEnd))
                btn.config(state = "disable")
                canvas.unbind('<Button-1>')
                winMessage = 'The Winner is ' + chessType + '('+ str(winner.agentType)  + ')'
                print(winMessage)
                canvas.create_text(width / 2,height / 2, text = winMessage, font = ('Times', '40', 'bold italic'), fill = 'red')
                btnIsStart = True
            else:
 #               currentPlayer.sampleHeuristic(b.chessboard)
                changePlayer()
 #               time.sleep(0)
                run()
        
            
        
                
            
    btn = Button(tk ,text="start", state = 'normal', command = buttonEvent)
    btn.pack()

    
 #   changePlayer()
#    print(currentPlayer.agentType)
 #   startGame()
    
 #       c += 1
#    canvas.create_rectangle(65, 70, 240, 130)
    tk.mainloop()


'''
def handlerAdaptor(fun, **kwds):
    return lambda event,fun=fun,kwds=kwds: fun(event, **kwds)  
'''
    
def startWinNoC(size, player1 = 'human', player2 = 'human', minmax_depth1 = None, minmax_depth2 = None, h1 = 'good', h2 = 'good',second1 = 8, second2 = 8):

    b = board(size, isPrint = False)
    playero = player('o', player1,minmax_depth1,h1,mcts_time = second1)
    playerx = player('x', player2,minmax_depth2,h2,mcts_time = second2)
    currentPlayer = playero

    res = ""
    win = 0
    on = 0
    xn = 0
    def preparePlayer():
        currentPlayer.checkDomain(b.chessboard)
        '''
        if len(currentPlayer.domain) != 0:
            pass
        else:
            b.playOne(None,None, b.currentPlayer)
            changePlayer()
        '''
        
    def changePlayer():
        nonlocal currentPlayer
        if currentPlayer == playerx:
            currentPlayer = playero
        else:
            currentPlayer = playerx
        preparePlayer()
    #    changePlayer()
 #   print(currentPlayer.agentType)
        
        
    def startGame():
        run()

    def run():
        nonlocal currentPlayer
        cb = deepcopy(b.chessboard)
        pi,pj = currentPlayer.playOne(cb)
        playOne(pi,pj)
                



    def playOne(i,j):

        isPlay = True
        isPlay = b.playOne(i,j, b.currentPlayer)
        if isPlay:
            resEnd = b.isEnd()
            if resEnd:


                nonlocal res, win, on,xn
                on = 0
                xn = 0
                for x in b.chessboard:
                    for y in x:
                        if y is not None:
                            if y == -1:
                                on += 1
                            else:
                                xn +=1
                
                if resEnd == 'o':
                    res = "win"
                    win = 1
                elif resEnd == 'x':
                    res = "lost"
                    win = 0
                elif resEnd == 'a draw':
                    res = "draw"
                    win = 0
                            
 #               b.printBoard()
            else:

                changePlayer()
                run()
        
            
    startGame()
    return res,win,on,xn


if __name__=="__main__":
    startWin(8,player1 = 'mcts', player2 = 'minmax', minmax_depth1 = 6, minmax_depth2 = 4, h1 = 'simple', h2 = 'good', time1 = 4, time2 = 8)

 #   startWinNoC(8,player1 = 'mcts', player2 = 'minmax', minmax_depth1 = 4, minmax_depth2 = 4, h1 = 'simple', h2 = 'good', second1 = 12.3, second2 = 10)

    '''
    n = 50
    times = [8]
    depth = [1,2]
    evaluation = ['good']
    # minmax vs random
    
    for d in depth:
        for e in evaluation:
            print(d,e)
            f = open("data/Minmax vs Random.txt", "a")
            sumOfon = 0
            sumOfxn = 0
            sumOfwin = 0
            
            f.write("*************")
            f.write("depth: " + str(d) + ", evaluation: " + str(e))
            f.write("*************\n")
            for i in range(n):
               res, win, on, xn = startWinNoC(8,player1 = 'minmax', player2 = 'random', minmax_depth1 = d, minmax_depth2 = 2, h1 = e, h2 = 'good', second1 = 4)
               sumOfwin += win
               sumOfon += on
               sumOfxn += xn
               f.write("result:" + str(res) + ", player1(white):" + str(on) + ", player2(black)" + str(xn) + '\n')
         #      print(res,win,on,ox)
            f.write("----------------------------\n")
            f.write("wins number:" + str(sumOfwin) + " out of " + str(n) + ", win radio:" + str(sumOfwin / n) + ", player1(white) average:" + str(sumOfon / n) + ", player2(black) average:" + str(sumOfxn / n) + '\n')
            f.write("----------------------------\n")
            f.write("\n")
            print(sumOfwin / n, sumOfon / n, sumOfxn / n)
            f.close()
    
    # mcts vs random
    '''
    '''
    for t in times:
        f = open("data/MCTS vs Random.txt", "a")
        sumOfon = 0
        sumOfxn = 0
        sumOfwin = 0
        
        f.write("*************")
        f.write("times: " + str(t))
        f.write("*************\n")
        for i in range(n):
           res, win, on, xn = startWinNoC(8,player1 = 'mcts', player2 = 'random', minmax_depth1 = 3, minmax_depth2 = 2, h1 = 'simple', h2 = 'good', second1 = t)
           sumOfwin += win
           sumOfon += on
           sumOfxn += xn
           f.write("result:" + str(res) + ", player1(white):" + str(on) + ", player2(black)" + str(xn) + '\n')
     #      print(res,win,on,ox)
        f.write("----------------------------\n")
        f.write("wins number:" + str(sumOfwin) + " out of " + str(n) + ", win radio:" + str(sumOfwin / n) + ", player1(white) average:" + str(sumOfon / n) + ", player2(black) average:" + str(sumOfxn / n) + '\n')
        f.write("----------------------------\n")
        f.write("\n")
        print(sumOfwin / n, sumOfon / n, sumOfxn / n)
        f.close()
    '''
    #mcts vs minmax
    '''
    for t in times:
        for e in evaluation:
            
            for d in depth:
                print(e,d)
                f = open("data/UCT(" + str(t) + "s) " + "vs Minmax(" + e + ").txt", "a")
                sumOfon = 0
                sumOfxn = 0
                sumOfwin = 0
                
                f.write("*************")
                f.write("UCT(" + str(t) + "s) " + "vs Minmax(" + str(d) + " depth).txt")
                f.write("*************\n")
                for i in range(n):
                   res, win, on, xn = startWinNoC(8,player1 = 'mcts', player2 = 'minmax', minmax_depth1 = d, minmax_depth2 = d, h1 = e, h2 = e, second1 = t)
                   sumOfwin += win
                   sumOfon += on
                   sumOfxn += xn
                   f.write("result:" + str(res) + ", player1(white):" + str(on) + ", player2(black)" + str(xn) + '\n')
             #      print(res,win,on,ox)
                f.write("----------------------------\n")
                f.write("wins number:" + str(sumOfwin) + " out of " + str(n) + ", win radio:" + str(sumOfwin / n) + ", player1(white) average:" + str(sumOfon / n) + ", player2(black) average:" + str(sumOfxn / n) + '\n')
                f.write("----------------------------\n")
                f.write("\n")
                print(("UCT(" + str(t) + "s) " + "vs Minmax(" + str(d) + " depth).txt"))
                print(sumOfwin / n, sumOfon / n, sumOfxn / n)
                f.close()
    
     '''                             
 #       startCmd(8)
        


