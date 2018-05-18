import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

#omr stats
tp = 12

ePreOMRstatsSame_1a= aba.getOMRScoreStatsMulti(e_omr_same_pre, stateRange=[3,3], timePoint=tp)
ePreOMRstatsSame_1b = aba.getOMRScoreStatsMulti(e_omr_same_pre, stateRange=[8,8], timePoint=tp)
ePreOMRstatsSame = aba.getOMRScoreStatsMulti(e_omr_same, stateRange=[3,3], timePoint=tp)
eEndOMRstatsSame = aba.getOMRScoreStatsMulti(e_omr_same_last, stateRange=[8,8], timePoint=tp)

cPreOMRstats_1a= aba.getOMRScoreStatsMulti(c_omr_pre, stateRange=[3,3], timePoint=tp)
cPreOMRstats_1b = aba.getOMRScoreStatsMulti(c_omr_pre, stateRange=[8,8], timePoint=tp)
cPreOMRstats = aba.getOMRScoreStatsMulti(c_omr, stateRange=[3,3], timePoint=tp)
cEndOMRstats = aba.getOMRScoreStatsMulti(c_omr_last, stateRange=[8,8], timePoint=tp)

#velocity stats 
sm=15

ePreVelSame_1a = aba.getMedianVelMulti(e_omr_same_pre, tRange=[0,15*30], smoothWinLen = sm)
ePreVelSame_1b = aba.getMedianVelMulti(e_omr_same_pre, tRange=[15*30,30*30], smoothWinLen = sm)
eVelSame = aba.getMedianVelMulti(e_omr_same, stateRange=[3,3], smoothWinLen=sm)
eEndVelSame = aba.getMedianVelMulti(e_omr_same_last, stateRange=[8,8], smoothWinLen=sm)

cPreVel_1a = aba.getMedianVelMulti(c_omr_pre, tRange=[0,15*30], smoothWinLen = sm)
cPreVel_1b = aba.getMedianVelMulti(c_omr_pre, tRange=[15*30,30*30], smoothWinLen = sm)
cVel = aba.getMedianVelMulti(c_omr, stateRange=[3,3], smoothWinLen=sm)
cEndVel = aba.getMedianVelMulti(c_omr_last, stateRange=[8,8], smoothWinLen=sm)

[tv, c_e_vel_end] = scipy.stats.ttest_ind(cEndVel, eEndVelSame)
[tv, c_e_vel] = scipy.stats.ttest_ind(cVel, eVelSame)
print 'velocity comparison at end',c_e_vel_end
print 'vel comparison at start', c_e_vel

def plotPairedConditions(states, statenames, color=[.5,.5,.5], ylabel=None, title=None):
    pyplot.hold(True)
    #for nState, state in enumerate(states):
    #    pyplot.plot(nState, [state], '.', color=color)
    pyplot.plot(range(len(states)),np.vstack(states),'.-', color=color)
    pyplot.xlim([-.25,len(states)-.75])
    ax = pyplot.gca()
    #ax.set_xticks(range(len(states)))
    #ax.set_xticklabels(statenames)
    if ylabel is not None:
        pyplot.ylabel(ylabel)
    if title is not None:
        pyplot.title(title)

def plotPairedConditionsMeanAndSEM(states, statenames, fmt='o-', color=[0,0,0], ylabel=None, title=None):
    pyplot.hold(True)
    yerr = []
    yu = []
    for nState, state in enumerate(states):
        yerr.append(scipy.stats.sem(state))
        yu.append(np.mean(state))
    print yu
    print yerr
    pyplot.errorbar(range(len(states)),yu,fmt=fmt, color=color, yerr=yerr, lw=3)
    pyplot.xlim([-.25,len(states)-.75])
    ax = pyplot.gca()
    #ax.set_xticks(range(len(states)))
    #ax.set_xticklabels(statenames)
    if ylabel is not None:
        pyplot.ylabel(ylabel)
    if title is not None:
        pyplot.title(title)


#omr analyzsis

#show recovery (missing controls)
pyplot.figure(2,figsize=(6,4))
pyplot.gcf().set_facecolor('w')
#pyplot.suptitle('Helplessness Assay with OMR')

