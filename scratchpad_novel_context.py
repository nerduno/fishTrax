import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
"""
e_shock =['/home/vburns/Dropbox/ConchisData/2013-01-17/f00089/f00089_2013-01-19-14-46-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-17/f00089/f00089_2013-01-19-14-46-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-17/f00090/f00090_2013-01-19-14-46-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-17/f00091/f00091_2013-01-19-14-46-08.json']
e_shock = aba.loadMultipleDataFiles(e_shock)

e_RT = ['/home/vburns/Dropbox/ConchisData/2013-01-17/f00088/f00088_2013-01-19-16-05-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-17/f00089/f00089_2013-01-19-16-05-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-17/f00090/f00090_2013-01-19-16-04-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-17/f00091/f00091_2013-01-19-16-04-55.json']
e_RT = aba.loadMultipleDataFiles(e_RT)

e_novel = ['/home/vburns/Dropbox/ConchisData/2013-01-17/f00088/f00088_2013-01-19-16-39-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-17/f00089/f00089_2013-01-19-16-44-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-17/f00090/f00090_2013-01-19-16-40-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-17/f00091/f00091_2013-01-19-16-41-51.json']
e_novel = aba.loadMultipleDataFiles(e_novel)

e_shock2 = ['/home/vburns/Dropbox/ConchisData/2013-01-24/f00101/f00101_2013-01-24-18-23-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-24/f00102/f00102_2013-01-24-18-23-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-24/f00103/f00103_2013-01-24-18-23-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-24/f00104/f00104_2013-01-24-18-23-57.json']
e_shock2 = aba.loadMultipleDataFiles(e_shock2)

e_RT2 = ['/home/vburns/Dropbox/ConchisData/2013-01-24/f00101/f00101_2013-01-24-18-55-25.json', 
'/home/vburns/Dropbox/ConchisData/2013-01-24/f00102/f00102_2013-01-24-18-55-23.json', 
'/home/vburns/Dropbox/ConchisData/2013-01-24/f00103/f00103_2013-01-24-18-55-20.json',
'/home/vburns/Dropbox/ConchisData/2013-01-24/f00104/f00104_2013-01-24-18-55-18.json']
e_RT2 = aba.loadMultipleDataFiles(e_RT2)

e_novel2 = ['/home/vburns/Dropbox/ConchisData/2013-01-24/f00101/f00101_2013-01-24-19-29-24.json',
'/home/vburns/Dropbox/ConchisData/2013-01-24/f00102/f00102_2013-01-24-19-29-26.json',
'/home/vburns/Dropbox/ConchisData/2013-01-24/f00103/f00103_2013-01-24-19-29-29.json',
'/home/vburns/Dropbox/ConchisData/2013-01-24/f00104/f00104_2013-01-24-19-29-32.json']
e_novel2 = aba.loadMultipleDataFiles(e_novel2)
"""
e_shock = ['/home/vburns/Dropbox/ConchisData/2013-01-30/f00117/f00117_2013-01-30-11-51-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00118/f00118_2013-01-30-11-51-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00119/f00119_2013-01-30-11-51-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00120/f00120_2013-01-30-11-51-01.json']
e_shock = aba.loadMultipleDataFiles(e_shock)

e_RT = ['/home/vburns/Dropbox/ConchisData/2013-01-30/f00117/f00117_2013-01-30-12-56-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00118/f00118_2013-01-30-12-56-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00119/f00119_2013-01-30-12-56-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00120/f00120_2013-01-30-12-56-14.json']
e_RT = aba.loadMultipleDataFiles(e_RT)

e_novel = ['/home/vburns/Dropbox/ConchisData/2013-01-30/f00117/f00117_2013-01-30-13-44-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00118/f00118_2013-01-30-13-44-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00119/f00119_2013-01-30-13-45-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00120/f00120_2013-01-30-13-45-26.json']
e_novel = aba.loadMultipleDataFiles(e_novel)

