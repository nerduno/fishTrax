import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

c_omr= ['/Users/andalman/Dropbox/ConchisData/2013-10-02/f00705/f00705_2013-10-02-10-15-25.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00706/f00706_2013-10-02-10-15-18.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00707/f00707_2013-10-02-10-15-11.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00708/f00708_2013-10-02-10-15-00.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00709/f00709_2013-10-02-10-14-53.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00710/f00710_2013-10-02-10-14-46.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00711/f00711_2013-10-02-10-14-39.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00712/f00712_2013-10-02-10-14-31.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00721/f00721_2013-10-02-12-12-59.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00722/f00722_2013-10-02-12-12-51.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00723/f00723_2013-10-02-12-12-44.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00724/f00724_2013-10-02-12-12-35.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00725/f00725_2013-10-02-12-12-27.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00726/f00726_2013-10-02-12-12-13.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00727/f00727_2013-10-02-12-12-02.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00728/f00728_2013-10-02-12-11-55.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00737/f00737_2013-10-02-13-45-00.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00738/f00738_2013-10-02-13-44-48.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00739/f00739_2013-10-02-13-44-41.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00740/f00740_2013-10-02-13-44-34.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00741/f00741_2013-10-02-13-44-25.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00742/f00742_2013-10-02-13-44-17.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00743/f00743_2013-10-02-13-44-07.json',
        '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00744/f00744_2013-10-02-13-44-01.json']
c_omr = aba.loadMultipleDataFiles(c_omr)

e_omr = ['~/Dropbox/ConchisData/2013-10-03/f00753/f00753_2013-10-03-13-24-05.json',
         '~/Dropbox/ConchisData/2013-10-03/f00754/f00754_2013-10-03-13-24-13.json',
         '~/Dropbox/ConchisData/2013-10-03/f00755/f00755_2013-10-03-13-24-22.json',
         '~/Dropbox/ConchisData/2013-10-03/f00756/f00756_2013-10-03-13-24-34.json',
         '~/Dropbox/ConchisData/2013-10-03/f00757/f00757_2013-10-03-13-25-15.json',
         '~/Dropbox/ConchisData/2013-10-03/f00758/f00758_2013-10-03-13-25-09.json',
         '~/Dropbox/ConchisData/2013-10-03/f00759/f00759_2013-10-03-13-24-59.json',
         '~/Dropbox/ConchisData/2013-10-03/f00760/f00760_2013-10-03-13-24-50.json',
         '~/Dropbox/ConchisData/2013-10-03/f00761/f00761_2013-10-03-15-22-25.json',
         '~/Dropbox/ConchisData/2013-10-03/f00762/f00762_2013-10-03-15-22-20.json',
         '~/Dropbox/ConchisData/2013-10-03/f00763/f00763_2013-10-03-15-22-12.json',
         '~/Dropbox/ConchisData/2013-10-03/f00764/f00764_2013-10-03-15-22-05.json',
         '~/Dropbox/ConchisData/2013-10-03/f00765/f00765_2013-10-03-15-23-01.json',
         '~/Dropbox/ConchisData/2013-10-03/f00766/f00766_2013-10-03-15-22-51.json',
         '~/Dropbox/ConchisData/2013-10-03/f00767/f00767_2013-10-03-15-22-38.json',
         '~/Dropbox/ConchisData/2013-10-03/f00768/f00768_2013-10-03-15-22-32.json',
         '~/Dropbox/ConchisData/2013-10-04/f00769/f00769_2013-10-04-09-56-41.json',
         '~/Dropbox/ConchisData/2013-10-04/f00770/f00770_2013-10-04-09-56-34.json',
         '~/Dropbox/ConchisData/2013-10-04/f00771/f00771_2013-10-04-09-56-21.json',
         '~/Dropbox/ConchisData/2013-10-04/f00772/f00772_2013-10-04-09-56-15.json',
         # '~/Dropbox/ConchisData/2013-10-04/f00773/f00773_2013-10-04-09-57-09.json', #low starting vel
         '~/Dropbox/ConchisData/2013-10-04/f00774/f00774_2013-10-04-09-57-02.json',
         '~/Dropbox/ConchisData/2013-10-04/f00775/f00775_2013-10-04-09-56-55.json',
         # '~/Dropbox/ConchisData/2013-10-04/f00776/f00776_2013-10-04-09-56-49.json' #low starting vel
         ]
e_omr = aba.loadMultipleDataFiles(e_omr)

