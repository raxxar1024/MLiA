# !/usr/bin/python
# -*- coding=utf-8 -*-

from numpy import *


def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    datArr = [map(float, line) for line in stringArr]
    return mat(datArr)


if __name__ == "__main__":
    dataMat = loadDataSet('testSet.txt')
