from factorInters import *


assert(choose_n(0, ['a', 'b', 'c']) == [[]])
assert(choose_n(1, ['a', 'b', 'c']) == [['a'], ['b'], ['c']])
assert(choose_n(2, ['a', 'b', 'c']) ==
       [['a', 'b'], ['a', 'c'], ['b', 'a'],
        ['b', 'c'], ['c', 'a'], ['c', 'b']])
# next one is lame: I get permutations (wanted singleton, but no big deal.
# cleaning with a later function
assert(choose_n(3, ['a', 'b', 'c']) ==
       [['a', 'b', 'c'], ['a', 'c', 'b'],
        ['b', 'a', 'c'], ['b', 'c', 'a'],
        ['c', 'a', 'b'], ['c', 'b', 'a']])


assert(allChoices(['a', 'b', 'c']) ==
       [[],

        ['a'], ['b'], ['c'],

        ['a', 'b'], ['a', 'c'], ['b', 'a'],
        ['b', 'c'], ['c', 'a'], ['c', 'b'],

        ['a', 'b', 'c'], ['a', 'c', 'b'],
        ['b', 'a', 'c'], ['b', 'c', 'a'],
        ['c', 'a', 'b'], ['c', 'b', 'a']])


assert(remDupes(allChoices(['a', 'b', 'c'])) ==
       [[], ['a'], ['b'], ['c'],
        ['a', 'b'], ['a', 'c'], ['b', 'c'],
        ['a', 'b', 'c']])

# empty dies alone
assert(remEmpty(remDupes(allChoices(['a', 'b', 'c']))) ==
       [['a'], ['b'], ['c'],
        ['a', 'b'], ['a', 'c'], ['b', 'c'],
        ['a', 'b', 'c']])

assert(genMap(['a', 'b', 'c']) ==
       [('a', 'b'), ('a', 'c'), ('b', 'a'),
        ('b', 'c'), ('c', 'a'), ('c', 'b')])

li1 = range(10)
li2 = range(5, 15)
li3 = range(13, 20) + range(3)
listRefs = listByID([li1, li2, li3])
assert(intersLookup(listRefs) ==
       {'1/2': 2,
        '0/2': 3,
        '0/1': 5,
        '1': 10,
        '0': 10,
        '2': 10,
        '0/1/2': 0})


# here I ask for children of a terminal
assert(getChildren(['a', 'b'], genMap(['a', 'b', 'c'])) ==
       [])
# this one is a non-terminal case. Tuples in the
# output list are (child, continuation).
# Continuation is necessary to check if the node
# ends up in the target or not.
assert(getChildren(['a', 'b'], genMap(['a', 'b', 'c', 'd'])) ==
       [(('a', 'b', 'c'), ()), (('a', 'b', 'd'), ())])


assert(getChildrByTarget(['b'], genMap(['a', 'b', 'c', 'd']), 'a') ==
       [('b', 'c'), ('b', 'd')])

assert(subunEq(subun(name=('b', 'c'), level=2),
               subun(name=('c', 'b'), level=2)) ==
       True)
    
assert(getUniqueNodes(facto(['b'], [subun(name=[[]], level=0)],
                            'a', 1, genMap(['a', 'b', 'c', 'd']), 4)) ==
       set(['b/c/d', 'b/d', 'b', 'b/c']))

assert(joinEndPts(endpoint(node=('b', 'c'), cardi=1,
                           inBelly=[subun(name=['b'], level=1), 
                                    subun(name=[[]], level=0)]),
                  endpoint(node=('c', 'b'), cardi=1,
                           inBelly=[subun(name=['c'], level=1),
                                    subun(name=[[]], level=0)])) ==
       endpoint(node=('b', 'c'), cardi=1,
                inBelly=[subun(name=['b'], level=1),
                         subun(name=[[]], level=0),
                         subun(name=['c'], level=1)]))


endptsList = (facto(['b'], [subun(name=[[]], level=0)],
                   'a', 1, genMap(['a', 'b', 'c', 'd']), 4) +
              facto(['c'], [subun(name=[[]], level=0)],
                   'a', 1, genMap(['a', 'b', 'c', 'd']), 4) +
              facto(['d'], [subun(name=[[]], level=0)],
                   'a', 1, genMap(['a', 'b', 'c', 'd']), 4))

