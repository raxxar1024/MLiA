# !/usr/bin/python
# -*- coding=utf-8 -*-
from numpy import *
import matplotlib.pyplot as plt


def loadDataSet(fileName):
    numFeat = len(open(fileName).readline().split('\t')) - 1
    dataMat, labelMat = [], []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat, labelMat


def standRegres(xArr, yArr):
    xMat = mat(xArr)
    yMat = mat(yArr).T
    xTx = xMat.T * xMat
    if linalg.det(xTx) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = xTx.I * (xMat.T * yMat)
    return ws


def lwlr(testPoint, xArr, yArr, k=1.0):
    xMat, yMat = mat(xArr), mat(yArr).T
    m = shape(xMat)[0]
    weights = mat(eye((m)))
    # 创建对角矩阵
    for j in range(m):
        # 权重值大小以指数级衰减
        diffMat = testPoint - xMat[j, :]
        weights[j, j] = exp(diffMat * diffMat.T / (-2.0 * k ** 2))
    xTx = xMat.T * (weights * xMat)
    if linalg.det(xTx) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = xTx.I * (xMat.T * (weights * yMat))
    return testPoint * ws


def lwlrTest(testArr, xArr, yArr, k=1.0):
    m = shape(testArr)[0]
    yHat = zeros(m)
    for i in range(m):
        yHat[i] = lwlr(testArr[i], xArr, yArr, k)
    return yHat


def rssError(yArr, yHatArr):
    return ((yArr - yHatArr) ** 2).sum()


def ridgeRegres(xMat, yMat, lam=0.2):
    xTx = xMat.T * xMat
    denom = xTx + eye(shape(xMat)[1]) * lam
    if linalg.det(denom) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = denom.I * (xMat.T * yMat)
    return ws


def ridgeTest(xArr, yArr):
    xMat, yMat = mat(xArr), mat(yArr).T
    yMean = mean(yMat, 0)
    # 数据标准化
    yMat = yMat - yMean
    xMeans = mean(xMat, 0)
    xVar = var(xMat, 0)
    xMat = (xMat - xMeans) / xVar
    numTestPts = 30
    wMat = zeros((numTestPts, shape(xMat)[1]))
    for i in range(numTestPts):
        ws = ridgeRegres(xMat, yMat, exp(i - 10))
        wMat[i, :] = ws.T
    return wMat


def regularize(xMat):  # regularize by columns
    inMat = xMat.copy()
    inMeans = mean(inMat, 0)  # calc mean then subtract it off
    inVar = var(inMat, 0)  # calc variance of Xi then divide by it
    inMat = (inMat - inMeans) / inVar
    return inMat


def stageWise(xArr, yArr, eps=0.01, numIt=100):
    xMat, yMat = mat(xArr), mat(yArr).T
    yMean = mean(yMat, 0)
    yMat = yMat - yMean
    xMat = regularize(xMat)
    m, n = shape(xMat)
    returnMat = zeros((numIt, 0))
    ws = zeros((n, 1))
    wsTest = ws.copy()
    wsMax = ws.copy()
    for i in range(numIt):
        print ws.T
        lowestError = inf
        for j in range(n):
            for sign in [-1, 1]:
                wsTest = ws.copy()
                wsTest[j] += eps * sign
                yTest = xMat * wsTest
                rssE = rssError(yMat.A, yTest.A)
                if rssE < lowestError:
                    lowestError = rssE
                    wsMax = wsTest
        ws = wsMax.copy()
        # returnMat[i, :] = ws.T
        # return returnMat


from bs4 import BeautifulSoup as bs
import re


