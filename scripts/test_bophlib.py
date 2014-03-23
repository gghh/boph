import unittest
import operator
from bophlib import *


class testNChooseK(unittest.TestCase):
    
    def test_chooseZero(self):
        self.assertTrue(choose_n(0, ['a', 'b', 'c']) == 
                        [[]])

    def test_chooseOne(self):
        self.assertTrue(choose_n(1, ['a', 'b', 'c']) == 
                        [['a'], ['b'], ['c']])

    def test_chooseTwo(self):
        self.assertTrue(choose_n(2, ['a', 'b', 'c']) ==
                        [['a', 'b'], ['a', 'c'], ['b', 'a'],
                         ['b', 'c'], ['c', 'a'], ['c', 'b']])

    def test_chooseAll(self):
        self.assertTrue(choose_n(3, ['a', 'b', 'c']) ==
                        [['a', 'b', 'c'], ['a', 'c', 'b'],
                         ['b', 'a', 'c'], ['b', 'c', 'a'],
                         ['c', 'a', 'b'], ['c', 'b', 'a']])


class testAllChoices(unittest.TestCase):

    def test_allChoicesBase(self):
        self.assertTrue(allChoices(['a', 'b', 'c']) ==
                        [[],
                         
                         ['a'], ['b'], ['c'],
                         
                         ['a', 'b'], ['a', 'c'], ['b', 'a'],
                         ['b', 'c'], ['c', 'a'], ['c', 'b'],
                         
                         ['a', 'c', 'b']])

    def test_allChoicesNoDupes(self):
        self.assertTrue(remDupes(allChoices(['a', 'b', 'c'])) ==
                        [[], ['a'], ['b'], ['c'],
                         ['a', 'b'], ['a', 'c'], ['b', 'c'],
                         ['a', 'b', 'c']])

    def test_allChoicesNoDupesNoSing(self):
        self.assertTrue(remEmpty(remDupes(allChoices(['a', 'b', 'c']))) ==
                        [['a'], ['b'], ['c'],
                         ['a', 'b'], ['a', 'c'], ['b', 'c'],
                         ['a', 'b', 'c']])


class testIntrsLookup(unittest.TestCase):

    def test_intersLookup(self):
        li1 = range(10)
        li2 = range(5, 15)
        li3 = range(13, 20) + range(3)
        listRefs = listByID([li1, li2, li3])
        self.assertTrue(intersLookup(listRefs) ==
                        {'1/2': 2,
                         '0/2': 3,
                         '0/1': 5,
                         '1': 10,
                         '0': 10,
                         '2': 10,
                         '0/1/2': 0})


class testChldrByTgt(unittest.TestCase):

    def test_getChildrByTarget(self):
        self.assertTrue(getChildrByTarget(['b'], 
                                          ['a', 'b', 'c', 'd'], 'a') ==
                        [['b', 'c'], ['b', 'd']])

class testSubunEq(unittest.TestCase):

    def test_subunEq(self):
        self.assertTrue(subunEq(subun(name=('b', 'c'), level=2),
                                subun(name=('c', 'b'), level=2)) ==
                        True)
    