# you always have to add ROOT (the all-in intersection) by hand,
# since I didn't find a convenient way to represent it via paths.
assert(mergeAllNodes(getUniqueNodes(endptsList), endptsList) +
       [endpoint(node=[[]], cardi=1, inBelly=[])] ==
       
       [endpoint(node=['c'], cardi=1,
                 inBelly=[subun(name=[[]], level=0)]),
        
        endpoint(node=['b'], cardi=1,
                 inBelly=[subun(name=[[]], level=0)]),
        
        endpoint(node=['d'], cardi=1,
                 inBelly=[subun(name=[[]], level=0)]),
        
        endpoint(node=('b', 'c', 'd'), cardi=1,
                 inBelly=[subun(name=('b', 'c'), level=2),
                          subun(name=['b'], level=1),
                          subun(name=[[]], level=0),
                          subun(name=('b', 'd'), level=2),
                          subun(name=['c'], level=1),
                          subun(name=('c', 'd'), level=2),
                          subun(name=['d'], level=1)]),
        
        endpoint(node=('c', 'd'), cardi=1,
                 inBelly=[subun(name=['c'], level=1),
                          subun(name=[[]], level=0),
                          subun(name=['d'], level=1)]),
        
        endpoint(node=('b', 'c'), cardi=1,
                 inBelly=[subun(name=['b'], level=1),
                          subun(name=[[]], level=0),
                          subun(name=['c'], level=1)]),
        
        endpoint(node=('b', 'd'), cardi=1,
                 inBelly=[subun(name=['b'], level=1),
                          subun(name=[[]], level=0),
                          subun(name=['d'], level=1)]),

        endpoint(node=[[]], cardi=1,
                 inBelly=[])])


subunList = [subun(name=['1'], level=1),
             subun(name=[[]], level=0),
             subun(name=['2'], level=1)]
li1 = range(10)
li2 = range(5, 15)
li3 = range(13, 20) + range(3)
listRefs = listByID([li1, li2, li3])
allInters = intersLookup(listRefs)
jSubuns = joinSubun(1, subunList)
assert(computeInters(jSubuns, '0', allInters) == 8)

# maybe level are to be raised by one, and empty must be formalized more,
# but it looks good
assert(facto(['b'], [subun(name=[[]], level=0)],
             'a', 1, genMap(['a', 'b', 'c']), 3) ==
       [endpoint(node=['b'], cardi=1, inBelly=[subun(name=[[]], level=0)]),
        endpoint(node=('b', 'c'), cardi=1,
                 inBelly=[subun(name=['b'], level=1),
                          subun(name=[[]], level=0)])])

assert(facto(['b'], [subun(name=[[]], level=0)],
             'a', 1, genMap(['a', 'b', 'c', 'd']), 4) ==
[endpoint(node=['b'],
         cardi=1, 
         inBelly=[subun(name=[[]], level=0)]), 

endpoint(node=('b', 'c'),
         cardi=1,
         inBelly=[subun(name=['b'], level=1),
                  subun(name=[[]], level=0)]),

endpoint(node=('b', 'c', 'd'),
         cardi=1,
         inBelly=[subun(name=('b', 'c'), level=2),
                  subun(name=['b'], level=1),
                  subun(name=[[]], level=0)]),

endpoint(node=('b', 'd'),
         cardi=1,
         inBelly=[subun(name=['b'], level=1),
                  subun(name=[[]], level=0)]),

endpoint(node=('b', 'd', 'c'),
         cardi=1,
         inBelly=[subun(name=('b', 'd'), level=2),
                  subun(name=['b'], level=1),
                  subun(name=[[]], level=0)])])

getSubs = subunByLevel([subun(name=('b', 'c'), level=2),
                        subun(name=['b'], level=1),
                        subun(name=[[]], level=0),
                        subun(name=('b', 'd'), level=2),
                        subun(name=['c'], level=1),
                        subun(name=('c', 'd'), level=2),
                        subun(name=['d'], level=1)])

assert([s for s in getSubs] ==

       [[subun(name=('c', 'd'), level=2),
         subun(name=('b', 'd'), level=2),
         subun(name=('b', 'c'), level=2)],

        [subun(name=['d'], level=1),
         subun(name=['c'], level=1),
         subun(name=['b'], level=1)],

        [subun(name=[[]], level=0)]])

assert(node2sets(endpoint(node=('c', 'd'), cardi=1,
                          inBelly=[subun(name=['c'], level=1),
                                   subun(name=[[]], level=0),
                                   subun(name=['d'], level=1)]),
                 ['a', 'b', 'c', 'd']) ==
       ['a', 'b'])

assert(node2sets(endpoint(node=[[]], cardi=1,
                          inBelly=[]),
                 ['a', 'b', 'c', 'd']) ==
       ['a', 'c', 'b', 'd'])

assert(node2sets(endpoint(node=('1', '2', '3'),
                          cardi=None,
                          inBelly=None),
                 ('1', '2', '3', '4')) ==
       ['4'])

