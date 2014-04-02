import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

if len(e_same_shock) < 1:
    print "No fish"
    1/0
else: 
    print "Fish data found"

#velocity analysis 
sm = 15; #smooth over 15 frames.

endWinLen = 5 * 60; #seconds

eBaseVel5_2a = aba.getMedianVelMulti(e_sec, (0,900), smoothWinLen = sm)
eBaseVel5_2b = aba.getMedianVelMulti(e_sec, (900,1800), smoothWinLen = sm)
cBaseVel_2a = aba.getMedianVelMulti(c_sec, (0,900), smoothWinLen = sm)
cBaseVel_2b = aba.getMedianVelMulti(c_sec, (900,1800), smoothWinLen = sm)

eBase5 = aba.getMedianVelMulti(e_shock, (0, 900), smoothWinLen = sm)
cBase = aba.getMedianVelMulti(c_shock, (0, 900), smoothWinLen = sm)
eEndVel5 = aba.getMedianVelMulti(e_shock, tRange=[-endWinLen,-0], smoothWinLen=sm)
cEndVel = aba.getMedianVelMulti(c_shock, tRange=[-endWinLen,-0], smoothWinLen = sm)

eBaseShockSame = aba.getMedianVelMulti(e_same_shock, (0, 900), smoothWinLen = sm)
eEndShockSame = aba.getMedianVelMulti(e_same_shock, tRange=[-endWinLen, -0], smoothWinLen = sm)
eBaseSame_2a = aba.getMedianVelMulti(e_same_sec, (0, 900), smoothWinLen = sm)
eBaseSame_2b = aba.getMedianVelMulti(e_same_sec, (900, 1800), smoothWinLen = sm)

'''
#comparisons 
[tv, exper5shock_end] = scipy.stats.ttest_ind(eEndVel5, eBaseVel5_2b)
[tv, experSameshock_end] = scipy.stats.ttest_ind(eEndShockSame, eBaseSame_2b)
[tv, controlshock_end] = scipy.stats.ttest_ind(cEndVel, cBaseVel_2b)
[tv, exper5shock_end_control] = scipy.stats.ttest_ind(eEndVel5, cEndVel)
[tv, experSameshock_end_control] = scipy.stats.ttest_ind(eEndShockSame, cEndVel)
[tv, experimental_control_endshock] = scipy.stats.ttest_ind(eEndVel5, cEndVel)

print 'shock tank, safe water to experimental at end',waterend_experimentalD
'''
#convert to array
eBV5_2a = np.array([np.array([eBaseVel5_2a[n]]) for n in range(len(eBaseVel5_2a))])
eBV5_2b = np.array([np.array([eBaseVel5_2b[n]]) for n in range(len(eBaseVel5_2b))])
cBV_2a = np.array([np.array([cBaseVel_2a[n]]) for n in range(len(cBaseVel_2a))])
cBV_2b = np.array([np.array([cBaseVel_2b[n]]) for n in range(len(cBaseVel_2b))])

eSV5 = np.array([np.array([eBase5[n]]) for n in range(len(eBase5))])
cSV = np.array([np.array([cBase[n]]) for n in range(len(cBase))])

eEV5 = np.array([np.array([eEndVel5[n]]) for n in range(len(eEndVel5))])
cEV = np.array([np.array([cEndVel[n]]) for n in range(len(cEndVel))])

eSVS = np.array([np.array([eBaseShockSame[n]]) for n in range(len(eBaseShockSame))])
eEVS = np.array([np.array([eEndShockSame[n]]) for n in range(len(eEndShockSame))])
eBVS_2a = np.array([np.array([eBaseSame_2a[n]]) for n in range(len(eBaseSame_2a))])
eBVS_2b = np.array([np.array([eBaseSame_2b[n]]) for n in range(len(eBaseSame_2b))])

experimental5 = np.transpose(np.hstack((eSV5, eEV5, eBV5_2a, eBV5_2b)))
experimentalsame = np.transpose(np.hstack((eSVS, eEVS, eBVS_2a, eBVS_2b)))
control = np.transpose(np.hstack((cSV, cEV, cBV_2a, cBV_2b)))