ax = pyplot.subplot2grid((1,2), (0,0))
#pyplot.title('Control')
pylab.axvline(x=1.5, color = 'k', lw=3, ls='dashed')
plotPairedConditions([cPreVel_1a,cPreVel_1b,cVel, cEndVel],['0-15 min\n neutral tank','15-30 min\n neutral tank', 'first 15 min \n shock tank','last 5 min \n shock tank'], color=[.5,.5,.5])
plotPairedConditionsMeanAndSEM([cPreVel_1a,cPreVel_1b,cVel, cEndVel],['0-15 min\n neutral tank','15-30 min\n neutral tank', 'first 15 min \n shock tank','last 15 min \n shock tank'], color=[0,0,0])
pyplot.ylim((0,4))
ax.set_yticks([0,1,2,3,4])
pyplot.axvspan(2.25,2.75,facecolor=[1,.5,.5], ec='None')
#pylab.ylabel('Median Speed (mm/s)')
ax.set_xticks([0,1,2,3])
ax.set_xticklabels([])
ax = pyplot.subplot2grid((1,2), (0,1))
#pyplot.title('Experimental')
pylab.axvline(x=1.5, color = 'k', lw=3, ls='dashed')
plotPairedConditions([ePreVelSame_1a,ePreVelSame_1b,eVelSame, eEndVelSame],['0-15 min\n neutral tank','15-30 min\n neutral tank', 'first 15 min \n shock tank','last 5 min \n shock tank'], color=[.5,.5,1])
plotPairedConditionsMeanAndSEM([ePreVelSame_1a,ePreVelSame_1b,eVelSame, eEndVelSame],['0-15 min\n neutral tank','15-30 min\n neutral tank', 'first 15 min \n shock tank','last 15 min \n shock tank'], color=[0,0,1])
pyplot.ylim((0,4))
ax.set_yticks([0,1,2,3,4])
pyplot.axvspan(2.25,2.75,facecolor=[1,.5,.5], ec='None')
#pylab.ylabel('Median Speed (mm/s)')
ax.set_xticks([0,1,2,3])
#ax.set_xticklabels([])



'''
pyplot.figure()
ax=pyplot.subplot(121)
pylab.axvline(x=1.5, color = 'k', lw=3, ls='dashed')
plotPairedConditionsMeanAndSEM([cPreVel_1a,cPreVel_1b,cVel, cEndVel],['0-15 min\n neutral tank','15-30 min\n neutral tank', 'first 15 min \n shock tank','last 15 min \n shock tank'], color=[0,0,0])
plotPairedConditionsMeanAndSEM([ePreVelSame_1a,ePreVelSame_1b,eVelSame, eEndVelSame],['0-15 min\n neutral tank','15-30 min\n neutral tank', 'first 15 min \n shock tank','last 15 min \n shock tank'], color=[0,0,1])
pyplot.ylim((0,3.5))
pyplot.axvspan(2.25,2.75,facecolor=[1,.5,.5], ec='None')
pylab.ylabel('Median Speed (mm/s)')
pyplot.title('Median Speed')
ax = pyplot.subplot(122)
pylab.axvline(x=1.5, color = 'k', lw=3, ls='dashed')
pyplot.title('Normalized OMR Metric')
plotPairedConditionsMeanAndSEM([cPreOMRstats_1a['omrResults']['avgnorm'], cPreOMRstats_1b['omrResults']['avgnorm'],cPreOMRstats['omrResults']['avgnorm'],cEndOMRstats['omrResults']['avgnorm']],['0-15 min\n neutral tank','15-30 min\n neutral tank', 'first 15 min \n shock tank','last 15 min \n shock tank'],color=[0,0,0])
plotPairedConditionsMeanAndSEM([ePreOMRstatsSame_1a['omrResults']['avgnorm'],ePreOMRstatsSame_1b['omrResults']['avgnorm'],ePreOMRstatsSame['omrResults']['avgnorm'],eEndOMRstatsSame['omrResults']['avgnorm']],['0-15 min\n neutral tank','15-30 min\n neutral tank', 'first 15 min \n shock tank','last 15 min \n shock tank'],color=[0,0,1])
pyplot.axvspan(2.25,2.75,facecolor=[1,.5,.5], ec='None')
pyplot.axvspan(2.25,2.75,facecolor=[1,.5,.5], ec='None')
pyplot.ylim((0,.65))
pyplot.ylabel('Normalized OMR Metric')
'''