li1 = range(10)
li2 = range(5, 15)
li3 = range(13, 20) + range(3)
li4 = [n for n in range(20) if n % 2 == 0]

listRefs = listByID([li1, li2, li3, li4])
allInters = intersLookup(listRefs)

assert(getCard(('1', '2', '3'), allInters,
               map(str, listRefs.keys())) == 
       10)

liA = []
liB = []
liC = []
liD = []

liA += [1]
liB += [1]
liC += [1]
liD += [1]

liA += range(2,4)
liB += range(2,4)
liC += range(2,4)

liA += range(4,7)
liB += range(4,7)
liD += range(4,7)

liA += range(7,11)
liC += range(7,11)
liD += range(7,11)

liB += range(11,16)
liC += range(11,16)
liD += range(11,16)

liA += range(16,22)
liB += range(16,22)

liA += range(22, 29)
liC += range(22, 29)

liA += range(29, 37)
liD += range(29, 37)

liB += range(37, 46)
liC += range(37, 46)

liB += range(46, 56)
liD += range(46, 56)

liC += range(56, 67)
liD += range(56, 67)

liA += range(67, 79)

liB += range(79, 92)

liC += range(92, 106)

liD += range(106, 121)

listRefs = {'A': liA,
            'B': liB,
            'C': liC,
            'D': liD}

epl = [endpoint(node=('B', 'C', 'D'),
                cardi=getCard(('B', 'C', 'D'), allInters,
                              map(str, listRefs.keys())),
                inBelly=[subun(name=('D', 'C'), level=2),
                         subun(name=('D', 'B'), level=2),
                         subun(name=('C', 'B'), level=2),
                         subun(name=['D'], level=1),
                         subun(name=['C'], level=1),
                         subun(name=['B'], level=1),
                         subun(name=[[]], level=0)]),

       endpoint(node=('C', 'D'),
                cardi=getCard(('C', 'D'), allInters,
                              map(str, listRefs.keys())),
                inBelly=[subun(name=['D'], level=1),
                         subun(name=['C'], level=1),
                         subun(name=[[]], level=0)]),

       endpoint(node=('B', 'D'),
                cardi=getCard(('B', 'D'), allInters,
                              map(str, listRefs.keys())),
                inBelly=[subun(name=['D'], level=1),
                         subun(name=['B'], level=1),
                         subun(name=[[]], level=0)]),

       endpoint(node=('B', 'C'),
                cardi=getCard(('B', 'C'), allInters,
                              map(str, listRefs.keys())),
                inBelly=[subun(name=['C'], level=1),
                         subun(name=['B'], level=1),
                         subun(name=[[]], level=0)]),

       endpoint(node=('D'),
                cardi=getCard(('D'), allInters,
                              map(str, listRefs.keys())),
                inBelly=[subun(name=[[]], level=0)]),

       endpoint(node=('C'),
                cardi=getCard(('C'), allInters,
                              map(str, listRefs.keys())),
                inBelly=[subun(name=[[]], level=0)]),

       endpoint(node=('B'),
                cardi=getCard(('B'), allInters,
                              map(str, listRefs.keys())),
                inBelly=[subun(name=[[]], level=0)])]

dissList = multiDeMoivre(epl, 'A', allInters, ['A', 'B', 'C', 'D'])

