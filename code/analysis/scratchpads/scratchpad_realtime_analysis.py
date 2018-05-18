import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np

#f is five day old fish, t is thirteen day old fish
f_fish = ['/home/vburns/Dropbox/ConchisData/2013-01-09/f00056/f00056_2013-01-09-15-15-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-09/f00057/f00057_2013-01-09-15-15-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-09/f00058/f00058_2013-01-09-15-15-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00113/f00113_2013-01-30-10-58-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00014/f00014_2013-01-30-10-58-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00115/f00115_2013-01-30-10-58-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00116/f00116_2013-01-30-10-58-42.json']
f_fish = aba.loadMultipleDataFiles(f_fish)

fb = '/home/vburns/Dropbox/ConchisData/2013-01-09/f00059/f00059_2013-01-09-15-15-24.json'
fb = aba.loadDataFromFile(fb)
fb['warpedTracking'][:,1] = 48-fb['warpedTracking'][:,1]

f_fish = f_fish + [fb]

t_fish = ['/home/vburns/Dropbox/ConchisData/2013-01-09/f00061/f00061_2013-01-09-14-30-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-09/f00062/f00062_2013-01-09-14-30-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-09/f00063/f00063_2013-01-09-14-30-10.json']
t_fish = aba.loadMultipleDataFiles(t_fish)

tb = '/home/vburns/Dropbox/ConchisData/2013-01-09/f00060/f00060_2013-01-09-14-30-04.json'
tb = aba.loadDataFromFile(tb)
tb['warpedTracking'][:,1] = 48-tb['warpedTracking'][:,1]

t_fish = t_fish + [tb]

c_fish = ['/home/vburns/Dropbox/ConchisData/2013-01-10/f00072/f00072_2013-01-10-17-16-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-10/f00073/f00073_2013-01-10-17-16-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-10/f00074/f00074_2013-01-10-17-16-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-10/f00075/f00075_2013-01-10-17-16-36.json']
c_fish = aba.loadMultipleDataFiles(c_fish)

#Real time avoidance statistics following extended shock (learned helplessness)
(ef_frac,ef_dist) = aba.getSidePreference_Multi(f_fish)
(et_frac,et_dist) = aba.getSidePreference_Multi(t_fish)
(c_frac, c_dist) = aba.getSidePreference_Multi(c_fish)

import scipy
[tv, ef_frac_stat] = scipy.stats.ttest_1samp(np.mean(ef_frac, axis = 1), 0.5)
[tv, et_frac_stat] = scipy.stats.ttest_1samp(np.mean(et_frac, axis = 1), 0.5)
[tv, ef_dist_stat] = scipy.stats.ttest_1samp(np.mean(ef_dist, axis = 1), 24)
[tv, et_dist_stat] = scipy.stats.ttest_1samp(np.mean(et_dist, axis = 1), 24)
[tv, c_frac_stat] = scipy.stats.ttest_1samp(np.mean(c_frac, axis = 1), 0.5)
[tv, c_dist_stat] = scipy.stats.ttest_1samp(np.mean(c_dist, axis = 1), 24)
[t, time_diff_five] = scipy.stats.ttest_ind(np.mean(ef_frac,1), np.mean(c_frac,1))
[t, time_diff_old] = scipy.stats.ttest_ind(np.mean(et_frac,1), np.mean(c_frac,1))
[t, dist_diff_five] = scipy.stats.ttest_ind(np.mean(ef_dist,1), np.mean(c_dist,1))
[t, dist_diff_old] = scipy.stats.ttest_ind(np.mean(et_dist,1), np.mean(c_dist,1))

print 'BY ANIMAL 5 DPF  Avoidance Post LH_5V (frac, distance): ', ef_frac_stat, ef_dist_stat
print 'BY ANIMAL 13 DPF Avoidance Post LH_5V (frac, distance): ', et_frac_stat, et_dist_stat
print 'BY ANIMAL Controls diff from Exper (time, dist) at 5 days: ', time_diff_five, dist_diff_five 
print 'BY ANIMAL Controls diff from Exper (time, dist) at 13 days: ', time_diff_five, dist_diff_five 

for n in range(len(f_fish)):
    pylab.figure(n+10); 
    ax1 = pylab.subplot2grid((4,1),(0,0),rowspan=2); 
    aba.plotFishXPosition(f_fish[n])
    ax = pylab.subplot2grid((4,1),(2,0),sharex=ax1);
    [sh,s,d,dsh,ds,st] = aba.getSidePreference(f_fish[n], cond=[3,4], refState='On')
    pylab.bar(st,np.array(s)/np.array(d),width=d)
    pylab.axhline(.5,color='k')
    pylab.ylabel('% time side1')
    ax.set_yticks((0,.5,1))
    ax = pylab.subplot2grid((4,1),(3,0),sharex=ax1);
    pylab.bar(st,np.array(ds),width=d); 
    pylab.ylim((0,48))
    pylab.axhline(24,color='k')
    ax.set_yticks((0,24,48))
    pylab.ylabel('Avg dist from\nside 1 (mm)')
    pylab.xlabel('Time (s)')
