import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

#15 acclimation, 30 shock bouts, 5 min post.
e_omr = ['/home/vburns/Dropbox/ConchisData/2013-10-03/f00753/f00753_2013-10-03-13-24-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00754/f00754_2013-10-03-13-24-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00755/f00755_2013-10-03-13-24-22.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00756/f00756_2013-10-03-13-24-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00757/f00757_2013-10-03-13-25-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00758/f00758_2013-10-03-13-25-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00759/f00759_2013-10-03-13-24-59.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00760/f00760_2013-10-03-13-24-50.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00761/f00761_2013-10-03-15-22-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00762/f00762_2013-10-03-15-22-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00763/f00763_2013-10-03-15-22-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00764/f00764_2013-10-03-15-22-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00765/f00765_2013-10-03-15-23-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00766/f00766_2013-10-03-15-22-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00767/f00767_2013-10-03-15-22-38.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00768/f00768_2013-10-03-15-22-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-04/f00769/f00769_2013-10-04-09-56-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-04/f00770/f00770_2013-10-04-09-56-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-04/f00771/f00771_2013-10-04-09-56-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-04/f00772/f00772_2013-10-04-09-56-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-04/f00773/f00773_2013-10-04-09-57-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-04/f00774/f00774_2013-10-04-09-57-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-04/f00775/f00775_2013-10-04-09-56-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-04/f00776/f00776_2013-10-04-09-56-49.json']
e_omr = aba.loadMultipleDataFiles(e_omr)

e_omr_post = ['/home/vburns/Dropbox/ConchisData/2013-10-03/f00753/f00753_2013-10-03-14-33-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00754/f00754_2013-10-03-14-33-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00755/f00755_2013-10-03-14-32-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00756/f00756_2013-10-03-14-32-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00757/f00757_2013-10-03-14-34-50.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00758/f00758_2013-10-03-14-34-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00759/f00759_2013-10-03-14-34-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00760/f00760_2013-10-03-14-34-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00761/f00761_2013-10-03-16-30-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00762/f00762_2013-10-03-16-31-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00763/f00763_2013-10-03-16-31-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00764/f00764_2013-10-03-16-31-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00765/f00765_2013-10-03-16-32-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00767/f00767_2013-10-03-16-33-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-03/f00768/f00768_2013-10-03-16-33-16.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-04/f00769/f00769_2013-10-04-11-11-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-04/f00770/f00770_2013-10-04-11-11-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-04/f00771/f00771_2013-10-04-11-11-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-04/f00772/f00772_2013-10-04-11-11-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-04/f00773/f00773_2013-10-04-11-12-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-04/f00774/f00774_2013-10-04-11-12-22.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-04/f00775/f00775_2013-10-04-11-12-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-04/f00776/f00776_2013-10-04-11-12-36.json']
e_omr_post = aba.loadMultipleDataFiles(e_omr_post)

#omr stats
tp = 10
tp2 = 15
ePreOMRstats = aba.getOMRScoreStatsMulti(e_omr, stateRange=[3,3], timePoint=tp)
ePostOMRstats = aba.getOMRScoreStatsMulti(e_omr, stateRange=[8,8], timePoint=tp)
esafePreOMRstats = aba.getOMRScoreStatsMulti(e_omr_post, stateRange=[3,3], timePoint=tp2)
esafeOMRstats = aba.getOMRScoreStatsMulti(c_omr, stateRange=[8,8], timePoint=tp2)

#velocity stats 
sm=15
ePreVel = aba.getMedianVelMulti(e_omr, stateRange=[3,3], smoothWinLen = sm)
ePostVel = aba.getMedianVelMulti(e_omr, stateRange=[8,8], smoothWinLen=sm)
esafePreVel = aba.getMedianVelMulti(c_omr, stateRange=[3,3], smoothWinLen = sm)
esafePostVel = aba.getMedianVelMulti(c_omr, stateRange=[8,8], smoothWinLen=sm)

#velocity comparisons 
[tv, exper_start_end] = scipy.stats.ttest_ind(ePreVel, ePostVel)


