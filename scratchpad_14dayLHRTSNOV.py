import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot

e_shock = ['/home/vburns/Dropbox/ConchisData/2013-01-30/f00117/f00117_2013-01-30-11-51-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00118/f00118_2013-01-30-11-51-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00119/f00119_2013-01-30-11-51-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00120/f00120_2013-01-30-11-51-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00125/f00125_2013-01-31-08-56-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00126/f00126_2013-01-31-08-56-22.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00127/f00127_2013-01-31-08-56-24.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00128/f00128_2013-01-31-08-56-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00147/f00147_2013-02-13-13-41-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00148/f00148_2013-02-13-13-41-50.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00149/f00149_2013-02-13-13-41-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00150/f00150_2013-02-13-13-41-46.json',]
e_shock = aba.loadMultipleDataFiles(e_shock)

e_RT = ['/home/vburns/Dropbox/ConchisData/2013-01-30/f00117/f00117_2013-01-30-12-56-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00118/f00118_2013-01-30-12-56-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00119/f00119_2013-01-30-12-56-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00120/f00120_2013-01-30-12-56-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00125/f00125_2013-01-31-10-25-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00126/f00126_2013-01-31-10-25-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00127/f00127_2013-01-31-10-25-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00128/f00128_2013-01-31-10-25-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00147/f00147_2013-02-13-14-32-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00148/f00148_2013-02-13-14-32-22.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00149/f00149_2013-02-13-14-32-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00150/f00150_2013-02-13-14-32-18.json']
e_RT = aba.loadMultipleDataFiles(e_RT)

e_novel = ['/home/vburns/Dropbox/ConchisData/2013-01-30/f00117/f00117_2013-01-30-13-44-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00118/f00118_2013-01-30-13-44-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00119/f00119_2013-01-30-13-45-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00120/f00120_2013-01-30-13-45-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00125/f00125_2013-01-31-11-07-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00126/f00126_2013-01-31-11-07-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00127/f00127_2013-01-31-11-07-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00128/f00128_2013-01-31-11-07-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00147/f00147_2013-02-13-15-16-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00148/f00148_2013-02-13-15-16-37.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00149/f00149_2013-02-13-15-16-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00150/f00150_2013-02-13-15-16-42.json']
e_novel = aba.loadMultipleDataFiles(e_novel)

c_shock = ['/home/vburns/Dropbox/ConchisData/2013-01-30/f00121/f00121_2013-01-30-14-54-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00122/f00122_2013-01-30-14-54-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00123/f00123_2013-01-30-14-54-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00124/f00124_2013-01-30-14-54-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-14/f00152/f00152_2013-02-14-12-41-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-14/f00153/f00153_2013-02-14-12-42-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-14/f00154/f00154_2013-02-14-12-43-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-14/f00155/f00155_2013-02-14-12-44-10.json']
c_shock = aba.loadMultipleDataFiles(c_shock)

c_RT = ['/home/vburns/Dropbox/ConchisData/2013-01-30/f00121/f00121_2013-01-30-16-00-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00122/f00122_2013-01-30-16-00-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00123/f00123_2013-01-30-16-00-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00124/f00124_2013-01-30-15-59-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-14/f00152/f00152_2013-02-14-13-33-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-14/f00153/f00153_2013-02-14-13-33-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-14/f00154/f00154_2013-02-14-13-33-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-14/f00155/f00155_2013-02-14-13-33-42.json']
c_RT = aba.loadMultipleDataFiles(c_RT)

c_novel = ['/home/vburns/Dropbox/ConchisData/2013-01-30/f00122/f00122_2013-01-30-16-40-59.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00123/f00123_2013-01-30-16-39-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00124/f00124_2013-01-30-16-39-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-14/f00152/f00152_2013-02-14-14-19-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-14/f00153/f00153_2013-02-14-14-19-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-14/f00154/f00154_2013-02-14-14-19-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-14/f00155/f00155_2013-02-14-14-18-58.json']
c_novel = aba.loadMultipleDataFiles(c_novel)

import pylab
#pop fish with velocity <0.5mm/s (fish 4 and 10)
#pop fish with velocity <1 mm/s (fish 4, 8, 9, 10) or 0.75mm/s (4, 9, 10)

#Real time avoidance statistics following extended shock (learned helplessness)
(e_fracShock,e_distShock) = aba.getSidePreference_Multi(e_shock)
(e_fracRT,e_distRT) = aba.getSidePreference_Multi(e_RT)
(e_fracNov,e_distNov) = aba.getSidePreference_Multi(e_novel)
#(e_fracRT2, e_distRT2) = aba.getSidePreference_Multi(e_RT2)