e_shock2 = ['/home/vburns/Dropbox/ConchisData/2013-01-31/f00125/f00125_2013-01-31-08-56-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00126/f00126_2013-01-31-08-56-22.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00127/f00127_2013-01-31-08-56-24.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00128/f00128_2013-01-31-08-56-27.json']
e_shock2 = aba.loadMultipleDataFiles(e_shock2)

e_RT2 = ['/home/vburns/Dropbox/ConchisData/2013-01-31/f00125/f00125_2013-01-31-10-25-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00126/f00126_2013-01-31-10-25-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00127/f00127_2013-01-31-10-25-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00128/f00128_2013-01-31-10-25-39.json']
e_RT2 = aba.loadMultipleDataFiles(e_RT2)

e_novel2 = ['/home/vburns/Dropbox/ConchisData/2013-01-31/f00125/f00125_2013-01-31-11-07-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00126/f00126_2013-01-31-11-07-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00127/f00127_2013-01-31-11-07-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-31/f00128/f00128_2013-01-31-11-07-31.json']
e_novel2 = aba.loadMultipleDataFiles(e_novel2)

"""

c_shock = ['/home/vburns/Dropbox/ConchisData/2013-01-10/f00072/f00072_2013-01-10-16-39-43.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-10/f00073/f00073_2013-01-10-16-39-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-10/f00074/f00074_2013-01-10-16-39-38.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-10/f00075/f00075_2013-01-10-16-39-36.json']
c_shock = aba.loadMultipleDataFiles(c_shock)

c_RT = ['/home/vburns/Dropbox/ConchisData/2013-01-10/f00072/f00072_2013-01-10-17-16-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-10/f00073/f00073_2013-01-10-17-16-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-10/f00074/f00074_2013-01-10-17-16-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-10/f00075/f00075_2013-01-10-17-16-36.json']
c_RT = aba.loadMultipleDataFiles(c_RT)

c_RT2 = ['/home/vburns/Dropbox/ConchisData/2013-01-09/f00046/f00046_2013-01-09-18-24-16.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-09/f00047/f00047_2013-01-09-18-24-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-09/f00048/f00048_2013-01-09-18-24-24.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-09/f00049/f00049_2013-01-09-18-24-26.json']
c_RT2 = aba.loadMultipleDataFiles(c_RT2)

"""
c_shock = ['/home/vburns/Dropbox/ConchisData/2013-01-30/f00121/f00121_2013-01-30-14-54-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00122/f00122_2013-01-30-14-54-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00123/f00123_2013-01-30-14-54-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00124/f00124_2013-01-30-14-54-55.json']
c_shock = aba.loadMultipleDataFiles(c_shock)

c_RT = ['/home/vburns/Dropbox/ConchisData/2013-01-30/f00121/f00121_2013-01-30-16-00-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00122/f00122_2013-01-30-16-00-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00123/f00123_2013-01-30-16-00-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00124/f00124_2013-01-30-15-59-57.json']
c_RT = aba.loadMultipleDataFiles(c_RT)

c_novel = ['/home/vburns/Dropbox/ConchisData/2013-01-30/f00122/f00122_2013-01-30-16-40-59.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00123/f00123_2013-01-30-16-39-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-30/f00124/f00124_2013-01-30-16-39-11.json']
c_novel = aba.loadMultipleDataFiles(c_novel)

import pylab
#Real time avoidance statistics following extended shock (learned helplessness)
(e_fracShock,e_distShock) = aba.getSidePreference_Multi(e_shock)
(e_fracRT,e_distRT) = aba.getSidePreference_Multi(e_RT)
(e_fracNov,e_distNov) = aba.getSidePreference_Multi(e_novel)

(e_fracShock2,e_distShock2) = aba.getSidePreference_Multi(e_shock2)
(e_fracRT2,e_distRT2) = aba.getSidePreference_Multi(e_RT2)
(e_fracNov2,e_distNov2) = aba.getSidePreference_Multi(e_novel2)

(c_fracRT,c_distRT) = aba.getSidePreference_Multi(c_RT)
(c_fracShock, c_distShock) = aba.getSidePreference_Multi(c_shock)
(c_fracNov,c_distNov) = aba.getSidePreference_Multi(c_novel)

