import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

#first is 30 min in safe tank, then standard shocking, then 30 min in safe tank
#held out of safe tank for approx 10 sec (two pipets + pouring time)
e_safe5_first= [
'/home/vburns/Dropbox/ConchisData/2013-06-13/f00514/f00514_2013-06-13-13-22-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00515/f00515_2013-06-13-13-22-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00516/f00516_2013-06-13-13-22-37.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00517/f00517_2013-06-13-13-22-45.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-13/f00518/f00518_2013-06-13-13-25-44.json', #low starting velocity
# '/home/vburns/Dropbox/ConchisData/2013-06-13/f00519/f00519_2013-06-13-13-25-49.json', #low starting velocity
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00520/f00520_2013-06-13-13-25-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00521/f00521_2013-06-13-13-26-01.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-14/f00530/f00530_2013-06-14-13-15-42.json', #poor tracking?
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00531/f00531_2013-06-14-13-15-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00532/f00532_2013-06-14-13-15-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00533/f00533_2013-06-14-13-16-07.json',
#'/home/vburns/Dropbox/ConchisData/2013-06-14/f00534/f00534_2013-06-14-13-17-09.json', #current imbalance
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00535/f00535_2013-06-14-13-17-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00536/f00536_2013-06-14-13-17-30.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-14/f00537/f00537_2013-06-14-13-17-34.json', #low velocity in base
]
e_safe5_first = aba.loadMultipleDataFiles(e_safe5_first)

e_shock5 = [
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00514/f00514_2013-06-13-13-54-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00515/f00515_2013-06-13-13-54-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00516/f00516_2013-06-13-13-54-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00517/f00517_2013-06-13-13-53-54.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-13/f00518/f00518_2013-06-13-13-57-02.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-13/f00519/f00519_2013-06-13-13-57-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00520/f00520_2013-06-13-13-57-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00521/f00521_2013-06-13-13-57-43.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-14/f00530/f00530_2013-06-14-13-48-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00531/f00531_2013-06-14-13-47-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00532/f00532_2013-06-14-13-47-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00533/f00533_2013-06-14-13-47-41.json',
#'/home/vburns/Dropbox/ConchisData/2013-06-14/f00534/f00534_2013-06-14-13-49-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00535/f00535_2013-06-14-13-49-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00536/f00536_2013-06-14-13-48-59.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-14/f00537/f00537_2013-06-14-13-48-52.json',
]
e_shock5 = aba.loadMultipleDataFiles(e_shock5)

e_safe5_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00514/f00514_2013-06-13-14-49-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00515/f00515_2013-06-13-14-49-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00516/f00516_2013-06-13-14-49-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00517/f00517_2013-06-13-14-49-01.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-13/f00518/f00518_2013-06-13-14-51-36.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-13/f00519/f00519_2013-06-13-14-51-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00520/f00520_2013-06-13-14-51-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00521/f00521_2013-06-13-14-51-56.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-14/f00530/f00530_2013-06-14-14-42-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00531/f00531_2013-06-14-14-42-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00532/f00532_2013-06-14-14-42-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00533/f00533_2013-06-14-14-42-29.json',
#'/home/vburns/Dropbox/ConchisData/2013-06-14/f00534/f00534_2013-06-14-14-45-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00535/f00535_2013-06-14-14-45-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00536/f00536_2013-06-14-14-45-19.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-14/f00537/f00537_2013-06-14-14-45-14.json',
]
e_safe5_sec = aba.loadMultipleDataFiles(e_safe5_sec)


#no clicking control
c_safe_first = [
'/home/vburns/Dropbox/ConchisData/2013-06-13/f00506/f00506_2013-06-13-11-16-34.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-13/f00507/f00507_2013-06-13-11-16-38.json', #low starting velocity
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00508/f00508_2013-06-13-11-16-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00509/f00509_2013-06-13-11-16-59.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00510/f00510_2013-06-13-11-18-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00512/f00512_2013-06-13-11-18-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00513/f00513_2013-06-13-11-18-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00522/f00522_2013-06-14-11-07-55.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-14/f00523/f00523_2013-06-14-11-07-49.json', #low starting velocity
# '/home/vburns/Dropbox/ConchisData/2013-06-14/f00524/f00524_2013-06-14-11-07-43.json', #low starting velocity
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00525/f00525_2013-06-14-11-07-37.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00526/f00526_2013-06-14-11-09-24.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00527/f00527_2013-06-14-11-09-22.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-14/f00528/f00528_2013-06-14-11-09-20.json', #low starting velocity
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00529/f00529_2013-06-14-11-09-18.json',

]
c_safe_first = aba.loadMultipleDataFiles(c_safe_first)

