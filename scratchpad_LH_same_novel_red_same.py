import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot

#first 15 min is baseline, then 60 bouts of 60 sec shocking (30 bouts total), then 5 min post
#bottom of novel tanks were changed to red
e_shockR = [
'/home/vburns/Dropbox/ConchisData/2013-03-24/f00225/f00225_2013-03-24-11-01-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00226/f00226_2013-03-24-11-01-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00227/f00227_2013-03-24-11-01-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00228/f00228_2013-03-24-11-01-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00229/f00229_2013-03-24-10-57-58.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00230/f00230_2013-03-24-10-57-56.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00231/f00231_2013-03-24-10-57-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00232/f00232_2013-03-24-10-57-51.json',
]
e_shockR = aba.loadMultipleDataFiles(e_shockR)

e_shockS = [
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00225/f00225_2013-03-24-11-56-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00226/f00226_2013-03-24-11-56-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00227/f00227_2013-03-24-11-56-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00228/f00228_2013-03-24-11-56-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00229/f00229_2013-03-24-11-54-44.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00230/f00230_2013-03-24-11-54-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00231/f00231_2013-03-24-11-54-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00232/f00232_2013-03-24-11-54-49.json',
]
e_shockS= aba.loadMultipleDataFiles(e_shockS)

e_shockN = [
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00225/f00225_2013-03-24-12-59-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00226/f00226_2013-03-24-12-59-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00227/f00227_2013-03-24-12-59-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00228/f00228_2013-03-24-13-00-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00229/f00229_2013-03-24-12-57-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00230/f00230_2013-03-24-12-57-16.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00231/f00231_2013-03-24-12-57-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00232/f00232_2013-03-24-12-57-28.json',
]
e_shockN = aba.loadMultipleDataFiles(e_shockN)

e_shockS2= [
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00225/f00225_2013-03-24-14-04-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00226/f00226_2013-03-24-14-04-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00227/f00227_2013-03-24-14-05-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00228/f00228_2013-03-24-14-05-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00229/f00229_2013-03-24-14-07-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00230/f00230_2013-03-24-14-07-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00231/f00231_2013-03-24-14-07-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-24/f00232/f00232_2013-03-24-14-06-45.json'
]
e_shockS2 = aba.loadMultipleDataFiles(e_shockS2)

c_shockR = [
'/home/vburns/Dropbox/ConchisData/2013-03-21/f00209/f00209_2013-03-21-10-22-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00210/f00210_2013-03-21-10-22-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00211/f00211_2013-03-21-10-22-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00212/f00212_2013-03-21-10-22-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00213/f00213_2013-03-21-10-25-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00214/f00214_2013-03-21-10-25-43.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00215/f00215_2013-03-21-10-25-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00216/f00216_2013-03-21-10-25-37.json', 
]
c_shockR = aba.loadMultipleDataFiles(c_shockR)
 
c_shockS = [
'/home/vburns/Dropbox/ConchisData/2013-03-21/f00209/f00209_2013-03-21-11-15-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00210/f00210_2013-03-21-11-15-16.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00211/f00211_2013-03-21-11-15-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00212/f00212_2013-03-21-11-15-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00213/f00213_2013-03-21-11-19-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00214/f00214_2013-03-21-11-19-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00215/f00215_2013-03-21-11-19-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00216/f00216_2013-03-21-11-19-39.json'
]
c_shockS= aba.loadMultipleDataFiles(c_shockS)

c_shockN = [
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00209/f00209_2013-03-21-12-20-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00210/f00210_2013-03-21-12-20-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00211/f00211_2013-03-21-12-20-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00212/f00212_2013-03-21-12-20-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00213/f00213_2013-03-21-12-24-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00214/f00214_2013-03-21-12-24-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00215/f00215_2013-03-21-12-24-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00216/f00216_2013-03-21-12-24-29.json',
]
c_shockN = aba.loadMultipleDataFiles(c_shockN)

c_shockS2= [
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00209/f00209_2013-03-21-13-22-56.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00210/f00210_2013-03-21-13-22-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00211/f00211_2013-03-21-13-22-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00212/f00212_2013-03-21-13-22-50.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00213/f00213_2013-03-21-13-26-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00214/f00214_2013-03-21-13-26-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00215/f00215_2013-03-21-13-26-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00216/f00216_2013-03-21-13-26-27.json'
]
c_shockS2 = aba.loadMultipleDataFiles(c_shockS2)


