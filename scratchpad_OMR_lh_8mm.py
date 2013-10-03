import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

#15 acclimation, 30 shock bouts, 5 min post.
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

e_omr = ['/Users/andalman/Dropbox/ConchisData/2013-10-02/f00713/f00713_2013-10-02-10-20-49.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00714/f00714_2013-10-02-10-20-40.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00715/f00715_2013-10-02-10-20-32.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00716/f00716_2013-10-02-10-20-23.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00717/f00717_2013-10-02-10-20-13.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00718/f00718_2013-10-02-10-20-06.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00719/f00719_2013-10-02-10-19-50.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00720/f00720_2013-10-02-10-19-40.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00729/f00729_2013-10-02-12-16-08.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00730/f00730_2013-10-02-12-16-15.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00731/f00731_2013-10-02-12-16-22.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00732/f00732_2013-10-02-12-16-29.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00733/f00733_2013-10-02-12-16-36.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00734/f00734_2013-10-02-12-16-46.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00735/f00735_2013-10-02-12-17-01.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00736/f00736_2013-10-02-12-17-06.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00745/f00745_2013-10-02-13-47-28.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00746/f00746_2013-10-02-13-47-22.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00747/f00747_2013-10-02-13-47-14.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00748/f00748_2013-10-02-13-47-06.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00749/f00749_2013-10-02-13-46-58.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00750/f00750_2013-10-02-13-46-52.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00751/f00751_2013-10-02-13-46-44.json',
         '/Users/andalman/Dropbox/ConchisData/2013-10-02/f00752/f00752_2013-10-02-13-46-38.json']
e_omr = aba.loadMultipleDataFiles(e_omr)

#omr stats
tp = 10
ePreOMRstats = aba.getOMRScoreStatsMulti(e_omr, stateRange=[3,3], timePoint=tp)
ePostOMRstats = aba.getOMRScoreStatsMulti(e_omr, stateRange=[8,8], timePoint=tp)
cPreOMRstats = aba.getOMRScoreStatsMulti(c_omr, stateRange=[3,3], timePoint=tp)
cPostOMRstats = aba.getOMRScoreStatsMulti(c_omr, stateRange=[8,8], timePoint=tp)

#velocity stats 
sm=15
ePreVel = aba.getMedianVelMulti(e_omr, stateRange=[3,3], smoothWinLen = sm)
ePostVel = aba.getMedianVelMulti(e_omr, stateRange=[8,8], smoothWinLen=sm)
cPreVel = aba.getMedianVelMulti(c_omr, stateRange=[3,3], smoothWinLen = sm)
cPostVel = aba.getMedianVelMulti(c_omr, stateRange=[8,8], smoothWinLen=sm)

#velocity comparisons 
[tv, exper_start_end] = scipy.stats.ttest_ind(ePreVel, ePostVel)
[tv, control_start_end] = scipy.stats.ttest_ind(cPreVel, cPostVel)
print 'Statistics comparing velocity between start and end velocity (experimental, control fish):', exper_start_end, control_start_end


def plotPairedScatterWithMeanAndSEM(state1,state2,state1name='state1',state2name='state2',color='k', lcolor=[.5,.5,.5], ylabel='', title=''):
    pyplot.plot(0, [state1], '.', color=color)
    pyplot.hold(True)
    pyplot.plot(1, [state2], '.', color=color)
    pyplot.plot([0,1],np.vstack([state1,state2]), '-', color=lcolor)
    yerr = (2*scipy.stats.sem(state1), 2*scipy.stats.sem(state2))
    pyplot.errorbar([0,1],[np.mean(state1), np.mean(state2)],fmt='o-', color=color, yerr=yerr, lw=3)
    ax.set_xticks((0,1))
    ax.set_xticklabels((state1name,state2name))
    pyplot.xlim((-.25,1.25))
    pyplot.ylabel(ylabel)
    pyplot.title(title)
    

