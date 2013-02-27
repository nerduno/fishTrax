import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot

e_shockR = ['/home/vburns/Dropbox/ConchisData/2013-02-17/f00160/f00160_2013-02-17-10-53-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00161/f00161_2013-02-17-10-53-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00162/f00162_2013-02-17-10-53-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00163/f00163_2013-02-17-10-52-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00164/f00164_2013-02-17-12-33-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00165/f00165_2013-02-17-12-33-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00166/f00166_2013-02-17-12-33-22.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00167/f00167_2013-02-17-12-33-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-24/f00190/f00190_2013-02-24-13-55-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-24/f00191/f00191_2013-02-24-13-56-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-24/f00192/f00192_2013-02-24-13-55-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00193/f00193_2013-02-26-14-46-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00194/f00194_2013-02-26-14-46-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00195/f00195_2013-02-26-14-46-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00196/f00196_2013-02-26-14-46-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00197/f00197_2013-02-26-14-46-16.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00198/f00198_2013-02-26-14-46-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00199/f00199_2013-02-26-14-46-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00200/f00200_2013-02-26-14-46-09.json']
e_shockR = aba.loadMultipleDataFiles(e_shockR)

e_RTR = [ '/home/vburns/Dropbox/ConchisData/2013-02-17/f00160/f00160_2013-02-17-11-45-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00161/f00161_2013-02-17-11-44-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00162/f00162_2013-02-17-11-44-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00164/f00164_2013-02-17-13-24-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00165/f00165_2013-02-17-13-24-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00166/f00166_2013-02-17-13-25-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00167/f00167_2013-02-17-13-25-49.json', 
 '/home/vburns/Dropbox/ConchisData/2013-02-24/f00190/f00190_2013-02-24-14-48-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-24/f00191/f00191_2013-02-24-14-47-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-24/f00192/f00192_2013-02-24-14-47-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00193/f00193_2013-02-26-15-38-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00194/f00194_2013-02-26-15-38-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00195/f00195_2013-02-26-15-38-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00196/f00196_2013-02-26-15-38-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00197/f00197_2013-02-26-15-38-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00198/f00198_2013-02-26-15-38-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00199/f00199_2013-02-26-15-38-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00200/f00200_2013-02-26-15-38-22.json']
e_RTR = aba.loadMultipleDataFiles(e_RTR)

e_shock = ['/home/vburns/Dropbox/ConchisData/2013-02-17/f00168/f00168_2013-02-17-14-20-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00169/f00169_2013-02-17-14-19-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00170/f00170_2013-02-17-14-19-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00171/f00171_2013-02-17-14-19-50.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-18/f00172/f00172_2013-02-18-10-57-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-18/f00173/f00173_2013-02-18-10-57-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-18/f00174/f00174_2013-02-18-10-57-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-18/f00175/f00175_2013-02-18-10-57-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00201/f00201_2013-02-26-16-24-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00202/f00202_2013-02-26-16-24-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00203/f00203_2013-02-26-16-24-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00204/f00204_2013-02-26-16-23-56.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00205/f00205_2013-02-26-16-23-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00206/f00206_2013-02-26-16-23-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00207/f00207_2013-02-26-16-23-43.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00208/f00208_2013-02-26-16-23-39.json']
e_shock = aba.loadMultipleDataFiles(e_shock)