(c_fracShock, c_distShock) = aba.getSidePreference_Multi(c_shock)
(c_fracRT,c_distRT) = aba.getSidePreference_Multi(c_RT)
(c_fracNov,c_distNov) = aba.getSidePreference_Multi(c_novel)

import scipy
[tv, e_fracRT_stat] = scipy.stats.ttest_1samp(np.mean(e_fracRT, axis = 1), 0.5)
[tv, e_distRT_stat] = scipy.stats.ttest_1samp(np.mean(e_distRT, axis = 1), 24)
#[tv, e_fracRT2_stat] = scipy.stats.ttest_1samp(np.mean(e_fracRT2, axis = 1), 0.5)
#[tv, e_distRT2_stat] = scipy.stats.ttest_1samp(np.mean(e_distRT2, axis = 1), 24)
[tv, c_fracRT_stat] = scipy.stats.ttest_1samp(np.mean(c_fracRT, axis = 1), 0.5)
[tv, c_distRT_stat] = scipy.stats.ttest_1samp(np.mean(c_distRT, axis = 1), 24)
[t, time_diff] = scipy.stats.ttest_ind(np.mean(e_fracRT,axis = 1), np.mean(c_fracRT,1))
[t, dist_diff] = scipy.stats.ttest_ind(np.mean(e_distRT,axis = 1), np.mean(c_distRT,1))
#[t, time_diff2] = scipy.stats.ttest_ind(np.mean(e_fracRT2,axis = 1), np.mean(c_fracRT,1))
#[t, dist_diff2] = scipy.stats.ttest_ind(np.mean(e_distRT2,axis = 1), np.mean(c_distRT,1))

print 'Avoidance Post LH_5V 14dpf (frac, distance): ', e_fracRT_stat, e_distRT_stat
#print 'Avoidance Post LH_5V 14dpf after novel (frac, distance):', e_fracRT2_stat, e_distRT2_stat
print 'Avoidance Control (frac, distance): ', c_fracRT_stat, c_distRT_stat
print 'Controls diff from Experimental in RTS (time, dist): ', time_diff, dist_diff 
#print 'Controls diff from Experimental (Second RTS) (time, dist): ', time_diff2, dist_diff2 
"""
for n in range(len(e_RT)):
    pylab.figure(n);
    ax1 = pylab.subplot2grid((4,1),(0,0),rowspan=2) 
    aba.plotFishXPosition(e_RTn[n])
    ax = pylab.subplot2grid((4,1),(2,0),sharex=ax1)
    [sh,s,d,dsh,ds,st] = aba.getSidePreference(e_RTn[n], cond=[3,4], refState='On')
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
pylab.show()


for y in range(len(c_RT)):
    pylab.figure(y+10);
    ax1 = pylab.subplot2grid((4,1),(0,0),rowspan=2); 
    aba.plotFishXPosition(c_RT[y])
    ax = pylab.subplot2grid((4,1),(2,0),sharex=ax1);
    [sh,s,d,dsh,ds,st] = aba.getSidePreference(c_RT[y], cond=[3,4], refState='On')
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
pylab.show()
"""

ae_f = np.mean(e_fracRT,1)
ac_f = np.mean(c_fracRT,1)
ae_d = np.mean(e_distRT,1)
ac_d = np.mean(c_distRT,1)
#ae_f2 = np.mean(e_fracRT2, 1)
#ae_d2 = np.mean(e_distRT2, 1)
pylab.figure(1)
ax = pylab.subplot(1,2,1)
pylab.errorbar([0,1],[np.mean(ae_f), np.mean(ac_f)],fmt='o',yerr=(2*scipy.stats.sem(ae_f),2*scipy.stats.sem(ac_f)), c = 'b')
pylab.axhline(.5, ls= '--', c ='k')
pylab.xlim((-1,2))
pylab.ylim((0,1))
pylab.ylabel('% Time on shock side')
ax.set_xticks((0,1))
ax.set_xticklabels(('exper', 'control'))
pylab.suptitle('Real-time shock avoidance following learned helplessness')
ax = pylab.subplot(1,2,2)
pylab.errorbar([0,1],[48-np.mean(ae_d),48-np.mean(ac_d)],fmt='o',yerr=(2*scipy.stats.sem(ae_d), 2*scipy.stats.sem(ac_d)), c = 'b')
pylab.axhline(24, ls = '--', c = 'k')
pylab.xlim((-1,2))
pylab.ylim((0,48))
pylab.ylabel('% Avg dist from safe side')
ax.set_xticks((0,1))
ax.set_xticklabels(('exper','control'))
ax.set_yticks((0,24,48))
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