import scipy
[tv, e_fracRT_stat] = scipy.stats.ttest_1samp(np.mean(e_fracRT, axis = 1), 0.5)
[tv, e_distRT_stat] = scipy.stats.ttest_1samp(np.mean(e_distRT, axis = 1), 24)
[tv, e_fracRT2_stat] = scipy.stats.ttest_1samp(np.mean(e_fracRT2, axis = 1), 0.5)
[tv, e_distRT2_stat] = scipy.stats.ttest_1samp(np.mean(e_distRT2, axis = 1), 24)
[tv, c_fracRT_stat] = scipy.stats.ttest_1samp(np.mean(c_fracRT, axis = 1), 0.5)
[tv, c_distRT_stat] = scipy.stats.ttest_1samp(np.mean(c_distRT, axis = 1), 24)
[t, time_diff] = scipy.stats.ttest_ind(np.mean(e_fracRT,axis = 1), np.mean(c_fracRT,1))
[t, dist_diff] = scipy.stats.ttest_ind(np.mean(e_distRT,axis = 1), np.mean(c_distRT,1))

print 'BY ANIMAL Avoidance Post LH_5V 14dpf (frac, distance): ', e_fracRT_stat, e_distRT_stat
print 'By ANIMAL Avoidance Post LH_5V 27dpf (frac, distance):', e_fracRT2_stat, e_distRT2_stat
print 'BY ANIMAL Avoidance Control: ', c_fracRT_stat, c_distRT_stat
print 'BY ANIMAL Controls diff from Exper (time, dist): ', time_diff, dist_diff 