pyplot.figure(1,figsize=(6,4))
ax=pyplot.subplot(121)
#pyplot.title('Control')
pylab.axvline(x=1.5, color = 'k', lw=3, ls='dashed')
plotPairedConditions([cPreOMRstats_1a['omrResults']['avgnorm'],cPreOMRstats_1b['omrResults']['avgnorm'], cPreOMRstats['omrResults']['avgnorm'],cEndOMRstats['omrResults']['avgnorm']],['0-15 min\n neutral tank','15-30 min\n neutral tank', 'first 15 min \n shock tank','last 15 min \n shock tank'],color=[.5,.5,.5])
plotPairedConditionsMeanAndSEM([cPreOMRstats_1a['omrResults']['avgnorm'], cPreOMRstats_1b['omrResults']['avgnorm'],cPreOMRstats['omrResults']['avgnorm'],cEndOMRstats['omrResults']['avgnorm']],['0-15 min\n neutral tank','15-30 min\n neutral tank', 'first 15 min \n shock tank','last 15 min \n shock tank'],color=[0,0,0])
pyplot.axvspan(2.25,2.75,facecolor=[1,.5,.5], ec='None')
pyplot.ylim((0,.65))
ax.set_yticks([0,0.25, 0.50])
#ax.set_yticklabels([])
#pyplot.ylabel('Normalized OMR Metric')
ax.set_xticks([0,1,2,3])
#ax.set_xticklabels([])
ax=pyplot.subplot(122)
pylab.axvline(x=1.5, color = 'k', lw=3, ls='dashed')
#pyplot.title('Experimental')
#pyplot.ylabel('Normalized OMR Metric')
ax.set_yticks([0,0.25, 0.50])
#ax.set_yticklabels([])
plotPairedConditions([ePreOMRstatsSame_1a['omrResults']['avgnorm'],ePreOMRstatsSame_1b['omrResults']['avgnorm'], ePreOMRstatsSame['omrResults']['avgnorm'],eEndOMRstatsSame['omrResults']['avgnorm']],['0-15 min\n neutral tank','15-30 min\n neutral tank', 'first 15 min \n shock tank','last 15 min \n shock tank'],color=[.5,.5,1])
plotPairedConditionsMeanAndSEM([ePreOMRstatsSame_1a['omrResults']['avgnorm'],ePreOMRstatsSame_1b['omrResults']['avgnorm'],ePreOMRstatsSame['omrResults']['avgnorm'],eEndOMRstatsSame['omrResults']['avgnorm']],['0-15 min\n neutral tank','15-30 min\n neutral tank', 'first 15 min \n shock tank','last 15 min \n shock tank'],color=[0,0,1])
pyplot.axvspan(2.25,2.75,facecolor=[1,.5,.5], ec='None')
pyplot.ylim((0,.65))
ax.set_xticks([0,1,2,3])
#ax.set_xticklabels([])

[tv, cc_omr] = scipy.stats.ttest_ind(cPreOMRstats['omrResults']['avgnorm'], cEndOMRstats['omrResults']['avgnorm'])
[tv, c_e_omr] = scipy.stats.ttest_ind(cPreOMRstats['omrResults']['avgnorm'], ePreOMRstatsSame['omrResults']['avgnorm'])
[tv, c_e_omr_post] = scipy.stats.ttest_ind(cEndOMRstats['omrResults']['avgnorm'], eEndOMRstatsSame['omrResults']['avgnorm'])
[tv, ee_omr] = scipy.stats.ttest_ind(ePreOMRstatsSame['omrResults']['avgnorm'], eEndOMRstatsSame['omrResults']['avgnorm'])
print 'omr control start to end', cc_omr
print 'omr exper start to end', ee_omr
print 'experimental pre to control pre',c_e_omr
print 'experimental post to control post', c_e_omr_post

#show signficance of OMR response
pyplot.figure(3,figsize=(11,3))
pyplot.gcf().set_facecolor('w')

