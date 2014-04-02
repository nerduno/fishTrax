import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy
import os

##make sure fish have been loaded
if len(e_first) < 1:
    print "No fish"
    1/0
else: 
    print "Fish data found"

#velocity analysis 
sm = 15; #smooth over 15 frames.
endWinLen = 5 * 60; #seconds

eBaseVel5_1a = aba.getMedianVelMulti(e_first, (0,900), smoothWinLen = sm)
eBaseVel5_1b = aba.getMedianVelMulti(e_first, (900,1800), smoothWinLen = sm)
cBaseVel_1a = aba.getMedianVelMulti(c_first, (0,900), smoothWinLen = sm)
cBaseVel_1b = aba.getMedianVelMulti(c_first, (900,1800), smoothWinLen = sm)

eBaseVel5_2a = aba.getMedianVelMulti(e_sec, (0,900), smoothWinLen = sm)
eBaseVel5_2b = aba.getMedianVelMulti(e_sec, (900,1800), smoothWinLen = sm)
cBaseVel_2a = aba.getMedianVelMulti(c_sec, (0,900), smoothWinLen = sm)
cBaseVel_2b = aba.getMedianVelMulti(c_sec, (900,1800), smoothWinLen = sm)

eBase5 = aba.getMedianVelMulti(e_shock, (0, 900), smoothWinLen = sm)
cBase = aba.getMedianVelMulti(c_shock, (0, 900), smoothWinLen = sm)
eEndVel5 = aba.getMedianVelMulti(e_shock, tRange=[-endWinLen,-0], smoothWinLen=sm)
cEndVel = aba.getMedianVelMulti(c_shock, tRange=[-endWinLen,-0], smoothWinLen = sm)
eBaseSame_1a = aba.getMedianVelMulti(e_same_first, (0, 900), smoothWinLen = sm)
eBaseSame_1b = aba.getMedianVelMulti(e_same_first, (900, 1800), smoothWinLen = sm)
eBaseShockSame = aba.getMedianVelMulti(e_same_shock, (0, 900), smoothWinLen = sm)
eEndShockSame = aba.getMedianVelMulti(e_same_shock, tRange=[-endWinLen, -0], smoothWinLen = sm)
eBaseSame_2a = aba.getMedianVelMulti(e_same_sec, (0, 900), smoothWinLen = sm)
eBaseSame_2b = aba.getMedianVelMulti(e_same_sec, (900, 1800), smoothWinLen = sm)

#comparisons 
[tv, control_experimental_start] = scipy.stats.ttest_ind(cBaseVel_1a, eBaseVel5_1a)
[tv, control_experimentalsame_start] = scipy.stats.ttest_ind(cBaseVel_1a, eBaseSame_1a)
[tv, experimental_experimentalsame_start] = scipy.stats.ttest_ind(eBaseVel5_1a, eBaseSame_1a)

[tv, control_experimental] = scipy.stats.ttest_ind(cBaseVel_2b, eBaseVel5_2b)
[tv, control_experimentalsame] = scipy.stats.ttest_ind(cBaseVel_2b, eBaseSame_2b)
[tv, experimental_experimentalsame] = scipy.stats.ttest_ind(eBaseVel5_2b, eBaseSame_2b)

[tv, control_experimental_start1b] = scipy.stats.ttest_ind(cBaseVel_1b, eBaseVel5_1b)
[tv, control_experimentalsame_start1b] = scipy.stats.ttest_ind(cBaseVel_1b, eBaseSame_1b)
[tv, experimental_experimentalsame_start1b] = scipy.stats.ttest_ind(eBaseVel5_1b, eBaseSame_1b)

[tv, control_experimental2a] = scipy.stats.ttest_ind(cBaseVel_2a, eBaseVel5_2a)
[tv, control_experimentalsame2a] = scipy.stats.ttest_ind(cBaseVel_2a, eBaseSame_2a)
[tv, experimental_experimentalsame2a] = scipy.stats.ttest_ind(eBaseVel5_2a, eBaseSame_2a)

[tv, exper5shock_end] = scipy.stats.ttest_ind(eEndVel5, eBaseVel5_2b)
[tv, experSameshock_end] = scipy.stats.ttest_ind(eEndShockSame, eBaseSame_2b)
[tv, controlshock_end] = scipy.stats.ttest_ind(cEndVel, cBaseVel_2b)
[tv, exper5shock_end_control] = scipy.stats.ttest_ind(eEndVel5, cEndVel)
[tv, experSameshock_end_control] = scipy.stats.ttest_ind(eEndShockSame, cEndVel)
[tv, experimental_control_endshock] = scipy.stats.ttest_ind(eEndVel5, cEndVel)


