import itertools
import exceptions
import operator
from collections import namedtuple

def o(f, g):
    # function composition
    def helper(x):
        return f(g(x))
    return helper

class upPath(object):
    pass

class downPath(object):
    pass

class node():
    def __init__(self, data, namelist, typ):
        self.ln = len(data)
        self.namelist = namelist
        if isinstance(typ, upPath):
            self.upPath = data
            self.downPath = None
        elif isinstance(typ, downPath): 
            self.downPath = data
            self.upPath = None

    def upStr(self):
        self.upString = '/'.join(map(str, self.upPath))
        return self.upString

    def dwnStr(self):
        self.downString = '/'.join(self.downPath)
        return self.downString

    def nrmDwnStr(self):
        if not self.downPath:
            self.dwnPth()
        self.normDownString = '/'.join(map(str, sorted(self.downPath)))
        return self.normDownString

    def nrmUpStr(self):
        pprint = lambda things: things if all(things) else []
        self.normUpString = '/'.join(sorted(pprint(self.upPath)))
        return self.normUpString

    def dwnPth(self):
        if not self.upPath:
            raise exceptions.Exception('asking for downPath w/o upPath. Bizarre')
        # convert up-path to down-path
        pprint = lambda things: things if all(things) else []
        self.downPath = list(set(self.namelist) -
                             set(pprint(self.upPath)))
        return self.downPath

def mergeEpts(dict1, dict2):
    for idx, ept in dict2.iteritems():
        if idx in dict1:
            dict1[idx].inBelly.update(dict2[idx].inBelly)
        else:
            dict1[idx] = ept
    return dict1

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
    tot = len(srcList)+1
    complem = lambda universe, ensemble: \
        list(set(universe) - set(ensemble))
    complSrcList = lambda ensemble: complem(srcList, ensemble)
    for i in range(tot):
        if i > tot / 2: # integer division
            out += map(complSrcList, choose_n(tot - (i + 1), srcList))
        else:
            out += choose_n(i, srcList)
        # print 'done with symbols for level', i
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

def listByID(listlist):
    # this is to store reference to the lists,
    # so that I can do all my computation symbolically,
    # and add numbers only at the end.
    #
    # input can be a list of lists,
    # or a list of tuples (list, name) to give your handles
    # to the data
    out = {}
    if all(len(x) == 2 and type(x) == tuple
           for x in listlist):
        for li, name in listlist:
            out[name] = li
    elif all(type(x) == list for x in listlist):
        for cnt, li in enumerate(listlist):
            out[cnt] = li
    else:
        raise exceptions.Exception('Malformed input.')
    return out

def inters_n(listlist):
    out = set(listlist[0])
    for li in listlist[1:]:
        out = out.intersection(set(li))
    return out
    
def intersLookup(listRefs):
    # print 'computing intersections lookup table'
    toInters = remEmpty(remDupes(allChoices(listRefs.keys())))
    doInter = lambda s, t: set(s).intersection(set(t))

    def inters_n(noude):
        nd_dwnstr = node(noude, [], downPath()).nrmDwnStr()
        return (nd_dwnstr,
                reduce(doInter,
                       [listRefs[r] for r in noude[1:]],
                       listRefs[noude[0]]))
    #inters_n = lambda node: \
    #    (node2str(node), reduce(doInter,
    #                            [listRefs[r] for r in node[1:]],
    #                            listRefs[node[0]]))
    count = lambda (namesChain, inters): (namesChain, len(inters))
    #return dict(map(o(count, inters_n), toInters))
    lt = dict(map(o(count, inters_n), toInters))
    return lt

def getChildrByTarget(innode, allNames, target):
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
    complem = lambda ensemble, universe: list(set(universe) - set(ensemble))
    complemNames = lambda ensemble: complem(ensemble, allNames)
    addOne = lambda ensemble, elem: ensemble + [elem]
    addOne2 = lambda elem: addOne(innode, elem)
    return map(addOne2, list(set(complemNames(innode)) - set([target])))