e_omr_post = ['~/Dropbox/ConchisData/2013-10-03/f00753/f00753_2013-10-03-14-33-29.json',
              '~/Dropbox/ConchisData/2013-10-03/f00754/f00754_2013-10-03-14-33-00.json',
              '~/Dropbox/ConchisData/2013-10-03/f00755/f00755_2013-10-03-14-32-34.json',
              '~/Dropbox/ConchisData/2013-10-03/f00756/f00756_2013-10-03-14-32-42.json',
              '~/Dropbox/ConchisData/2013-10-03/f00757/f00757_2013-10-03-14-34-50.json',
              '~/Dropbox/ConchisData/2013-10-03/f00758/f00758_2013-10-03-14-34-45.json',
              '~/Dropbox/ConchisData/2013-10-03/f00759/f00759_2013-10-03-14-34-39.json',
              '~/Dropbox/ConchisData/2013-10-03/f00760/f00760_2013-10-03-14-34-33.json',
              '~/Dropbox/ConchisData/2013-10-03/f00761/f00761_2013-10-03-16-30-57.json',
              '~/Dropbox/ConchisData/2013-10-03/f00762/f00762_2013-10-03-16-31-26.json',
              '~/Dropbox/ConchisData/2013-10-03/f00763/f00763_2013-10-03-16-31-36.json',
              '~/Dropbox/ConchisData/2013-10-03/f00764/f00764_2013-10-03-16-31-40.json',
              '~/Dropbox/ConchisData/2013-10-03/f00765/f00765_2013-10-03-16-32-47.json',
              '~/Dropbox/ConchisData/2013-10-03/f00766/f00766_2013-10-03-16-32-54.json',
              '~/Dropbox/ConchisData/2013-10-03/f00767/f00767_2013-10-03-16-33-03.json',
              '~/Dropbox/ConchisData/2013-10-03/f00768/f00768_2013-10-03-16-33-16.json',
              '~/Dropbox/ConchisData/2013-10-04/f00769/f00769_2013-10-04-11-11-05.json',
              '~/Dropbox/ConchisData/2013-10-04/f00770/f00770_2013-10-04-11-11-14.json',
              '~/Dropbox/ConchisData/2013-10-04/f00771/f00771_2013-10-04-11-11-29.json',
              '~/Dropbox/ConchisData/2013-10-04/f00772/f00772_2013-10-04-11-11-35.json',
              # '~/Dropbox/ConchisData/2013-10-04/f00773/f00773_2013-10-04-11-12-15.json',
              '~/Dropbox/ConchisData/2013-10-04/f00774/f00774_2013-10-04-11-12-22.json',
              '~/Dropbox/ConchisData/2013-10-04/f00775/f00775_2013-10-04-11-12-28.json',
              # '~/Dropbox/ConchisData/2013-10-04/f00776/f00776_2013-10-04-11-12-36.json'
              ]
e_omr_post = aba.loadMultipleDataFiles(e_omr_post)

#omr stats
tp = 12
cPreOMRstats = aba.getOMRScoreStatsMulti(c_omr, stateRange=[3,3], timePoint=tp)
cPostOMRstats = aba.getOMRScoreStatsMulti(c_omr, stateRange=[8,8], timePoint=tp)
ePreOMRstats = aba.getOMRScoreStatsMulti(e_omr, stateRange=[3,3], timePoint=tp)
ePostOMRstats = aba.getOMRScoreStatsMulti(e_omr, stateRange=[8,8], timePoint=tp)
esafePreOMRstats = aba.getOMRScoreStatsMulti(e_omr_post, stateRange=[3,3], timePoint=tp)
esafePostOMRstats = aba.getOMRScoreStatsMulti(e_omr_post, stateRange=[8,8], timePoint=tp)

#velocity stats 
sm=15
cPreVel = aba.getMedianVelMulti(c_omr, stateRange=[3,3], smoothWinLen = sm)
cPostVel = aba.getMedianVelMulti(c_omr, stateRange=[8,8], smoothWinLen=sm)
ePreVel = aba.getMedianVelMulti(e_omr, stateRange=[3,3], smoothWinLen = sm)
ePostVel = aba.getMedianVelMulti(e_omr, stateRange=[8,8], smoothWinLen=sm)
esafePreVel = aba.getMedianVelMulti(e_omr_post, stateRange=[3,3], smoothWinLen = sm)
esafePostVel = aba.getMedianVelMulti(e_omr_post, stateRange=[8,8], smoothWinLen=sm)

#velocity comparisons 
[tv, exper_start_end] = scipy.stats.ttest_ind(ePreVel, ePostVel)
[tv, exper_end_end] = scipy.stats.ttest_ind(esafePostVel, ePostVel)
[tv, exper_start_end_post] = scipy.stats.ttest_ind(esafePreVel, esafePostVel)
print "Stats (pre end vel, end end vel, start to end post):", exper_start_end, exper_end_end, exper_start_end_post

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

#show that shock reduces omr response.
pyplot.figure()
pyplot.gcf().set_facecolor('w')
pyplot.suptitle('Helplessness Assay with OMR')

