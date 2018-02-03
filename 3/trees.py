from math import log


def clacShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}

    for feaVec in dataSet:
        currentLabel = feaVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1

    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)

    return shannonEnt


def createDataSet():
    dataSet = [
        [1, 1, 'yes'],
        [1, 1, 'yes'],
        [1, 0, 'no'],
        [0, 1, 'no'],
        [0, 1, 'no']
    ]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels


if __name__ == "__main__":
    myDat, labels = createDataSet()
    print clacShannonEnt(myDat)
