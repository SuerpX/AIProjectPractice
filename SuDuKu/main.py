from searchAlgorithm import *
from table import *
from time import *

def SuDuKus(filename):
    tables = [[],[],[],[]]
    tableFile = open(filename)
    try:
        eachLine = tableFile.readline( )
        index = 0
        table = []
        while eachLine:
            
            #print (eachLine)
            
            if eachLine.find("Easy") >= 0:
                index = 0
            elif eachLine.find("Medium") >= 0:
                index = 1
            elif eachLine.find("Hard") >= 0:
                index = 2
            elif eachLine.find("Evil") >= 0:
                index = 3
            elif eachLine == "\n":
                #for j in table:
                    #print(j)
                #print("-------------------------")
                tables[index].append(Table(table))
                table = []
            else:
                row = []
                for x in eachLine:
                    if x is not ' ' and x is not '\n' and x is not '\t':
                        row.append(x)
                table.append(row)

            eachLine = tableFile.readline( )
    finally:
        tableFile.close()
        
        t = tables
        n = 1
        '''
        print(len(t[0]),len(t[1]),len(t[2]),len(t[3]))
        en = 0
        mn = 0
        hn = 0
        evn = 0
        for k, i in enumerate(t):
            if k == 0:
                print('Easy:')
            elif k == 1:
                print('Medium:')
            elif k == 2:
                print('Hard:')
            elif k == 3:
                print('Evil:')
            for j in i:
                for x in j.table:
                    for y in x:
                        if y.filled:
                            if k == 0:
                                en += 1
                            elif k == 1:
                                mn += 1
                            elif k == 2:
                                hn += 1
                            elif k == 3:
                                evn += 1
            if k == 0:
                print(en / 23)
            elif k == 1:
                print(mn / 21)
            elif k == 2:
                print(hn / 18)
            elif k == 3:
                print(evn / 15)

        t = tables
        n = 1
        '''
        
        num = [23,21,18,15]
        for mOrF in range(0,2):
            for rule in range(0, 4):
                n = 0
                for k, i in enumerate(t):
                    if k == 0:
                        level = "easy"
 #                       print("easy:")
                    elif k == 1:
                        level = "medium"
 #                       print("medium:")
                    elif k == 2:
                        level = "hard"
 #                       print("hard:")
                    elif k == 3:
                        level = "evil"
 #                       print("evil:")
                    nOfSloved = 0
                    sumOfnOfBack = 0
                    time = 0
                    for j in i:
                        #print(n)
                        start = process_time()
                        if mOrF == 1:
                            res, nOfBack = backtracking(j,True,rule,True)
                        else:
                            res, nOfBack = backtracking(j,False,rule,True)
                        if not res:
                            print("fail")
                        else:
 #                           print(nOfBack)
                             nOfSloved += 1
                        sumOfnOfBack += nOfBack
                        end = process_time() - start
                        time += end
                        n += 1
                        print(n)
                        if res:
                            res.writeFile()
                    outcome(mOrF, rule, level, nOfSloved, sumOfnOfBack, time, num[k])
        
'''                  
        for rule in range(1, 4):
            for k, i in enumerate(t):
                if k == 0:
                    level = "easy"
                elif k == 1:
                    level = "medium"
                elif k == 2:
                    level = "hard"
                elif k == 3:
                    level = "evil"
                num = 0

                if rule == 0:
                    name = "noInfer_"
                elif rule == 1:
                    name = "single_"
                elif rule == 2:
                    name = "sinPair_"
                else:
                    name = "sinPairTri_"
                for j in i:
                    if b(j,rule):
                        num += 1
                print(level + "("+ name +")" +  str(num))
'''
                        
                

def outcome(mOrF, rule, level, nOfSloved, nOfBack, time, nk):
    filename = ""
    if mOrF == 0:
        filename += "fixed_"
    else:
        filename += "mcv_"
    if rule == 0:
        filename += "noInfer_"
    elif rule == 1:
        filename += "single_"
    elif rule == 2:
        filename += "sinPair_"
    else:
        filename += "sinPairTri_"
    filename += level
    print(filename)
    output = open("resultData.txt", 'a')
    output.write("---------------------------------------\n")
    output.write(filename + ":\n")
    output.write("percentage of solved:" + str(nOfSloved / nk) + " (" + str(nOfSloved) + ")" + "\n")
    output.write("average number of backtracking:" + str(nOfBack / nk) + "\n")
    output.write("average time:" + str(time / nk) + "\n")
    output.close()
    
SuDuKus("sudoku-problems.txt")


#print

'''
for k, i in enumerate(t):
    if k == 0:
        print('Easy:')
    elif k == 1:
        print('Medium:')
    elif k == 2:
        print('Hard:')
    elif k == 3:
        print('Evil:')
    for j in i:
        #print(j)
        n = 0
        tl = j.tableList 
        for m in tl:
            n += 1
            print(m)
        if n != 9:
            print ("error")
            break
        print("*********************")

'''
