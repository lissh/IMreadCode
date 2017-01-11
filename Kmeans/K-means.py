#!--encoding=utf-8

from __future__ import print_function
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MiniBatchKMeans
import sys,os

reload(sys)
sys.setdefaultencoding('utf-8')
base_path = os.path.split(os.path.realpath(sys.argv[0]))[0]

def loadDataset():
    '''导入文本数据集'''
    f = open(base_path+'/36krout','r')
    dataset = []
    lastPage = None
    for line in f.readlines():
        print  (line)
        if '< title >' in line and '< / title >' in line:
            if lastPage:
                dataset.append(lastPage)
            lastPage = line
        else:
            lastPage += line
    if lastPage:
        dataset.append(lastPage)
    f.close()
    return dataset

def transform(dataset,n_features=1000):
    vectorizer = TfidfVectorizer(max_df=0.5, max_features=n_features, min_df=2,use_idf=True)
    X = vectorizer.fit_transform(dataset)
    return X,vectorizer

def train(X,vectorizer,true_k=10,minibatch = False,showLable = False):
    #使用采样数据还是原始数据训练k-means，
    if minibatch:
        km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=1,
                             init_size=1000, batch_size=1000, verbose=False)
    else:
        km = KMeans(n_clusters=true_k, init='k-means++', max_iter=300, n_init=1,
                    verbose=False)
    km.fit(X)
    if showLable:
        print("Top terms per cluster:")
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()
        print (vectorizer.get_stop_words())
        for i in range(true_k):
            print("Cluster %d:" % i, end='')
            for ind in order_centroids[i, :10]:
                print(' %s' % terms[ind], end='')
            print()
    result = list(km.predict(X))
    print ('Cluster distribution:')
    print (dict([(i, result.count(i)) for i in result]))
    return -km.score(X)

def test():
    '''测试选择最优参数'''
    dataset = loadDataset()
    print("%d documents" % len(dataset))
    X,vectorizer = transform(dataset,n_features=500)
    true_ks = []
    scores = []
    for i in xrange(3,80,1):
        score = train(X,vectorizer,true_k=i)/len(dataset)
        print (i,score)
        true_ks.append(i)
        scores.append(score)
    plt.figure(figsize=(8,4))
    plt.plot(true_ks,scores,label="error",color="red",linewidth=1)
    plt.xlabel("n_features")
    plt.ylabel("error")
    plt.legend()
    plt.show()

def out():
    '''在最优参数下输出聚类结果'''
    dataset = loadDataset()
    X,vectorizer = transform(dataset,n_features=500)
    score = train(X,vectorizer,true_k=10,showLable=True)/len(dataset)
    print (score)
#test()
out()