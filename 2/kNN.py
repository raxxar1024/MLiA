from os import listdir
import operator
from numpy import *


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in xrange(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def file2matrix(filename):
    fr = open(filename)
    arrayOlines = fr.readlines()
    numberOfLines = len(arrayOlines)
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []

    index = 0
    for line in arrayOlines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelVector.append((listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet / tile(ranges, (m, 1))
    return normDataSet, ranges, minVals


def datingClassTest():
    hoRatio = 0.50
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :],
                                     datingLabels[numTestVecs:m], 3)
        print "the classifier came back with: %s, the real answer is: %s" % (
            classifierResult, datingLabels[i]
        )
        if classifierResult != datingLabels[i]:
            errorCount += 1.0
    print "the total error rate is: %f" % (errorCount / float(numTestVecs))


def img2vector(filename):
    returnVector = zeros((1, 1024))
    fr = open(filename)
    for i in xrange(32):
        lineStr = fr.readline()
        for j in xrange(32):
            returnVector[0, 32 * i + j] = int(lineStr[j])
    return returnVector


def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')

    m = len(trainingFileList)
    trainingMat = zeros((m, 1024))
    for i in xrange(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split(".")[0]

        classNumStr = int(fileStr.split("_")[0])
        hwLabels.append(classNumStr)
        trainingMat[i, :] = img2vector("trainingDigits/%s" % fileNameStr)

    testFileList = listdir('testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in xrange(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split(".")[0]
        classNumStr = int(fileStr.split("_")[0])
        vectorUnderTest = img2vector("testDigits/%s" % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print "test %d, the classifier came back with: %d, the real answer is: %d" % (i, classifierResult, classNumStr)
        if classifierResult != classNumStr:
            errorCount += 1
    print "the total number of errors is: %d " % errorCount
    print "the total error rate is: %f" % (errorCount / float(mTest))


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # group, labels = createDataSet()
    # classify0([0, 0], group, labels, 3)

    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:, 1], datingDataMat[:, 2])
    # ax.scatter(datingDataMat[:, 1], datingDataMat[:, 2], 15.0 * array(datingLabels), 15.0 * array(datingLabels))
    plt.show()

    # normMat, ranges, minVals = autoNorm(datingDataMat)
    # print normMat

    # datingClassTest()

    # testVector = img2vector("testDigits/0_13.txt")
    # print testVector[0, 0:31]
    # print testVector[0, 32:63]

    # handwritingClassTest()
