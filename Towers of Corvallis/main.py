import searchAlgorithm
def Towers(filename):
    Towers = []
    mapFile = open(filename)
    try:
        for i in range(0,20):
            eachLine = mapFile.readline( )
            eachTower = [[],[],[]]
            for disk in eachLine:
                    if disk == '\n':
                        break
                    eachTower[0].append(int(disk))

            #print(eachTower)
            Towers.insert(0,eachTower)
		
    finally:
        mapFile.close()
        return Towers

def run(filenames):
    heristicTypes = [False, True]
    beamWidths = [5, 10, 15, 20, 25, 50, 100, float('inf')]
    for ht in heristicTypes:
        for bw in beamWidths:
            for fn in filenames:
                towers = Towers(fn)
                for t in towers:
                    searchAlgorithm.beamSearch(t, 1000, ht, bw)

            
    

run(['6_Disks.txt','7_Disks.txt','8_Disks.txt', '9_Disks.txt'])

'''
       For each heuristic function h, 
         For beam widths 5, 10, 15, 20, 25, 50, 100, infty
           For at least 4 different sizes (number of disks)
             For each of the 20 problems p, 
		Solve p using h or until NMAX nodes are expanded. 
                Record the solution length if successful, the number of nodes 
	               expanded, and the total CPU time spent on evaluating
                       the heuristic and on solving the whole problem.
'''
