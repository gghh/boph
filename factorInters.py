# interMap is all the permutations of the sets

import itertools
import exceptions
from collections import namedtuple

# convert ensemble name to ID thru a global dictionary getID

def o(f, g):
    # function composition
    def helper(x):
        return f(g(x))
    return helper

def choose_n(n, srcList):
    if n == 0:
        return [[]]
    else:
        out = []
        for cnt, elem in enumerate(srcList):
            out += map(lambda x: [elem] + x,
                       choose_n(n-1, srcList[:cnt] + srcList[(cnt+1):]))
        return out

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

def allChoices(srcList):
    out = []
    for i in range(len(srcList)+1):
        out += choose_n(i, srcList)
    return out

assert(allChoices(['a', 'b', 'c']) ==
       [[],

        ['a'], ['b'], ['c'],

        ['a', 'b'], ['a', 'c'], ['b', 'a'],
        ['b', 'c'], ['c', 'a'], ['c', 'b'],

        ['a', 'b', 'c'], ['a', 'c', 'b'],
        ['b', 'a', 'c'], ['b', 'c', 'a'],
        ['c', 'a', 'b'], ['c', 'b', 'a']])

def remDupes(listlist):
    out = []
    for li in listlist:
        li.sort()
        if not li in out:
            out.append(li)
    return out

assert(remDupes(allChoices(['a', 'b', 'c'])) ==
       [[], ['a'], ['b'], ['c'],
        ['a', 'b'], ['a', 'c'], ['b', 'c'],
        ['a', 'b', 'c']])

def remEmpty(lis):
    for cnt, elem in enumerate(lis):
        if len(elem) == 0:
            return lis[:cnt] + lis[(cnt+1):]
    raise exceptions.Exception('empty non found')

# empty dies alone
assert(remEmpty(remDupes(allChoices(['a', 'b', 'c']))) ==
       [['a'], ['b'], ['c'],
        ['a', 'b'], ['a', 'c'], ['b', 'c'],
        ['a', 'b', 'c']])

def genMap(IDList):
    removeLast = lambda x: x[:-1]
    # removing last elem in up-path of the lattice
    # is a key point. Otherwise the concept of
    # `ensemble on top of chain` is meaningless,
    # since `empty` is on top of all chains.
    return map(removeLast,
               [p for p in itertools.permutations(IDList)])

assert(genMap(['a', 'b', 'c']) ==
       [('a', 'b'), ('a', 'c'), ('b', 'a'),
        ('b', 'c'), ('c', 'a'), ('c', 'b')])

def node2str(node):
    # node is a list of IDs indentifying the node from the bottom
    # of the lattice. Well, the bottom on the diagram I drew
    # on the witheboard :-)
    # Note: they're numerical IDs, so no risk of clashes with char '/'
    return '/'.join(map(str, node))

def listByID(listlist):
    # this is to store reference to the lists,
    # so that I can do all my computation symbolically,
    # and add numbers only at the end.
    out = {}
    for cnt, li in enumerate(listlist):
        out[cnt] = li
    return out

def inters_n(listlist):
    out = set(listlist[0])
    for li in listlist[1:]:
        out = out.intersection(set(li))
    return out
    
def intersLookup(listRefs):
    toInters = remEmpty(remDupes(allChoices(listRefs.keys())))
    doInter = lambda s, t: set(s).intersection(set(t))
    inters_n = lambda node: \
        (node2str(node), reduce(doInter,
                                [listRefs[r] for r in node[1:]],
                                listRefs[node[0]]))
    count = lambda (namesChain, inters): (namesChain, len(inters))
    return dict(map(o(count, inters_n), toInters))

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

def getChildren(node, allPaths):
    # NODE is a partial path, starting from the
    # all-intersected ensebles.
    # ALLPATHS are complete paths, from one end
    # to the other of the lattice. You get them via
    # genMap.
    out = []
    for path in allPaths:
        if len(path) > len(node) and \
                node2str(path).startswith(node2str(node)):
            # print 'path:', path, 'node:', node # DBG
            # I need to give also the continuation of the
            # in order to know, later, if it's target-free
            out.append( (path[:(len(node) + 1)], path[(len(node) + 1):]) )
    return out

# here I ask for children of a terminal
assert(getChildren(['a', 'b'], genMap(['a', 'b', 'c'])) ==
       [])
# this one is a non-terminal case. Tuples in the
# output list are (child, continuation).
# Continuation is necessary to check if the node
# ends up in the target or not.
assert(getChildren(['a', 'b'], genMap(['a', 'b', 'c', 'd'])) ==
       [(('a', 'b', 'c'), ()), (('a', 'b', 'd'), ())])

