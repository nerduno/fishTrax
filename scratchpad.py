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

