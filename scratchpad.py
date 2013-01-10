
import ClassicalConditioningAnalysis as cc
import numpy as np
import matplotlib.pyplot as pyplot
import matplotlib as mpl

epre = [None]*4 
epre[0] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00051/f00051_2013-01-08-15-25-17.json')
epre[1] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00052/f00052_2013-01-08-15-25-19.json')
epre[2] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00053/f00053_2013-01-08-15-25-21.json')
epre[3] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00054/f00054_2013-01-08-15-25-24.json')
epost = [None]*4
epost[0] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00051/f00051_2013-01-08-16-52-01.json')
epost[1] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00052/f00052_2013-01-08-16-51-58.json')
epost[2] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00053/f00053_2013-01-08-16-51-56.json')
epost[3] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00054/f00054_2013-01-08-16-51-54.json')
apost = [None]*4
apost[0] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00051/f00051_2013-01-08-17-21-31.json')
apost[1] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00052/f00052_2013-01-08-17-21-28.json')
apost[2] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00053/f00053_2013-01-08-17-21-26.json')
apost[3] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00054/f00054_2013-01-08-17-21-24.json')


cpre = [None]*4 
cpre[0] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00046/f00046_2013-01-08-17-58-26.json')
cpre[1] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00047/f00047_2013-01-08-17-58-24.json')
cpre[2] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00048/f00048_2013-01-08-17-58-22.json')
cpre[3] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00049/f00049_2013-01-08-17-58-20.json')
cpost = [None]*4
cpost[0] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00046/f00046_2013-01-08-19-22-26.json')
cpost[1] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00047/f00047_2013-01-08-19-22-27.json')
cpost[2] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00048/f00048_2013-01-08-19-22-30.json')
cpost[3] = cc.loadDataFromFile('/home/vburns/data/2013-01-08/f00049/f00049_2013-01-08-19-22-32.json')

#clean up the tracking

t = epre[0]['warpedTracking']
t = t[t[:,1]<77,:]
t = t[np.logical_or(t[:,1]<74.05, t[:,1]>74.4),:]
t = t[np.logical_and(t[:,0]>0+t[0,0], t[:,0]<600+t[0,0]),:]
epre[0]['warpedTracking'] = t

t = epre[1]['warpedTracking']
t = t[np.logical_and(t[:,0]>0+t[0,0], t[:,0]<600+t[0,0]),:]
epre[1]['warpedTracking'] = t

t = epre[2]['warpedTracking']
t = t[t[:,1]<77.2,:]
t = t[np.logical_and(t[:,0]>0+t[0,0], t[:,0]<600+t[0,0]),:]
epre[2]['warpedTracking'] = t

t = epre[3]['warpedTracking']
t = t[np.logical_or(t[:,1]<21.9, t[:,1]>22.05),:]
t = t[np.logical_and(t[:,0]>0+t[0,0], t[:,0]<600+t[0,0]),:]
epre[3]['warpedTracking'] = t

t = epost[0]['warpedTracking']
t = t[np.logical_or(t[:,1]<29.5, t[:,1]>30.5),:]
epost[0]['warpedTracking'] = t

t = epost[1]['warpedTracking']
t = t[np.logical_and(t[:,0]>215+t[0,0], t[:,0]<610+t[0,0]),:]
epost[1]['warpedTracking'] = t

t = epost[2]['warpedTracking']
t = t[np.logical_or(t[:,1]<56.5, t[:,1]>57.5),:]
t = t[np.logical_or(t[:,1]<22.7, t[:,1]>23.5),:]
epost[2]['warpedTracking'] = t

t = epost[3]['warpedTracking']
t = t[np.logical_or(t[:,1]<56, t[:,1]>57),:]
epost[3]['warpedTracking'] = t



t = cpre[0]['warpedTracking']
t = t[np.logical_or(t[:,1]<70.5, t[:,1]>72),:]
t = t[np.logical_or(t[:,1]<27.5, t[:,1]>30),:]
t = t[np.logical_and(t[:,0]>0+t[0,0], t[:,0]<1000+t[0,0]),:]
cpre[0]['warpedTracking'] = t

t = cpre[1]['warpedTracking']
t = t[np.logical_and(t[:,0]>0+t[0,0], t[:,0]<1000+t[0,0]),:]
cpre[1]['warpedTracking'] = t

t = cpre[2]['warpedTracking']
t = t[np.logical_and(t[:,0]>0+t[0,0], t[:,0]<1000+t[0,0]),:]
cpre[2]['warpedTracking'] = t

