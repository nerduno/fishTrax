import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np

e_fish_red = ['/home/vburns/Dropbox/ConchisData/2012-12-12/120612_HuC_f1/120612_HuC_f1_2012-12-12-15-31-39.json',
 '/home/vburns/Dropbox/ConchisData/2012-12-12/120612_HuC_f2/120612_HuC_f2_2012-12-12-15-31-32.json',]
e_fish_red = aba.loadMultipleDataFiles(e_fish_red)

e_fish_blue = ['/home/vburns/Dropbox/ConchisData/2012-12-12/120612_HuC_f3/120612_HuC_f3_2012-12-12-15-31-47.json',
'/home/vburns/Dropbox/ConchisData/2012-12-12/120612_HuC_f4/120612_HuC_f4_2012-12-12-15-31-52.json']
e_fish_blue = aba.loadMultipleDataFiles(e_fish_blue)

c_fish = ['/home/vburns/Dropbox/ConchisData/2013-01-16/f00084/f00084_2013-01-16-15-28-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-16/f00085/f00085_2013-01-16-15-28-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-16/f00086/f00086_2013-01-16-15-28-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-16/f00087/f00087_2013-01-16-15-28-06.json']
c_fish = aba.loadMultipleDataFiles(c_fish)

#assumes cocaine is on red
(e_frac_pr, e_dist_pr) = aba.getSidePreference_Multi(e_fish_red, cond = [3,3], refState ='Red')
(e_frac_pb, e_dist_pb) = aba.getSidePreference_Multi(e_fish_blue, cond = [3,3], refState ='Blue')
(e_frac_por, e_dist_por) = aba.getSidePreference_Multi(e_fish_red, cond = [8,8], refState ='Red')
(e_frac_pob, e_dist_pob) = aba.getSidePreference_Multi(e_fish_blue, cond = [8,8], refState ='Blue')
(c_frac_pre,c_dist_pre) = aba.getSidePreference_Multi(c_fish, cond = [3,3], refState = 'Red')
(c_frac_post,c_dist_post) = aba.getSidePreference_Multi(c_fish, cond = [8,8], refState = 'Red')

e_frac_pre = np.append(e_frac_pr, e_frac_pb, axis = 0)
e_frac_post = np.append(e_frac_por, e_frac_pob, axis =0)
e_dis_pre = np.append(e_dist_pr, e_dist_pb, axis = 0)
e_dis_post = np.append(e_dist_por, e_dist_pob, axis = 0)

import scipy
[tv, c_pre_mid] = scipy.stats.ttest_1samp(np.mean(c_frac_pre, axis = 1), 0.5)
[tv, c_post_mid] = scipy.stats.ttest_1samp(np.mean(c_frac_post, axis = 1), 0.5)
[tv, c_pre_post] = scipy.stats.ttest_1samp(np.mean(c_frac_pre, axis = 1) - np.mean(c_frac_post, axis = 1), 0)

[tv, e_pre_mid] = scipy.stats.ttest_1samp(np.mean(e_frac_pre, axis = 1), 0.5)
[tv, e_post_mid] = scipy.stats.ttest_1samp(np.mean(e_frac_post, axis = 1), 0.5)
[tv, e_pre_post] = scipy.stats.ttest_1samp(np.mean(e_frac_pre, axis = 1) - np.mean(e_frac_post, axis = 1), 0)

print 'experimental pre,post,prevspost: ', e_pre_mid, e_post_mid, e_pre_post
print 'control pre,post,prevspost: ', c_pre_mid, c_post_mid, c_pre_post

