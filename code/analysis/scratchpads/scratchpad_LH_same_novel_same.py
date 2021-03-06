import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot

#first 15 min is baseline, then 60 bouts of 60 sec shocking (30 bouts total), then 5 min post
e_shockR = [
'/home/vburns/Dropbox/ConchisData/2013-03-21/f00217/f00217_2013-03-21-14-35-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00218/f00218_2013-03-21-14-35-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00219/f00219_2013-03-21-14-35-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00220/f00220_2013-03-21-14-35-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00221/f00221_2013-03-21-14-37-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00222/f00222_2013-03-21-14-37-16.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00223/f00223_2013-03-21-14-37-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00224/f00224_2013-03-21-14-37-23.json', 
]
e_shockR = aba.loadMultipleDataFiles(e_shockR)

e_shockS = [
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00217/f00217_2013-03-21-15-29-22.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00218/f00218_2013-03-21-15-29-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00219/f00219_2013-03-21-15-30-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00220/f00220_2013-03-21-15-29-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00221/f00221_2013-03-21-15-31-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00222/f00222_2013-03-21-15-31-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00223/f00223_2013-03-21-15-32-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00224/f00224_2013-03-21-15-32-12.json',
]
e_shockS= aba.loadMultipleDataFiles(e_shockS)

e_shockN = [
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00217/f00217_2013-03-21-16-33-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00218/f00218_2013-03-21-16-33-24.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00219/f00219_2013-03-21-16-33-22.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00220/f00220_2013-03-21-16-33-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00221/f00221_2013-03-21-16-33-38.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00222/f00222_2013-03-21-16-33-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00223/f00223_2013-03-21-16-34-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00224/f00224_2013-03-21-16-34-16.json', 
]
e_shockN = aba.loadMultipleDataFiles(e_shockN)

