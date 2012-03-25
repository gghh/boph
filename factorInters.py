# interMap is all the permutations of the sets

import itertools
import exceptions

p = [pp for pp in itertools.permutations([1,2,3])]
dir(p)
type(p)
print p

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

def getChildren(node, allPaths):
    # NODE is a partial path, starting from the
    # all-intersected ensebles.
    # ALLPATHS are complete paths, from one end
    # to the other of the lattice. You get them via
    # genMap.
    out = []
    for path in allPaths:
        if node2str(path).startswith(node2str(node)):
            for cnt, endpoint in enumerate(path):
                if not endpoint == node[cnt]:
                    # first endpoint who differs,
                    # that the repr of a kid. Put in the backpack.
                    out.append(path[:cnt])
                    break
    return out

def node2str(node):
    # node is a list of IDs indentifying the node from the bottom
    # of the lattice. Well, the bottom on the diagram I drew
    # on the witheboard :-)
    # Note: they're numerical IDs, so no risk of clashes with char '/'
    return '/'.join(map(str, node))


def genMap(IDList):
    return [p for p in itertools.permutations(IDList)]

paths = genMap(['A', 'B', 'C', 'D'])
slice = namedtuple('slice', ['node', 'cardi', 'addiInfo'])

def facto(inters, subUns, interMap):
    
    