import pylab
pylab.figure(1)
pylab.clf()
pylab.suptitle('Clasical Conditioning Analysis')
ax = pylab.subplot(1,2,1)
pylab.plot([0,1],[np.mean(e_frac_pre, 1),np.mean(e_frac_post, 1)],'.-r')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylim((0,1))
pylab.ylabel('Percent Time on Shock Color (Experimental)')
pylab.hold(True)
pylab.errorbar([0,1],[np.mean(e_frac_pre),np.mean(e_frac_post)], yerr=2*scipy.stats.sem([np.mean(e_frac_pre,1),np.mean(e_frac_post,1)], axis = 1), capsize = 5, fmt = '.-k', linewidth = 3, markersize = 10)
pylab.axhline(.5,color='k',linestyle=':')
ax = pylab.subplot(1,2,2,sharey=ax)
pylab.plot([0,1],[np.mean(c_frac_pre, 1),np.mean(c_frac_post,1)],'.-b')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylim((0,1))
pylab.ylabel('Percent Time on Shock Color (Control)')
pylab.hold(True)
pylab.errorbar([0,1],[np.mean(c_frac_pre),np.mean(c_frac_post)], yerr=2*scipy.stats.sem([np.mean(c_frac_pre,1),np.mean(c_frac_post,1)], axis = 1), capsize = 5, fmt = '.-k', linewidth = 3, markersize = 10)
pylab.axhline(.5,color='k',linestyle=':')
pylab.show()

def plotColoredPathClassical(runData, cond=[2,3], color='Red'):
    state = runData['stateinfo']
    ndx = np.nonzero([x in cond for x in [y[1] for y in state]])[0]
    w = runData['warpedTracking']
    for switchNdx in ndx:
        bNdxWin = np.logical_and(w[:,0]>state[switchNdx][0], w[:,0]<state[switchNdx+1][0])
        if state[switchNdx][2]==color:
            pyplot.plot(w[bNdxWin,1],w[bNdxWin,2],'r')
        else:
            pyplot.plot(w[bNdxWin,1],w[bNdxWin,2],'b')

pylab.figure(2)
pylab.clf()
pylab.suptitle('Experimental Fish Paths')
ax = pylab.subplot(2,2,1)
aba.plotColoredPath(e_fish_red[0], cond=[8], color = 'Red');
pylab.xlim((0,48))
pylab.ylim((0,22))
pylab.title('Fish 1')
pylab.hold(True)
ax = pylab.subplot(2,2,2, sharey=ax, sharex=ax)
aba.plotColoredPath(e_fish_red[1], cond=[8], color = 'Red');
pylab.xlim((0,48))
pylab.ylim((0,22))
pylab.title('Fish 2')
ax = pylab.subplot(2,2,3, sharey=ax, sharex=ax)
aba.plotColoredPath(e_fish_blue[0], cond=[8], color = 'Blue');
pylab.xlim((0,48))
pylab.ylim((0,22))
pylab.title('Fish 3')
ax = pylab.subplot(2,2,4, sharey=ax, sharex=ax)
aba.plotColoredPath(e_fish_blue[1], cond=[8], color = 'Blue');
pylab.xlim((0,48))
pylab.ylim((0,22))
pylab.title('Fish 4')

pylab.figure(3)
pylab.clf()
pylab.suptitle('Control Fish Paths')
ax = pylab.subplot(2,2,1)
aba.plotColoredPath(c_fish[0], cond=[8], color = 'Red');
pylab.xlim((0,48))
pylab.ylim((0,22))
pylab.title('Fish 1')
pylab.hold(True)
ax = pylab.subplot(2,2,2, sharey=ax, sharex=ax)
aba.plotColoredPath(c_fish[1], cond=[8], color = 'Red');
pylab.xlim((0,48))
pylab.ylim((0,22))
pylab.title('Fish 2')
ax = pylab.subplot(2,2,3, sharey=ax, sharex=ax)
aba.plotColoredPath(c_fish[2], cond=[8], color = 'Red');
pylab.xlim((0,48))
pylab.ylim((0,22))
pylab.title('Fish 3')
ax = pylab.subplot(2,2,4, sharey=ax, sharex=ax)
aba.plotColoredPath(c_fish[3], cond=[8], color = 'Red');
pylab.xlim((0,48))
pylab.ylim((0,22))
pylab.title('Fish 4')
