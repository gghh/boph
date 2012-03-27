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