print 'Statistics comparing velocity between control and experimental (rec), control and experimental (same), and experimental (rec) and experimental (same) for first 15 min and last 15 min:', control_experimental_start, control_experimentalsame_start, experimental_experimentalsame_start, control_experimental, control_experimentalsame, experimental_experimentalsame
print 'Statistics comparing end shock to final velocity, 5V and same, control:', exper5shock_end, experSameshock_end, controlshock_end
print 'Statistic acclimation second  15 control to 5v:',control_experimental_start1b
print 'Statistic end of shock velocity control to experimental5v:', experimental_control_endshock


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

eBVS_1a = np.array([np.array([eBaseSame_1a[n]]) for n in range(len(eBaseSame_1a))])
eBVS_1b = np.array([np.array([eBaseSame_1b[n]]) for n in range(len(eBaseSame_1b))])
eSVS = np.array([np.array([eBaseShockSame[n]]) for n in range(len(eBaseShockSame))])
eEVS = np.array([np.array([eEndShockSame[n]]) for n in range(len(eEndShockSame))])
eBVS_2a = np.array([np.array([eBaseSame_2a[n]]) for n in range(len(eBaseSame_2a))])
eBVS_2b = np.array([np.array([eBaseSame_2b[n]]) for n in range(len(eBaseSame_2b))])

experimental5 = np.transpose(np.hstack((eBV5_1a, eBV5_1b, eSV5, eEV5, eBV5_2a, eBV5_2b)))
experimentalsame = np.transpose(np.hstack((eBVS_1a, eBVS_1b, eSVS, eEVS, eBVS_2a, eBVS_2b)))
control = np.transpose(np.hstack((cBV_1a, cBV_1b, cSV, cEV, cBV_2a, cBV_2b)))
'''
pylab.figure()
pylab.suptitle('Learned Helplessness Assay at 5V - Safe, Shocking, Safe')
ax = pylab.subplot(1,3,1)
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
pylab.title('Control Fish in Rec Tanks')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,3,2)
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
pylab.title('Experimental fish at 5V (all rec tanks)')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,3,3)
pylab.plot(experimentalsame)
pylab.plot(0, [eBaseSame_1a], 'r.')
pylab.plot(1, [eBaseSame_1b], 'r.')
pylab.plot(2,[eBaseShockSame],'r.')
pylab.plot(3, [eEndShockSame], 'r.')
pylab.plot(4, [eBaseSame_2a], 'r.')
pylab.plot(5, [eBaseSame_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)],'o-k', lw=3)
yerrS = (2*scipy.stats.sem(eBaseSame_1a), 2*scipy.stats.sem(eBaseSame_1b), 2*scipy.stats.sem(eBaseShockSame), 2*scipy.stats.sem(eEndShockSame), 2*scipy.stats.sem(eBaseSame_2a), 2*scipy.stats.sem(eBaseSame_2b))
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)], lw=3,fmt='ok', yerr=yerrS)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 5V (stay in shocking tank)')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
'''

yerr = (2*scipy.stats.sem(cBaseVel_1a), 2*scipy.stats.sem(cBaseVel_1b), 2*scipy.stats.sem(cBase), 2*scipy.stats.sem(cEndVel), 2*scipy.stats.sem(cBaseVel_2a), 2*scipy.stats.sem(cBaseVel_2b))
yerr5 = (2*scipy.stats.sem(eBaseVel5_1a), 2*scipy.stats.sem(eBaseVel5_1b), 2*scipy.stats.sem(eBase5), 2*scipy.stats.sem(eEndVel5), 2*scipy.stats.sem(eBaseVel5_2a), 2*scipy.stats.sem(eBaseVel5_2b))
yerrS = (2*scipy.stats.sem(eBaseSame_1a), 2*scipy.stats.sem(eBaseSame_1b), 2*scipy.stats.sem(eBaseShockSame), 2*scipy.stats.sem(eEndShockSame), 2*scipy.stats.sem(eBaseSame_2a), 2*scipy.stats.sem(eBaseSame_2b))

pylab.figure()
pylab.suptitle('Summary of Median Velocities (mm/s)')
ax = pylab.subplot(1,1,1)
control = ax.plot([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],'o-k', lw=3, label='Control Fish: No shocking and safe=nonshock tank')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],fmt='ok',yerr=yerr, lw=3)
experimental5 = ax.plot([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],'o-b', lw=3, label='Experimental Fish (5V): Safe=nonshock tank')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],fmt='ob', yerr=yerr5, lw=3)
experimentalsame = ax.plot([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)],'o-r', lw=3, label='Experimental Fish (5V): Safe=shock tank')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)], lw=3,fmt='or', yerr=yerrS)
handles, labels=ax.get_legend_handles_labels()
ax.legend(handles, labels)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline\n shock', 'last 5 min\n of shock', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
patch3 = mpl.patches.Rectangle((1.5,0), 2, 10, color='g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch3)

pyplot.show()