endpoint = namedtuple('endpoint', ['node', 'cardi', 'inBelly'])
subun = namedtuple('subun', ['name', 'level'])

def getCard(pathFromBottom, allInters, allNames):
    # input are endpoints, i.e. path from bottom.
    nd = node(pathFromBottom, allNames, upPath())
    return allInters[nd.nrmDwnStr()]

# mock function
## getCard = lambda x: 1

def facto(nd, subUns, target, lvl,
          numSet, allInters, allNames, tab=''):
    # note: node are ident by path from the bottm,
    # so it isn't real clear how to refer to the lower terminal
    # which, strictly speaking, is the empty.
    # You know what? I can launch N instances, where N is
    # the number of my ensembles. Then I join the result.
    #
    # I need numSet to know if I am at the end of run
    if target in nd:
        raise exceptions.Exception('Error: target is in node.' +
                                   " It doesn't make sense")
    ## print tab + 'facto:: enter. Node is', nd
    if len(nd) == numSet-1 and not target in nd:
        # all subunions, accumulated, get finally into this
        ## print tab + 'facto:: terminal return. Node:', nd
        return {node(nd, allNames, upPath()).nrmUpStr():
                    endpoint(node=nd, cardi=getCard(nd, allInters, allNames),
                             inBelly=subUns)}
    else:
        out = {node(nd, allNames, upPath()).nrmUpStr():
                   endpoint(node=nd, cardi=getCard(nd, allInters, allNames),
                             inBelly=subUns)}
        for child in getChildrByTarget(nd, allNames, target):
            mergeEpts(out,
                      facto(child,
                            mergeEpts({node(nd, allNames, upPath()).nrmUpStr():
                                           subun(name=nd, level=lvl)},
                                      subUns),
                            target, lvl+1, numSet, allInters,
                            allNames, tab=tab+' '))
        ## print tab + 'facto:: return from node', nd
        return out

def subunEq(subun1, subun2):
    # here we have to go f.a.s.t.
    #
    if subun1.name:
        if subun2.name:
            return sorted(subun1.name) == sorted(subun2.name) and \
                subun1.level == subun2.level
        else:
            return False
    else:
        if subun2.name:
            return False
        else:
            return subun1.level == subun2.level

def flip():
    curr = 1
    while True:
        yield curr
        curr *= -1

def computeInters(jointSubuns, allInter, nameList):
    # for a joint subun, gives the sum of cardinalities
    # of the nodes intersecated with target.
    # JOINTSUBUN is the out of joinSubun(level, subunList)
    # ALLINTER is the lookup table for intersection
    ## print 'jSubs:', jointSubuns # DBG
    return sum([allInter[node(subun.name,
                              nameList,
                              upPath()).nrmDwnStr()]
                for subun in [s[1] for s in jointSubuns]])

# ok I made up this word. It means the cardinality of
# a set without all the subunions it have in the belly.
dissipation = namedtuple('dissipation', ['name', 'value'])

def subunByLevel(subunDict):
    sortedSubun = sorted(subunDict.iteritems(),
                         key=o(operator.attrgetter('level'),
                               operator.itemgetter(1)))
    while sortedSubun:
        out = [sortedSubun.pop()]
        while True:
            if sortedSubun:
                current = sortedSubun.pop()
                if (current[1].level) != (out[-1][1].level):
                    # back in list
                    sortedSubun += [current]
                    break
                else:
                    # append to output
                    out += [current]
            else:
                break
        yield out

def deMoivre(endpt, allInters, nameList):
    lvlSubs = [s for s in subunByLevel(endpt.inBelly)]
    currentInters = allInters[node(endpt.node,
                                   nameList,
                                   upPath()).nrmDwnStr()]
    # De Moivre formula! Yay!
    sign = flip()
    subunValue = \
        sum(map(lambda (sign, value): sign * value,
                zip(sign,
                    map(lambda js: computeInters(js, allInters, nameList),
                        lvlSubs))))
    # print 'Computed De Moivre for ' + str(endpt.node)
    return dissipation(name=endpt.node,
                       value = currentInters - subunValue)