class testMergeEpts(unittest.TestCase):
    
    def test_mergeEpts(self):
        li1 = []
        li2 = []
        li3 = []
        li4 = []
        
        listRefs = listByID([(li1, 'a'),
                             (li2, 'b'),
                             (li3, 'c'),
                             (li4, 'd')])
        
        allInters = intersLookup(listRefs)
        
        
        d1 = {'b/c/d': endpoint(node=['b', 'd', 'c'], 
                                cardi=0, 
                                inBelly={'b/d': subun(name=['b', 'd'], 
                                                      level=2), 
                                         'b'  : subun(name=['b'], 
                                                      level=1), 
                                         ''   : subun(name=[[]], 
                                                      level=0)})}
        
        d2 = {'b': endpoint(node=['b'], 
                            cardi=0, 
                            inBelly={'': subun(name=[[]], level=0)}),
              'b/c/d': endpoint(node=['b', 'c', 'd'], 
                                cardi=0, 
                                inBelly={'b/c': subun(name=['b', 'c'], 
                                                      level=2), 
                                         'b'  : subun(name=['b'], 
                                                      level=1), 
                                         ''   : subun(name=[[]], 
                                                      level=0)})}
 
        self.assertTrue(\
            mergeEpts(d1, d2) ==
            
            {'b': endpoint(node=['b'],
                           cardi=0,
                           inBelly={'': subun(name=[[]], level=0)}),
             
             'b/c/d': endpoint(node=['b', 'd', 'c'],
                               cardi=0,
                               inBelly={'': subun(name=[[]], level=0),
                                        'b': subun(name=['b'], level=1),
                                        'b/c': subun(name=['b', 'c'], 
                                                     level=2),
                                        'b/d': subun(name=['b', 'd'], 
                                                     level=2)})})
        

class testComputeInters(unittest.TestCase):

    def test_computeInters(self):
        li1 = []
        li2 = []
        li3 = []
        li4 = []
        
        listRefs = listByID([(li1, 'a'),
                             (li2, 'b'),
                             (li3, 'c'),
                             (li4, 'd')])
        
        allInters = intersLookup(listRefs)
        
        endptsList = \
            (mergeEpts(\
                facto(['b'], {'': subun(name=[[]], level=0)},
                      'a', 1, 4,
                      allInters, ['a', 'b', 'c', 'd']),
                mergeEpts(\
                        facto(['c'], {'': subun(name=[[]], level=0)},
                              'a', 1, 4,
                              allInters, ['a', 'b', 'c', 'd']),
                        facto(['d'], {'': subun(name=[[]], level=0)},
                              'a', 1, 4,
                              allInters, ['a', 'b', 'c', 'd']))))
        li1 = range(10)
        li2 = range(5, 15)
        li3 = range(13, 20) + range(3)
        listRefs = listByID([(li1, 'a'),
                             (li2, 'b'),
                             (li3, 'c')])
        allInters = intersLookup(listRefs)
        subunDict = {'b': subun(name=['b'], level=1),
                     '' : subun(name=[[]], level=0),
                     'c': subun(name=['c'], level=1)}
        subuns = [s for s in subunByLevel(subunDict)]
        self.assertTrue(computeInters(subuns[0], 
                                      allInters, 
                                      ['a', 'b', 'c']) == 8)

class testFacto(unittest.TestCase):

    def test_facto3(self):
        # maybe level are to be raised by one,
        # and empty must be formalized more,
        # but it looks good
        li1 = []
        li2 = []
        li3 = []
        listRefs = listByID([(li1, 'a'),
                             (li2, 'b'),
                             (li3, 'c')])
        allInters = intersLookup(listRefs)
        
        self.assertTrue(\
            facto(['b'], {'': subun(name=[[]], level=0)},
                  'a', 1, 3,
                  allInters, ['a', 'b', 'c']) ==
            {'b': endpoint(node=['b'],
                           cardi=0,
                           inBelly={'': subun(name=[[]], level=0)}),
             'b/c': endpoint(node=['b', 'c'],
                             cardi=0,
                             inBelly={'b': subun(name=['b'], level=1),
                                      '' : subun(name=[[]], level=0)})})

    def test_facto4(self):
    
        li1 = []
        li2 = []
        li3 = []
        li4 = []
        listRefs = listByID([(li1, 'a'),
                             (li2, 'b'),
                             (li3, 'c'),
                             (li4, 'd')])
        allInters = intersLookup(listRefs)

        self.assertTrue(\
            facto(['b'], {'': subun(name=[[]], level=0)},
                  'a', 1, 4,
                  allInters, ['a', 'b', 'c', 'd']) ==
            
            {'b/d': endpoint(node=['b', 'd'], 
                             cardi=0,
                             inBelly={'b': subun(name=['b'], level=1), 
                                      '' : subun(name=[[]], level=0)}), 
             'b': endpoint(node=['b'], 
                           cardi=0, 
                           inBelly={'' : subun(name=[[]], level=0)}), 
             'b/c/d': endpoint(node=['b', 'c', 'd'], 
                               cardi=0, 
                               inBelly={'b/c': subun(name=['b', 'c'], 
                                                     level=2), 
                                        'b'  : subun(name=['b'], level=1), 
                                        ''   : subun(name=[[]], level=0),
                                        'b/d': subun(name=['b', 'd'], 
                                                     level=2), 
                                        'b'  : subun(name=['b'], level=1), 
                                        ''   : subun(name=[[]], level=0)}), 
             'b/c': endpoint(node=['b', 'c'], 
                             cardi=0, 
                             inBelly={'b' : subun(name=['b'], level=1),
                                      ''  : subun(name=[[]], level=0)})})

