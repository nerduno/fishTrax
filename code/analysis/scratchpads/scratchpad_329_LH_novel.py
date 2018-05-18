import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy


#first is shocking, second is 15 min in novel context 
e_shock5 = [
'/home/vburns/Dropbox/ConchisData/2013-03-30/f00263/f00263_2013-03-30-14-13-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00264/f00264_2013-03-30-14-13-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00265/f00265_2013-03-30-14-13-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00266/f00266_2013-03-30-14-13-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00267/f00267_2013-03-30-14-15-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00268/f00268_2013-03-30-14-15-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00269/f00269_2013-03-30-14-15-24.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00270/f00270_2013-03-30-14-15-21.json',
]
e_shock5 = aba.loadMultipleDataFiles(e_shock5)

e_shock25 = [
'/home/vburns/Dropbox/ConchisData/2013-03-30/f00271/f00271_2013-03-30-15-33-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00272/f00272_2013-03-30-15-33-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00273/f00273_2013-03-30-15-33-29.json',
# '/home/vburns/Dropbox/ConchisData/2013-03-30/f00274/f00274_2013-03-30-15-33-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00275/f00275_2013-03-30-15-35-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00276/f00276_2013-03-30-15-35-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00277/f00277_2013-03-30-15-34-59.json',
# '/home/vburns/Dropbox/ConchisData/2013-03-30/f00278/f00278_2013-03-30-15-34-57.json',
]
e_shock25= aba.loadMultipleDataFiles(e_shock25)

e_novel5 = [
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00263/f00263_2013-03-30-15-06-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00264/f00264_2013-03-30-15-06-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00265/f00265_2013-03-30-15-09-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00266/f00266_2013-03-30-15-09-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00267/f00267_2013-03-30-15-09-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00268/f00268_2013-03-30-15-09-58.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00269/f00269_2013-03-30-15-10-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00270/f00270_2013-03-30-15-10-19.json'
]
e_novel5 = aba.loadMultipleDataFiles(e_novel5)

e_novel25 = [
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00271/f00271_2013-03-30-16-27-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00272/f00272_2013-03-30-16-27-37.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00273/f00273_2013-03-30-16-27-39.json',
# '/home/vburns/Dropbox/ConchisData/2013-03-30/f00274/f00274_2013-03-30-16-27-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00275/f00275_2013-03-30-16-29-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00276/f00276_2013-03-30-16-29-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00277/f00277_2013-03-30-16-29-05.json',
# '/home/vburns/Dropbox/ConchisData/2013-03-30/f00278/f00278_2013-03-30-16-29-08.json'
]
e_novel25 = aba.loadMultipleDataFiles(e_novel25)

c_shock = [
'/home/vburns/Dropbox/ConchisData/2013-03-30/f00287/f00287_2013-03-30-18-48-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00288/f00288_2013-03-30-18-48-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00289/f00289_2013-03-30-18-48-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00290/f00290_2013-03-30-18-48-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00291/f00291_2013-03-30-18-50-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00292/f00292_2013-03-30-18-50-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00293/f00293_2013-03-30-18-50-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00294/f00294_2013-03-30-18-50-27.json',
]
c_shock = aba.loadMultipleDataFiles(c_shock)
 
c_novel = [
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00287/f00287_2013-03-30-19-42-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00288/f00288_2013-03-30-19-42-16.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00289/f00289_2013-03-30-19-42-22.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00290/f00290_2013-03-30-19-43-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00291/f00291_2013-03-30-19-43-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00292/f00292_2013-03-30-19-43-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00293/f00293_2013-03-30-19-44-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00294/f00294_2013-03-30-19-44-14.json'
]
c_novel = aba.loadMultipleDataFiles(c_novel)


#velocity analysis 
endWinLen = 5 * 60; #seconds
sm = 15; #smooth over 15 frames.

eEndVel5 = aba.getMedianVelMulti(e_shock5, tRange=[-endWinLen,-0], smoothWinLen=sm)
eEndVel25 = aba.getMedianVelMulti(e_shock25, tRange=[-endWinLen,-0], smoothWinLen=sm)
cEndVel = aba.getMedianVelMulti(c_shock, tRange=[-endWinLen,-0], smoothWinLen = sm)

baseWinLen = 15*60
eBaseVel25 = aba.getVelMulti(e_shock25, tRange=(0,baseWinLen), smoothWinLen=sm)
eBaseVel5 = aba.getVelMulti(e_shock5, tRange=(0,baseWinLen), smoothWinLen=sm)
cBaseVel = aba.getVelMulti(c_shock, tRange=(0,baseWinLen), smoothWinLen=sm)