import operator
assert(sorted(dissList, key=operator.attrgetter('value')) ==
       [dissipation(name='D', value=2),
        dissipation(name='C', value=3),
        dissipation(name='B', value=4),
        dissipation(name=('C', 'D'), value=6),
        dissipation(name=('B', 'D'), value=7),
        dissipation(name=('B', 'C'), value=8),
        dissipation(name=('B', 'C', 'D'), value=12)]


eptsLi_tA = (facto(['B'], [subun(name=[[]], level=0)],
                   'A', 1, genMap(['A', 'B', 'C', 'D']), 4,
                   allInters, ['A', 'B', 'C', 'D']) +
             facto(['C'], [subun(name=[[]], level=0)],
                   'A', 1, genMap(['A', 'B', 'C', 'D']), 4,
                   allInters, ['A', 'B', 'C', 'D']) +
             facto(['D'], [subun(name=[[]], level=0)],
                   'A', 1, genMap(['A', 'B', 'C', 'D']), 4,
                   allInters, ['A', 'B', 'C', 'D']))

eptsLi_tA_nodupes = (mergeAllNodes(getUniqueNodes(eptsLi_tA),
                                   eptsLi_tA) + 
                     [endpoint(node=[[]], cardi=1, inBelly=[])])

dissLi_tA = multiDeMoivre(eptsLi_tA_nodupes, allInters,
                          ['A', 'B', 'C', 'D'])

assert(sorted(dissLi_tA, key=operator.attrgetter('value')) ==
       sorted(dissList, key=operator.attrgetter('value'))

assert(sorted(getDiss_tgt('A', ['A', 'B', 'C', 'D'], allInters),
              key=operator.attrgetter('value')) ==
       sorted(dissList, key=operator.attrgetter('value'))


assert(getDiss_tgt('B', ['A', 'B', 'C', 'D'], allInters) ==
       [dissipation(name=['A'], value=5),
        dissipation(name=['C'], value=3),
        dissipation(name=('A', 'D'), value=9),
        dissipation(name=('A', 'C'), value=10),
        dissipation(name=['D'], value=2),
        dissipation(name=('A', 'C', 'D'), value=13),
        dissipation(name=('C', 'D'), value=6),
        dissipation(name=[[]], value=1)])

assert(getDiss_tgt('D', ['A', 'B', 'C', 'D'], allInters) ==
       [dissipation(name=['A'], value=5),
        dissipation(name=['C'], value=3),
        dissipation(name=['B'], value=4),
        dissipation(name=('A', 'C'), value=10),
        dissipation(name=('A', 'B'), value=11),
        dissipation(name=('A', 'B', 'C'), value=15),
        dissipation(name=('C', 'B'), value=8),
        dissipation(name=[[]], value=1)])

assert(getDiss_tgt('C', ['A', 'B', 'C', 'D'], allInters) ==
       [dissipation(name=['A'], value=5),
        dissipation(name=['B'], value=4),
        dissipation(name=('A', 'B'), value=11),
        dissipation(name=('A', 'D'), value=9),
        dissipation(name=('A', 'B', 'D'), value=14),
        dissipation(name=('B', 'D'), value=7),
        dissipation(name=['D'], value=2),
        dissipation(name=[[]], value=1)])

d = getDiss_glb(['A', 'B', 'C', 'D'], allInters)
assert(sorted(d.iteritems(), key=operator.itemgetter(1)) ==
       [('A/B/C/D', 1),
        ('A/B/C', 2),
        ('A/B/D', 3),
        ('A/C/D', 4),
        ('B/C/D', 5),
        ('A/B', 6),
        ('A/C', 7),
        ('A/D', 8),
        ('B/C', 9),
        ('B/D', 10),
        ('C/D', 11),
        ('A', 12),
        ('B', 13),
        ('C', 14),
        ('D', 15)])

d = getDiss_inlists([liA, liB, liC, liD])
assert(sorted(d.iteritems(), key=operator.itemgetter(1)) ==
       ('0/1/2/3', 1),
       ('0/1/2', 2),
       ('0/1/3', 3),
       ('0/2/3', 4),
       ('1/2/3', 5),
       ('0/1', 6),
       ('0/2', 7),
       ('0/3', 8),
       ('1/2', 9),
       ('1/3', 10),
       ('2/3', 11),
       ('0', 12),
       ('1', 13),
       ('2', 14),
       ('3', 15))

assert(pprintDiss([liA, liB, liC, liD]) == 
       """var connsX = [
{groups: "1", value: "13"},
{groups: "1,3", value: "10"},
{groups: "0,1,2,3", value: "1"},
{groups: "1,2,3", value: "5"},
{groups: "0,2", value: "7"},
{groups: "0,3", value: "8"},
{groups: "0,1", value: "6"},
{groups: "0,2,3", value: "4"},
{groups: "0", value: "12"},
{groups: "3", value: "15"},
{groups: "2", value: "14"},
{groups: "0,1,2", value: "2"},
{groups: "0,1,3", value: "3"},
];
""")

assert(pprintDiss([(liA, 'foo'), (liB, 'bar'),
                   (liC, 'scoiattolo'), (liD, 'gattino')]) ==
       """var connsX = [
{groups: "foo,scoiattolo", value: "7"},
{groups: "scoiattolo", value: "14"},
{groups: "bar", value: "21"},
{groups: "foo", value: "18"},
{groups: "foo,gattino", value: "13"},
{groups: "bar,foo", value: "9"},
{groups: "gattino", value: "25"},
{groups: "bar,gattino", value: "16"},
{groups: "bar,foo,scoiattolo", value: "2"},
{groups: "bar,foo,gattino,scoiattolo", value: "1"},
{groups: "gattino,scoiattolo", value: "11"},
{groups: "bar,scoiattolo", value: "9"},
{groups: "foo,gattino,scoiattolo", value: "4"},
];
""")
