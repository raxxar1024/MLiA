# !/usr/bin/python
# -*- coding=utf-8 -*-

from numpy import *
from numpy import linalg as la


def loadExData():
    return [
        [0, 0, 0, 2, 2],
        [0, 0, 0, 3, 3],
        [0, 0, 0, 1, 1],
        [1, 1, 1, 0, 0],
        [2, 2, 2, 0, 0],
        [5, 5, 5, 0, 0],
        [1, 1, 1, 0, 0]
    ]


def loadExData2():
    return [
        [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
        [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
        [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
        [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
        [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
        [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
        [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
        [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
        [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
        [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]
    ]


def ecludSim(inA, inB):
    return 1.0 / (1.0 + la.norm(inA - inB))


def pearsSim(inA, inB):
    if len(inA) < 3:
        return 1.0
    return 0.5 + 0.5 * corrcoef(inA, inB, rowvar=0)[0][1]


def cosSim(inA, inB):
    num = float(inA.T * inB)
    denom = la.norm(inA) * la.norm(inB)
    return 0.5 + 0.5 * (num / denom)


def standEst(dataMat, user, simMeas, item):
    n = shape(dataMat)[1]
    simTotal = 0.0
    ratSimTotal = 0.0
    for j in range(n):
        userRating = dataMat[user, j]
        if userRating == 0:
            continue
        overlap = nonzero(logical_and(dataMat[:, item].A > 0, dataMat[:, j].A > 0))[0]
        if len(overlap) == 0:
            similarity = 0
        else:
            similarity = simMeas(dataMat[overlap, item], dataMat[overlap, j])
        # print 'the %d and %d similarty is: %f' % (item, j, similarity)
        simTotal += similarity
        ratSimTotal += similarity * userRating
    if simTotal == 0:
        return 0
    else:
        return ratSimTotal / simTotal


def svdEst(dataMat, user, simMeas, item):
    n = shape(dataMat)[1]
    simTotal = 0.0
    ratSimTotal = 0.0
    U, Sigma, VT = la.svd(dataMat)
    Sig4 = mat(eye(4) * Sigma[:4])
    xformedItems = dataMat.T * U[:, : 4] * Sig4.I
    for j in range(n):
        userRating = dataMat[user, j]
        if userRating == 0 or j == item:
            continue
        similarity = simMeas(xformedItems[item, :].T, xformedItems[j, :].T)
        print 'the %d and %d similarity is: %f' % (item, j, similarity)
        simTotal += similarity
        ratSimTotal += similarity * userRating
    if simTotal == 0:
        return 0
    else:
        return ratSimTotal / simTotal


def recommend(dataMat, user, N=3, simMeas=cosSim, estMethod=standEst):
    unratedItems = nonzero(dataMat[user, :].A == 0)[1]
    if len(unratedItems) == 0:
        return 'you rated everything'
    itemScores = []
    for item in unratedItems:
        estimatedScore = estMethod(dataMat, user, simMeas, item)
        itemScores.append((item, estimatedScore))
    return sorted(itemScores, key=lambda jj: jj[1], reverse=True)[:N]


def printMat(inMat, thresh=0.8):
    for i in range(32):
        for k in range(32):
            if float(inMat[i, k]) > thresh:
                print 1
            else:
                print 0
        print ''
        

if __name__ == "__main__":
    # Data = loadExData()
    # U, Sigma, VT = linalg.svd(Data)
    # print Sigma
    # Sig3 = mat([[Sigma[0], 0, 0], [0, Sigma[1], 0], [0, 0, Sigma[2]]])
    # print U[:, : 3] * Sig3 * VT[: 3, :]

    # myMat = mat(loadExData())
    # print euclidSim(myMat[:, 0], myMat[:, 4])
    # print euclidSim(myMat[:, 0], myMat[:, 0])
    # print cosSim(myMat[:, 0], myMat[:, 4])
    # print cosSim(myMat[:, 0], myMat[:, 0])
    # print pearsSim(myMat[:, 0], myMat[:, 4])
    # print pearsSim(myMat[:, 0], myMat[:, 0])

    # myMat = mat(loadExData())
    # myMat[0, 1] = myMat[0, 0] = myMat[1, 0] = myMat[2, 0] = 4
    # myMat[3, 3] = 2
    # print myMat
    # print recommend(myMat, 2)
    # print recommend(myMat, 2, simMeas=ecludSim)
    # print recommend(myMat, 2, simMeas=pearsSim)

    # U, Sigma, VT = linalg.svd(loadExData2())
    # print Sigma
    # Sig2 = Sigma ** 2
    # print "sum of sig2 is %d, 90%% is %d" % (sum(Sig2), sum(Sig2) * 0.9)
    # print "first 2 is %d" % sum(Sig2[:2])
    # print "first 3 is %d" % sum(Sig2[:3])
    # Sig3 = mat([[Sigma[0], 0, 0], [0, Sigma[1], 0], [0, 0, Sigma[2]]])
    # print U[:, : 3] * Sig3 * VT[: 3, :]

    myMat = mat(loadExData2())
    print recommend(myMat, 1, estMethod=svdEst)
    print recommend(myMat, 1, estMethod=svdEst, simMeas=pearsSim)