class testSubunByLevel(unittest.TestCase):
    
    def test_subunByLevel(self):
        getSubs = subunByLevel({'b/c': subun(name=['b', 'c'], level=2),
                                'b'  : subun(name=['b'], level=1),
                                ''   : subun(name=[[]], level=0),
                                'b/d': subun(name=['b', 'd'], level=2),
                                'c'  : subun(name=['c'], level=1),
                                'c/d': subun(name=['c', 'd'], level=2),
                                'd'  : subun(name=['d'], level=1)})
        
        self.assertTrue([s for s in getSubs] ==
                        
                        [[('b/d', subun(name=['b', 'd'], level=2)),
                          ('b/c', subun(name=['b', 'c'], level=2)),
                          ('c/d', subun(name=['c', 'd'], level=2))],

                         [('d', subun(name=['d'], level=1)),
                          ('b', subun(name=['b'], level=1)),
                          ('c', subun(name=['c'], level=1))],
                         
                         [('', subun(name=[[]], level=0))]])


class testNode(unittest.TestCase):
    
    def test_node1(self):
        self.assertTrue(node(['c', 'd'],
                             ['a', 'b', 'c', 'd'],
                             upPath()).dwnPth() ==
                        ['a', 'b'])

    def test_node2(self):
        self.assertTrue(node([[]], 
                             ['a', 'b', 'c', 'd'], 
                             upPath()).dwnPth() ==
                        ['a', 'c', 'b', 'd'])

    def test_node3(self):
        self.assertTrue(node(['1', '2', '3'],
                             ['1', '2', '3', '4'],
                             upPath()).dwnPth() ==
                        ['4'])

class testGetCard(unittest.TestCase):

    def test_getCard(self):
        li1 = range(10)
        li2 = range(5, 15)
        li3 = range(13, 20) + range(3)
        li4 = [n for n in range(20) if n % 2 == 0]
        
        listRefs = listByID([li1, li2, li3, li4])
        allInters = intersLookup(listRefs)
        
        self.assertTrue(getCard(('1', '2', '3'), allInters,
                                map(str, listRefs.keys())) == 
                        10)

class testBaseCase(unittest.TestCase):

    def test_basecase(self):
        A = range(3)
        B = range(3)
        C = range(3)
        
        listlist = [(A, 'A'), (B, 'B'), (C, 'C')]
        
        names = [e[1] for e in listlist]
        li = [e[0] for e in listlist]
        ids = map(str, range(len(names)))
        names_map = dict(zip(ids, names))
        listlist = zip(li, ids)
        
        self.assertTrue(getDiss_inlists(listlist) ==
                        {'1/2': 0,
                         '0/2': 0,
                         '0/1': 0,
                         '1': 0,
                         '0': 0,
                         '2': 0,
                         '0/1/2': 3})

