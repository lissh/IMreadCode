from numpy import *
import os,kmean
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
base_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
print base_path
## step 1: load data  
print "step 1: load data..."
dataSet = []
fileIn = open(base_path + '/test.txt')
for line in fileIn.readlines():
    # print line.replace('\n','') 
    # lineArr = line.strip().split(',')
    # dataSet.append([int(lineArr[0]), int(lineArr[1])])
    dataSet.append([int(line.replace('\n',''))])
# print dataSet
## step 2: clustering...  
print "step 2: clustering..."
dataSet = mat(dataSet)
# print dataSet 
k = 2
centroids, clusterAssment = kmean.kmeans(dataSet, k)

print centroids

## step 3: show the result  
print "step 3: show the result..."
kmean.showCluster(dataSet, k, centroids, clusterAssment) 