ax = pyplot.subplot2grid((1,2), (0,0))
plotPairedConditions([ePreVel,ePostVel],['Pre Shock','Post\nShock'], color=[.5,.5,1], ylabel='Median Speed (mm/s)', title='Speed')
plotPairedConditions([cPreVel,cPostVel],['Pre\nShock','Post\nShock'], color=[.5,.5,.5])
plotPairedConditionsMeanAndSEM([ePreVel,ePostVel],['Pre\nShock','Post\nShock'],color='b')
plotPairedConditionsMeanAndSEM([cPreVel,cPostVel],['Pre\nShock','Post\nShock'],color='k')
pyplot.ylim((0,5.5))

ax = pyplot.subplot2grid((1,2), (0,1))
plotPairedConditions([ePreOMRstats['omrResults']['avgnorm'],ePostOMRstats['omrResults']['avgnorm']],['Pre\nShock','Post\nShock'], color=[.5,.5,1], ylabel='Normalized OMR Metric', title='OMR Response')
plotPairedConditions([cPreOMRstats['omrResults']['avgnorm'],cPostOMRstats['omrResults']['avgnorm']],['Pre\nShock','Post\nShock'], color=[.5,.5,.5])
plotPairedConditionsMeanAndSEM([ePreOMRstats['omrResults']['avgnorm'],ePostOMRstats['omrResults']['avgnorm']],['Pre\nShock','Post\nShock'],color='b')
plotPairedConditionsMeanAndSEM([cPreOMRstats['omrResults']['avgnorm'],cPostOMRstats['omrResults']['avgnorm']],['Pre\nShock','Post\nShock'],color='k')
pyplot.ylim((0,1))


#show recovery (missing controls)
pyplot.figure()
pyplot.gcf().set_facecolor('w')
pyplot.suptitle('Helplessness Assay with OMR')

ax = pyplot.subplot2grid((1,2), (0,0))
plotPairedConditions([cPreVel,cPostVel],['Pre\nShock','Post\nShock'], color=[.5,.5,.5])
plotPairedConditions([ePreVel,ePostVel,esafePreVel, esafePostVel],
                     ['Pre\nShock','Post\nShock','Early New\nContext','Late New\nContext'], color=[.5,.5,1], ylabel='Median Speed (mm/s)', title='Speed')
plotPairedConditionsMeanAndSEM([cPreVel,cPostVel],['Pre\nShock','Post\nShock'],color='k')
plotPairedConditionsMeanAndSEM([ePreVel,ePostVel,esafePreVel,esafePostVel],
                               ['Pre\nShock','Post\nShock','Early New\nContext','Late New\nContext'], color='b')
pyplot.ylim((0,5.5))
pyplot.axvspan(-.5,1.5,facecolor='g',alpha=.5)


ax = pyplot.subplot2grid((1,2), (0,1))
plotPairedConditions([cPreOMRstats['omrResults']['avgnorm'],cPostOMRstats['omrResults']['avgnorm']],
                     ['Pre\nShock','Post\nShock'], color=[.5,.5,.5])
plotPairedConditions([ePreOMRstats['omrResults']['avgnorm'],ePostOMRstats['omrResults']['avgnorm'],
                      esafePreOMRstats['omrResults']['avgnorm'],esafePostOMRstats['omrResults']['avgnorm']],
                     ['Pre\nShock','Post\nShock','Early New\nContext','Late New\nContext'], color=[.5,.5,1], ylabel='Normalized OMR Metric', title='OMR Response')
plotPairedConditionsMeanAndSEM([cPreOMRstats['omrResults']['avgnorm'],cPostOMRstats['omrResults']['avgnorm']],
                               ['Pre\nShock','Post\nShock'],color='k')
plotPairedConditionsMeanAndSEM([ePreOMRstats['omrResults']['avgnorm'],ePostOMRstats['omrResults']['avgnorm'],
                               esafePreOMRstats['omrResults']['avgnorm'],esafePostOMRstats['omrResults']['avgnorm']],
                               ['Pre\nShock','Post\nShock','Early New\nContext','Late New\nContext'],color='b')
pyplot.ylim((0,1))
pyplot.axvspan(-.5,1.5,facecolor='g',alpha=.5)

#show signficance of OMR response
pyplot.figure()
pyplot.gcf().set_facecolor('w')

ax = pyplot.subplot2grid((2,2), (0,0))
_, p = scipy.stats.ttest_rel(cPreOMRstats['omrResults']['avgnorm'],cPreOMRstats['omrControl']['avgnorm'])
plotPairedConditions([cPreOMRstats['omrControl']['avgnorm'],cPreOMRstats['omrResults']['avgnorm']],['NonOMR','OMR'], color=[.5,.5,.5], ylabel='Normalized OMR Metric', title='Pre Shock Control p=%0.3f'%p)
plotPairedConditionsMeanAndSEM([cPreOMRstats['omrControl']['avgnorm'],cPreOMRstats['omrResults']['avgnorm']],['NonOMR','OMR'], color=[0,0,0], ylabel='Normalized OMR Metric', title='Pre Shock Control p=%0.3f'%p)
pyplot.ylim((0,1))
 
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

pylab.show()