t = cpre[3]['warpedTracking']
t = t[np.logical_or(t[:,1]<43, t[:,1]>44),:]
t = t[np.logical_or(t[:,1]<56.6, t[:,1]>57),:]
t = t[np.logical_and(t[:,0]>0+t[0,0], t[:,0]<1000+t[0,0]),:]
cpre[3]['warpedTracking'] = t

t = cpost[0]['warpedTracking']
t = t[np.logical_or(t[:,1]<26, t[:,1]>29),:]
cpost[0]['warpedTracking'] = t

t = cpost[1]['warpedTracking']
t = t[np.logical_or(t[:,1]<61.8, t[:,1]>62.4),:]
t = t[np.logical_or(t[:,1]<70.8, t[:,1]>71.3),:]
t = t[np.logical_or(t[:,1]<72, t[:,1]>72.4),:]
cpost[1]['warpedTracking'] = t

t = cpost[2]['warpedTracking']
cpost[2]['warpedTracking'] = t

t = cpost[3]['warpedTracking']
t = t[np.logical_or(t[:,1]<42, t[:,1]>44),:]
t = t[np.logical_or(t[:,1]<31.5, t[:,1]>33),:]
cpost[3]['warpedTracking'] = t

data = [epre,epost,cpre,cpost]

#compute total path length in first 5 minutes
meanv = np.zeros((len(data),max([len(x) for x in data])))
medv = np.zeros((len(data),len(epre)))
avel = [[None]*4]*4
for d in range(len(data)):
    for n in range(len(data[d])):
        t = data[d][n]['warpedTracking']
        seglen = np.sqrt(pow(np.diff(t[:,1]),2) + pow(np.diff(t[:,2]),2))
        segdur = np.diff(t[:,0])
        vel = seglen / segdur
        avel[d][n] = vel
        meanv[d,n] = np.mean(vel)
        medv[d,n] = np.median(vel)

pyplot.plot([0,1],medv[0:2,:],'r');
pyplot.plot([0,1],medv[2:4,:],'b'); 
pyplot.xlim([-0.5,1.5]);
pyplot.ylabel('Median Velocity (mm/s)') 
pyplot.show()

"""
import ClassicalConditioningAnalysis as cc


#load the data
d_pre = list(range(4))
d_pre[0] = cc.loadData('/home/vburns/data/2012-12-06/120612_HuC_f1')
d_pre[1] = cc.loadData('/home/vburns/data/2012-12-06/120612_HuC_f2')
d_pre[2] = cc.loadData('/home/vburns/data/2012-12-06/120612_HuC_f3')
d_pre[3] = cc.loadData('/home/vburns/data/2012-12-06/120612_HuC_f4')
d_post = list(range(4))
d_post[0] = cc.loadData('/home/vburns/data/2012-12-06/120612_HuC_f1 post')
d_post[1] = cc.loadData('/home/vburns/data/2012-12-06/120612_HuC_f2 post')
d_post[2] = cc.loadData('/home/vburns/data/2012-12-06/120612_HuC_f3 post')
d_post[3] = cc.loadData('/home/vburns/data/2012-12-06/120612_HuC_f4 post')


import numpy as np
import matplotlib.pyplot as pyplot
import matplotlib as mpl

#extract % on red
d_pre_red = []
d_post_red = []
d_pre_s1 = []
d_post_s1 = []
for nF in range(len(d_pre)):
    [cr,s1,d] = cc.getSidePreference(d_pre[nF],cond=3,color='Red')
    d_pre_red.append(np.array(cr) / np.array(d))
    d_pre_s1.append(np.array(s1) / np.array(d))
    [cr,s1,d] = cc.getSidePreference(d_post[nF], cond=8, color='Red')
    d_post_red.append(np.array(cr) / np.array(d))
    d_post_s1.append(np.array(s1) / np.array(d))

# plot avg for fish
pyplot.figure(1)
pyplot.clf()
pyplot.hold(True)
for nF in range(len(d_pre)):
    pyplot.plot([0,1],[np.mean(d_pre_red[nF]),np.mean(d_post_red[nF])])
pyplot.legend(['1','2','3','4'])
pyplot.show()

    
# plot individual switches
pyplot.figure(2)
pyplot.hold(True)
for nF in [3]:
    pyplot.plot(np.hstack([np.zeros(len(d_pre_red[nF])),np.ones(len(d_post_red[nF]))]),
                np.hstack([d_pre_red[nF], d_post_red[nF]]), 'o')
pyplot.legend(['1','2','3','4'])
pyplot.xlim([-1,2])
pyplot.show()
"""