class completeTests(unittest.TestCase):

    def setUp(self):
        self.liA = []
        self.liB = []
        self.liC = []
        self.liD = []
        
        self.liA += [1]
        self.liB += [1]
        self.liC += [1]
        self.liD += [1]
        
        self.liA += range(2,4)
        self.liB += range(2,4)
        self.liC += range(2,4)
        
        self.liA += range(4,7)
        self.liB += range(4,7)
        self.liD += range(4,7)
        
        self.liA += range(7,11)
        self.liC += range(7,11)
        self.liD += range(7,11)
        
        self.liB += range(11,16)
        self.liC += range(11,16)
        self.liD += range(11,16)
        
        self.liA += range(16,22)
        self.liB += range(16,22)
        
        self.liA += range(22, 29)
        self.liC += range(22, 29)
        
        self.liA += range(29, 37)
        self.liD += range(29, 37)
        
        self.liB += range(37, 46)
        self.liC += range(37, 46)
        
        self.liB += range(46, 56)
        self.liD += range(46, 56)
        
        self.liC += range(56, 67)
        self.liD += range(56, 67)
        
        self.liA += range(67, 79)
        
        self.liB += range(79, 92)
        
        self.liC += range(92, 106)
        
        self.liD += range(106, 121)
        
        self.listRefs = {'A': self.liA,
                         'B': self.liB,
                         'C': self.liC,
                         'D': self.liD}
        self.allInters = intersLookup(self.listRefs)

    def test_multiDemoivre(self):
        epl = {'B/C/D': endpoint(node=['B', 'C', 'D'],
                                 cardi=getCard(['B', 'C', 'D'], 
                                               self.allInters,
                                               map(str,
                                                   self.listRefs.keys())),
                                 inBelly={'D/C': subun(name=['D', 'C'],
                                                       level=2),
                                          'D/B': subun(name=['D', 'B'],
                                                       level=2),
                                          'C/B': subun(name=['C', 'B'],
                                                       level=2),
                                          'D'  : subun(name=['D'],
                                                       level=1),
                                          'C'  : subun(name=['C'],
                                                       level=1),
                                          'B'  : subun(name=['B'],
                                                       level=1),
                                          ''   : subun(name=[[]],
                                                       level=0)}),

               'C/D': endpoint(node=['C', 'D'],
                               cardi=getCard(['C', 'D'], 
                                             self.allInters,
                                             map(str, 
                                                 self.listRefs.keys())),
                               inBelly={'D': subun(name=['D'], level=1),
                                        'C': subun(name=['C'], level=1),
                                        '' : subun(name=[[]], level=0)}),
               
               'B/D': endpoint(node=['B', 'D'],
                               cardi=getCard(['B', 'D'],
                                             self.allInters,
                                             map(str,
                                                 self.listRefs.keys())),
                               inBelly={'D': subun(name=['D'], level=1),
                                        'B': subun(name=['B'], level=1),
                                        '' : subun(name=[[]], level=0)}),

               'B/C': endpoint(node=['B', 'C'],
                               cardi=getCard(['B', 'C'],
                                             self.allInters,
                                             map(str,
                                                 self.listRefs.keys())),
                               inBelly={'C': subun(name=['C'], level=1),
                                        'B': subun(name=['B'], level=1),
                                        '' : subun(name=[[]], level=0)}),

               'D': endpoint(node=['D'],
                             cardi=getCard(['D'], self.allInters,
                                           map(str, self.listRefs.keys())),
                             inBelly={'': subun(name=[[]], level=0)}),
               
               'C': endpoint(node=['C'],
                             cardi=getCard(['C'], self.allInters,
                                           map(str, self.listRefs.keys())),
                             inBelly={'': subun(name=[[]], level=0)}),
               
               'B': endpoint(node=['B'],
                             cardi=getCard(['B'], self.allInters,
                                           map(str, self.listRefs.keys())),
                             inBelly={'': subun(name=[[]], level=0)})}
        
        dissList = multiDeMoivre(epl.values(), 
                                 self.allInters,
                                 ['A', 'B', 'C', 'D'])

        self.assertTrue(sorted(dissList, 
                               key=operator.attrgetter('value')) ==
                        [dissipation(name=['D'], value=2),
                         dissipation(name=['C'], value=3),
                         dissipation(name=['B'], value=4),
                         dissipation(name=['C', 'D'], value=6),
                         dissipation(name=['B', 'D'], value=7),
                         dissipation(name=['B', 'C'], value=8),
                         dissipation(name=['B', 'C', 'D'], value=12)])


    def test_multiDemoivreTgt(self):
        
        eptsLi_tA = (mergeEpts(\
                facto(['B'], {'': subun(name=[[]], level=0)},
                      'A', 1, 4,
                      self.allInters, ['A', 'B', 'C', 'D']),
                mergeEpts(\
                    facto(['C'], {'': subun(name=[[]], level=0)},
                          'A', 1, 4,
                          self.allInters, ['A', 'B', 'C', 'D']),
                    mergeEpts(\
                        facto(['D'], {'': subun(name=[[]], level=0)},
                              'A', 1, 4,
                              self.allInters, ['A', 'B', 'C', 'D']),
                        {node([[]], ['a', 'b', 'c', 'd'],
                              upPath()).nrmUpStr():
                             endpoint(node=[[]], cardi=1, inBelly={})}))))
        
        
        dissLi_tA = multiDeMoivre(eptsLi_tA.values(), self.allInters,
                                  ['A', 'B', 'C', 'D'])
        
        dissList = [dissipation(name=['C'], value=3), 
                    dissipation(name=['B'], value=4), 
                    dissipation(name=['D'], value=2), 

                    dissipation(name=['C', 'D'], value=6), 
                    dissipation(name=['B', 'C'], value=8), 
                    dissipation(name=['B', 'D'], value=7),

                    dissipation(name=['B', 'C', 'D'], value=12)]

        self.assertTrue(sorted(dissLi_tA, 
                               key=operator.attrgetter('value')) ==
                        ([dissipation(name=[[]], value=1)] +
                         sorted(dissList,
                                key=operator.attrgetter('value'))))
        
        
    def test_getDiss_tgt(self):

        self.assertTrue(sorted(getDiss_tgt('A', ['A', 'B', 'C', 'D'],
                                           self.allInters),
                               key=operator.attrgetter('value')) ==
                        [dissipation(name=[[]], value=1),
                         dissipation(name=['D'], value=2),
                         dissipation(name=['C'], value=3),
                         dissipation(name=['B'], value=4),
                         dissipation(name=['C', 'D'], value=6),
                         dissipation(name=['B', 'D'], value=7),
                         dissipation(name=['C', 'B'], value=8),
                         dissipation(name=['C', 'B', 'D'], value=12)])

        
    def test_getDiss_tgt2(self):

        self.assertTrue(sorted(getDiss_tgt('B', ['A', 'B', 'C', 'D'], 
                                           self.allInters),
                               key=operator.attrgetter('value')) ==
                        [dissipation(name=[[]], value=1),
                         dissipation(name=['D'], value=2),
                         dissipation(name=['C'], value=3),
                         dissipation(name=['A'], value=5),
                         dissipation(name=['C', 'D'], value=6),
                         dissipation(name=['A', 'D'], value=9),
                         dissipation(name=['A', 'C'], value=10),
                         dissipation(name=['A', 'C', 'D'], value=13)])
        

    def test_getDiss_tgt3(self):
        
        self.assertTrue(sorted(getDiss_tgt('D', ['A', 'B', 'C', 'D'],
                                           self.allInters),
                               key=operator.attrgetter('value')) ==
                        [dissipation(name=[[]], value=1),
                         dissipation(name=['C'], value=3),
                         dissipation(name=['B'], value=4),
                         dissipation(name=['A'], value=5),
                         dissipation(name=['C', 'B'], value=8),
                         dissipation(name=['A', 'C'], value=10),
                         dissipation(name=['A', 'B'], value=11),
                         dissipation(name=['A', 'C', 'B'], value=15)])
        

    def test_getDiss_tgt4(self):
        
        self.assertTrue(sorted(getDiss_tgt('C', ['A', 'B', 'C', 'D'],
                                           self.allInters),
                               key=operator.attrgetter('value')) ==
                        [dissipation(name=[[]], value=1),
                         dissipation(name=['D'], value=2),
                         dissipation(name=['B'], value=4),
                         dissipation(name=['A'], value=5),
                         dissipation(name=['B', 'D'], value=7),
                         dissipation(name=['A', 'D'], value=9),
                         dissipation(name=['A', 'B'], value=11),
                         dissipation(name=['A', 'B', 'D'], value=14)])


    def test_getDiss_glb(self):
        
        d = getDiss_glb(['A', 'B', 'C', 'D'], self.allInters)
        self.assertTrue(sorted(d.iteritems(),
                               key=operator.itemgetter(1)) ==
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


    def test_dissByLevel(self):
        d = getDiss_inlists([self.liA, self.liB, self.liC, self.liD])
        self.assertTrue(sorted(d.iteritems(), 
                               key=operator.itemgetter(1)) ==
                        [('0/1/2/3', 1),
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
                         ('3', 15)])

    def test_pprintDiss1(self):

        self.assertTrue(pprintDiss([(self.liA, 'foo'),
                                    (self.liB, 'bar'),
                                    (self.liC, 'squirrel'),
                                    (self.liD, 'kitten')],
                                   out_format='csv') ==

       """group,value
1,5
2,5
3,5
group,value
1,10
3,10
group,value
1,9
2,9
group,value
0,7
2,7
group,value
0,8
3,8
group,value
0,6
1,6
group,value
0,4
2,4
3,4
group,value
0,12
group,value
3,15
group,value
1,13
group,value
0,1
1,1
2,1
3,1
group,value
0,3
1,3
3,3
group,value
2,14
group,value
2,11
3,11
group,value
0,2
1,2
2,2
labels
foo
bar
squirrel
kitten
""")

    def test_pprintDiss2(self):
        self.assertTrue(pprintDiss([(self.liA, 'foo'),
                                    (self.liB, 'bar'),
                                    (self.liC, 'squirrel'),
                                    (self.liD, 'kitten')],
                                   out_format='js') ==
                        """connections = [ [
	{group: 1, value: 5},
	{group: 2, value: 5},
	{group: 3, value: 5}
],
[
	{group: 1, value: 10},
	{group: 3, value: 10}
],
[
	{group: 1, value: 9},
	{group: 2, value: 9}
],
[
	{group: 0, value: 7},
	{group: 2, value: 7}
],
[
	{group: 0, value: 8},
	{group: 3, value: 8}
],
[
	{group: 0, value: 6},
	{group: 1, value: 6}
],
[
	{group: 0, value: 4},
	{group: 2, value: 4},
	{group: 3, value: 4}
],
[
	{group: 0, value: 12}
],
[
	{group: 3, value: 15}
],
[
	{group: 1, value: 13}
],
[
	{group: 0, value: 1},
	{group: 1, value: 1},
	{group: 2, value: 1},
	{group: 3, value: 1}
],
[
	{group: 0, value: 3},
	{group: 1, value: 3},
	{group: 3, value: 3}
],
[
	{group: 2, value: 14}
],
[
	{group: 2, value: 11},
	{group: 3, value: 11}
],
[
	{group: 0, value: 2},
	{group: 1, value: 2},
	{group: 2, value: 2}
] ];


labels = {
	0: "foo",
	1: "bar",
	2: "squirrel",
	3: "kitten"
};
""")


if __name__ == '__main__':
    unittest.main()