c_shock = [
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00506/f00506_2013-06-13-11-50-55.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-13/f00507/f00507_2013-06-13-11-51-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00508/f00508_2013-06-13-11-51-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00509/f00509_2013-06-13-11-51-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00510/f00510_2013-06-13-11-52-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00512/f00512_2013-06-13-11-52-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00513/f00513_2013-06-13-11-52-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00522/f00522_2013-06-14-11-45-33.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-14/f00523/f00523_2013-06-14-11-45-31.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-14/f00524/f00524_2013-06-14-11-45-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00525/f00525_2013-06-14-11-45-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00526/f00526_2013-06-14-11-47-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00527/f00527_2013-06-14-11-47-36.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-14/f00528/f00528_2013-06-14-11-47-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00529/f00529_2013-06-14-11-47-19.json',
]
c_shock = aba.loadMultipleDataFiles(c_shock)
 
c_safe_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00506/f00506_2013-06-13-12-38-06.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-13/f00507/f00507_2013-06-13-12-38-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00508/f00508_2013-06-13-12-38-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00509/f00509_2013-06-13-12-38-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00510/f00510_2013-06-13-12-39-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00512/f00512_2013-06-13-12-39-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-13/f00513/f00513_2013-06-13-12-39-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00522/f00522_2013-06-14-12-32-59.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-14/f00523/f00523_2013-06-14-12-33-05.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-14/f00524/f00524_2013-06-14-12-33-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00525/f00525_2013-06-14-12-33-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00526/f00526_2013-06-14-12-34-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00527/f00527_2013-06-14-12-34-53.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-14/f00528/f00528_2013-06-14-12-35-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-14/f00529/f00529_2013-06-14-12-35-05.json',
]
c_safe_sec = aba.loadMultipleDataFiles(c_safe_sec)

#velocity analysis 
sm = 15; #smooth over 15 frames.

endWinLen = 5 * 60; #seconds

eBaseVel5_1a = aba.getMedianVelMulti(e_safe5_first, (0,900), smoothWinLen = sm)
eBaseVel5_1b = aba.getMedianVelMulti(e_safe5_first, (900,1800), smoothWinLen = sm)
cBaseVel_1a = aba.getMedianVelMulti(c_safe_first, (0,900), smoothWinLen = sm)
cBaseVel_1b = aba.getMedianVelMulti(c_safe_first, (900,1800), smoothWinLen = sm)

eBaseVel5_2a = aba.getMedianVelMulti(e_safe5_sec, (0,900), smoothWinLen = sm)
eBaseVel5_2b = aba.getMedianVelMulti(e_safe5_sec, (900,1800), smoothWinLen = sm)
cBaseVel_2a = aba.getMedianVelMulti(c_safe_sec, (0,900), smoothWinLen = sm)
cBaseVel_2b = aba.getMedianVelMulti(c_safe_sec, (900,1800), smoothWinLen = sm)

eBase5 = aba.getMedianVelMulti(e_shock5, (0, 900), smoothWinLen = sm)
cBase = aba.getMedianVelMulti(c_shock, (0, 900), smoothWinLen = sm)
eEndVel5 = aba.getMedianVelMulti(e_shock5, tRange=[-endWinLen,-0], smoothWinLen=sm)
cEndVel = aba.getMedianVelMulti(c_shock, tRange=[-endWinLen,-0], smoothWinLen = sm)

#comparisons 
[tv, control_experimental_start] = scipy.stats.ttest_ind(cBaseVel_1a, eBaseVel5_1a)
[tv, control_experimental] = scipy.stats.ttest_ind(cBaseVel_2b, eBaseVel5_2b)
[tv, control_experimental_start1b] = scipy.stats.ttest_ind(cBaseVel_1b, eBaseVel5_1b)
[tv, control_experimental2a] = scipy.stats.ttest_ind(cBaseVel_2a, eBaseVel5_2a)

