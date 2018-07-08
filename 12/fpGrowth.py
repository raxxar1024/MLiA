# !/usr/bin/python
# -*- coding=utf-8 -*-

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        print ' ' * ind, self.name, ' ', self.count
        for child in self.children.values():
            child.disp(ind + 1)


def createTree(dateSet, minSup=1):
    headerTable = {}
    for trans in dateSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dateSet[trans]
        for k in headerTable.keys():
            if headerTable[k] < minSup:
                del (headerTable[k])
        freqitemSet = set(headerTable.keys())
        if len(freqitemSet) == 0:
            return None, None
        for k in headerTable:
            headerTable[k] = [headerTable[k], None]
        retTree = treeNode('Null Set', 1, None)
        for tranSet, count in dateSet.items():
            localD = {}
            for item in tranSet:
                if item in freqitemSet:
                    localD[item] = headerTable[item]
            if len(localD) > 0:
                orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
                updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode()
        if headerTable[item[0]][1] == None:
            headerTable[items][1] = inTree
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode):
    while nodeToTest.nodeLink != None:
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


if __name__ == "__main__":
    rootNode = treeNode('pyramid', 9, None)
    rootNode.children['eye'] = treeNode('eye', 13, None)
    rootNode.disp()
    rootNode.children['phoenix'] = treeNode('phoenix', 3, None)
    rootNode.disp()