eNovel25 = aba.getVelMulti(e_novel25, smoothWinLen=sm)
eNovel5 = aba.getVelMulti(e_novel5, smoothWinLen=sm)
cNovel = aba.getVelMulti(c_novel, smoothWinLen=sm)

#same context
[tv, e_statBase25] = scipy.stats.ttest_ind(eBaseVel25, cBaseVel)
[tv, e_statBase5] = scipy.stats.ttest_ind(eBaseVel5, cBaseVel)

[tv, e_statEnd25] = scipy.stats.ttest_ind(eEndVel25, cEndVel)
[tv, e_statEnd5] = scipy.stats.ttest_ind(eEndVel5, cEndVel)

[tv, e_statNovel25] = scipy.stats.ttest_ind(eNovel25, cNovel)
[tv, e_statNovel5] = scipy.stats.ttest_ind(eNovel5, cNovel)

print 'Statistics comparing velocities baseline to controls (2.5, 5): ', e_statBase25, e_statBase5
print 'Statistics comparing velocities last 5 min to controls (2.5, 5): ', e_statEnd25, e_statEnd5
print 'Statistics comparing velocities novel tank to controls (2.5, 5): ', e_statNovel25, e_statNovel5
"""
#fix
eNovel25 = np.insert(eNovel25, 3, None)
eBaseVel25 = np.insert(eBaseVel25, 4, None)
"""
#convert to array
eBV25 = np.array([np.array([eBaseVel25[n]]) for n in range(len(eBaseVel25))])
eBV5 = np.array([np.array([eBaseVel5[n]]) for n in range(len(eBaseVel5))])
cBV = np.array([np.array([cBaseVel[n]]) for n in range(len(cBaseVel))])

eSV25 = np.array([np.array([eEndVel25[n]]) for n in range(len(eEndVel25))])
eSV5 = np.array([np.array([eEndVel5[n]]) for n in range(len(eEndVel5))])
cSV = np.array([np.array([cEndVel[n]]) for n in range(len(cEndVel))])

eN25 = np.array([np.array([eNovel25[n]]) for n in range(len(eNovel25))])
eN5 = np.array([np.array([eNovel5[n]]) for n in range(len(eNovel5))])
cN = np.array([np.array([cNovel[n]]) for n in range(len(cNovel))])

experimental25 = np.transpose(np.hstack((eBV25, eSV25, eN25)))
experimental5 = np.transpose(np.hstack((eBV5, eSV5, eN5)))
control = np.transpose(np.hstack((cBV, cSV, cN)))

pylab.figure()
pylab.suptitle('Learned Helplessness Assay - Shocking, 15min novel')
ax = pylab.subplot(1,3,1)
pylab.plot(experimental25)
pylab.plot(0, [eBaseVel25], 'r.')
pylab.plot(1,[eEndVel25],'r.')
pylab.plot(2,[eNovel25],'r.')
pylab.plot([0,1,2],[np.mean(eBaseVel25), np.mean(eEndVel25), scipy.stats.nanmean(eNovel25)],'o-k', lw=3)
ax.set_xticks((0,1,2))
ax.set_xticklabels(('baseline', 'last 5 min\n(shock)', 'novel tank\n 15'))
pylab.xlim((-.25,2.5))
pylab.ylim((0,4.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 2.5V')
patch1 = mpl.patches.Rectangle((1.5,0), 1,5, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,3,2)
pylab.plot(experimental5)
pylab.plot(0, [eBaseVel5], 'r.')
pylab.plot(1,[eEndVel5],'r.')
pylab.plot(2,[eNovel5],'r.')
pylab.plot([0,1,2],[np.mean(eBaseVel5), np.mean(eEndVel5), np.mean(eNovel5)],'o-k', lw=3)
ax.set_xticks((0,1,2))
ax.set_xticklabels(('baseline', 'last 5 min\n(shock)', 'novel tank\n 15'))
pylab.xlim((-.25,2.5))
pylab.ylim((0,4.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 5V')
patch1 = mpl.patches.Rectangle((1.5,0), 1,5, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,3,3)
pylab.plot(control)
pylab.plot(0, [cBaseVel], 'r.')
pylab.plot(1,[cEndVel],'r.')
pylab.plot(2,[cNovel],'r.')
pylab.plot([0,1,2],[np.mean(cBaseVel), np.mean(cEndVel), np.mean(cNovel)],'o-k', lw=3)
ax.set_xticks((0,1,2))
ax.set_xticklabels(('baseline', 'last 5 min\n(shock)', 'novel tank\n 15'))
pylab.xlim((-.25,2.5))
pylab.ylim((0,4.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Control fish')
patch1 = mpl.patches.Rectangle((1.5,0), 1,5, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)

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