ax = pyplot.subplot2grid((1,4), (0,0))
_, p = scipy.stats.ttest_rel(cPreOMRstats['omrResults']['avgnorm'],cPreOMRstats['omrControl']['avgnorm'])
plotPairedConditions([cPreOMRstats['omrControl']['avgnorm'],cPreOMRstats['omrResults']['avgnorm']],['PreOMR','OMR'], color=[.5,.5,.5], ylabel='Normalized OMR Metric', title='Control Score: first 15 min shock tank \np=%0.5f'%p)
plotPairedConditionsMeanAndSEM([cPreOMRstats['omrControl']['avgnorm'],cPreOMRstats['omrResults']['avgnorm']],['PreOMR','OMR'], color='k')
pyplot.ylim((0,.65))
pyplot.axvspan(.25,.75,facecolor=[1,.5,.5], ec='None')
ax.set_yticks([0,0.25, 0.50])
ax.set_yticklabels([])
ax.set_xticks([0,1])
ax.set_xticklabels([])
ax = pyplot.subplot2grid((1,4), (0,1))
_, p = scipy.stats.ttest_rel(cEndOMRstats['omrResults']['avgnorm'],cEndOMRstats['omrControl']['avgnorm'])
plotPairedConditions([cEndOMRstats['omrControl']['avgnorm'],cEndOMRstats['omrResults']['avgnorm']],['PreOMR','OMR'], color=[.5,.5,.5], ylabel='Normalized OMR Metric', title='Control Score: last 15 min shock tank \np=%0.5f'%p)
plotPairedConditionsMeanAndSEM([cEndOMRstats['omrControl']['avgnorm'],cEndOMRstats['omrResults']['avgnorm']],['PreOMR','OMR'], color='k')
pyplot.ylim((0,.65))
pyplot.axvspan(.25,.75,facecolor=[1,.5,.5], ec='None')
ax.set_yticks([0,0.25, 0.50])
ax.set_yticklabels([])
ax.set_xticks([0,1])
ax.set_xticklabels([])
ax = pyplot.subplot2grid((1,4), (0,2))
_, p = scipy.stats.ttest_rel(ePreOMRstatsSame['omrResults']['avgnorm'],ePreOMRstatsSame['omrControl']['avgnorm'])
plotPairedConditions([ePreOMRstatsSame['omrControl']['avgnorm'],ePreOMRstatsSame['omrResults']['avgnorm']],['PreOMR','OMR'], color=[.5,.5,1], ylabel='Normalized OMR Metric', title='Experimental Score: first 15 min shock tank \np=%0.5f'%p)
plotPairedConditionsMeanAndSEM([ePreOMRstatsSame['omrControl']['avgnorm'],ePreOMRstatsSame['omrResults']['avgnorm']],['PreOMR','OMR'], color='b')
pyplot.ylim((0,.65))
pyplot.axvspan(.25,.75,facecolor=[1,.5,.5], ec='None')
ax.set_yticks([0,0.25, 0.50])
ax.set_yticklabels([])
ax.set_xticks([0,1])
ax.set_xticklabels([])
ax = pyplot.subplot2grid((1,4), (0,3))
_, p = scipy.stats.ttest_rel(eEndOMRstatsSame['omrResults']['avgnorm'],eEndOMRstatsSame['omrControl']['avgnorm'])
plotPairedConditions([eEndOMRstatsSame['omrControl']['avgnorm'],eEndOMRstatsSame['omrResults']['avgnorm']],['PreOMR','OMR'], color=[.5,.5,1], ylabel='Normalized OMR Metric', title='Experimental Score: last 15 min shock tank \np=%0.5f'%p)
plotPairedConditionsMeanAndSEM([eEndOMRstatsSame['omrControl']['avgnorm'],eEndOMRstatsSame['omrResults']['avgnorm']],['PreOMR','OMR'], color='b')
pyplot.ylim((0,.65))
pyplot.axvspan(.25,.75,facecolor=[1,.5,.5], ec='None')
ax.set_yticks([0,0.25, 0.50])
ax.set_yticklabels([])
ax.set_xticks([0,1])
ax.set_xticklabels([])