def plotPairedScatterWithMeanAndSEM(state1,state2,state1name='state1',state2name='state2',color='k', lcolor=[.5,.5,.5], ylabel='', title=''):
    pyplot.plot(0, [state1], '.', color=color)
    pyplot.hold(True)
    pyplot.plot(1, [state2], '.', color=color)
    pyplot.hold(True)
    pyplot.plot(3, [state3],'.',color=color)
    pyplot.hold(True)
    pyplot.plot(4, [state4], '.', color=color)
    pyplot.plot([0,1,2,3],np.vstack([state1,state2,state3, state4]), '-', color=lcolor)
    yerr = (2*scipy.stats.sem(state1), 2*scipy.stats.sem(state2), 2*scipy.stats.sem(state3), 2*scipy.stats.sem(state4))
    pyplot.errorbar([0,1,2,3],[np.mean(state1), np.mean(state2), np.mean(state3), np.mean(state4)],fmt='o-', color=color, yerr=yerr, lw=3)
    ax.set_xticks((0,1,2,3))
    ax.set_xticklabels((state1name,state2name, state3name, state4name))
    pyplot.xlim((-.25,3.25))
    pyplot.ylabel(ylabel)
    pyplot.title(title)
    
#om
pyplot.figure()
pyplot.suptitle('OMR-based Learned Helplessness Assay at 5V (experimental fish)')
ax = pyplot.subplot2grid((2,4), (0,0), colspan=4)
plotPairedScatterWithMeanAndSEM(ePreVel,ePostVel,esafePreVel, esafePostVel,'Pre','Post','0-15', '15-30',color='r',
                                ylabel='Median Speed (mm/s)', title='Experimental Velocity with OMR')
pyplot.ylim((0,5.5))

ax = pyplot.subplot2grid((2,2), (1,1), colspan=2)
plotPairedScatterWithMeanAndSEM(ePreOMRstats['omrResults']['avgnorm'], ePostOMRstats['omrResults']['avgnorm'], esafePreOMRstats['omrResults']['avgnomr'], esafePostOMRstats['omrResults']['avgnorm'],'Pre',
                                'Post', '0-15', '15-30',color='r', lcolor=[1,.5,.5], ylabel='OMRscore', title='Experimental OMR Response')
pyplot.ylim((0,.8))
"""
ax = pyplot.subplot2grid((2,2), (1,3), colspan=2)
plotPairedScatterWithMeanAndSEM(cPreOMRstats['omrResults']['avgnorm'], cPostOMRstats['omrResults']['avgnorm'], 'Pre',
                                'Post', color='r', lcolor=[1,.5,.5], ylabel='OMRscore', title='Control OMR Response')
pyplot.ylim((0,.8))

_, p_cPreOMR = scipy.stats.ttest_rel(cPreOMRstats['omrResults']['avgnorm'],cPreOMRstats['omrControl']['avgnorm'])
_, p_cPostOMR = scipy.stats.ttest_rel(cPostOMRstats['omrResults']['avgnorm'],cPostOMRstats['omrControl']['avgnorm'])
_, p_ePreOMR = scipy.stats.ttest_rel(ePreOMRstats['omrResults']['avgnorm'],ePreOMRstats['omrControl']['avgnorm'])
_, p_ePostOMR = scipy.stats.ttest_rel(ePostOMRstats['omrResults']['avgnorm'],ePostOMRstats['omrControl']['avgnorm'])
_, p_ePreVsPostOMR = scipy.stats.ttest_rel(ePostOMRstats['omrResults']['avgnorm'],ePreOMRstats['omrResults']['avgnorm'])
_, p_cPreVsPostOMR = scipy.stats.ttest_rel(cPostOMRstats['omrResults']['avgnorm'],cPreOMRstats['omrResults']['avgnorm'])
print 'OMR response p-values cPre %f cPost %f ePre %f ePost %f'%(p_cPreOMR, p_cPostOMR, p_ePreOMR, p_ePostOMR)
print 'OMR response to shocks exp %f control %f'%(p_ePreVsPostOMR,p_cPreVsPostOMR)
"""
pylab.show()
