
import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy
import os

e_safe5_first= aba.loadDataFromFile(os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00438/f00438_2013-05-16-14-13-03.json'))
e_shock5 = aba.loadDataFromFile(os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00438/f00438_2013-05-16-14-44-45.json'))
e_safe5_sec = aba.loadDataFromFile(os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00438/f00438_2013-05-16-15-39-01.json'))

e_safe_same=aba.loadDataFromFile(os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00411/f00411_2013-05-07-14-15-17.json')) #,bAcqArenaPoly=True)
e_shock_same = aba.loadDataFromFile(os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00411/f00411_2013-05-07-14-46-43.json'))
e_safe_same_sec = aba.loadDataFromFile(os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00411/f00411_2013-05-07-15-40-02.json'))

mpl.rcParams.update({'font.size': 18})
def plotFishpathandTraces(dataArr, colorArr):
    fig = pyplot.figure(1,figsize=(11,7))
    for i in range(2):
        if i==0:
            for k in range(3):
                ax =pyplot.subplot(4,3,k+1)   
                aba.plotFishPath(dataArr[k], color=colorArr[k], smoothWinLen=5)
        #pyplot.title('Fish Path in Tank')
                pyplot.xlabel('46 mm')
                pyplot.ylabel('22 mm')
                ax.set_xticks([20,40])
                ax.set_yticks([10,20])
                ax2=pyplot.subplot(4,3,k+4)
                aba.plotFishXPosition(dataArr[k],fmt=colorArr[k],smooth=5)
                ax2.set_yticks([20,40])
                pyplot.ylabel('x position')
                if k ==1:
                    patch5 = mpl.patches.Rectangle((900,0), 1844, 50, color=[1,.5,.5], fill=True)
                    pyplot.gca().add_patch(patch5)
                    
        if i==1:
            for k in range(3):
                ax =pyplot.subplot(4,3,i+k+6)   
                aba.plotFishPath(dataArr[k+i+2], color=colorArr[k+i+2], smoothWinLen=5)
        #pyplot.title('Fish Path in Tank')
                pyplot.xlabel('46 mm')
                pyplot.ylabel('22 mm')
                ax.set_xticks([20,40])
                ax.set_yticks([10,20])
                ax2=pyplot.subplot(4,3,i+k+9)
                aba.plotFishXPosition(dataArr[k+i+2],fmt=colorArr[k+i+2],smooth=5)
                pyplot.ylabel('x position')
                ax2.set_yticks([20,40])
                if k ==1:
                    patch5 = mpl.patches.Rectangle((900,0), 1844, 50, color=[1,.5,.5], fill=True)
                    pyplot.gca().add_patch(patch5)
        #pyplot.title('Fish Y Position')

plotFishpathandTraces([e_safe_same, e_shock_same, e_safe_same_sec,e_safe5_first, e_shock5, e_safe5_sec],['b','b','b','b','b','b'])

pyplot.gcf()
pyplot.subplot(432).clear()
aba.plotFishPath(e_shock5,trange=[0,900], color='b', smoothWinLen=5)
#aba.plotFishPath(e_shock5,trange=[900,2744], color=[1,.5,.5], smoothWinLen=5)
aba.plotFishPath(e_shock5,trange=[2744,3105], color='r', smoothWinLen=5)
pyplot.gcf()
pyplot.subplot(438).clear()
aba.plotFishPath(e_shock_same,trange=[0,900], color='b', smoothWinLen=5)
#aba.plotFishPath(e_shock5,trange=[900,2744], color=[1,.5,.5], smoothWinLen=5)
aba.plotFishPath(e_shock_same,trange=[2744,3105], color='r', smoothWinLen=5)

b = [False, False, False, False, False, False, False, False, False, True, False, False]
for i in range(len(b)):
    if not b[i]:
        ax=pyplot.subplot(4,3,i+1)
        ax.set_xticks([])
        ax.set_yticks([])
        pyplot.ylabel('')
        pyplot.xlabel('')
ax=pyplot.subplot(4,3,4)
pyplot.ylabel('x position')
ax.set_yticks([20,40])
ax=pyplot.subplot(4,3,11)
pyplot.xlabel('Time (s)')
ax.set_xticks([0,1000,2000,3000])
ax=pyplot.subplot(4,3,12)
pyplot.xlabel('Time (s)')
ax.set_xticks([0,500,1000,1500])
        

pylab.show()