print 'Statistics comparing control and experimental:', 

#fix
#eEndVel25[2]= np.nan

#convert to array
eBV5_1a = np.array([np.array([eBaseVel5_1a[n]]) for n in range(len(eBaseVel5_1a))])
eBV5_1b = np.array([np.array([eBaseVel5_1b[n]]) for n in range(len(eBaseVel5_1b))])
cBV_1a = np.array([np.array([cBaseVel_1a[n]]) for n in range(len(cBaseVel_1a))])
cBV_1b = np.array([np.array([cBaseVel_1b[n]]) for n in range(len(cBaseVel_1b))])

eBV5_2a = np.array([np.array([eBaseVel5_2a[n]]) for n in range(len(eBaseVel5_2a))])
eBV5_2b = np.array([np.array([eBaseVel5_2b[n]]) for n in range(len(eBaseVel5_2b))])
cBV_2a = np.array([np.array([cBaseVel_2a[n]]) for n in range(len(cBaseVel_2a))])
cBV_2b = np.array([np.array([cBaseVel_2b[n]]) for n in range(len(cBaseVel_2b))])

eSV5 = np.array([np.array([eBase5[n]]) for n in range(len(eBase5))])
cSV = np.array([np.array([cBase[n]]) for n in range(len(cBase))])

eEV5 = np.array([np.array([eEndVel5[n]]) for n in range(len(eEndVel5))])
cEV = np.array([np.array([cEndVel[n]]) for n in range(len(cEndVel))])

experimental5 = np.transpose(np.hstack((eBV5_1a, eBV5_1b, eSV5, eEV5, eBV5_2a, eBV5_2b)))
control = np.transpose(np.hstack((cBV_1a, cBV_1b, cSV, cEV, cBV_2a, cBV_2b)))

pylab.figure()
pylab.suptitle('Learned Helplessness Assay at 5V - Safe, Shocking, Safe')
ax = pylab.subplot(1,2,1)
pylab.plot(control)
pylab.plot(0, [cBaseVel_1a], 'r.')
pylab.plot(1, [cBaseVel_1b], 'r.')
pylab.plot(2,[cBase],'r.')
pylab.plot(3, [cEndVel], 'r.')
pylab.plot(4, [cBaseVel_2a], 'r.')
pylab.plot(5, [cBaseVel_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],'o-k',lw=3)
yerr = (2*scipy.stats.sem(cBaseVel_1a), 2*scipy.stats.sem(cBaseVel_1b), 2*scipy.stats.sem(cBase), 2*scipy.stats.sem(cEndVel), 2*scipy.stats.sem(cBaseVel_2a), 2*scipy.stats.sem(cBaseVel_2b))
pyplot.errorbar([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],fmt='ok',yerr=yerr, lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Control Fish in Rec Tanks - no clicking')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,2,2)
pylab.plot(experimental5)
pylab.plot(0, [eBaseVel5_1a], 'r.')
pylab.plot(1, [eBaseVel5_1b], 'r.')
pylab.plot(2,[eBase5],'r.')
pylab.plot(3, [eEndVel5], 'r.')
pylab.plot(4, [eBaseVel5_2a], 'r.')
pylab.plot(5, [eBaseVel5_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],'o-k', lw=3)
yerr5 = (2*scipy.stats.sem(eBaseVel5_1a), 2*scipy.stats.sem(eBaseVel5_1b), 2*scipy.stats.sem(eBase5), 2*scipy.stats.sem(eEndVel5), 2*scipy.stats.sem(eBaseVel5_2a), 2*scipy.stats.sem(eBaseVel5_2b))
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],fmt='ok', yerr=yerr5, lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 5V (all rec tanks)-long pipet')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)

pylab.figure()
pylab.suptitle('Summary of Median Velocities (mm/s)')
ax = pylab.subplot(1,1,1)
control = ax.plot([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],'o-k', lw=3, label='Control Fish: Safe = colored')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],fmt='ok',yerr=yerr, lw=3)
experimental5 = ax.plot([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],'o-b', lw=3, label='Experimental Fish (5V): Safe = colored')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],fmt='ob', yerr=yerr5, lw=3)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline\n shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')

pylab.show()

