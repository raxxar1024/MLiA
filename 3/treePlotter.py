# !/usr/bin/python
# -*- coding=utf-8 -*-
from pylab import *
import matplotlib.pyplot as plt

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords="axes fraction", xytext=centerPt,
                            textcoords="axes fraction", va="center", ha="center",
                            bbox=nodeType, arrowprops=arrow_args)


def createPlot():
    print u"决策节点"
    fig = plt.figure(1, facecolor="white")
    fig.clf()
    createPlot.ax1 = plt.subplot(111, frameon=False)
    plotNode(u"决策节点", (0.5, 0.1), (0.1, 0.5), decisionNode)
    plotNode(u"叶子节点", (0.8, 0.1), (0.3, 0.8), leafNode)
    plt.show()


if __name__ == "__main__":
    createPlot()