pylab.figure()
pylab.suptitle('Learned Helplessness Assay at 5V - Safe, Shocking, Safe')
ax = pylab.subplot(1,3,1)
pylab.plot(control)
pylab.plot(0,[cBase],'r.')
pylab.plot(1, [cEndVel], 'r.')
pylab.plot(2, [cBaseVel_2a], 'r.')
pylab.plot(3, [cBaseVel_2b], 'r.')
pylab.plot([0,1,2,3],[np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],'o-k',lw=3)
yerr = (2*scipy.stats.sem(cBase), 2*scipy.stats.sem(cEndVel), 2*scipy.stats.sem(cBaseVel_2a), 2*scipy.stats.sem(cBaseVel_2b))
pyplot.errorbar([0,1,2,3],[np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],fmt='ok',yerr=yerr, lw=3)
ax.set_xticks((0,1,2,3))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,3.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Control Fish in Rec Tanks')
patch1 = mpl.patches.Rectangle((0.25,0), .5,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,3,2)
pylab.plot(experimental5)
pylab.plot(0,[eBase5],'r.')
pylab.plot(1, [eEndVel5], 'r.')
pylab.plot(2, [eBaseVel5_2a], 'r.')
pylab.plot(3, [eBaseVel5_2b], 'r.')
pylab.plot([0,1,2,3],[np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],'o-k',lw=3)
yerr5 = (2*scipy.stats.sem(eBase5), 2*scipy.stats.sem(eEndVel5), 2*scipy.stats.sem(eBaseVel5_2a), 2*scipy.stats.sem(eBaseVel5_2b))
pyplot.errorbar([0,1,2,3],[np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],fmt='ok',yerr=yerr5, lw=3)
ax.set_xticks((0,1,2,3))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,3.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental Fish in Rec Tanks')
patch1 = mpl.patches.Rectangle((0.25,0), .5,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,3,3)
pylab.plot(experimentalsame)
pylab.plot(0,[eBaseShockSame],'r.')
pylab.plot(1, [eEndShockSame], 'r.')
pylab.plot(2, [eBaseSame_2a], 'r.')
pylab.plot(3, [eBaseSame_2b], 'r.')
pylab.plot([0,1,2,3], [np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)],'o-k', lw=3)
yerrS = (2*scipy.stats.sem(eBaseShockSame), 2*scipy.stats.sem(eEndShockSame), 2*scipy.stats.sem(eBaseSame_2a), 2*scipy.stats.sem(eBaseSame_2b))
pyplot.errorbar([0,1,2,3],[np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)], lw=3,fmt='ok', yerr=yerrS)
ax.set_xticks((0,1,2,3))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,3.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 5V (stay in shocking tank)')
patch1 = mpl.patches.Rectangle((0.25,0), .5,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)

fig = pylab.figure(100, figsize=(6,5))
pylab.suptitle('Summary of Median Velocities (mm/s)')
ax = pylab.subplot(1,1,1)
control = ax.plot([0,1,2,3],[np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],'o-k', lw=3, label='Control Fish: No shocking and safe=nonshock tank')
pyplot.errorbar([0,1,2,3],[np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],fmt='ok',yerr=yerr, lw=3)
experimental5 = ax.plot([0,1,2,3],[np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],'o-b', lw=3, label='Experimental Fish (5V): Safe=nonshock tank')
pyplot.errorbar([0,1,2,3],[np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],fmt='ob', yerr=yerr5, lw=3)
experimentalsame = ax.plot([0,1,2,3],[np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)],'o-r', lw=3, label='Experimental Fish (5V): Safe=shock tank')
pyplot.errorbar([0,1,2,3],[np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)], lw=3,fmt='or', yerr=yerrS)
handles, labels=ax.get_legend_handles_labels()
ax.legend(handles, labels)
ax.set_xticks((0,1,2,3))
ax.set_xticklabels(('first 15 min \n shock tank', 'last 5 min \n shock tank', '0-15 min \n test tank', '15-30 min \n test tank'))
pylab.xlim((-.25,3.25))
pylab.ylim((0,4))
pylab.ylabel('Median Speed (mm/s)')
pylab.axvline(x=1.5, color = 'k', lw=3, ls='dashed')
pylab.axvline(x=3.5, color = 'k', lw=3, ls='dashed')
patch3 = mpl.patches.Rectangle((.25,0), .5, 10, color=[1,.5,.5], fill=True)
pyplot.gca().add_patch(patch3)

'''
pylab.figure()
pylab.suptitle('Summary of Median Velocities (mm/s)')
ax3 = pylab.subplot(1,1,1)
experimental5 = ax3.plot([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],'o-b', lw=3, label='Experimental Fish (5V): Safe=nonshock tank')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],fmt='ob', yerr=yerr5, lw=3)
experimentalwater = ax3.plot([0,1,2,3,4,5],[np.mean(eBaseVelW_1a), np.mean(eBaseVelW_1b), np.mean(eBaseW), np.mean(eEndVelW), np.mean(eBaseVelW_2a), np.mean(eBaseVelW_2b)],'o-m', lw=3, label='Experimental Fish (5V): Safe=shock tank with new water')
experimentalsame = ax3.plot([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)],'o-r', lw=3, label='Experimental Fish (5V): Safe=shock tank')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)], lw=3,fmt='or', yerr=yerrS)
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelW_1a), np.mean(eBaseVelW_1b), np.mean(eBaseW), np.mean(eEndVelW), np.mean(eBaseVelW_2a), np.mean(eBaseVelW_2b)],fmt='om', yerr=yerrW, lw=3)
handles1, labels1 = ax3.get_legend_handles_labels()
ax3.legend(handles1, labels1)
ax3.set_xticks((0,1,2,3,4,5))
ax3.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline\n shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
patch5 = mpl.patches.Rectangle((1.5,0), 2, 10, color='g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch5)
'''
pylab.show()

