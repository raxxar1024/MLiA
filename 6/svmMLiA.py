# !/usr/bin/python
# -*- coding=utf-8 -*-
from math import *
from numpy import *


def loadDataSet(filename):
    dataMat, labelMat = [], []
    fr = open(filename)
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat


if __name__ == "__main__":
    print 1
	