def multiDeMoivre(endptList, allInters, nameList):
    return map(lambda ep: deMoivre(ep, allInters, nameList),
               endptList)
               
                                
def getDiss_tgt(target, nameList, allInters):
    eptLi = {}
    for e in list(set(nameList) - set([target])):
        mergeEpts(eptLi, facto([e], {'': subun(name=[[]], level=0)},
                               target, 1,
                               len(nameList), allInters, nameList))
        # print '  done with step [' + e + ']'
    # just to find a key in eptLi
    for k in eptLi:
        break
    # print ('merging ' + str(len(eptLi)) + ' nodes, ' +
    #       str(len(eptLi[k])) + ' nested levels each...')
    eptLi = mergeEpts(eptLi,
                      {node([[]], nameList, upPath()).nrmUpStr():
                           endpoint(node=[[]],
                                    cardi=getCard([[]], allInters, nameList),
                                    inBelly={})})
    # print 'merged nodes'
    dissLi = multiDeMoivre(eptLi.values(), allInters, nameList)
    return dissLi

def getDiss_glb(nameList, allInters):
    diss_dict = {}
    for name in nameList:
        # print 'processing target [' + name + ']'
        for diss in getDiss_tgt(name, nameList, allInters):
            ep_dwnstr = node(diss.name, nameList, upPath()).nrmDwnStr()
            if ep_dwnstr not in diss_dict:
                diss_dict[ep_dwnstr] = diss.value
            else:
                pass
    return diss_dict


def getDiss_inlists(listlist):
    listRefs = listByID(listlist)
    allInters = intersLookup(listRefs)
    return getDiss_glb(map(str, listRefs.keys()), allInters)
    

def pprintDiss(listlist, out_format='csv'):
    names = [e[1] for e in listlist]
    li = [e[0] for e in listlist]
    ids = map(str, range(len(names)))
    names_map = dict(zip(ids, names))
    listlist = zip(li, ids)
    diss_dict = getDiss_inlists(listlist)
    diss_dict_nonil = []
    for k, v in diss_dict.iteritems():
        if v > 0:
            diss_dict_nonil.append((k, v))
    diss_dict_nonil = dict(diss_dict_nonil)
    if out_format == 'csv':
        out = ''
        for k in diss_dict_nonil:
            out += 'group,value\n'
            eps = k.split('/')
            for ep in eps:
                out += str(ep) + ',' + str(diss_dict_nonil[k]) + '\n'
        out += 'labels\n'
        for idx in range(len(names_map)):
            out += names_map[str(idx)] + '\n'
        return out
    elif out_format == 'js':
        edge = lambda x, y: '{group: %s, value: %s}' % (x, str(y))
        connections = []
        for k in diss_dict_nonil:
            eps = k.split('/')
            edges = []
            for ep in eps:
                edges.append(edge(ep, diss_dict_nonil[k]))
            connections.append(',\n\t'.join(edges))
        connections = map(lambda x: '[\n\t' + x + '\n]', connections)
        labels = []
        for idx in range(len(names_map)):
            labels.append(str(idx) + ': "' + names_map[str(idx)] + '"')
        labels = ',\n\t'.join(labels)
        labels = 'labels = {\n\t' + labels + '\n};\n'
        connections = 'connections = [ ' + ',\n'.join(connections) + ' ];\n'
        return connections + '\n\n' + labels
        

if __name__ == '__main__':

    nice_people = ['charline', 'martin', 'benedikt', 'camilla']
    rich_people = ['sebastian', 'camilla']
    smart_people = ['larry', 'camilla', 'charline', 'gustavo', 'audrey']
    
    print pprintDiss([(nice_people, 'nice_people'),
                      (rich_people, 'rich_people'),
                      (smart_people, 'smart_people')],
                     out_format='csv')
