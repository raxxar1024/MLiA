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
    mat0 = dataSet[nonzero(dataSet[:, feature] > value)[0], :][0]
    mat1 = dataSet[nonzero(dataSet[:, feature] <= value)[0], :][0]
    return mat0, mat1


# def createTree(dataSet, leafType=regLeaf, errType=regErr. ops=(1,4)):
#     feat, val = chooseBestSplit(dataSet, leafType, errType, ops)
#     # 满足停止条件时返回叶节点值
#     if feat == None:
#         return val
#     retTree = {}
#     retTree['spInd'] = feat
#     retTree['spVal'] = val
#     lSet, rSet = binSplitDataSet(dataSet, feat, val)
#     retTree['left'] = createTree(lSet, leafType, errType, ops)
#     retTree['right'] = createTree(rSet, leafType, errType, ops)
#     return retTree



if __name__ == "__main__":
    testMat = mat(eye(4))
    print binSplitDataSet(testMat, 1, 0.5)
