# interMap is all the permutations of the sets

import itertools
import exceptions
from collections import namedtuple

# convert ensemble name to ID thru a global dictionary getID

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
 #   for c in getChildren(node, allPaths):
 #       print 'current node:', node
 #       print 'child allinfo:', c
 #       print 'target:', target
 #       print 'just child:', c[0]
 #       print 'postfix (cont):', (c[0][-1],) + c[1]

#assert(getChildrByTarget(['b'], genMap(['a', 'b', 'c', 'd']), 'a') ==
#       [('b', 'c'), ('b', 'd')])

endpoint = namedtuple('endpoint', ['node', 'cardi', 'addiInfo'])
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
        print 'Termination:', subUns
        # all subunions, accumulated, get finally into this
        return [endpoint(node=nd, cardi=getCard(nd),
                    addiInfo=[subun(name=nd, level=lvl)] + subUns)]
    else:
        out = [endpoint(node=nd, cardi=getCard(nd),
                        addiInfo=subUns)]
        print 'recursion. Current subunions:', subUns
        for child in getChildrByTarget(nd, interMap, target):
            print 'child:', child
            out += facto(child, [subun(name=nd, level=lvl)] + subUns,
                         target, lvl+1, interMap, numSet)
        return out

# maybe level are to be raised by one, and empty must be formalized more,
# but it looks good
assert(facto(['b'], [[]], 'a', 0, genMap(['a', 'b', 'c']), 3) ==
       [endpoint(node=['b'], cardi=1, addiInfo=[[]]),
        endpoint(node=('b', 'c'), cardi=1,
                 addiInfo=[subun(name=('b', 'c'), level=1),
                           subun(name=['b'], level=0),
                           []])])

# launch it on 4, you'll have the bug.
[endpoint(node=['b'], cardi=1, addiInfo=[[]]),

endpoint(node=('b', 'c'), cardi=1, addiInfo=[subun(name=['b'], level=0), []]),

endpoint(node=('b', 'c', 'd'), cardi=1, addiInfo=[subun(name=('b', 'c', 'd'), level=2), subun(name=('b', 'c'), level=1), subun(name=['b'], level=0), []]),

endpoint(node=('b', 'd'), cardi=1, addiInfo=[subun(name=['b'], level=0), []]),

endpoint(node=('b', 'd', 'c'), cardi=1, addiInfo=[subun(name=('b', 'd', 'c'), level=2), subun(name=('b', 'd'), level=1), subun(name=['b'], level=0), []])]