import pylab
import scipy

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
n=5
minutes = n * 60
e_maxtimes = []
for n in range(len(e_shockR)):
    mtime = getmintime(e_shockR[n])
    e_maxtimes.append(mtime)
e_mintimes = [x - minutes for x in e_maxtimes]

eBaseVelEnd = []
for n in range(len(e_shockR)):
    velocity = getVelRaw(e_shockR[n], (e_mintimes[n], e_maxtimes[n]))
    eBaseVelEnd.append(np.median(velocity))

c_maxtimes = []
for n in range(len(c_shockR)):
    mtime = getmintime(c_shockR[n])
    c_maxtimes.append(mtime)
c_mintimes = [x - minutes for x in c_maxtimes]

cBaseVelEnd = []
for n in range(len(c_shockR)):
    cvelocity = getVelRaw(c_shockR[n], (c_mintimes[n], c_maxtimes[n]))
    cBaseVelEnd.append(np.median(cvelocity))

#velocity locomation analysis
eBaseVelStart = getVelMulti(e_shockR, (0,900))
#for eBaseVelEnd, see function to take exactly last 5 min
#eSameTank = getVelMulti(e_shockS)
#eNovelTank = getVelMulti(e_shockN)
#eSameTank2 = getVelMulti(e_shockS2)
start = 60*30
end = 60*60
eSameTank = getVelMulti(e_shockS, (start, end))
eNovelTank = getVelMulti(e_shockN, (start, end))
eSameTank2 = getVelMulti(e_shockS2, (start, end))

cBaseVelStart = getVelMulti(c_shockR, (0,900))
#for cBaseVelEnd, see function to take exactly last 5 min
#cSameTank = getVelMulti(c_shockS)
#cNovelTank = getVelMulti(c_shockN)
#cSameTank2 = getVelMulti(c_shockS2)
cSameTank = getVelMulti(c_shockS, (start, end))
cNovelTank = getVelMulti(c_shockN, (start, end))
cSameTank2 = getVelMulti(c_shockS2, (start, end))
"""
#same context
[tv, e_Base_RTN] = scipy.stats.ttest_ind(eBaseVelN, eLHVelN)
[tv, e_Base_Nov] = scipy.stats.ttest_ind(eBaseVelN, eVellate)
[tv, e_shockN_LH] = scipy.stats.ttest_ind(eShockVelN, eLHVelN)
[tv, e_shockN_Nov] = scipy.stats.ttest_ind(eShockVelN, eVellate)
[tv, e_LH_Nov] = scipy.stats.ttest_ind(eLHVelN, eVellate)
#red tanks
[tv, e_Base_RT2] = scipy.stats.ttest_ind(eBaseVelR, eLHVelR)
[tv, e_shockN_LH2] = scipy.stats.ttest_ind(eShockR, eLHVelR)

#comparisons 
[tv, e_shockN_Shock] = scipy.stats.ttest_ind(eLHVelN, eLHVelR)

print 'Statistics comparing velocities baseline/RT, last 15 min Shock/RT, RT/last 15 min Nov, baseline/novel experimental in same context with pipeting: ', e_Base_RTN, e_shockN_LH, e_LH_Nov, e_Base_Nov
print 'Statistics comparing velocities baseline/RT, last 15 min Shock/RT, experimental in new context  with pipeting: ', e_Base_RT2, e_shockN_LH2, 
print 'Statistics comparing velocity between pippetted RT and novel context RT:', e_shockN_Shock

#fix
eLHVelR = np.insert(eLHVelR, 3, None)
"""
#convert to array
eBVS = np.array([np.array([eBaseVelStart[n]]) for n in range(len(eBaseVelStart))])
eBVE = np.array([np.array([eBaseVelEnd[n]]) for n in range(len(eBaseVelEnd))])
eST = np.array([np.array([eSameTank[n]]) for n in range(len(eSameTank))])
eNT = np.array([np.array([eNovelTank[n]]) for n in range(len(eNovelTank))])
eST2  = np.array([np.array([eSameTank2[n]]) for n in range(len(eSameTank2))])
cBVS = np.array([np.array([cBaseVelStart[n]]) for n in range(len(cBaseVelStart))])
cBVE = np.array([np.array([cBaseVelEnd[n]]) for n in range(len(cBaseVelEnd))])
cST = np.array([np.array([cSameTank[n]]) for n in range(len(cSameTank))])
cNT = np.array([np.array([cNovelTank[n]]) for n in range(len(cNovelTank))])
cST2  = np.array([np.array([cSameTank2[n]]) for n in range(len(cSameTank2))])