def getChildrByTarget(node, allPaths, target):
    # NODE and ALLPATHS as in getChildren,
    # TARGET is an endpoint.
    #
    # The `if` clause looks bizarre, but you
    # have to think that path are from the bottom,
    # and that path don't include the last step
    # (were arrows meet in the `universe`, so to speak.
    # 
    # by induction we assume that the children ('s prefix)
    # is target-free. Kind of a contract: be nice when
    # yuo call my function, initiate recursivity with
    # a meaningful input (i.e., target-free)
    # OMG that's dirty! continuation somehow must include
    # also the 'current endpoint'; what if the target is there?
    return [c[0] for c in getChildren(node, allPaths)
            if not target in (c[0][-1],) + c[1]]


assert(getChildrByTarget(['b'], genMap(['a', 'b', 'c', 'd']), 'a') ==
       [('b', 'c'), ('b', 'd')])

endpoint = namedtuple('endpoint', ['node', 'cardi', 'inBelly'])
subun = namedtuple('subun', ['name', 'level'])

# mock function
getCard = lambda x: 1

def facto(nd, subUns, target, lvl, interMap, numSet):
    # note: node are ident by path from the bottm,
    # so it isn't real clear how to refer to the lower terminal
    # which, strictly speaking, is the empty.
    # You know what? I can launch N instances, where N is
    # the number of my ensembles. Then I join the result.
    #
    # I need numSet to know if I am at the end of run
    if len(nd) == numSet-1 and not target in nd:
        # all subunions, accumulated, get finally into this
        return [endpoint(node=nd, cardi=getCard(nd),
                         inBelly=subUns)]
    else:
        out = [endpoint(node=nd, cardi=getCard(nd),
                        inBelly=subUns)]
        for child in getChildrByTarget(nd, interMap, target):
            out += facto(child, [subun(name=nd, level=lvl)] + subUns,
                         target, lvl+1, interMap, numSet)
        return out

def subunEq(subun1, subun2):
    # equality for subuns
    # wow finally using dynamic typing in the python way!
    # len(.) gives non zero for endpts names, and zero for []
    pprint = lambda x: x if len(x) > 0 else 'ROOT'
    return set(map(pprint, subun1.name)) == \
        set(map(pprint, subun2.name)) and \
        subun1.level == subun2.level

def getUniqueNodes(endptsList):
    # if two paths are the same up to reordering,
    # they represent the same endpoint. That's why the sort.
    namesList = [sorted(list(e.node)) for e in endptsList]
    uniqueNames = set(map(node2str, namesList))
    return uniqueNames
    
assert(getUniqueNodes(facto(['b'], [subun(name=[[]], level=0)],
                            'a', 1, genMap(['a', 'b', 'c', 'd']), 4)) ==
       set(['b/c/d', 'b/d', 'b', 'b/c']))

def joinEndPts(endpt1, endpt2):
    # they're supposed to have the same name (node)
    return endpoint(node=endpt1.node,
                    cardi=endpt1.cardi,
                    inBelly = endpt1.inBelly +
                    [inbly for inbly in endpt2.inBelly
                     if all(map(lambda x: not subunEq(inbly, x),
                                endpt1.inBelly))])
                    # if clause is: add this subun from endpt2.inBelly
                    # if it wasn't already in endpt1.inBelly

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

def flip():
    curr = 1
    while True:
        yield curr
        curr *= -1

def mergeNode(normName, endptsList):
    # merge all nodes that have permutation of a given name
    for ep in endptsList:
        if ep.name == normName.split('/'):
            first = ep
            break
    else:
        raise exception.Exception('endpoint not found')
    rightNameEndpts = [ep for ep in endptsList
                       if '/'.join(sorted(ep.name)) == normName]
    return reduce(joinEndPts, rightNameEndpts, first)

def mergeAllNodes(uniqueNames, endptsList):
    # for each normalized name, merge nodes.
    return [mergeNode(name, endptsList) for name in uniqueNames]

def joinSubun(level, subunList):
    # create the list of names with the same level
    return (level, [su for su in subunList if su.level == level])

def computeInters(jointSubuns, target, allInter):
    # for a joint subun, gives the sum of cardinalities
    # of the nodes intersecated with target.
    # JOINTSUBUN is the out of joinSubun(level, subunList)
    # ALLINTER is the lookup table for intersection
    return sum([allInter[node2str(sorted(subun.name + [target]))]
              for subun in jointSubuns[1]])

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