def getVelRaw(d, tRange=None):
    w = d['warpedTracking']
    if tRange:
        bNdxWin = np.logical_and(w[:,0]>tRange[0]+w[0,0], w[:,0]<tRange[1]+w[0,0])
        vel = np.sqrt(pow(np.diff(w[bNdxWin,1]),2) + pow(np.diff(w[bNdxWin,2]),2)) / np.diff(w[bNdxWin,0])
    else:
        vel = np.sqrt(pow(np.diff(w[:,1]),2) + pow(np.diff(w[:,2]),2)) / np.diff(w[:,0])
    return vel

def getmintime(d):
    tracking = aba.getTracking(d)
    frametime = tracking[:,0]
    mintime = max(frametime)-min(frametime)
    return mintime

#velocity analysis for shock periods, last n min, covering different acclimation times
n=15
minutes = n * 60
e_maxtimes = []
for n in range(len(e_shock)):
    mtime = getmintime(e_shock[n])
    e_maxtimes.append(mtime)
e_mintimes = [x - minutes for x in e_maxtimes]

eShockVel = []
for n in range(len(e_shock)):
    velocity = getVelRaw(e_shock[n], (e_mintimes[n], e_maxtimes[n]))
    eShockVel.append(np.median(velocity))

c_maxtimes = []
for n in range(len(c_shock)):
    mtime = getmintime(c_shock[n])
    c_maxtimes.append(mtime)
c_mintimes = [x - minutes for x in c_maxtimes]

cShockVel = []
for n in range(len(c_shock)):
    cvelocity = getVelRaw(c_shock[n], (c_mintimes[n], c_maxtimes[n]))
    cShockVel.append(np.median(cvelocity))

#velocity analysis for starting shock periods, last m min, covering different acclimation times
m=15
mins = m * 60
e_shocktimemin = []
for n in range(len(e_shock)):
    acclimate = e_shock[n]['parameters']['acclimate (m)']*60
    e_shocktimemin.append(acclimate)
e_shocktimemax = [x + minutes for x in e_shocktimemin]

eStartShockVel = []
for k in range(len(e_shock)):
    eshockvel = getVelRaw(e_shock[k], (e_shocktimemin[k], e_shocktimemax[k]))
    eStartShockVel.append(np.median(eshockvel))

c_shocktimemin = []
for n in range(len(c_shock)):
    cacclimate = c_shock[n]['parameters']['acclimate (m)']*60
    c_shocktimemin.append(cacclimate)
c_shocktimemax = [y + minutes for y in c_shocktimemin]

cStartShockVel = []
for n in range(len(c_shock)):
    csvelocity = getVelRaw(c_shock[n], (c_shocktimemin[n], c_shocktimemax[n]))
    cStartShockVel.append(np.median(csvelocity))


#velocity locomation analysis
#eStartShockVel = starting shock velocity
eBaseVel = getVelMulti(e_shock, (0,900))
#eShockVel = getVelMulti(e_shock, (2700,3600))
eLHVel = getVelMulti(e_RT)
eNovVel = getVelMulti(e_novel, (0,900))
eNovVellate = getVelMulti(e_novel, (2700,3600))
eNov = getVelMulti(e_novel)
#eLHVel2 = getVelMulti(e_RT2, (0,900))

test = getVelRaw(e_shock[0])

cBaseVel = getVelMulti(c_shock, (0, 900))
#cShockVel = getVelMulti(c_shock, (2700,3600))
cLHVel = getVelMulti(c_RT)
cNovVel = getVelMulti(c_novel, (0,900))
cNovVellate = getVelMulti(c_novel, (2700,3600))
cNov = getVelMulti(c_novel)

[tv, e_Base_RT] = scipy.stats.ttest_ind(eBaseVel, eLHVel)
[tv, e_Base_Nov] = scipy.stats.ttest_ind(eBaseVel, eNov)
[tv, e_Shock_LH] = scipy.stats.ttest_ind(eShockVel, eLHVel)
[tv, e_Shock_Nov] = scipy.stats.ttest_ind(eShockVel, eNov)
[tv, e_LH_Nov] = scipy.stats.ttest_ind(eLHVel, eNov)
#[tv, e_Shock_LH2] = scipy.stats.ttest_ind(eShockVel, eLHVel2)
#[tv, e_Shock_Shock] = scipy.stats.ttest_ind(eLHVel, eLHVel2)