e_shockS2= [
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00217/f00217_2013-03-21-17-35-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00218/f00218_2013-03-21-17-35-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00219/f00219_2013-03-21-17-35-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00220/f00220_2013-03-21-17-35-56.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00221/f00221_2013-03-21-17-37-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00222/f00222_2013-03-21-17-37-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00223/f00223_2013-03-21-17-37-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-21/f00224/f00224_2013-03-21-17-37-38.json'
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
    velocity = aba.getVelRaw(e_shockR[n], (e_mintimes[n], e_maxtimes[n]))
    eBaseVelEnd.append(np.median(velocity))

c_maxtimes = []
for n in range(len(c_shockR)):
    mtime = getmintime(c_shockR[n])
    c_maxtimes.append(mtime)
c_mintimes = [x - minutes for x in c_maxtimes]

cBaseVelEnd = []
for n in range(len(c_shockR)):
    cvelocity = aba.getVelRaw(c_shockR[n], (c_mintimes[n], c_maxtimes[n]))
    cBaseVelEnd.append(np.median(cvelocity))

#velocity locomation analysis
eBaseVelStart1 = aba.getVelMulti(e_shockR, (0,450))
eBaseVelStart2 = aba.getVelMulti(e_shockR, (450,900))
eBaseVel = aba.getVelMulti(e_shockR, (900,1800))
eBaseVel2 = aba.getVelMulti(e_shockR, (1800,2700))
#for eBaseVelEnd, see function to take exactly last 5 min
#eSameTank = aba.getVelMulti(e_shockS)
eSameTank = aba.getVelMulti(e_shockS, (0,900))
eSameTank2 = aba.getVelMulti(e_shockS, (900,1800))
eSameTank3 = aba.getVelMulti(e_shockS, (1800,2700))
eSameTank4 = aba.getVelMulti(e_shockS, (2700,3600))
#eNovelTank = aba.getVelMulti(e_shockN)
eNovelTank = aba.getVelMulti(e_shockN, (0,900))
eNovelTank2 = aba.getVelMulti(e_shockN, (900,1800))
eNovelTank3 = aba.getVelMulti(e_shockN, (1800,2700))
eNovelTank4 = aba.getVelMulti(e_shockN, (2700,3600))
#eSameTank2 = aba.getVelMulti(e_shockS2)
eSameTank22 = aba.getVelMulti(e_shockS2, (0,900))
eSameTank222 = aba.getVelMulti(e_shockS2, (900,1800))
eSameTank223 = aba.getVelMulti(e_shockS2, (1800,2700))
eSameTank224 = aba.getVelMulti(e_shockS2, (2700,3600))
cBaseVelStart1 = aba.getVelMulti(c_shockR, (0,450))
cBaseVelStart2 = aba.getVelMulti(c_shockR, (450,900))
cBaseVel = aba.getVelMulti(c_shockR, (900,1800))
cBaseVel2 = aba.getVelMulti(c_shockR, (900,2700))
#for cBaseVelEnd, see function to take exactly last 5 min
#cSameTank = aba.getVelMulti(c_shockS)
#cNovelTank = aba.getVelMulti(c_shockN)
#cSameTank2 = aba.getVelMulti(c_shockS2)
cSameTank = aba.getVelMulti(c_shockS, (0,900))
cSameTank2 = aba.getVelMulti(c_shockS, (900,1800))
cSameTank3 = aba.getVelMulti(c_shockS, (1800,2700))
cSameTank4 = aba.getVelMulti(c_shockS, (2700,3600))
cNovelTank = aba.getVelMulti(c_shockN, (0,900))
cNovelTank2 = aba.getVelMulti(c_shockN, (900,1800))
cNovelTank3 = aba.getVelMulti(c_shockN, (1800,2700))
cNovelTank4 = aba.getVelMulti(c_shockN, (2700,3600))
cSameTank22 = aba.getVelMulti(c_shockS2, (0,900))
cSameTank222 = aba.getVelMulti(c_shockS2, (900,1800))
cSameTank223 = aba.getVelMulti(c_shockS2, (1800,2700))
cSameTank224 = aba.getVelMulti(c_shockS2, (2700,3600))

eSameTank[5] =np.nan
eSameTank2[5] =np.nan
eSameTank3[5] =np.nan
eSameTank4[5] =np.nan

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
eBVS = np.array([np.array([eBaseVelStart1[n]]) for n in range(len(eBaseVelStart1))])
eBVS2 = np.array([np.array([eBaseVelStart2[n]]) for n in range(len(eBaseVelStart2))])
eBV = np.array([np.array([eBaseVel[n]]) for n in range(len(eBaseVel))])
eBV2 = np.array([np.array([eBaseVel2[n]]) for n in range(len(eBaseVel2))])
eBVE = np.array([np.array([eBaseVelEnd[n]]) for n in range(len(eBaseVelEnd))])
eST = np.array([np.array([eSameTank[n]]) for n in range(len(eSameTank))])
eST2 = np.array([np.array([eSameTank2[n]]) for n in range(len(eSameTank))])
eST3 = np.array([np.array([eSameTank3[n]]) for n in range(len(eSameTank))])
eST4 = np.array([np.array([eSameTank4[n]]) for n in range(len(eSameTank))])
eNT = np.array([np.array([eNovelTank[n]]) for n in range(len(eNovelTank))])
eNT2 = np.array([np.array([eNovelTank2[n]]) for n in range(len(eNovelTank))])
eNT3 = np.array([np.array([eNovelTank3[n]]) for n in range(len(eNovelTank))])
eNT4 = np.array([np.array([eNovelTank4[n]]) for n in range(len(eNovelTank))])
eST22  = np.array([np.array([eSameTank22[n]]) for n in range(len(eSameTank2))])
eST222  = np.array([np.array([eSameTank222[n]]) for n in range(len(eSameTank2))])
eST223  = np.array([np.array([eSameTank223[n]]) for n in range(len(eSameTank2))])
eST224  = np.array([np.array([eSameTank224[n]]) for n in range(len(eSameTank2))])
cBVS = np.array([np.array([cBaseVelStart1[n]]) for n in range(len(cBaseVelStart1))])
cBVS2 = np.array([np.array([cBaseVelStart2[n]]) for n in range(len(cBaseVelStart2))])
cBV = np.array([np.array([cBaseVel[n]]) for n in range(len(cBaseVel))])
cBV2 = np.array([np.array([cBaseVel2[n]]) for n in range(len(cBaseVel2))])
cBVE = np.array([np.array([cBaseVelEnd[n]]) for n in range(len(cBaseVelEnd))])
cST = np.array([np.array([cSameTank[n]]) for n in range(len(cSameTank))])
cST2 = np.array([np.array([cSameTank2[n]]) for n in range(len(cSameTank))])
cST3 = np.array([np.array([cSameTank3[n]]) for n in range(len(cSameTank))])
cST4 = np.array([np.array([cSameTank4[n]]) for n in range(len(cSameTank))])
cNT = np.array([np.array([cNovelTank[n]]) for n in range(len(cNovelTank))])
cNT2 = np.array([np.array([cNovelTank2[n]]) for n in range(len(cNovelTank))])
cNT3 = np.array([np.array([cNovelTank3[n]]) for n in range(len(cNovelTank))])
cNT4 = np.array([np.array([cNovelTank4[n]]) for n in range(len(cNovelTank))])
cST22  = np.array([np.array([cSameTank22[n]]) for n in range(len(cSameTank2))])
cST222  = np.array([np.array([cSameTank222[n]]) for n in range(len(cSameTank2))])
cST223  = np.array([np.array([cSameTank223[n]]) for n in range(len(cSameTank2))])
cST224  = np.array([np.array([cSameTank224[n]]) for n in range(len(cSameTank2))])

experimental = np.transpose(np.hstack((eBVS, eBVS2, eBV, eBV2, eBVE, eST, eST2, eST3, eST4, eNT, eNT2, eNT3, eNT4, eST22, eST222, eST223, eST224)))
control = np.transpose(np.hstack((cBVS, cBVS2, cBV, cBV2, cBVE, cST, cST2, cST3, cST4, cNT, cNT2, cNT3, cNT4, cST22, cST222, cST223, cST224)))

pylab.figure()
pylab.suptitle('Learned Helplessness Assay - LH/Same Tank/Novel Tank/Same Tank')
ax = pylab.subplot(1,1,1)
pylab.plot(experimental)
pylab.plot(0, [eBaseVelStart1], 'r.')
pylab.plot(1, [eBaseVelStart2], 'r')
pylab.plot(2, [eBaseVel], 'r')
pylab.plot(3, [eBaseVel2], 'r')
pylab.plot(4, [eBaseVelEnd], 'r.')
pylab.plot(5,[eSameTank], 'r.')
pylab.plot(6,[eSameTank2], 'r.')
pylab.plot(7,[eSameTank3], 'r.')
pylab.plot(8,[eSameTank4], 'r.')
pylab.plot(9,[eNovelTank], 'r.')
pylab.plot(10,[eNovelTank2], 'r.')
pylab.plot(11,[eNovelTank3], 'r.')
pylab.plot(12,[eNovelTank4], 'r.')
pylab.plot(13,[eSameTank22],'r.')
pylab.plot(14,[eSameTank222],'r.')
pylab.plot(15,[eSameTank223],'r.')
pylab.plot(16,[eSameTank224],'r.')
pylab.plot([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[np.mean(eBaseVelStart1), np.mean(eBaseVelStart2), np.mean(eBaseVel), np.mean(eBaseVel2), np.mean(eBaseVelEnd), scipy.stats.nanmean(eSameTank),scipy.stats.nanmean(eSameTank2), scipy.stats.nanmean(eSameTank3), scipy.stats.nanmean(eSameTank4), scipy.stats.nanmean(eNovelTank), scipy.stats.nanmean(eNovelTank2), scipy.stats.nanmean(eNovelTank3), scipy.stats.nanmean(eNovelTank4), np.mean(eSameTank22), np.mean(eSameTank222), np.mean(eSameTank223), np.mean(eSameTank224)],'o-k', lw=3)
ax.set_xticks((0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,16))
ax.set_xticklabels(('baseline', 'last 5 min\n(shock)', 'same tank\n 15','same tank 30', 'same tank45', 'same tank 60', 'novel tank\n15', 'nove tank 30', 'novel 45', 'novel 60', 'same tank\n1 hour'))
pylab.xlim((-.25,16.5))
pylab.ylim((0,6))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish')
patch1 = mpl.patches.Rectangle((8.5,0), 4,5, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
pylab.figure(2)
ax1 = pylab.subplot(1,1,1)
pylab.plot(control)
pylab.plot(0, [cBaseVelStart1], 'r.')
pylab.plot(1, [cBaseVelStart2], 'r')
pylab.plot(2, [cBaseVel], 'r')
pylab.plot(3, [cBaseVel2],'r')
pylab.plot(4, [cBaseVelEnd], 'r.')
pylab.plot(5,[cSameTank], 'r.')
pylab.plot(6,[cSameTank2], 'r.')
pylab.plot(7,[cSameTank3], 'r.')
pylab.plot(8,[cSameTank4], 'r.')
pylab.plot(9,[cNovelTank], 'r.')
pylab.plot(10,[cNovelTank2], 'r.')
pylab.plot(11,[cNovelTank3], 'r.')
pylab.plot(12,[cNovelTank4], 'r.')
pylab.plot(13,[cSameTank22],'r.')
pylab.plot(14,[cSameTank222],'r.')
pylab.plot(15,[cSameTank223],'r.')
pylab.plot(16,[cSameTank224],'r.')
pylab.plot([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],[np.mean(cBaseVelStart1), np.mean(cBaseVelStart2), np.mean(cBaseVel), np.mean(cBaseVel2), np.mean(cBaseVelEnd), scipy.stats.nanmean(cSameTank),scipy.stats.nanmean(cSameTank2), scipy.stats.nanmean(cSameTank3), scipy.stats.nanmean(cSameTank4), scipy.stats.nanmean(cNovelTank), scipy.stats.nanmean(cNovelTank2), scipy.stats.nanmean(cNovelTank3), scipy.stats.nanmean(cNovelTank4), np.mean(cSameTank22), np.mean(cSameTank222), np.mean(cSameTank223), np.mean(cSameTank224)],'o-k', lw=3)
#pylab.plot([0,1,2,3,4],[np.mean(cBaseVelStart), np.mean(cBaseVelEnd), np.mean(cSameTank),scipy.stats.nanmean(cNovelTank), np.mean(cSameTank2)],'o-k', lw=3)
ax1.set_xticks((0,1,2,3,4,6,7,8,9,10,11,12,13, 14, 15, 16))
ax1.set_xticklabels(('baseline', 'last 5 min\n(shock)', 'same tank\n 15','same tank 30', 'same tank45', 'same tank 60', 'novel tank\n15', 'nove tank 30', 'novel 45', 'novel 60', 'same tank\n1 hour'))
pylab.xlim((-.25,16.5))
pylab.ylim((0, 6))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Control fish')
patch3 = mpl.patches.Rectangle((8.5,0), 4,5, color = 'g', fill=True, alpha=0.5)
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