e_RTn = e_RT + e_RT2
for n in range(len(e_RTn)):
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
pylab.figure(5)
pylab.subplot(2,2,1)
aba.plotFishXPosition(e_RT[0])
pylab.subplot(2,2,2)
aba.plotFishXPosition(e_RT[1])
pylab.subplot(2,2,3)
aba.plotFishXPosition(e_RT[2])
pylab.subplot(2,2,4)
aba.plotFishXPosition(e_RT[3])
"""
ae_f = np.mean(e_fracRT,1)
ac_f = np.mean(c_fracRT,1)
ae_d = np.mean(e_distRT,1)
ac_d = np.mean(c_distRT,1)
ae_f2 = np.mean(e_fracRT2, 1)
ae_d2 = np.mean(e_distRT2, 1)
pylab.figure(20)
ax = pylab.subplot(1,2,1)
pylab.errorbar([0,1],[np.mean(ae_f),np.mean(ac_f)],fmt='o',yerr=(2*scipy.stats.sem(ae_f),2*scipy.stats.sem(ac_f)))
pylab.axhline(.5)
pylab.xlim((-1,2))
pylab.ylim((0,1))
pylab.ylabel('% Time on shock side')
ax.set_xticks((0,1))
ax.set_xticklabels(('exper','control'))
pylab.suptitle('Real-time shock avoidance following learned helplessness 14dpf')
ax = pylab.subplot(1,2,2)
pylab.errorbar([0,1],[48-np.mean(ae_d),48-np.mean(ac_d)],fmt='o',yerr=(2*scipy.stats.sem(ae_d),2*scipy.stats.sem(ac_d)))
pylab.axhline(24)
pylab.xlim((-1,2))
pylab.ylim((0,48))
pylab.ylabel('% Avg dist from safe side')
ax.set_xticks((0,1))
ax.set_xticklabels(('exper','control'))
ax.set_yticks((0,24,48))

pylab.figure(21)
ax = pylab.subplot(1,2,1)
pylab.errorbar([0,1],[np.mean(ae_f2),np.mean(ac_f)],fmt='o',yerr=(2*scipy.stats.sem(ae_f2),2*scipy.stats.sem(ac_f)))
pylab.axhline(.5)
pylab.xlim((-1,2))
pylab.ylim((0,1))
pylab.ylabel('% Time on shock side')
ax.set_xticks((0,1))
ax.set_xticklabels(('exper','control'))
pylab.suptitle('Real-time shock avoidance following learned helplessness 28dpf')
ax = pylab.subplot(1,2,2)
pylab.errorbar([0,1],[48-np.mean(ae_d2),48-np.mean(ac_d)],fmt='o',yerr=(2*scipy.stats.sem(ae_d2),2*scipy.stats.sem(ac_d)))
pylab.axhline(24)
pylab.xlim((-1,2))
pylab.ylim((0,48))
pylab.ylabel('% Avg dist from safe side')
ax.set_xticks((0,1))
ax.set_xticklabels(('exper','control'))
ax.set_yticks((0,24,48))

#pylab.title('Real-time shock avoidance following \nlearned helplessness induction')

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
eShockVel = getVelMulti(e_shock, (0, 900))
eLHVel = getVelMulti(e_RT)
eShockVel2 = getVelMulti(e_shock2, (0,900))
eLHVel2 = getVelMulti(e_RT2)
eNovVel = getVelMulti(e_novel, (0,900))
eNovVel2 = getVelMulti(e_novel2, (0,900))
eNovVellate = getVelMulti(e_novel, (1800,2700))
eNovVel2late = getVelMulti(e_novel2, (1800,2700))
cShockVel = getVelMulti(c_shock, (0, 900))
cLHVel = getVelMulti(c_RT)
cNovVel = getVelMulti(c_novel, (0,900))
cNovVellate = getVelMulti(c_novel, (1800,2700))

cNovVel = cNovVel + [0]
cNovVellate = cNovVellate + [0]

[tv, e_Shock_LH] = scipy.stats.ttest_ind(eShockVel, eLHVel)
[tv, e_Shock_Nov] = scipy.stats.ttest_ind(eShockVel, eNovVel)
[tv, e_LH_Nov] = scipy.stats.ttest_ind(eLHVel, eNovVel)
[tv, e_Shock_LH2] = scipy.stats.ttest_ind(eShockVel2, eLHVel2)
[tv, e_Shock_Nov2] = scipy.stats.ttest_ind(eShockVel2, eNovVel2)
[tv, e_LH_Nov2] = scipy.stats.ttest_ind(eLHVel2, eNovVel2)

print 'Velocity at Shock, Real Time Test, Novel (exp): ', eShockVel, eLHVel, eNovVel
print 'Statistcs comparing Shock/LH, Shock/Nov, LH/Nov: ', e_Shock_LH, e_Shock_Nov, e_LH_Nov
print 'Statistcs comparing Shock/LH, Shock/Nov, LH/Nov 28: ', e_Shock_LH2, e_Shock_Nov2, e_LH_Nov2

pylab.figure(30)
ax = pylab.subplot(1,3,1)
pylab.plot([0,1,2,3],[eShockVel,eLHVel,eNovVel,eNovVellate],'.-r')
ax.set_xticks((0,1,2,3))
ax.set_xticklabels(('shock','RT', 'novel', 'novel late'))
pylab.xlim((-.25,3.25))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Effect of LH protocol on velocity in novel context\n(Experimental Fish 14)')
ax = pylab.subplot(1,3,2,sharey=ax)
pylab.plot([0,1,2,3],[eShockVel2,eLHVel2,eNovVel2,eNovVel2late],'.-r')
ax.set_xticks((0,1,2,3))
ax.set_xticklabels(('shock','RT', 'novel', 'novel late'))
pylab.xlim((-.25,3.25))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Effect of LH protocol on velocity in novel context\n(Experimental Fish 28)')
ax = pylab.subplot(1,3,3,sharey=ax)
pylab.plot([0,1,2,3],[cShockVel,cLHVel, cNovVel, cNovVellate],'.-k')
ax.set_xticks((0,1,2,3))
ax.set_xticklabels(('shock','RT', 'novel', 'novel late'))
pylab.xlim((-.25,3.25))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Effect of LH protocol on velocity\nControl Fish')
pylab.show()