[tv, c_Base_RT] = scipy.stats.ttest_ind(cBaseVel, cLHVel)
[tv, c_Base_Nov] = scipy.stats.ttest_ind(cBaseVel, cNov)
[tv, c_Shock_LH] = scipy.stats.ttest_ind(cShockVel, cLHVel)
[tv, c_Shock_Nov] = scipy.stats.ttest_ind(cShockVel, cNov)
[tv, c_LH_Nov] = scipy.stats.ttest_ind(cLHVel, cNov)

[tv, ce_Base] = scipy.stats.ttest_ind(cBaseVel, eBaseVel)
[tv, ce_Shock] = scipy.stats.ttest_ind(cShockVel, eShockVel)
[tv, ce_RT] = scipy.stats.ttest_ind(cLHVel, eLHVel)
[tv, ce_Nov] = scipy.stats.ttest_ind(cNov, eNov)

print 'Statistics comparing velocities Baseline/RT, last 15 Shock/RT, baseline/total Nov, RT/total Nov, experimental: ', e_Base_RT, e_Shock_LH, e_Base_Nov, e_LH_Nov
print 'Statistics comparing velocities Baseline/RT, last 15 Shock/RT, baseline/Nov, RT/Nov control: ', c_Base_RT, c_Shock_LH, c_Base_Nov, c_LH_Nov
print 'Statistics comparing control and experimental base/base, last 15 Shock/Shock, RT/RT, Nov/Nov: ', ce_Base, ce_Shock, ce_RT, ce_Nov  

#convert to array
eBV = np.array([np.array([eBaseVel[n]]) for n in range(len(eBaseVel))])
eSSV = np.array([np.array([eStartShockVel[n]]) for n in range(len(eStartShockVel))])
eSV = np.array([np.array([eShockVel[n]]) for n in range(len(eShockVel))])
eLH = np.array([np.array([eLHVel[n]]) for n in range(len(eLHVel))])
eNV = np.array([np.array([eNovVel[n]]) for n in range(len(eNovVel))])
eNVL = np.array([np.array([eNovVellate[n]]) for n in range(len(eNovVellate))])
eNtot = np.array([np.array([eNov[n]]) for n in range(len(eNov))])

#fix
old_cNovVel = cNovVel
old_cNovVellate = cNovVellate
cNov = np.insert(cNov, 0, None)
cNovVel = np.insert(cNovVel,0,None)
cNovVellate = np.insert(cNovVellate, 0, None)

cBV = np.array([np.array([cBaseVel[n]]) for n in range(len(cBaseVel))])
cSSV = np.array([np.array([cStartShockVel[n]]) for n in range(len(cStartShockVel))])
cSV = np.array([np.array([cShockVel[n]]) for n in range(len(cShockVel))])
cLH = np.array([np.array([cLHVel[n]]) for n in range(len(cLHVel))])
cNV = np.array([np.array([cNovVel[n]]) for n in range(len(cNovVel))])
cNVL = np.array([np.array([cNovVellate[n]]) for n in range(len(cNovVellate))])
cNtot = np.array([np.array([cNov[n]]) for n in range(len(cNov))])

experimental = np.transpose(np.hstack((eBV, eSSV, eSV, eLH, eNVL)))
controls = np.transpose(np.hstack((cBV, cSSV, cSV, cLH, cNVL)))