def searchForSet(retX, retY, setNum, yr, numPce, origPrc):
    file_handle = open("lego/lego%d.html" % setNum, "r")
    html_content = "\n".join(file.readlines(file_handle))
    file_handle.close()
    lst_search_result = bs(html_content, "lxml").find_all(class_="li")

    for i in range(len(lst_search_result)):
        try:
            if lst_search_result[i].find_all(class_="vip", text=re.compile(r'new|nisb', re.I)):
                newFlag = 1.0
            else:
                newFlag = 0.0
            sellingPrice = 0.0
            for string in lst_search_result[i].find(class_="prc").stripped_strings:
                if "$" in string:
                    string = "".join(string.split(","))
                    sellingPrice = float(string[1:])
            if sellingPrice > origPrc * 0.5:
                # 过滤掉不完整的套装
                print "%d\t%d\t%d\t%f\t%f" % (yr, numPce, newFlag, origPrc, sellingPrice)
                retX.append([yr, numPce, newFlag, origPrc])
                retY.append(sellingPrice)
        except:
            print "problem with item %d" % i


def setDataCollect(retX, retY):
    searchForSet(retX, retY, 8288, 2006, 800, 49.99)
    searchForSet(retX, retY, 10030, 2002, 3096, 269.99)
    searchForSet(retX, retY, 10179, 2007, 5195, 499.99)
    searchForSet(retX, retY, 10181, 2007, 3428, 199.99)
    searchForSet(retX, retY, 10189, 2008, 5922, 299.99)
    searchForSet(retX, retY, 10196, 2009, 3263, 249.99)
    print retX, retY


if __name__ == "__main__":
    # xArr, yArr = loadDataSet('ex0.txt')
    # ws = standRegres(xArr, yArr)
    # xMat, yMat = mat(xArr), mat(yArr)
    # yHat = xMat * ws
    #
    # fig = plt.figure()
    # print "break here in case no tk ..."
    # ax = fig.add_subplot(111)
    # ax.scatter(xMat[:, 1].flatten().A[0], yMat.T[:, 0].flatten().A[0])
    #
    # xCopy = xMat.copy()
    # xCopy.sort(0)
    # yHat = xCopy * ws
    # ax.plot(xCopy[:, 1], yHat)
    # print "wait..."

    # abX, abY = loadDataSet("abalone.txt")
    # yHat01 = lwlrTest(abX[0:99], abX[0:99], abY[0:99], 0.1)
    # yHat1 = lwlrTest(abX[0:99], abX[0:99], abY[0:99], 1)
    # yHat10 = lwlrTest(abX[0:99], abX[0:99], abY[0:99], 10)
    # print rssError(abY[0:99], yHat01.T), \
    #     rssError(abY[0:99], yHat1.T), \
    #     rssError(abY[0:99], yHat10.T)
    #
    # yHat01 = lwlrTest(abX[100:199], abX[0:99], abY[0:99], 0.1)
    # yHat1 = lwlrTest(abX[100:199], abX[0:99], abY[0:99], 1)
    # yHat10 = lwlrTest(abX[100:199], abX[0:99], abY[0:99], 10)
    # print rssError(abY[100:199], yHat01.T), \
    #     rssError(abY[100:199], yHat1.T), \
    #     rssError(abY[100:199], yHat10.T)
    #
    # ws = standRegres(abX[0:99], abY[0:99])
    # yHat = mat(abX[100:199]) * ws
    # print rssError(abY[100:199], yHat.T.A)

    # abX, abY = loadDataSet("abalone.txt")
    # ridgeWeights = ridgeTest(abX, abY)
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(ridgeWeights)
    # plt.show()

    # xArr, yArr = loadDataSet("abalone.txt")
    # print stageWise(xArr, yArr, 0.01, 200)
    # print stageWise(xArr, yArr, 0.001, 5000)
    # xMat = mat(xArr)
    # yMat = mat(yArr).T
    # xMat = regularize(xMat)
    # yM = mean(yMat, 0)
    # yMat = yMat - yM
    # weights = standRegres(xMat, yMat.T)
    # print weights.T

    lgX, lgY = [], []
    setDataCollect(lgX, lgY)