e_RT= ['/home/vburns/Dropbox/ConchisData/2013-02-17/f00168/f00168_2013-02-17-15-09-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00169/f00169_2013-02-17-15-09-44.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00170/f00170_2013-02-17-15-09-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00171/f00171_2013-02-17-15-09-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-18/f00172/f00172_2013-02-18-11-48-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-18/f00173/f00173_2013-02-18-11-47-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-18/f00174/f00174_2013-02-18-11-47-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-18/f00175/f00175_2013-02-18-11-46-46.json', 
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00201/f00201_2013-02-26-17-11-56.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00202/f00202_2013-02-26-17-12-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00203/f00203_2013-02-26-17-12-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00204/f00204_2013-02-26-17-12-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00205/f00205_2013-02-26-17-12-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00206/f00206_2013-02-26-17-12-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00207/f00207_2013-02-26-17-12-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00208/f00208_2013-02-26-17-12-59.json']
e_RT = aba.loadMultipleDataFiles(e_RT)

e_long = ['/home/vburns/Dropbox/ConchisData/2013-02-17/f00168/f00168_2013-02-17-15-50-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00169/f00169_2013-02-17-15-50-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00170/f00170_2013-02-17-15-50-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-17/f00171/f00171_2013-02-17-15-50-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-18/f00172/f00172_2013-02-18-12-28-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-18/f00173/f00173_2013-02-18-12-28-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-18/f00174/f00174_2013-02-18-12-28-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-18/f00175/f00175_2013-02-18-12-28-34.json', 
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00201/f00201_2013-02-26-17-55-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00202/f00202_2013-02-26-17-55-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00203/f00203_2013-02-26-17-55-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00204/f00204_2013-02-26-17-55-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00205/f00205_2013-02-26-17-55-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00206/f00206_2013-02-26-17-55-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00207/f00207_2013-02-26-17-56-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-26/f00208/f00208_2013-02-26-17-56-13.json']
e_long = aba.loadMultipleDataFiles(e_long)

#pop fish with velocity <1mm/s (fish 1, 5,6) 
#pop red tank fish with velocity <1mm/s (fish 1,2,5)

"""
c_shock = ['/home/vburns/Dropbox/ConchisData/2013-02-13/f00143/f00143_2013-02-13-10-40-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00144/f00144_2013-02-13-10-40-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00145/f00145_2013-02-13-10-40-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00146/f00146_2013-02-13-10-40-17.json']
c_shock = aba.loadMultipleDataFiles(c_shock)

c_RT = ['/home/vburns/Dropbox/ConchisData/2013-02-13/f00143/f00143_2013-02-13-11-43-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00144/f00144_2013-02-13-11-43-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00145/f00145_2013-02-13-11-43-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00146/f00146_2013-02-13-11-43-03.json']
c_RT = aba.loadMultipleDataFiles(c_RT)

c_novel = ['/home/vburns/Dropbox/ConchisData/2013-02-13/f00143/f00143_2013-02-13-12-28-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00144/f00144_2013-02-13-12-28-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00145/f00145_2013-02-13-12-28-22.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-13/f00146/f00146_2013-02-13-12-28-15.json']
c_novel = aba.loadMultipleDataFiles(c_novel)
"""
import pylab
#Real time avoidance statistics following extended shock (learned helplessness)
(e_fracRT,e_distRT) = aba.getSidePreference_Multi(e_RT)
(e_fracRT2, e_distRT2) = aba.getSidePreference_Multi(e_RTR)
#(c_fracRT,c_distRT) = aba.getSidePreference_Multi(c_RT)


import scipy
[tv, e_fracRT_stat] = scipy.stats.ttest_1samp(np.mean(e_fracRT, axis = 1), 0.5)
[tv, e_distRT_stat] = scipy.stats.ttest_1samp(np.mean(e_distRT, axis = 1), 24)
[tv, e_fracRT2_stat] = scipy.stats.ttest_1samp(np.mean(e_fracRT2, axis = 1), 0.5)
[tv, e_distRT2_stat] = scipy.stats.ttest_1samp(np.mean(e_distRT2, axis = 1), 24)

print 'Avoidance Post LH_5V 14dpf with pipetting (frac, distance): ', e_fracRT_stat, e_distRT_stat
print 'Avoidance Post LH_5V 14dpf, tested in new context (frac, distance):', e_fracRT2_stat, e_distRT2_stat

ae_f = np.mean(e_fracRT,1)
#ac_f = np.mean(c_fracRT,1)
ae_d = np.mean(e_distRT,1)
#ac_d = np.mean(c_distRT,1)
ae_f2 = np.mean(e_fracRT2, 1)
ae_d2 = np.mean(e_distRT2, 1)
pylab.figure(1)
ax = pylab.subplot(1,2,1)
pylab.errorbar([0,1],[np.mean(ae_f), np.mean(ae_f2)],fmt='o',yerr=(2*scipy.stats.sem(ae_f),2*scipy.stats.sem(ae_f2)))
pylab.axhline(.5, ls = '--', c = 'k')
pylab.xlim((-1,2))
pylab.ylim((0,1))
pylab.ylabel('% Time on shock side')
ax.set_xticks((0,1))
ax.set_xticklabels(('exper RTS\nwith pipetting', 'exper RTS\nin novel context'))
pylab.suptitle('Real-time shock avoidance following learned helplessness')
ax = pylab.subplot(1,2,2)
pylab.errorbar([0,1],[48-np.mean(ae_d),48-np.mean(ae_d2)], fmt='o',yerr=(2*scipy.stats.sem(ae_d), 2*scipy.stats.sem(ae_d2)))
pylab.axhline(24, ls = '--', c = 'k')
pylab.xlim((-1,2))
pylab.ylim((0,48))
pylab.ylabel('% Avg dist from safe side')
ax.set_xticks((0,1))
ax.set_xticklabels(('exper RTS\nwith pipetting','exper RTS\nin novel context'))
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

#velocity locomation analysis
n = 15 # minutes to look at
eBaseVel = getVelMulti(e_shock, (0,900))
eStartShockVel = getVelMulti(e_shock, (900, 60*(15+n)))
eShockVel = getVelMulti(e_shock, (60*(45-n), 60*45))
eLHVel = getVelMulti(e_RT)
eVellate = getVelMulti(e_long, (2700,3600))
#eNovVel = getVelMulti(e_novel, (0,900))
eBaseVelR = getVelMulti(e_shockR, (0, 900))
eStartShockR = getVelMulti(e_shockR, (900, 60*(15*n)))
eShockR = getVelMulti(e_shockR, (60*(45-n), 60*45))
eLHVelR = getVelMulti(e_RTR)

#same context
[tv, e_Base_RT] = scipy.stats.ttest_ind(eBaseVel, eLHVel)
[tv, e_Base_Nov] = scipy.stats.ttest_ind(eBaseVel, eVellate)
[tv, e_Shock_LH] = scipy.stats.ttest_ind(eShockVel, eLHVel)
[tv, e_Shock_Nov] = scipy.stats.ttest_ind(eShockVel, eVellate)
[tv, e_LH_Nov] = scipy.stats.ttest_ind(eLHVel, eVellate)
#red tanks
[tv, e_Base_RT2] = scipy.stats.ttest_ind(eBaseVelR, eLHVelR)
[tv, e_Shock_LH2] = scipy.stats.ttest_ind(eShockR, eLHVelR)

#comparisons 
[tv, e_Shock_Shock] = scipy.stats.ttest_ind(eLHVel, eLHVelR)

print 'Statistics comparing velocities baseline/RT, last 15 min Shock/RT, RT/last 15 min Nov, baseline/novel experimental in same context with pipeting: ', e_Base_RT, e_Shock_LH, e_LH_Nov, e_Base_Nov
print 'Statistics comparing velocities baseline/RT, last 15 min Shock/RT, experimental in new context  with pipeting: ', e_Base_RT2, e_Shock_LH2, 
print 'Statistics comparing velocity between pippetted RT and novel context RT:', e_Shock_Shock

#fix
eLHVelR = np.insert(eLHVelR, 3, None)

#convert to array
eBV = np.array([np.array([eBaseVel[n]]) for n in range(len(eBaseVel))])
eSSV = np.array([np.array([eStartShockVel[n]]) for n in range(len(eStartShockVel))])
eSV = np.array([np.array([eShockVel[n]]) for n in range(len(eShockVel))])
eLH = np.array([np.array([eLHVel[n]]) for n in range(len(eLHVel))])
eVlate = np.array([np.array([eVellate[n]]) for n in range(len(eVellate))])
eBVR = np.array([np.array([eBaseVelR[n]]) for n in range(len(eBaseVelR))])
eSSR = np.array([np.array([eStartShockR[n]]) for n in range(len(eStartShockR))])
eSR = np.array([np.array([eShockR[n]]) for n in range(len(eShockR))])
eLHR = np.array([np.array([eLHVelR[n]]) for n in range(len(eLHVelR))])

experimental = np.transpose(np.hstack((eBV, eSSV, eSV, eLH, eVlate)))
experimental2 = np.transpose(np.hstack((eBVR, eSSR, eSR, eLHR)))

pylab.figure(31)
pylab.suptitle('Learned Helplessness/Blocking Assay')
ax = pylab.subplot(1,2,1)
pylab.plot(experimental)
pylab.plot(0, [eBaseVel], 'r.')
pylab.plot(1, [eStartShockVel], 'r.')
pylab.plot(2,[eShockVel], 'r.')
pylab.plot(3,[eLHVel], 'r.')
pylab.plot(4,[eVellate],'r.')
pylab.plot([0,1,2,3,4],[np.mean(eBaseVel), np.mean(eStartShockVel), np.mean(eShockVel),scipy.stats.nanmean(eLHVel), np.mean(eVellate)],'o-k', lw=3)
ax.set_xticks((0,1,2,3,4))
ax.set_xticklabels(('baseline', '0-15 min\nshock', '15-30 min\nshock','avoidance\ntest', 'novel\ncontext'))
pylab.xlim((-.25,4.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish avoidance-tested in same tank')
patch1 = mpl.patches.Rectangle((2.5,0), 1,5, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,2,2)
pylab.plot(experimental2)
pylab.plot(0, [eBaseVelR], 'b.')
pylab.plot(1, [eStartShockR], 'b.')
pylab.plot(2,[eShockR], 'b.')
pylab.plot(3,[eLHVelR], 'b.')
pylab.plot([0,1,2,3],[np.mean(eBaseVelR), np.mean(eStartShockR), np.mean(eShockR),scipy.stats.nanmean(eLHVelR)],'o-k', lw=3)
ax.set_xticks((0,1,2,3))
ax.set_xticklabels(('baseline', '0-15 min\nshock', '15-30 min\nshock','avoidance test\n(novel tank)',))
pylab.xlim((-.25,3.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish avoidance-tested in novel tank')
patch3 = mpl.patches.Rectangle((2.5,0), 1,5, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch3)

pylab.figure(41)
wid = 0.5
xvalues = range(1,2*len(experimental)+1,2)
shift = [x+wid for x in xvalues]
shift.pop(len(shift)-1)
pylab.bar(xvalues, (np.mean(eBaseVel), np.mean(eStartShockVel), np.mean(eShockVel),scipy.stats.nanmean(eLHVel), np.mean(eVellate)), color = 'm', width = 0.5, align = 'center', label = 'same context')
pylab.bar(shift, (np.mean(eBaseVelR), np.mean(eStartShockR), np.mean(eShockR),scipy.stats.nanmean(eLHVelR)), color = 'g', width = 0.5, align = 'center', label = 'novel context')
pylab.errorbar(xvalues,(np.mean(eBaseVel), np.mean(eStartShockVel), np.mean(eShockVel),scipy.stats.nanmean(eLHVel), np.mean(eVellate)),yerr=(2*scipy.stats.sem(eBaseVel),2*scipy.stats.sem(eStartShockVel),2*scipy.stats.sem(eShockVel),2*scipy.stats.sem(eLHVel),2*scipy.stats.sem(eVellate)), fmt = None, ecolor = 'k')
pylab.errorbar(shift,(np.mean(eBaseVelR), np.mean(eStartShockR), np.mean(eShockR),scipy.stats.nanmean(eLHVelR)), yerr=(2*scipy.stats.sem(eBaseVelR),2*scipy.stats.sem(eStartShockR),2*scipy.stats.sem(eShockR),2*scipy.stats.sem(eLHVelR)),fmt = None, ecolor = 'k')
pylab.ylim((0,3))
pylab.title('Velocity Summary')
pylab.legend()
pylab.ylabel('Mean Velocities (mm/s)')
labels = ['    baseline', '    shock', '    late\n    shock', '    RTS', '    late\n    nov']
pylab.xticks(xvalues, labels)
pylab.show()
