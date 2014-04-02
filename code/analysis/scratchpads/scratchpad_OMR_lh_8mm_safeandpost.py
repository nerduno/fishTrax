import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

#omr stats
tp = 12
'''
ePreOMRstats = aba.getOMRScoreStatsMulti(e_omr, stateRange=[3,3], timePoint=tp)
eEndOMRstats = aba.getOMRScoreStatsMulti(e_omr, stateRange=[8,8], timePoint=tp)
ePostOMRstats_2a= aba.getOMRScoreStatsMulti(e_omr_post, stateRange=[3,3], timePoint=tp)
ePostOMRstats_2b = aba.getOMRScoreStatsMulti(e_omr_post, stateRange=[8,8], timePoint=tp)
'''
ePreOMRstatsSame_1a= aba.getOMRScoreStatsMulti(e_omr_same_pre, stateRange=[3,3], timePoint=tp)
ePreOMRstatsSame_1b = aba.getOMRScoreStatsMulti(e_omr_same_pre, stateRange=[8,8], timePoint=tp)
ePreOMRstatsSame = aba.getOMRScoreStatsMulti(e_omr_same, stateRange=[3,3], timePoint=tp)
#eEndOMRstatsSame = aba.getOMRScoreStatsMulti(e_omr_same, stateRange=[8,8], timePoint=tp)
eEndOMRstatsSame = aba.getOMRScoreStatsMulti(e_omr_same_last, stateRange=[8,8], timePoint=tp)
ePostOMRstatsSame_2a= aba.getOMRScoreStatsMulti(e_omr_same_post, stateRange=[3,3], timePoint=tp)
ePostOMRstatsSame_2b = aba.getOMRScoreStatsMulti(e_omr_same_post, stateRange=[8,8], timePoint=tp)

cPreOMRstats_1a= aba.getOMRScoreStatsMulti(c_omr_pre, stateRange=[3,3], timePoint=tp)
cPreOMRstats_1b = aba.getOMRScoreStatsMulti(c_omr_pre, stateRange=[8,8], timePoint=tp)
cPreOMRstats = aba.getOMRScoreStatsMulti(c_omr, stateRange=[3,3], timePoint=tp)
#cEndOMRstats = aba.getOMRScoreStatsMulti(c_omr, stateRange=[8,8], timePoint=tp)
cEndOMRstats = aba.getOMRScoreStatsMulti(c_omr_last, stateRange=[8,8], timePoint=tp)
cPostOMRstats_2a= aba.getOMRScoreStatsMulti(c_omr_post, stateRange=[3,3], timePoint=tp)
cPostOMRstats_2b = aba.getOMRScoreStatsMulti(c_omr_post, stateRange=[8,8], timePoint=tp)

#velocity stats 
sm=15
'''
ePreVel_1a = aba.getMedianVelMulti(e_omr_pre, tRange=[0,15*30], smoothWinLen = sm)
ePreVel_1b = aba.getMedianVelMulti(e_omr_pre, tRange=[15*30,30*30], smoothWinLen = sm)
eVel = aba.getMedianVelMulti(e_omr, stateRange=[3,3], smoothWinLen=sm)
eEndVel = aba.getMedianVelMulti(e_omr, stateRange=[8,8], smoothWinLen=sm)
ePostVel_2a = aba.getMedianVelMulti(e_omr_post, stateRange=[3,3], smoothWinLen = sm)
ePostVel_2b = aba.getMedianVelMulti(e_omr_post, stateRange=[8,8], smoothWinLen = sm)
'''
ePreVelSame_1a = aba.getMedianVelMulti(e_omr_same_pre, tRange=[0,15*30], smoothWinLen = sm)
ePreVelSame_1b = aba.getMedianVelMulti(e_omr_same_pre, tRange=[15*30,30*30], smoothWinLen = sm)
eVelSame = aba.getMedianVelMulti(e_omr_same, stateRange=[3,3], smoothWinLen=sm)
#eEndVelSame = aba.getMedianVelMulti(e_omr_same, stateRange=[8,8], smoothWinLen=sm)
eEndVelSame = aba.getMedianVelMulti(e_omr_same_last, stateRange=[8,8], smoothWinLen=sm)
ePostVelSame_2a = aba.getMedianVelMulti(e_omr_same_post, stateRange=[3,3], smoothWinLen = sm)
ePostVelSame_2b = aba.getMedianVelMulti(e_omr_same_post, stateRange=[8,8], smoothWinLen = sm)