#om
pyplot.figure()
pyplot.suptitle('OMR-based Learned Helplessness Assay at 5V (experimental fish)')
ax = pyplot.subplot2grid((2,2), (0,0))
plotPairedScatterWithMeanAndSEM(ePreVel,ePostVel,'Pre','Post',color='r',
                                ylabel='Median Speed (mm/s)', title='Experimental Velocity with OMR')
pyplot.ylim((0,5.5))

ax = pyplot.subplot2grid((2,2), (0,1))
plotPairedScatterWithMeanAndSEM(cPreVel,cPostVel,'Pre','Post',color='k',
                                ylabel='Median Speed (mm/s)', title='Control Velocity with OMR')
pyplot.ylim((0,5.5))

ax = pyplot.subplot2grid((2,2), (1,0))
plotPairedScatterWithMeanAndSEM(ePreOMRstats['omrResults']['avgnorm'], ePostOMRstats['omrResults']['avgnorm'], 'Pre',
                                'Post', color='r', lcolor=[1,.5,.5], ylabel='OMRscore', title='Experimental OMR Response')
plotPairedScatterWithMeanAndSEM(ePreOMRstats['omrControl']['avgnorm'], ePostOMRstats['omrControl']['avgnorm'], 'Pre',
                                'Post', color='c', lcolor=[.7,1,1], ylabel='OMRscore', title='Experimental OMR Response')
pyplot.ylim((0,.8))

ax = pyplot.subplot2grid((2,2), (1,1))
plotPairedScatterWithMeanAndSEM(cPreOMRstats['omrResults']['avgnorm'], cPostOMRstats['omrResults']['avgnorm'], 'Pre',
                                'Post', color='r', lcolor=[1,.5,.5], ylabel='OMRscore', title='Control OMR Response')
plotPairedScatterWithMeanAndSEM(cPreOMRstats['omrControl']['avgnorm'], cPostOMRstats['omrControl']['avgnorm'], 'Pre',
                                'Post', color='c', lcolor=[.7,1,1], ylabel='OMRscore', title='Control OMR Response')
pyplot.ylim((0,.8))

_, p_cPreOMR = scipy.stats.ttest_rel(cPreOMRstats['omrResults']['avgnorm'],cPreOMRstats['omrControl']['avgnorm'])
_, p_cPostOMR = scipy.stats.ttest_rel(cPostOMRstats['omrResults']['avgnorm'],cPostOMRstats['omrControl']['avgnorm'])
_, p_ePreOMR = scipy.stats.ttest_rel(ePreOMRstats['omrResults']['avgnorm'],ePreOMRstats['omrControl']['avgnorm'])
_, p_ePostOMR = scipy.stats.ttest_rel(ePostOMRstats['omrResults']['avgnorm'],ePostOMRstats['omrControl']['avgnorm'])
_, p_ePreVsPostOMR = scipy.stats.ttest_rel(ePostOMRstats['omrResults']['avgnorm'],ePreOMRstats['omrResults']['avgnorm'])
_, p_cPreVsPostOMR = scipy.stats.ttest_rel(cPostOMRstats['omrResults']['avgnorm'],cPreOMRstats['omrResults']['avgnorm'])
print 'OMR response p-values cPre %f cPost %f ePre %f ePost %f'%(p_cPreOMR, p_cPostOMR, p_ePreOMR, p_ePostOMR)
print 'OMR response to shocks exp %f control %f'%(p_ePreVsPostOMR,p_cPreVsPostOMR)

#Alright so last time, we were had convinceing behavior, which seems reasonable rich...
# it has depression/learned helplessness/stress component
# it has memory component
#But our first attempt translate this behavior and image didn't go particularly well..
#most fish had low velocity, and even our best fish dropped dramatically in velocity with out shock.
#So rather than give on up this behavior, we been trying make the head fixed environment more naturalistic.
#The thought was to build a VR setup in which the fix would feel less fixed and in which we could present motivating stimuli.
#We build the following setup, description images, tie in with Noah.
#Images of setup
#Movie of tails
#C-Turns, Forward Swims, Escape Turns.
#Desciption of algorithm
#Movie of left right center
#Nice example of fish responding for an hour.
#So things looks good, the OMR seems to yield movements even when still, but this is somewhat of a concern
#b/c OMR may be immune to the reduced locamotion we can induce in-vivo.
#If OMR is immune to embedded suppression, maybe it is also immune to the LH protocol... so we set up the following experiment.
#Developed a system by whch OMR delivered to Free Swimming fish 
#Tested whether fish react to this system, they do.

