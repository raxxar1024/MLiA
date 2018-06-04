# !/usr/bin/python
# -*- coding=utf-8 -*-
from numpy import *


def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        # 将每行映射成浮点数
        fltLine = map(float, curLine)
        dataMat.append(fltLine)
    return dataMat


def binSplitDataSet(dataSet, feature, value):
    mat0 = dataSet[nonzero(dataSet[:, feature] > value)[0], :]
    mat1 = dataSet[nonzero(dataSet[:, feature] <= value)[0], :]
    return mat0, mat1


def regLeaf(dataSet):
    return mean(dataSet[:, -1])


def regErr(dataSet):
    return var(dataSet[:, -1]) * shape(dataSet)[0]


def linearSolve(dataSet):
    m, n = shape(dataSet)
    # （以下两行）将X和Y中的数据格式化
    X = mat(ones((m, n)))
    # Y = mat(ones((m, 1)))
    X[:, 1:n] = dataSet[:, 0:n - 1]
    Y = mat(dataSet[:, -1])
    xTx = X.T * X
    if linalg.det(xTx) == 0.0:
        raise NameError('This matrox is singular, cannot do inverse, try increasing the second value of ops')
    ws = xTx.I * (X.T * Y)
    return ws, X, Y


def modelLeaf(dataSet):
    ws, X, Y = linearSolve(dataSet)
    return ws


def modelErr(dataSet):
    ws, X, Y = linearSolve(dataSet)
    yHat = X * ws
    return sum(power(Y - yHat, 2))


def chooseBestSplit(dataSet, leafType=regLeaf, errType=regErr, ops=(1, 4)):
    tolS = ops[0]
    tolN = ops[1]
    # （以下两行）如果所有值相等则退出
    if len(set(dataSet[:, -1].T.tolist()[0])) == 1:
        return None, leafType(dataSet)
    m, n = shape(dataSet)
    S = errType(dataSet)
    bestS = inf
    bestIndex = 0
    bestValue = 0
    for featIndex in range(n - 1):
        for splitVal in set(dataSet[:, featIndex].T.tolist()[0]):
            mat0, mat1 = binSplitDataSet(dataSet, featIndex, splitVal)
            if shape(mat0)[0] < tolN or shape(mat1)[0] < tolN:
                continue
            newS = errType(mat0) + errType(mat1)
            if newS < bestS:
                bestIndex = featIndex
                bestValue = splitVal
                bestS = newS
    # （以下两行）如果误差减少不大则退出
    if (S - bestS) < tolS:
        return None, leafType(dataSet)
    mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)
    if shape(mat0)[0] < tolN or shape(mat1)[0] < tolN:
        # （以下两行）如果切分出的数据集很小则退出
        return None, leafType(dataSet)
    return bestIndex, bestValue


def createTree(dataSet, leafType=regLeaf, errType=regErr, ops=(1, 4)):
    feat, val = chooseBestSplit(dataSet, leafType, errType, ops)
    # 满足停止条件时返回叶节点值
    if feat == None:
        return val
    retTree = {}
    retTree['spInd'] = feat
    retTree['spVal'] = val
    lSet, rSet = binSplitDataSet(dataSet, feat, val)
    retTree['left'] = createTree(lSet, leafType, errType, ops)
    retTree['right'] = createTree(rSet, leafType, errType, ops)
    return retTree


def isTree(obj):
    return type(obj).__name__ == 'dict'


def getMean(tree):
    if isTree(tree['right']):
        tree['right'] = getMean(tree['right'])
    if isTree(tree['left']):
        tree['left'] = getMean(tree['left'])
    return (tree['left'] + tree['right']) / 2.0


def prune(tree, testData):
    # 没有测试数据就对树进行塌陷处理
    if shape(testData)[0] == 0:
        return getMean(tree)
    if isTree(tree['right']) or isTree(tree['left']):
        lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
    if isTree(tree['left']):
        tree['left'] = prune(tree['left'], lSet)
    if isTree(tree['right']):
        tree['right'] = prune(tree['right'], rSet)
    if not isTree(tree['left']) and not isTree(tree['right']):
        lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
        errorNoMerge = sum(power(lSet[:, -1] - tree['left'], 2)) + sum(power(rSet[:, -1] - tree["right"], 2))
        treeMean = (tree['left'] + tree['right']) / 2.0
        errMerge = sum(power(testData[:, -1] - treeMean, 2))
        if errMerge < errorNoMerge:
            print 'merging'
            return treeMean
        else:
            return tree
    else:
        return tree


if __name__ == "__main__":
    # testMat = mat(eye(4))
    # print binSplitDataSet(testMat, 1, 0.5)

    # myDat = loadDataSet('ex00.txt')
    # myMat = mat(myDat)
    # print createTree(myMat)

    # myDat1 = loadDataSet('ex0.txt')
    # myMat1 = mat(myDat1)
    # print createTree(myMat1)

    # myDat2 = loadDataSet('ex2.txt')
    # myMat2 = mat(myDat2)
    # print createTree(myMat2)
    # print createTree(myMat2, ops=(10000, 4))

    # myTree = createTree(myMat2, ops=(0, 1))
    # myDatTest = loadDataSet('ex2test.txt')
    # myMat2Test = mat(myDatTest)
    # print prune(myTree, myMat2Test)

    myMat2 = mat(loadDataSet('exp2.txt'))
    print createTree(myMat2, modelLeaf, modelErr, (1, 10))
