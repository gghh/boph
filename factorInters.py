import itertools
import exceptions
import operator
from collections import namedtuple

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

def allChoices(srcList):
    out = []
    for i in range(len(srcList)+1):
        out += choose_n(i, srcList)
    return out

def remDupes(listlist):
    out = []
    for li in listlist:
        li.sort()
        if not li in out:
            out.append(li)
    return out

def remEmpty(lis):
    for cnt, elem in enumerate(lis):
        if len(elem) == 0:
            return lis[:cnt] + lis[(cnt+1):]
    raise exceptions.Exception('empty non found')

def genMap(IDList):
    removeLast = lambda x: x[:-1]
    # removing last elem in up-path of the lattice
    # is a key point. Otherwise the concept of
    # `ensemble on top of chain` is meaningless,
    # since `empty` is on top of all chains.
    return map(removeLast,
               [p for p in itertools.permutations(IDList)])

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

endpoint = namedtuple('endpoint', ['node', 'cardi', 'inBelly'])
subun = namedtuple('subun', ['name', 'level'])

def getCard(pathFromBottom, allInters, allNames):
    # input are endpoints, i.e. path from bottom.
    pathFromTop = node2sets(endpoint(node=pathFromBottom,
                                     cardi=None,
                                     inBelly=None),
                            allNames)
    return allInters['/'.join(sorted(pathFromTop))]

# mock function
## getCard = lambda x: 1

def facto(nd, subUns, target, lvl, interMap,
          numSet, allInters, allNames):
    # note: node are ident by path from the bottm,
    # so it isn't real clear how to refer to the lower terminal
    # which, strictly speaking, is the empty.
    # You know what? I can launch N instances, where N is
    # the number of my ensembles. Then I join the result.
    #
    # I need numSet to know if I am at the end of run
    if len(nd) == numSet-1 and not target in nd:
        # all subunions, accumulated, get finally into this
        return [endpoint(node=nd, cardi=getCard(nd, allInters, allNames),
                         inBelly=subUns)]
    else:
        out = [endpoint(node=nd, cardi=getCard(nd, allInters, allNames),
                        inBelly=subUns)]
        for child in getChildrByTarget(nd, interMap, target):
            out += facto(child, [subun(name=nd, level=lvl)] + subUns,
                         target, lvl+1, interMap, numSet, allInters,
                         allNames)
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

def flip():
    curr = 1
    while True:
        yield curr
        curr *= -1

def mergeNode(normName, endptsList):
    # merge all nodes that have permutation of a given name
    for ep in endptsList:
        if '/'.join(sorted(ep.node)) == normName:
            first = ep
            break
    else:
        # I am assuming that for each normalized name,
        # there exists an endpoint with exactly *that* name,
        # I mean in the 'normalized' order
        print normName
        raise exceptions.Exception('endpoint not found')
    rightNameEndpts = [ep for ep in endptsList
                       if '/'.join(sorted(ep.node)) == normName]
    return reduce(joinEndPts, rightNameEndpts, first)

def mergeAllNodes(uniqueNames, endptsList):
    # for each normalized name, merge nodes.
    return [mergeNode(name, endptsList) for name in uniqueNames]

def joinSubun(level, subunList):
    # create the list of names with the same level
    return (level, [su for su in subunList if su.level == level])

def computeInters(jointSubuns, allInter, nameList):
    # for a joint subun, gives the sum of cardinalities
    # of the nodes intersecated with target.
    # JOINTSUBUN is the out of joinSubun(level, subunList)
    # ALLINTER is the lookup table for intersection
    ## print 'jSubs:', jointSubuns # DBG
    findPoint =  \
        lambda pathFromBottom: \
        node2sets(endpoint(node = pathFromBottom,
                           cardi=None,
                           inBelly=None), nameList)
    return sum([allInter[node2str(sorted(list(findPoint(subun.name))))]
                for subun in jointSubuns[1]])

# ok I made up this word. It means the cardinality of
# a set without all the subunions it have in the belly.
dissipation = namedtuple('dissipation', ['name', 'value'])

def subunByLevel(subunList):
    sortedSubun = sorted(subunList,
                         key=operator.attrgetter('level'))
    while sortedSubun:
        out = [sortedSubun.pop()]
        while True:
            if sortedSubun:
                current = sortedSubun.pop()
                if (current.level) != (out[-1].level):
                    # back in list
                    sortedSubun += [current]
                    break
                else:
                    # append to output
                    out += [current]
            else:
                break
        yield out

def node2sets(endpt, nameList):
    # cryptic. this is because the all-in intersection
    # has [[]] as the sole node (list isn't hashable
    pprint = lambda things: things if all(things) else []
    return list(set(nameList) - set(pprint(endpt.node)))

def deMoivre(endpt, allInters, nameList):
    lvlSubs = [s for s in subunByLevel(endpt.inBelly)]
    jSubs = [joinSubun(lvl, lvlSub)
             for lvl, lvlSub in zip(range(len(lvlSubs)-1,-1,-1),
                                    lvlSubs)]
    pathFromTop = node2sets(endpt, nameList)
    currentInters = allInters['/'.join(sorted(pathFromTop))]
    # De Moivre formula! Yay!
    sign = flip()
    subunValue = \
        sum(map(lambda (sign, value): sign * value,
                zip(sign,
                    map(lambda js: computeInters(js, allInters, nameList),
                        jSubs))))
    return dissipation(name=endpt.node,
                       value = currentInters - subunValue)

def multiDeMoivre(endptList, allInters, nameList):
    return map(lambda ep: deMoivre(ep, allInters, nameList),
               endptList)
               
                                
def getDiss_tgt(target, nameList, allInters):
    eptLi = []
    for e in list(set(nameList) - set(target)):
        eptLi += facto([e], [subun(name=[[]], level=0)],
                      target, 1, genMap(nameList),
                      len(nameList), allInters, nameList)
    eptLi_nodupes = (mergeAllNodes(getUniqueNodes(eptLi),
                                    eptLi) + 
                      [endpoint(node=[[]], cardi=1, inBelly=[])])
    dissLi = multiDeMoivre(eptLi_nodupes, allInters, nameList)
    return dissLi

def getDiss_glb(nameList, allInters):
    diss_dict = {}
    for name in nameList:
        for diss in getDiss_tgt(name, nameList, allInters):
            ep = endpoint(node=diss.name, cardi=None, inBelly=None)
            upPath_str = '/'.join(sorted(node2sets(ep, nameList)))
            if upPath_str not in diss_dict:
                diss_dict[upPath_str] = diss.value
            else:
                pass
    return diss_dict


def getDiss_inlists(listlist):
    listRefs = listByID(listlist)
    allInters = intersLookup(listRefs)
    return getDiss_glb(map(str, listRefs.keys()), allInters)
    