experimental = np.transpose(np.hstack((eBVS, eBVE, eST, eNT, eST2)))
control = np.transpose(np.hstack((cBVS, cBVE, cST, cNT, cST2)))

pylab.figure()
pylab.suptitle('Learned Helplessness Assay - LH/Same Tank/Novel Tank/Same Tank')
ax = pylab.subplot(1,2,1)
pylab.plot(experimental)
pylab.plot(0, [eBaseVelStart], 'r.')
pylab.plot(1, [eBaseVelEnd], 'r.')
pylab.plot(2,[eSameTank], 'r.')
pylab.plot(3,[eNovelTank], 'r.')
pylab.plot(4,[eSameTank2],'r.')
pylab.plot([0,1,2,3,4],[np.mean(eBaseVelStart), np.mean(eBaseVelEnd), scipy.stats.nanmean(eSameTank),scipy.stats.nanmean(eNovelTank), np.mean(eSameTank2)],'o-k', lw=3)
ax.set_xticks((0,1,2,3,4))
ax.set_xticklabels(('baseline', 'last 5 min\n(shock)', 'same tank\n 1 hour','novel tank\n1 hour', 'same tank\n1 hour'))
pylab.xlim((-.25,4.5))
pylab.ylim((0, 2.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish')
patch1 = mpl.patches.Rectangle((2.5,0), 1,5, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,2,2)
pylab.plot(control)
pylab.plot(0, [cBaseVelStart], 'r.')
pylab.plot(1, [cBaseVelEnd], 'r.')
pylab.plot(2,[cSameTank], 'r.')
pylab.plot(3,[cNovelTank], 'r.')
pylab.plot(4,[cSameTank2],'r.')
pylab.plot([0,1,2,3,4],[np.mean(cBaseVelStart), np.mean(cBaseVelEnd), np.mean(cSameTank),scipy.stats.nanmean(cNovelTank), np.mean(cSameTank2)],'o-k', lw=3)
ax.set_xticks((0,1,2,3,4))
ax.set_xticklabels(('baseline', 'last 5 min\n(shock)', 'same tank\n 1 hour','novel tank\n1 hour', 'same tank\n1 hour'))
pylab.xlim((-.25,4.5))
pylab.ylim((0,2.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Control fish')
patch3 = mpl.patches.Rectangle((2.5,0), 1,5, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch3)


"""
pylab.figure(41)
wid = 0.5
xvalues = range(1,2*len(experimental)+1,2)
shift = [x+wid for x in xvalues]
shift.pop(len(shift)-1)
pylab.bar(xvalues, (np.mean(eBaseVelN), np.mean(eStartShockVelN), np.mean(eShockVelN),scipy.stats.nanmean(eLHVelN), np.mean(eVellate)), color = 'm', width = 0.5, align = 'center', label = 'same context')
pylab.bar(shift, (np.mean(eBaseVelR), np.mean(eStartShockR), np.mean(eShockR),scipy.stats.nanmean(eLHVelR)), color = 'g', width = 0.5, align = 'center', label = 'novel context')
pylab.errorbar(xvalues,(np.mean(eBaseVelN), np.mean(eStartShockVelN), np.mean(eShockVelN),scipy.stats.nanmean(eLHVelN), np.mean(eVellate)),yerr=(2*scipy.stats.sem(eBaseVelN),2*scipy.stats.sem(eStartShockVelN),2*scipy.stats.sem(eShockVelN),2*scipy.stats.sem(eLHVelN),2*scipy.stats.sem(eVellate)), fmt = None, ecolor = 'k')
pylab.errorbar(shift,(np.mean(eBaseVelR), np.mean(eStartShockR), np.mean(eShockR),scipy.stats.nanmean(eLHVelR)), yerr=(2*scipy.stats.sem(eBaseVelR),2*scipy.stats.sem(eStartShockR),2*scipy.stats.sem(eShockR),2*scipy.stats.sem(eLHVelR)),fmt = None, ecolor = 'k')
pylab.ylim((0,3))
pylab.title('Velocity Summary')
pylab.legend()
pylab.ylabel('Mean Velocities (mm/s)')
labels = ['    baseline', '    shock', '    late\n    shock', '    RTS', '    late\n    nov']
pylab.xticks(xvalues, labels)
"""
pylab.show()