''' 
ax = pyplot.subplot2grid((2,2), (0,1))
_, p = scipy.stats.ttest_rel(cPostOMRstats['omrResults']['avgnorm'],cPostOMRstats['omrControl']['avgnorm'])
plotPairedConditions([cPostOMRstats['omrControl']['avgnorm'],cPostOMRstats['omrResults']['avgnorm']],['NonOMR','OMR'], color=[.5,.5,.5], ylabel='Normalized OMR Metric', title='Post Shock Control p=%0.3f'%p)
plotPairedConditionsMeanAndSEM([cPostOMRstats['omrControl']['avgnorm'],cPostOMRstats['omrResults']['avgnorm']],['NonOMR','OMR'], color=[0,0,0], ylabel='Normalized OMR Metric', title='Post Shock Control p=%0.3f'%p)
pyplot.ylim((0,1))

ax = pyplot.subplot2grid((2,2), (1,0))
_, p = scipy.stats.ttest_rel(ePreOMRstats['omrResults']['avgnorm'],ePreOMRstats['omrControl']['avgnorm'])
plotPairedConditions([ePreOMRstats['omrControl']['avgnorm'],ePreOMRstats['omrResults']['avgnorm']],['NonOMR','OMR'], color=[.5,.5,1], ylabel='Normalized OMR Metric', title='Pre Shock Experimental p=%0.3f'%p)
plotPairedConditionsMeanAndSEM([ePreOMRstats['omrControl']['avgnorm'],ePreOMRstats['omrResults']['avgnorm']],['NonOMR','OMR'], color=[0,0,1], ylabel='Normalized OMR Metric', title='Pre Shock Experimental p=%0.3f'%p)
pyplot.ylim((0,1))

ax = pyplot.subplot2grid((2,2), (1,1))
_, p = scipy.stats.ttest_rel(ePostOMRstats['omrResults']['avgnorm'],ePostOMRstats['omrControl']['avgnorm'])
plotPairedConditions([ePostOMRstats['omrControl']['avgnorm'],ePostOMRstats['omrResults']['avgnorm']],['NonOMR','OMR'], color=[.5,.5,1], ylabel='Normalized OMR Metric', title='Post Shock Experimental p=%0.3f'%p)
plotPairedConditionsMeanAndSEM([ePostOMRstats['omrControl']['avgnorm'],ePostOMRstats['omrResults']['avgnorm']],['NonOMR','OMR'], color=[0,0,1], ylabel='Normalized OMR Metric', title='Post Shock Experimental p=%0.3f'%p)
pyplot.ylim((0,1))

#plotPairedConditionsMeanAndSEM([ePreOMRstats['omrResults']['avgnorm'],ePostOMRstats['omrResults']['avgnorm']],['Pre\nShock','Post\nShock'],color='b')
#plotPairedConditionsMeanAndSEM([cPreOMRstats['omrResults']['avgnorm'],cPostOMRstats['omrResults']['avgnorm']],['Pre\nShock','Post\nShock'],color='k')

_, p_esafePreOMR = scipy.stats.ttest_rel(esafePreOMRstats['omrResults']['avgnorm'],esafePreOMRstats['omrControl']['avgnorm'])
_, p_esafePostOMR = scipy.stats.ttest_rel(esafePostOMRstats['omrResults']['avgnorm'],esafePostOMRstats['omrControl']['avgnorm'])
_, p_ePreOMR = scipy.stats.ttest_rel(ePreOMRstats['omrResults']['avgnorm'],ePreOMRstats['omrControl']['avgnorm'])
_, p_ePostOMR = scipy.stats.ttest_rel(ePostOMRstats['omrResults']['avgnorm'],ePostOMRstats['omrControl']['avgnorm'])
_, p_ePreVsPostOMR = scipy.stats.ttest_rel(ePostOMRstats['omrResults']['avgnorm'],ePreOMRstats['omrResults']['avgnorm'])
_, p_esafePreVsPostOMR = scipy.stats.ttest_rel(esafePostOMRstats['omrResults']['avgnorm'],esafePreOMRstats['omrResults']['avgnorm'])
print 'OMR response p-values cPre %f cPost %f ePre %f ePost %f'%(p_esafePreOMR, p_esafePostOMR, p_ePreOMR, p_ePostOMR)
print 'OMR response to shocks exp %f control %f'%(p_ePreVsPostOMR,p_esafePreVsPostOMR)
'''
pylab.show()