"""
pylab.figure(5)
pylab.subplot(2,2,1)
aba.plotFishXPosition(t_fish[0])
pylab.subplot(2,2,2)
aba.plotFishXPosition(t_fish[1])
pylab.subplot(2,2,3)
aba.plotFishXPosition(t_fish[2])
pylab.subplot(2,2,4)
aba.plotFishXPosition(t_fish[3])
"""
pylab.show()

ae_f = np.mean(ef_frac,1)
ac_f = np.mean(c_frac,1)
ae_d = np.mean(ef_dist,1)
ac_d = np.mean(c_dist,1)
pylab.figure(1)
ax = pylab.subplot(1,2,1)
pylab.errorbar([0,1],[np.mean(ae_f),np.mean(ac_f)],fmt='o',yerr=(2*scipy.stats.sem(ae_f),2*scipy.stats.sem(ac_f)))
pylab.axhline(.5)
pylab.xlim((-1,2))
pylab.ylim((0,1))
pylab.ylabel('% Time on shock side')
ax.set_xticks((0,1))
ax.set_xticklabels(('exper','control'))
pylab.suptitle('Real-time shock avoidance 5dpf')
ax = pylab.subplot(1,2,2)
pylab.errorbar([0,1],[48-np.mean(ae_d),48-np.mean(ac_d)],fmt='o',yerr=(2*scipy.stats.sem(ae_d),2*scipy.stats.sem(ac_d)))
pylab.axhline(24)
pylab.xlim((-1,2))
pylab.ylim((0,48))
pylab.ylabel('% Avg dist from safe side')
ax.set_xticks((0,1))
ax.set_xticklabels(('exper','control'))
ax.set_yticks((0,24,48))
#pylab.title('Real-time shock avoidance following \nlearned helplessness induction')
pylab.show()
"""
#n is an shockblock (120s)
import scipy
[t,p_e_time] = scipy.stats.ttest_1samp(e_fracTimeOnShock.flatten(),.5)
[t,p_c_time] = scipy.stats.ttest_1samp(c_fracTimeOnShock.flatten(),.5)
[t,p_e_dist] = scipy.stats.ttest_1samp(e_distFromShock.flatten(),24)
[t,p_c_dist] = scipy.stats.ttest_1samp(c_distFromShock.flatten(),24)
[t,p_time_diff] = scipy.stats.ttest_ind(e_fracTimeOnShock.flatten(), c_fracTimeOnShock.flatten())
[t,p_dist_diff] = scipy.stats.ttest_ind(e_distFromShock.flatten(), c_distFromShock.flatten())
print 'BY SHOCKBLOCK Avoidance Post LH_5V      p_frac,p_dist: ', p_e_time, p_e_dist
print 'BY SHOCKBLOCK Avoidance Post LH_CONTROL p_frac,p_dist: ', p_c_time, p_c_dist
print 'BY SHOCKBLOCK Controls diff from Exper (time,dist): ', p_time_diff, p_dist_diff 
pylab.figure(2)
pylab.subplot(1,2,1)
pylab.boxplot([e_fracTimeOnShock,c_fracTimeOnShock])
pylab.subplot(1,2,2)
pylab.boxplot([e_distFromShock,c_distFromShock])
pylab.show()

def getVelMulti(datasets, tRange=None):
    medVel = []
    for d in datasets:
        w = d['warpedTracking']
        if tRange:
            bNdxWin = np.logical_and(w[:,0]>tRange[0]+w[0,0], w[:,0]<tRange[1]+w[0,0])
            vel = np.sqrt(pow(np.diff(w[bNdxWin,1]),2) + pow(np.diff(w[bNdxWin,2]),2)) / np.diff(w[bNdxWin,0])
        else:
            vel = np.sqrt(pow(np.diff(w[:,1]),2) + pow(np.diff(w[:,2]),2)) / np.diff(w[:,0])
        medVel.append(np.median(vel))     
    return medVel

#velocity locomation analysis
eTestVel = getVelMulti(e_test)
eLHVel = getVelMulti(e_lh, (300,900))
cTestVel = getVelMulti(c_test)
cLHVel = getVelMulti(c_lh, (300,900))
pylab.figure(3)
ax = pylab.subplot(1,2,1)
pylab.plot([0,1],[eLHVel,eTestVel],'.-r')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Effect of LH protocol on velocity\nExperimental Fish')
ax = pylab.subplot(1,2,2,sharey=ax)
pylab.plot([0,1],[cLHVel,cTestVel],'.-k')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Effect of LH protocol on velocity\nControl Fish')
pylab.show()
"""
