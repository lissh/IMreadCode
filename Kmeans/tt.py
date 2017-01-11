__author__ = 'lish'
from numpy import *
from scipy.cluster.vq import vq, kmeans, whiten


dataSet = []
fileIn = open('test2.txt')
for line in fileIn.readlines():
    # print line.replace('\n','')
    # lineArr = line.strip().split(',')
    # dataSet.append([int(lineArr[0]), int(lineArr[1])])
    dataSet.append([int(line.replace('\n',''))])
# dataSet=mat(dataSet)
# features  = array([[ 1.9,2.3], [ 1.5,2.5],[ 0.8,0.6],[ 0.4,1.8],[ 0.1,0.1],[ 0.2,1.8], [ 2.0,0.5],[ 0.3,1.5], [ 1.0,1.0]])
whitened = whiten(dataSet)
# print whitened
book = array((whitened[0],whitened[1]))

print kmeans(whitened,book,2)
# (array([[ 2.3110306 ,  2.86287398],    # random
#        [ 0.93218041,  1.24398691]]), 0.85684700941625547)

dataSet=mat(dataSet)
codes = 2
print kmeans(dataSet,codes)
