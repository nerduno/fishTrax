import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

##make sure fish have been loaded
if len(e_first) < 1:
    print "No fish"
    1/0
else: 
    print "Fish data found"

def getTimeinCenterMulti(datasets, windowSize= None, tRange=None, stateRange=None):
    durations = []
    if tRange is not None: 
        endWindow = tRange[-1] 
    else: 
        for i in range(len(datasets)):
            tracking = datasets[i]['warpedTracking']
            if stateRange is not None: 
                _,et,_,_ = aba.state_to_time(datasets[i], stateRange[1])
                durations.append(et-tracking[0,0])
            else: 
                durations.append(datasets[i]['warpedTracking'][-1,0]-datasets[i]['warpedTracking'][0,0])
        endWindow = np.min(durations)

    windowsize = 30
    if windowSize is not None: 
        windowsize = windowSize
 
    ticks = np.arange(0,endWindow, windowsize)
    eTimeinCenter = np.zeros((len(datasets),len(ticks)-1))
    for i in range(len(ticks)-1):
        startT = ticks[i]
        endT = ticks[i+1]
        for d in range(len(datasets)):
            eTimeinCenter[d,i] = aba.getPercentTimeinCenter(datasets[d], tRange=[startT, endT])
    
    return eTimeinCenter

tR = 15*60
e_first_1a = getTimeinCenterMulti(e_first, tRange = [0,tR])
e_first_1b = getTimeinCenterMulti(e_first, tRange = [tR, tR*2])
e_shock5_start = getTimeinCenterMulti(e_shock, stateRange=[1,1])
e_shock5_end = getTimeinCenterMulti(e_shock, stateRange=[8,8])
e_sec_2a = getTimeinCenterMulti(e_sec, tRange=[0,tR])
e_sec_2b = getTimeinCenterMulti(e_sec, tRange=[tR,tR*2])

e_first_same_1a = getTimeinCenterMulti(e_same_first, tRange = [0,tR])
e_first_same_1b = getTimeinCenterMulti(e_same_first, tRange = [tR, tR*2])
e_shock5_same_start = getTimeinCenterMulti(e_same_shock, stateRange=[1,1])
e_shock5_same_end = getTimeinCenterMulti(e_same_shock, stateRange=[8,8])
e_sec_same_2a = getTimeinCenterMulti(e_same_sec, tRange=[0,tR])
e_sec_same_2b = getTimeinCenterMulti(e_same_sec, tRange=[tR,tR*2])

c_first_1a = getTimeinCenterMulti(c_first, tRange = [0,tR])
c_first_1b = getTimeinCenterMulti(c_first, tRange = [tR, tR*2])
c_shock5_start = getTimeinCenterMulti(c_shock, stateRange=[1,1])
c_shock5_end = getTimeinCenterMulti(c_shock, stateRange=[8,8])
c_sec_2a = getTimeinCenterMulti(c_sec, tRange=[0,tR])
c_sec_2b = getTimeinCenterMulti(c_sec, tRange=[tR,tR*2])

experimental = np.hstack((e_first_1a, e_first_1b, e_shock5_start, e_shock5_end, e_sec_2a, e_sec_2b))

pylab.figure()
#pylab.suptitle('Summary of Median Velocities (mm/s)')
ax = pylab.subplot(1,1,1)
ax.plot([0,1,2,3,4,5],[np.mean(e_first_1a), np.mean(e_first_1b), np.mean(e_shock5_start), np.mean(e_shock5_end), np.mean(e_sec_2a), np.mean(e_sec_2b)],'o-r', lw=3, label='Experimental Fish - Safe=non-shock tank')
yerrE = (scipy.stats.sem(np.mean(e_first_1a,1)), scipy.stats.sem(np.mean(e_first_1b,1)), scipy.stats.sem(np.mean(e_shock5_start,1)), scipy.stats.sem(np.mean(e_shock5_end,1)), scipy.stats.sem(np.mean(e_sec_2a,1)), scipy.stats.sem(np.mean(e_sec_2b,1)))
pyplot.errorbar([0,1,2,3,4,5],[np.mean(e_first_1a), np.mean(e_first_1b), np.mean(e_shock5_start), np.mean(e_shock5_end), np.mean(e_sec_2a), np.mean(e_sec_2b)],fmt='or',yerr=yerrE, lw=3)

#ax.plot([0,1,2,3,4,5],[np.mean(e_first_same_1a), np.mean(e_first_same_1b), np.mean(e_shock5_same_start), np.mean(e_shock5_same_end), np.mean(e_sec_same_2a), np.mean(e_sec_same_2b)],'o-b', lw=3, label='Experimental Fish - Safe=shock tank')
#yerrS = (scipy.stats.sem(np.mean(e_first_same_1a,1)), scipy.stats.sem(np.mean(e_first_same_1b,1)), scipy.stats.sem(np.mean(e_shock5_same_start,1)), scipy.stats.sem(np.mean(e_shock5_same_end,1)), scipy.stats.sem(np.mean(e_sec_same_2a,1)), scipy.stats.sem(np.mean(e_sec_same_2b,1)))
#pyplot.errorbar([0,1,2,3,4,5],[np.mean(e_first_same_1a), np.mean(e_first_same_1b), np.mean(e_shock5_same_start), np.mean(e_shock5_same_end), np.mean(e_sec_same_2a), np.mean(e_sec_same_2b)],fmt='ob',yerr=yerrS, lw=3)

ax.plot([0,1,2,3,4,5],[np.mean(c_first_1a), np.mean(c_first_1b), np.mean(c_shock5_start), np.mean(c_shock5_end), np.mean(c_sec_2a), np.mean(c_sec_2b)],'o-k', lw=3, label='Control Fish - Safe=non-shock tank')
yerrC = (scipy.stats.sem(np.mean(c_first_1a,1)), scipy.stats.sem(np.mean(c_first_1b,1)), scipy.stats.sem(np.mean(c_shock5_start,1)), scipy.stats.sem(np.mean(c_shock5_end,1)), scipy.stats.sem(np.mean(c_sec_2a,1)), scipy.stats.sem(np.mean(c_sec_2b,1)))
pyplot.errorbar([0,1,2,3,4,5],[np.mean(c_first_1a), np.mean(c_first_1b), np.mean(c_shock5_start), np.mean(c_shock5_end), np.mean(c_sec_2a), np.mean(c_sec_2b)],fmt='ok',yerr=yerrC, lw=3)
#handles, labels=ax.get_legend_handles_labels()
#ax.legend(handles, labels)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('0-15 min \n neutral tank', '15-30 min \n neutral tank', 'first 15 min \n shock tank', 'last 5 min \n shock tank', '0-15 min \n test tank', '15-30 min \n test tank'))
pylab.xlim((-.25,5.25))
pylab.ylim((0,.7))
pylab.ylabel('Fraction of Time in Center')
pylab.axvline(x=1.5, color = 'k', lw=3, ls='dashed')
pylab.axvline(x=3.5, color = 'k', lw=3, ls='dashed')
patch4 = mpl.patches.Rectangle((2.25,0), .5, 10, color=[1,.5,.5], fill=True)
pyplot.gca().add_patch(patch4)

pylab.show()