pylab.figure(30)
pylab.suptitle('Effect of LH protocol on velocity')
ax = pylab.subplot(1,2,1)
pylab.plot(experimental)
pylab.plot(0, [eBaseVel], 'r.')
pylab.plot(1,[eStartShockVel], 'r.')
pylab.plot(2,[eShockVel], 'r.')
pylab.plot(3,[eLHVel], 'r.')
#pylab.plot(4,[eNovVel],'r.')
pylab.plot(4,[eNovVellate],'r.')
pylab.plot([0,1,2,3,4],[np.mean(eBaseVel), np.mean(eStartShockVel), np.mean(eShockVel),np.mean(eLHVel), np.mean(eNovVellate)],'o-k', lw=3)
pylab.axvline(3.5, ls= '-', c ='k', lw=2)
ax.set_xticks((0,1,2,3,4))
ax.set_xticklabels(('baseline','0-15 min\nshock', '15-30 min\nshock','avoidance\ntest', 'novel\ncontext'))
pylab.xlim((-.25,4.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental Fish')
patch1 = mpl.patches.Rectangle((2.5,0), 1,5, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,2,2,sharey=ax)
pylab.plot(controls)
pylab.plot(0, [cBaseVel], 'b.')
pylab.plot(1,[cStartShockVel], 'b.')
pylab.plot(2,[cShockVel], 'b.')
pylab.plot(3,[cLHVel], 'b.')
#pylab.plot(4,[cNovVel],'b.')
pylab.plot(4,[cNovVellate],'b.')
pylab.plot([0,1,2,3,4],[np.mean(cBaseVel), np.mean(cStartShockVel), np.mean(cShockVel),np.mean(cLHVel),scipy.stats.nanmean(cNovVellate)],'o-k', lw=3)
pylab.axvline(3.5, ls= '-', c ='k', lw=2)
ax.set_xticks((0,1,2,3,4))
ax.set_xticklabels(('baseline', '0-15 min\nshock', '15-30 min\nshock','avoidance\ntest', 'novel\ncontext'))
pylab.xlim((-.25,4.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Control Fish')
patch2 = mpl.patches.Rectangle((2.5,0), 1,5, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch2)

pylab.figure(40)
wid = 0.5
xvalues = range(1,2*len(experimental)+1,2)
shift = [x+wid for x in xvalues]
pylab.bar(shift, (np.mean(eBaseVel), np.mean(eStartShockVel), np.mean(eShockVel),scipy.stats.nanmean(eLHVel), np.mean(eNovVellate)), color = 'm', width = 0.5, align = 'center', label = 'experimental')
pylab.bar(xvalues, (np.mean(cBaseVel), np.mean(cStartShockVel), np.mean(cShockVel),np.mean(cLHVel), scipy.stats.nanmean(cNovVellate)), color = 'g', width = 0.5, align = 'center', label = 'control')
pylab.errorbar(shift,(np.mean(eBaseVel), np.mean(eStartShockVel), np.mean(eShockVel),scipy.stats.nanmean(eLHVel), np.mean(eNovVellate)),yerr=(2*scipy.stats.sem(eBaseVel),2*scipy.stats.sem(eStartShockVel),2*scipy.stats.sem(eShockVel),2*scipy.stats.sem(eLHVel),2*scipy.stats.sem(eNovVellate)), fmt = None, ecolor = 'k')
pylab.errorbar(xvalues,(np.mean(cBaseVel), np.mean(cStartShockVel), np.mean(cShockVel),scipy.stats.nanmean(cLHVel), scipy.stats.nanmean(cNovVellate)),yerr=(2*scipy.stats.sem(cBaseVel),2*scipy.stats.sem(cStartShockVel),2*scipy.stats.sem(cShockVel),2*scipy.stats.sem(cLHVel),2*scipy.stats.sem(old_cNovVellate)), fmt = None, ecolor = 'k')
pylab.ylim((0,3))
pylab.title('Velocity Summary')
pylab.legend()
pylab.ylabel('Mean Velocities (mm/s)')
labels = ['    baseline', '    shock', '    late\n    shock', '    RTS', '    late\n    nov']
pylab.xticks(xvalues, labels)
pylab.show()

"""
pylab.figure(100)
pylab.suptitle('Summary Effect of LH protocol on velocity')
ax = pylab.subplot(1,1,1)
pylab.plot([0,1,2,3,4],[np.mean(eBaseVel), np.mean(eStartShockVel), np.mean(eShockVel),np.mean(eLHVel), np.mean(eNovVellate)], lw=3, label = 'experimental with no pipetting')
pylab.plot([0,1,2,3,4],[np.mean(cBaseVel), np.mean(cStartShockVel), np.mean(cShockVel),np.mean(cLHVel),scipy.stats.nanmean(cNovVellate)], lw=3, label = 'control with no pipetting')
pylab.plot([0,1,2,3,4],[np.mean(eBaseVelN), np.mean(eStartShockVelN), np.mean(eShockVelN),scipy.stats.nanmean(eLHVelN), np.mean(eVellate)], lw=3, label = 'experimental pipetted into same tank')
pylab.plot([0,1,2,3],[np.mean(eBaseVelR), np.mean(eStartShockR), np.mean(eShockR),scipy.stats.nanmean(eLHVelR)], lw=3, label = 'experimental pipetted into novel tank')
ax.set_xticks((0,1,2,3,4))
ax.set_xticklabels(('baseline','0-15 min\nshock', '15-30 min\nshock','avoidance\ntest', 'novel\ncontext'))
pylab.xlim((-.25,4.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental Fish')
patch1 = mpl.patches.Rectangle((2.5,0), 1,5, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
pylab.legend()
"""







