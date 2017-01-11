# -*- coding:utf-8 -*-
__author__ = 'lish'
import random
from scipy import stats
import run,time
import matplotlib.pyplot as plt
import numpy as np


class RunFrequency(object):

    def __init__(self,_tasknum,_runtime,_featurs):
        self.tasknum=_tasknum
        self.runtime=_runtime
        self.featurs=_featurs

    def runtask(self):
        """
            probabilitydict:概率分布字典
            tasknum:任务执行的总次数
            runtime:执行单次任务所需时间
            注:参数的时间单位都必须统一转化为秒
        """
        probabilitydict=self.probabilitydict
        tasknum=self.tasknum
        runtime=self.runtime
        #将毫秒转化为秒
        runtime=float(runtime)/1000
        currenttime=time.strftime('%H',time.localtime())
        diffprobability=probabilitydict[currenttime]
        runnum=int(diffprobability*tasknum)
        # print runnum
        totaltime=3600
        runtotaltime=runnum*runtime
        if runtotaltime<totaltime:
            freetotaltime=totaltime-runtotaltime
            #通过泊松分布生成runmun的列表，且由其特性，所有元素即概率值之和唯一，随机分布休息时间。该分布多运用与排队论等问题，故让脚本运行的休眠时间满足泊松分使得数据更真实
            n=np.arange(1,runnum+1)
            rate=random.randint(1,runnum+1)
            freetimePvalues=stats.poisson.pmf(n,rate)
            runcont=0
            # print runnum
            while runcont<runnum:
                freetime=int(freetimePvalues[runcont]*freetotaltime)
                time.sleep(freetime)
                run.runtest(runtime)
                runcont+=1
        else:
            print '任务执行时间过长，无法在指定的时间区间内完成指定次数任务'


    def multiNormalDistribution(self):
        """ mu : 这里我们用来确定波峰的位置。
                 μ是正态分布的位置参数，描述正态分布的集中趋势位置.概率规律为取与μ邻近的值的概率大，而取离μ越远的值的概率越小。
            sigma:这里我们用来确定波的坡度，即是否平缓，是否陡峭。
                 σ描述正态分布资料数据分布的离散程度，σ越大，数据分布越分散，σ越小，数据分布越集中。也称为是正态分布的形状参数，σ越大，曲线越扁平，反之，σ越小，曲线越瘦高。
            xsection：这里是时间的区间，单位可以是S,M,.
                 正态分布资料数据自变量的取值区间
        """
        featurs=self.featurs
        Yvalues=[]
        Xvalues=[]
        for featur in featurs:
            mu=featur['mu']
            sigma=featur['sigma']
            xsection=featur['section']

            xvalues=np.arange(xsection['lower'],xsection['upper'])
            if Yvalues!=[]:
                Xvalues=np.concatenate((Xvalues,xvalues))
            else:
                Xvalues=xvalues

            yvalues=stats.norm.pdf(xvalues,mu,sigma)
            #加上随机浮动值，我们这里是取矩阵元素的最大值的1%，作为概率浮动值
            randomsectionvalue=max(yvalues)*0.01
            randomvalue=random.uniform(-randomsectionvalue,randomsectionvalue)
            yvalues=yvalues+randomvalue
            if Yvalues!=[]:
                Yvalues=np.concatenate((Yvalues,yvalues))
            else:
                Yvalues=yvalues

        #标准化概率值，即将生产的概率矩阵标准化为，所有元素值之和为1
        TotalProbability=0
        for Yvalue in Yvalues:
            TotalProbability+=float(Yvalue)
        Ystandvalue=Yvalues/TotalProbability

        self.Xvalues=Xvalues
        self.Ystandvalue=Ystandvalue

        _probabilitydict={}
        i=0
        while i<len(Xvalues):
            _probabilitydict=dict(_probabilitydict, **{str(Xvalues[i]):Yvalues[i]})
            i+=1
        self.probabilitydict=_probabilitydict

    def Drawchart(self):
        Xvalues=self.Xvalues
        Ystandvalue=self.Ystandvalue

        plt.plot(Xvalues,Ystandvalue,'r',Xvalues,Ystandvalue,'bo')
        plt.xticks(np.arange(min(Xvalues),max(Xvalues)+1))
        plt.xlabel('Time(Units of measurement: h )')
        plt.title('Multi Poisson Random Variable')
        plt.show()

if __name__ == '__main__':
    featurs=[{'mu':-4,'section':{'lower':0,'upper':4},'sigma':9},{'mu':13,'section':{'lower':4,'upper':17},'sigma':9},{'mu':22,'section':{'lower':17,'upper':25},'sigma':8}]
    tasknum=10000
    runtime=3000
    app=RunFrequency(tasknum,runtime,featurs)
    app.multiNormalDistribution()
    # app.runtask()
    app.Drawchart()