#Need to do - show shocking reduces head-fixed OMR response.
#Need to do - show context change yield OMR recovery.
#Need to do - text water ph change.

#Poster goals: 
#Setting up for the future.
#Resolve why VR is somewhat stalled.

#Other stuff GCaMP6 fish (first movie?)
#Ted stuff.
#Sutter scope.
#RGeco with ChR2

"""
ax2=pylab.subplot2grid((2,3), (1,0))
pylab.plot(experimentalDist)
pylab.plot(0, [eBaseMaxDist],'r.')
pylab.plot(1, [eEndMaxDist],'r.')
pylab.plot([0,1],[np.mean(eBaseMaxDist), np.mean(eEndMaxDist)],'o-k',lw=3)
yerrMD = (2*scipy.stats.sem(eBaseMaxDist), 2*scipy.stats.sem(eEndMaxDist))
pyplot.errorbar([0,1],[np.mean(eBaseMaxDist), np.mean(eEndMaxDist)],fmt='ok',yerr=yerrMD, lw=3)
ax2.set_xticks((0,1))
ax2.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Maximum Distance')

ax3=pylab.subplot2grid((2,3),(1,1))
pylab.plot(experimentalTotalDist)
pylab.plot(0, [eBaseTotalDist],'r.')
pylab.plot(1, [eEndTotalDist],'r.')
pylab.plot([0,1],[np.mean(eBaseTotalDist), np.mean(eEndTotalDist)],'o-k',lw=3)
yerrTD = (2*scipy.stats.sem(eBaseTotalDist), 2*scipy.stats.sem(eEndTotalDist))
pyplot.errorbar([0,1],[np.mean(eBaseTotalDist), np.mean(eEndTotalDist)],fmt='ok',yerr=yerrTD, lw=3)
ax3.set_xticks((0,1))
ax3.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Total Distance')

ax4=pylab.subplot2grid((2,3),(1,2))
pylab.plot(experimentalFrac)
pylab.plot(0, [eBaseFrac],'r.')
pylab.plot(1, [eEndFrac],'r.')
pylab.plot([0,1],[np.mean(eBaseFrac), np.mean(eEndFrac)],'o-k',lw=3)
yerrF = (2*scipy.stats.sem(eBaseFrac), 2*scipy.stats.sem(eEndFrac))
pyplot.errorbar([0,1],[np.mean(eBaseFrac), np.mean(eEndFrac)],fmt='ok',yerr=yerrF, lw=3)
ax4.set_xticks((0,1))
ax4.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Fraction of time')

pylab.figure()
pylab.suptitle('OMR-based Learned Helplessness Assay at 5V (control fish)')
ax = pylab.subplot2grid((2,3), (0,0), colspan=3)
pylab.plot(0, [cPreVel], 'r.')
pylab.plot(1, [cPostVel], 'r.')
pylab.plot([0,1],[np.mean(cPreVel), np.mean(cPostVel)],'o-k',lw=3)
yerrC = (2*scipy.stats.sem(cPreVel), 2*scipy.stats.sem(cPostVel))
pyplot.errorbar([0,1],[np.mean(cPreVel), np.mean(cPostVel)],fmt='ok',yerr=yerr, lw=3)
ax.set_xticks((0,1,2,3))
ax.set_xticklabels(('baseline\n (15 min)','last 5 min', 'post 0-15', 'post 15-30'))
pylab.xlim((-.25,3.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Control Fish - OMR and Learned Helplessness')
patch1 = mpl.patches.Rectangle((-.25,0), 1.5,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax2=pylab.subplot2grid((2,3), (1,0))
pylab.plot(controlDist)
pylab.plot(0, [cBaseMaxDist],'r.')
pylab.plot(1, [cEndMaxDist],'r.')
pylab.plot([0,1],[np.mean(cBaseMaxDist), np.mean(cEndMaxDist)],'o-k',lw=3)
yerrMDC = (2*scipy.stats.sem(cBaseMaxDist), 2*scipy.stats.sem(cEndMaxDist))
pyplot.errorbar([0,1],[np.mean(cBaseMaxDist), np.mean(cEndMaxDist)],fmt='ok',yerr=yerrMD, lw=3)
ax2.set_xticks((0,1))
ax2.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Maximum Distance')
ax3=pylab.subplot2grid((2,3),(1,1))
pylab.plot(controlTotalDist)
pylab.plot(0, [cBaseTotalDist],'r.')
pylab.plot(1, [cEndTotalDist],'r.')
pylab.plot([0,1],[np.mean(cBaseTotalDist), np.mean(cEndTotalDist)],'o-k',lw=3)
yerrTDC = (2*scipy.stats.sem(cBaseTotalDist), 2*scipy.stats.sem(cEndTotalDist))
pyplot.errorbar([0,1],[np.mean(cBaseTotalDist), np.mean(cEndTotalDist)],fmt='ok',yerr=yerrTD, lw=3)
ax3.set_xticks((0,1))
ax3.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Total Distance')
ax4=pylab.subplot2grid((2,3),(1,2))
pylab.plot(controlFrac)
pylab.plot(0, [cBaseFrac],'r.')
pylab.plot(1, [cEndFrac],'r.')
pylab.plot([0,1],[np.mean(cBaseFrac), np.mean(cEndFrac)],'o-k',lw=3)
yerrFC = (2*scipy.stats.sem(cBaseFrac), 2*scipy.stats.sem(cEndFrac))
pyplot.errorbar([0,1],[np.mean(cBaseFrac), np.mean(cEndFrac)],fmt='ok',yerr=yerrF, lw=3)
ax4.set_xticks((0,1))
ax4.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Fraction of time')


pylab.figure()
pylab.suptitle('OMR-LH Summary')
ax = pylab.subplot2grid((2,3), (0,0), colspan=3)
experimentalfish = ax.plot([0,1],[np.mean(ePreVel), np.mean(ePostVel)],'o-b', lw=3, label='Experimental Fish (5V)')
pyplot.errorbar([0,1],[np.mean(ePreVel), np.mean(ePostVel)],fmt='ob', yerr=yerr, lw=3)
controlfish = ax.plot([0,1],[np.mean(cPreVel), np.mean(cPostVel)],'o-k', lw=3, label='Control Fish (5V)')
pyplot.errorbar([0,1],[np.mean(cPreVel), np.mean(cPostVel)],fmt='ok', yerr=yerrC, lw=3)
handles, labels=ax.get_legend_handles_labels()
ax.legend(handles, labels)
ax.set_xticks((0,1,2,3))
ax.set_xticklabels(('baseline\n (15min)', 'last 5 min\n of shock','post 0-15', 'post 15-30'))
pylab.xlim((-.25,3.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
patch3 = mpl.patches.Rectangle((-.25,0),1.5 , 10, color='g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch3)
ax2=pylab.subplot2grid((2,3), (1,0))
maxdistance = ax2.plot([0,1],[np.mean(eBaseMaxDist), np.mean(eEndMaxDist)],'o-b',lw=3)
pyplot.errorbar([0,1],[np.mean(eBaseMaxDist), np.mean(eEndMaxDist)],fmt='ob',yerr=yerrMD, lw=3)
maxdistancecontrol = ax2.plot([0,1],[np.mean(cBaseMaxDist), np.mean(cEndMaxDist)],'o-k',lw=3)
pyplot.errorbar([0,1],[np.mean(cBaseMaxDist), np.mean(cEndMaxDist)],fmt='ok',yerr=yerrMDC, lw=3)
ax2.set_xticks((0,1))
ax2.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Maximum Distance')
ax3=pylab.subplot2grid((2,3), (1,1))
totaldistance = ax3.plot([0,1],[np.mean(eBaseTotalDist), np.mean(eEndTotalDist)],'o-b',lw=3)
pyplot.errorbar([0,1],[np.mean(eBaseTotalDist), np.mean(eEndTotalDist)],fmt='ob',yerr=yerrTD, lw=3)
totaldistancecontrol = ax3.plot([0,1],[np.mean(cBaseTotalDist), np.mean(cEndTotalDist)],'o-k',lw=3)
pyplot.errorbar([0,1],[np.mean(cBaseTotalDist), np.mean(cEndTotalDist)],fmt='ok',yerr=yerrTDC, lw=3)
ax3.set_xticks((0,1))
ax3.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Total Distance')
ax4=pylab.subplot2grid((2,3), (1,2))
fraction = ax4.plot([0,1],[np.mean(eBaseFrac), np.mean(eEndFrac)],'o-b',lw=3)
pyplot.errorbar([0,1],[np.mean(eBaseFrac), np.mean(eEndFrac)],fmt='ob',yerr=yerrF, lw=3)
fractioncontrol = ax4.plot([0,1],[np.mean(cBaseFrac), np.mean(cEndFrac)],'o-k',lw=3)
pyplot.errorbar([0,1],[np.mean(cBaseFrac), np.mean(cEndFrac)],fmt='ok',yerr=yerrFC, lw=3)
ax4.set_xticks((0,1))
ax4.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Fraction of time')

pylab.figure()
pylab.suptitle('Is OMR working?')
ax2=pylab.subplot(231)
maxdistancecontrol = ax2.plot([0,1],[np.mean(cBaseMaxDist), np.mean(cEndMaxDist)],'o-k',lw=3, label="OMR on")
pyplot.errorbar([0,1],[np.mean(cBaseMaxDist), np.mean(cEndMaxDist)],fmt='ok',yerr=yerrMDC, lw=3)
maxdistancecontrolnon = ax2.plot([0,1],[np.mean(cBaseMaxDistNon), np.mean(cEndMaxDistNon)],'o-m',lw=3, label="OMR off")
yerrMDCN = (2*scipy.stats.sem(cBaseMaxDistNon), 2*scipy.stats.sem(cEndMaxDistNon))
pyplot.errorbar([0,1],[np.mean(cBaseMaxDistNon), np.mean(cEndMaxDistNon)],fmt='om',yerr=yerrMDCN, lw=3)
handles, labels=ax2.get_legend_handles_labels()
ax2.legend(handles, labels)
ax2.set_xticks((0,1))
ax2.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Control Maximum Distance')
ax3=pylab.subplot(232)
totaldistancecontrol = ax3.plot([0,1],[np.mean(cBaseTotalDist), np.mean(cEndTotalDist)],'o-k',lw=3, label = "OMR on")
pyplot.errorbar([0,1],[np.mean(cBaseTotalDist), np.mean(cEndTotalDist)],fmt='ok',yerr=yerrTDC, lw=3)
totaldistancecontrolnon = ax3.plot([0,1],[np.mean(cBaseTotalDistNon), np.mean(cEndTotalDistNon)],'o-m',lw=3, label = "OMR off")
yerrTDCN = (2*scipy.stats.sem(cBaseTotalDistNon), 2*scipy.stats.sem(cEndTotalDistNon))
pyplot.errorbar([0,1],[np.mean(cBaseTotalDistNon), np.mean(cEndTotalDistNon)],fmt='om',yerr=yerrTDCN, lw=3)
handles, labels=ax3.get_legend_handles_labels()
ax3.legend(handles, labels)
ax3.set_xticks((0,1))
ax3.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Control Total Distance')
ax4=pylab.subplot(233)
fractioncontrol = ax4.plot([0,1],[np.mean(cBaseFrac), np.mean(cEndFrac)],'o-k',lw=3,label = "OMR on")
pyplot.errorbar([0,1],[np.mean(cBaseFrac), np.mean(cEndFrac)],fmt='ok',yerr=yerrFC, lw=3)
fractioncontrolnon = ax4.plot([0,1],[np.mean(cBaseFracNon), np.mean(cEndFracNon)],'o-m',lw=3,label = "OMR off")
yerrFCN = (2*scipy.stats.sem(cBaseFracNon), 2*scipy.stats.sem(cEndFracNon))
pyplot.errorbar([0,1],[np.mean(cBaseFracNon), np.mean(cEndFracNon)],fmt='om',yerr=yerrFCN, lw=3)
handles, labels=ax4.get_legend_handles_labels()
ax4.legend(handles, labels)
ax4.set_xticks((0,1))
ax4.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Control Fraction of time')
ax5=pylab.subplot(234)
maxdistance = ax5.plot([0,1],[np.mean(eBaseMaxDist), np.mean(eEndMaxDist)],'o-k',lw=3, label="OMR on")
pyplot.errorbar([0,1],[np.mean(eBaseMaxDist), np.mean(eEndMaxDist)],fmt='ok',yerr=yerrMD, lw=3)
maxdistancenon = ax5.plot([0,1],[np.mean(eBaseMaxDistNon), np.mean(eEndMaxDistNon)],'o-m',lw=3, label="OMR off")
yerrMDN = (2*scipy.stats.sem(eBaseMaxDistNon), 2*scipy.stats.sem(eEndMaxDistNon))
pyplot.errorbar([0,1],[np.mean(eBaseMaxDistNon), np.mean(eEndMaxDistNon)],fmt='om',yerr=yerrMDN, lw=3)
handles, labels=ax2.get_legend_handles_labels()
ax5.legend(handles, labels)
ax5.set_xticks((0,1))
ax5.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Experimental Maximum Distance')
ax6=pylab.subplot(235)
totaldistance = ax6.plot([0,1],[np.mean(eBaseTotalDist), np.mean(eEndTotalDist)],'o-k',lw=3, label = "OMR on")
pyplot.errorbar([0,1],[np.mean(eBaseTotalDist), np.mean(eEndTotalDist)],fmt='ok',yerr=yerrTD, lw=3)
totaldistancenon = ax6.plot([0,1],[np.mean(eBaseTotalDistNon), np.mean(eEndTotalDistNon)],'o-m',lw=3, label = "OMR off")
yerrTDN = (2*scipy.stats.sem(eBaseTotalDistNon), 2*scipy.stats.sem(eEndTotalDistNon))
pyplot.errorbar([0,1],[np.mean(eBaseTotalDistNon), np.mean(eEndTotalDistNon)],fmt='om',yerr=yerrTDN, lw=3)
handles, labels=ax6.get_legend_handles_labels()
ax6.legend(handles, labels)
ax6.set_xticks((0,1))
ax6.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Experimental Total Distance')
ax7=pylab.subplot(236)
fraction = ax7.plot([0,1],[np.mean(eBaseFrac), np.mean(eEndFrac)],'o-k',lw=3,label = "OMR on")
pyplot.errorbar([0,1],[np.mean(eBaseFrac), np.mean(eEndFrac)],fmt='ok',yerr=yerrF, lw=3)
fractionnon = ax7.plot([0,1],[np.mean(eBaseFracNon), np.mean(eEndFracNon)],'o-m',lw=3,label = "OMR off")
yerrFN = (2*scipy.stats.sem(eBaseFracNon), 2*scipy.stats.sem(eEndFracNon))
pyplot.errorbar([0,1],[np.mean(eBaseFracNon), np.mean(eEndFracNon)],fmt='om',yerr=yerrFN, lw=3)
handles, labels=ax7.get_legend_handles_labels()
ax7.legend(handles, labels)
ax7.set_xticks((0,1))
ax7.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Experimental Fraction of time')

pylab.show()
"""
