# interMap is all the permutations of the sets

import itertools
import exceptions

p = [pp for pp in itertools.permutations([1,2,3])]
dir(p)
type(p)
print p

def choose_n(n, srcList):
    if n == 0:
        return [[]]
    else:
        out = []
        for cnt, elem in enumerate(srcList):
            out += map(lambda x: [elem] + x,
                       choose_n(n-1, srcList[:cnt] + srcList[(cnt+1):]))
        return out

choose_n(0, ['a', 'b', 'c'])

choose_n(1, ['a', 'b', 'c'])

choose_n(2, ['a', 'b', 'c'])

choose_n(3, ['a', 'b', 'c'])

def allChoices(srcList):
    out = []
    for i in range(len(srcList)+1):
        out += choose_n(i, srcList)
    return out

allChoices(['a', 'b', 'c'])

def remDupes(listlist):
    out = []
    for li in listlist:
        li.sort()
        if not li in out:
            out.append(li)
    return out

remDupes(allChoices(['a', 'b', 'c']))

def remEmpty(lis):
    for cnt, elem in enumerate(lis):
        if len(elem) == 0:
            return lis[:cnt] + lis[(cnt+1):]
    raise exceptions.Exception('empty non found')

remEmpty(remDupes(allChoices(['a', 'b', 'c'])))


def genMap(setNames):
    return [p for p in itertools.permutations(setNames)]

paths = genMap(['A', 'B', 'C', 'D'])
slice = namedtuple('slice', ['node', 'card', 'addiInfo'])

def facto(inters, subUns, interMap):
    
    