cPreVel_1a = aba.getMedianVelMulti(c_omr_pre, tRange=[0,15*30], smoothWinLen = sm)
cPreVel_1b = aba.getMedianVelMulti(c_omr_pre, tRange=[15*30,30*30], smoothWinLen = sm)
cVel = aba.getMedianVelMulti(c_omr, stateRange=[3,3], smoothWinLen=sm)
#cEndVel = aba.getMedianVelMulti(c_omr, stateRange=[8,8], smoothWinLen=sm)
cEndVel = aba.getMedianVelMulti(c_omr_last, stateRange=[8,8], smoothWinLen=sm)
cPostVel_2a = aba.getMedianVelMulti(c_omr_post, stateRange=[3,3], smoothWinLen = sm)
cPostVel_2b = aba.getMedianVelMulti(c_omr_post, stateRange=[8,8], smoothWinLen = sm)
'''
#velocity comparisons 
[tv, exper_start_end] = scipy.stats.ttest_ind(ePreVel, ePostVel)
[tv, exper_end_end] = scipy.stats.ttest_ind(esafePostVel, ePostVel)
[tv, exper_start_end_post] = scipy.stats.ttest_ind(esafePreVel, esafePostVel)
print "Stats (pre end vel, end end vel, start to end post):", exper_start_end, exper_end_end, exper_start_end_post
'''
def plotPairedConditions(states, statenames, color=[.5,.5,.5], ylabel=None, title=None):
    pyplot.hold(True)
    #for nState, state in enumerate(states):
    #    pyplot.plot(nState, [state], '.', color=color)
    pyplot.plot(range(len(states)),np.vstack(states),'.-', color=color)
    pyplot.xlim([-.25,len(states)-.75])
    ax = pyplot.gca()
    ax.set_xticks(range(len(states)))
    ax.set_xticklabels(statenames)
    if ylabel is not None:
        pyplot.ylabel(ylabel)
    if title is not None:
        pyplot.title(title)

def plotPairedConditionsMeanAndSEM(states, statenames, fmt='o-', color=[0,0,0], ylabel=None, title=None):
    pyplot.hold(True)
    yerr = []
    yu = []
    for nState, state in enumerate(states):
        yerr.append(2*scipy.stats.sem(state))
        yu.append(np.mean(state))
    print yu
    print yerr
    pyplot.errorbar(range(len(states)),yu,fmt=fmt, color=color, yerr=yerr, lw=3)
    pyplot.xlim([-.25,len(states)-.75])
    ax = pyplot.gca()
    ax.set_xticks(range(len(states)))
    ax.set_xticklabels(statenames)
    if ylabel is not None:
        pyplot.ylabel(ylabel)
    if title is not None:
        pyplot.title(title)


#omr analyzsis
#show recovery (missing controls)
pyplot.figure()
pyplot.gcf().set_facecolor('w')
pyplot.suptitle('Helplessness Assay with OMR')

ax = pyplot.subplot2grid((1,2), (0,0))
pyplot.title('Control Velocity')
plotPairedConditions([cPreVel_1a,cPreVel_1b,cVel, cEndVel, cPostVel_2a, cPostVel_2b],['Pre-Shock\n0-15 min','Pre-Shock\n 15-30 min', 'Acclimation','Post-shock', 'Recovery\n0-15','Recovery\n15-30'], color=[.5,.5,.5])
plotPairedConditionsMeanAndSEM([cPreVel_1a,cPreVel_1b,cVel, cEndVel, cPostVel_2a, cPostVel_2b],['Pre-Shock\n0-15 min','Pre-Shock\n 15-30 min', 'Acclimation','Post-shock', 'Recovery\n0-15','Recovery\n15-30'], color=[0,0,0])
pyplot.ylim((0,5.5))
pyplot.axvspan(1.5,3.5,facecolor='g',alpha=.5)

ax = pyplot.subplot2grid((1,2), (0,1))
pyplot.title('Experimental Velocity')
plotPairedConditions([ePreVelSame_1a,ePreVelSame_1b,eVelSame, eEndVelSame, ePostVelSame_2a, ePostVelSame_2b],['Pre-Shock\n0-15 min','Pre-Shock\n 15-30 min', 'Acclimation','Post-shock', 'Recovery\n0-15','Recovery\n15-30'], color=[.5,.5,.5])
plotPairedConditionsMeanAndSEM([ePreVelSame_1a,ePreVelSame_1b,eVelSame, eEndVelSame, ePostVelSame_2a, ePostVelSame_2b],['Pre-Shock\n0-15 min','Pre-Shock\n 15-30 min', 'Acclimation','Post-shock', 'Recovery\n0-15','Recovery\n15-30'], color=[0,0,0])
pyplot.ylim((0,5.5))
pyplot.axvspan(1.5,3.5,facecolor='g',alpha=.5)


