from copy import deepcopy
def nakedPair(table):
    changed = False
    t = table.table
    for x in t:
        for y in x:
            if not y.filled and y.domain_size() == 2:                   
                alldiff = y.getConstraintVariable(0)
                for n in alldiff:
                    if n.domain == y.domain:
                        for m in alldiff:
                            if m != y and m != n:
                                ch1 = m.remove(y.domain[0])
                                ch2 = m.remove(y.domain[1])
                                if ch1 or ch2:
                                    changed = True
                alldiff = y.getConstraintVariable(1)
                for n in alldiff:
                    if n.domain == y.domain:
                        for m in alldiff:
                            if m != y and m != n:
                                ch1 = m.remove(y.domain[0])
                                ch2 = m.remove(y.domain[1])
                                if ch1 or ch2:
                                    changed = True
                alldiff = y.getConstraintVariable(2)
                for n in alldiff:
                    if n.domain == y.domain:
                        for m in alldiff:
                            if m != y and m != n:
                                ch1 = m.remove(y.domain[0])
                                ch2 = m.remove(y.domain[1])
                                if ch1 or ch2:
                                    changed = True
    return changed
'''
def hiddenPair(table):
    changed = False
    def checkAndRemove(r):
        changed = False
        d = ['1','2','3','4','5','6','7','8','9']
        for c in r:
            if c.filled:
                if c.num in d:
                    d.remove(c.num)
        for i, x in enumerate(d):
            for y in d[i:]:
                n = 0
                targetCells = []
                if (x == y):
                    continue
                for c in r:
                    if not c.filled and c.domain_size() >= 2:
                        if x in c.domain and y in c.domain:
                            targetCells.append(c)
                            n += 1
                           # print(x,y,c.domain,n)
                        elif x in c.domain or y in c.domain:
                            n = 0
                            break
                if n == 2:
                    for c in r:
                        if c in targetCells:
                            c.domain = [x,y]
                            changed = True
        return changed
    t = table.table
    for r in t:
        changed = checkAndRemove(r)
    i = 0
    j = 0
    r = []
    for i in range(0,9):
        r = []
        for j in range(0,9):
            r.append(t[j][i])
        changed = checkAndRemove(r)
    r = []
    for i in range(0,3):
        for j in range(0,3):
            r = []
            for n in range(i * 3, i * 3 + 3):
                for m in range(j * 3, j * 3 + 3):
                    r.append(t[n][m])
            changed = checkAndRemove(r)
    return changed
'''
'''
def hiddenSingle(table):
    changed = False
    t = table.table
    for x in t:
        for y in x:
            if not y.filled and y.domain_size() > 1:
                for d in y.domain:
                    alldiff = y.getConstraintVariable(0)
                    flag = False
                    for ad in alldiff:
                        if d in ad.domain:
                            flag = True
                            break
                    if not flag:
                        hiddenSingleValue = d
                        y.filled = True
                        y.num = hiddenSingleValue
                        table.forwardChecking(y)
                        changed = True
                        continue
                    
                    alldiff = y.getConstraintVariable(1)
                    flag = False
                    
                    for ad in alldiff:
                        if d in ad.domain:
                            flag = True
                            break
                    if not flag:
                        hiddenSingleValue = d
                        y.filled = True
                        y.num = hiddenSingleValue
                        table.forwardChecking(y)
                        changed = True
                        continue
                    
                    alldiff = y.getConstraintVariable(2)
                    flag = False
                    for ad in alldiff:
                        if d in ad.domain:
                            flag = True
                            break
                    if not flag:
                        hiddenSingleValue = d
                        y.filled = True
                        y.num = hiddenSingleValue
                        table.forwardChecking(y)
                        changed = True
                        continue
    
    return changed
'''
def nakedSingle(table):
    t = table.table
    changed = False
    for x in t:
        for y in x:
            if not y.filled:
                if y.domain_size() == 1:
                    nakedSingleValue = y.domain[0]
                    y.filled = True
                    y.num = nakedSingleValue
                    table.forwardChecking(y)
                    changed = True
 #  print('***********\n')
    return changed

def nakedTriple(Table):
    changed = False
    for x in Table.table:
        for y in x:
            if not y.filled and y.domain_size() <= 3:
                alldiff = y.getConstraintVariable(0)
                for i, ad in enumerate(alldiff):
                    if i + 1 >= len(alldiff) or ad.domain_size() > 3:
                        continue
                    for bd in alldiff[i + 1:]:
                        if bd.domain_size() <= 3:
                            m = set(ad.domain) | set(y.domain) | set(bd.domain)
                            if len(m) == 3:
                                for n in alldiff:
                                    if n != ad and n != bd:
                                        nd = n.domain
                                        n.domain = list(set(n.domain) - m)
                                        if n.domain != nd:
                                            changed = True
                                
                alldiff = y.getConstraintVariable(1)
                for i, ad in enumerate(alldiff):
                    if i + 1 >= len(alldiff) or ad.domain_size() > 3:
                        continue
                    for bd in alldiff[i + 1:]:
                        if bd.domain_size() <= 3:
                            m = set(ad.domain) | set(y.domain) | set(bd.domain)
                            if len(m) == 3:
                                for n in alldiff:
                                    if n != ad and n != bd:
                                        nd = n.domain
                                        n.domain = list(set(n.domain) - m)
                                        if n.domain != nd:
                                            changed = True
                                    
                alldiff = y.getConstraintVariable(2)
                for i, ad in enumerate(alldiff):
                    if i + 1 >= len(alldiff) or ad.domain_size() > 3:
                        continue
                    for bd in alldiff[i + 1:]:
                        if bd.domain_size() <= 3:
                            m = set(ad.domain) | set(y.domain) | set(bd.domain)
                            if len(m) == 3:
                                for n in alldiff:
                                    if n != ad and n != bd:
                                        nd = n.domain
                                        n.domain = list(set(n.domain) - m)
                                        if n.domain != nd:
                                            changed = True
    return changed