pyplot.figure()
ax=pyplot.subplot(121)
pyplot.title('Control OMR')
plotPairedConditions([cPreOMRstats_1a['omrResults']['avgnorm'],cPreOMRstats_1b['omrResults']['avgnorm'], cPreOMRstats['omrResults']['avgnorm'],cEndOMRstats['omrResults']['avgnorm'], cPostOMRstats_2a['omrResults']['avgnorm'],cPostOMRstats_2b['omrResults']['avgnorm']],['Pre-shock \n 0-15', 'Pre-shock\n 15-30','Pre\nShock','Post\nShock','Post shock \n 0-15','Post shock\n15-30'],color='b')
plotPairedConditionsMeanAndSEM([cPreOMRstats_1a['omrResults']['avgnorm'], cPreOMRstats_1b['omrResults']['avgnorm'],cPreOMRstats['omrResults']['avgnorm'],cEndOMRstats['omrResults']['avgnorm'],cPostOMRstats_2a['omrResults']['avgnorm'],cPostOMRstats_2b['omrResults']['avgnorm']],['Pre-shock \n 0-15', 'Pre-shock\n 15-30','Pre\nShock','Post\nShock','Post shock \n 0-15','Post shock\n15-30'],color='b')
ax=pyplot.subplot(122)
pyplot.title('Experimental OMR')
plotPairedConditions([ePreOMRstatsSame_1a['omrResults']['avgnorm'],ePreOMRstatsSame_1b['omrResults']['avgnorm'], ePreOMRstatsSame['omrResults']['avgnorm'],eEndOMRstatsSame['omrResults']['avgnorm'],ePostOMRstatsSame_2a['omrResults']['avgnorm'],ePostOMRstatsSame_2b['omrResults']['avgnorm']],['Pre-shock \n 0-15', 'Pre-shock\n 15-30','Pre\nShock','Post\nShock','Post shock \n 0-15','Post shock\n15-30'],color='b')
plotPairedConditionsMeanAndSEM([ePreOMRstatsSame_1a['omrResults']['avgnorm'],ePreOMRstatsSame_1b['omrResults']['avgnorm'],ePreOMRstatsSame['omrResults']['avgnorm'],eEndOMRstatsSame['omrResults']['avgnorm'],ePostOMRstatsSame_2a['omrResults']['avgnorm'],ePostOMRstatsSame_2b['omrResults']['avgnorm']],['Pre-shock \n 0-15', 'Pre-shock\n 15-30','Pre\nShock','Post\nShock','Post shock \n 0-15','Post shock\n15-30'],color='b')


#show signficance of OMR response
pyplot.figure()
pyplot.gcf().set_facecolor('w')

ax = pyplot.subplot2grid((2,2), (0,0))
_, p = scipy.stats.ttest_rel(cPreOMRstats['omrResults']['avgnorm'],cPreOMRstats['omrControl']['avgnorm'])
plotPairedConditions([cPreOMRstats['omrControl']['avgnorm'],cPreOMRstats['omrResults']['avgnorm']],['NonOMR','OMR'], color=[.5,.5,.5], ylabel='Normalized OMR Metric', title='Pre Shock Control p=%0.3f'%p)
pyplot.ylim((0,1))
ax = pyplot.subplot2grid((2,2), (0,1))
_, p = scipy.stats.ttest_rel(cEndOMRstats['omrResults']['avgnorm'],cEndOMRstats['omrControl']['avgnorm'])
plotPairedConditions([cEndOMRstats['omrControl']['avgnorm'],cEndOMRstats['omrResults']['avgnorm']],['NonOMR','OMR'], color=[.5,.5,.5], ylabel='Normalized OMR Metric', title='Post Shock Control p=%0.3f'%p)
pyplot.ylim((0,1))
ax = pyplot.subplot2grid((2,2), (1,0))
_, p = scipy.stats.ttest_rel(ePreOMRstatsSame['omrResults']['avgnorm'],ePreOMRstatsSame['omrControl']['avgnorm'])
plotPairedConditions([ePreOMRstatsSame['omrControl']['avgnorm'],ePreOMRstatsSame['omrResults']['avgnorm']],['NonOMR','OMR'], color=[.5,.5,.5], ylabel='Normalized OMR Metric', title='Pre Shock Same p=%0.3f'%p)
pyplot.ylim((0,1))
ax = pyplot.subplot2grid((2,2), (1,1))
_, p = scipy.stats.ttest_rel(eEndOMRstatsSame['omrResults']['avgnorm'],eEndOMRstatsSame['omrControl']['avgnorm'])
plotPairedConditions([eEndOMRstatsSame['omrControl']['avgnorm'],eEndOMRstatsSame['omrResults']['avgnorm']],['NonOMR','OMR'], color=[.5,.5,.5], ylabel='Normalized OMR Metric', title='Post Shock Same p=%0.3f'%p)
pyplot.ylim((0,1))



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