def hiddenPair(Table):
    changed = False
    for x in Table.table:
        for y in x:
            if not y.filled and y.domain_size() >= 2:
                alldiff = y.getConstraintVariable(0)
                for ad in alldiff:
                    m = set(ad.domain) | set(y.domain)
                    for n in alldiff:
                        if n != ad:
                            m = m - set(n.domain)
                    if len(m) == 2:
                        for n in alldiff:
                            if n != ad:
                                nd = n.domain
                                n.domain = list(set(n.domain) - m)
                                if n.domain != nd:
                                    changed = True
                                
                alldiff = y.getConstraintVariable(1)
                for ad in alldiff:
                    m = set(ad.domain) | set(y.domain)
                    for n in alldiff:
                        if n != ad:
                            m = m - set(n.domain)
                    if len(m) == 2:
                        for n in alldiff:
                            if n != ad:
                                nd = n.domain
                                n.domain = list(set(n.domain) - m)
                                if n.domain != nd:
                                    changed = True
                                    
                alldiff = y.getConstraintVariable(2)
                for ad in alldiff:
                    m = set(ad.domain) | set(y.domain)
                    for n in alldiff:
                        if n != ad:
                            m = m - set(n.domain)
                    if len(m) == 2:
                        for n in alldiff:
                            if n != ad:
                                nd = n.domain
                                n.domain = list(set(n.domain) - m)
                                if n.domain != nd:
                                    changed = True
    return changed

def hiddenTriple(Table): 
    changed = False
    for x in Table.table:
        for y in x:
            if not y.filled and y.domain_size() >= 3:
                alldiff = y.getConstraintVariable(0)
                for i, ad in enumerate(alldiff):
                    if i + 1 >= len(alldiff):
                        continue
                    for bd in alldiff[i + 1:]:
                        m = set(ad.domain) | set(y.domain) | set(bd.domain)
                        for n in alldiff:
                            if n != ad and n != bd:
                                m = m - set(n.domain)
                        if len(m) == 3:
                            for n in alldiff:
                                if n != ad and n != bd:
                                    nd = n.domain
                                    n.domain = list(set(n.domain) - m)
                                    if n.domain != nd:
                                        changed = True
                                
                alldiff = y.getConstraintVariable(1)
                for i, ad in enumerate(alldiff):
                    if i + 1 >= len(alldiff):
                        continue
                    for bd in alldiff[i + 1:]:
                        m = set(ad.domain) | set(y.domain) | set(bd.domain)
                        for n in alldiff:
                            if n != ad and n != bd:
                                m = m - set(n.domain)
                        if len(m) == 3:
                            for n in alldiff:
                                if n != ad and n != bd:
                                    nd = n.domain
                                    n.domain = list(set(n.domain) - m)
                                    if n.domain != nd:
                                        changed = True
                                    
                alldiff = y.getConstraintVariable(2)
                for i, ad in enumerate(alldiff):
                    if i + 1 >= len(alldiff):
                        continue
                    for bd in alldiff[i + 1:]:
                        m = set(ad.domain) | set(y.domain) | set(bd.domain)
                        for n in alldiff:
                            if n != ad and n != bd:
                                m = m - set(n.domain)
                        if len(m) == 3:
                            for n in alldiff:
                                if n != ad and n != bd:
                                    nd = n.domain
                                    n.domain = list(set(n.domain) - m)
                                    if n.domain != nd:
                                        changed = True
    return changed

def hiddenSingle(Table):
    changed = False
    for x in Table.table:
        for y in x:
            if not y.filled and y.domain_size() > 1:
                alldiff = y.getConstraintVariable(0)
                m = deepcopy(y.domain)
                for n in alldiff:
                    m = list(set(m) - set(n.domain))
                if len(m) == 1:
                    hiddenSingleValue = m[0]
                    y.filled = True
                    y.num = hiddenSingleValue
                    Table.forwardChecking(y)
                    changed = True
                    continue
                alldiff = y.getConstraintVariable(1)
                m = deepcopy(y.domain)
                for n in alldiff:
                    m = list(set(m) - set(n.domain))
                if len(m) == 1:
                    hiddenSingleValue = m[0]
                    y.filled = True
                    y.num = hiddenSingleValue
                    Table.forwardChecking(y)
                    changed = True
                    continue
                alldiff = y.getConstraintVariable(2)
                m = deepcopy(y.domain)
                for n in alldiff:
                    m = list(set(m) - set(n.domain))
                if len(m) == 1:
                    hiddenSingleValue = m[0]
                    y.filled = True
                    y.num = hiddenSingleValue
                    Table.forwardChecking(y)
                    changed = True
                    continue
    return changed

def test():
    a = [1,2,3,4,5,6,7]
    l = len(a)
    for i, n in enumerate(a):
        if i + 1 < l:
            for j, m in enumerate(a[i + 1:]):
                if i + j + 2 < l:
                    for k, o in enumerate(a[i + j + 2:]):
                        print(n,m,o)
#test()
