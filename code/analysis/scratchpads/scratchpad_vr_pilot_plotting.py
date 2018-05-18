import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

##assume vanessa-style naming
def plot_drug_data(datasets, datanames,sbplt=(2,2)):
    suby = sbplt[0]
    subx = sbplt[1]
    numfish = len(datasets[0])
     
    #initialize arrays and timing
    e_first_startshock = []
    e_first_endshock = []
    mean_line = []
    sm = 15
    endWinLen = 5*60 #amount of tracking at end

    for i in range(0,len(datasets),2): 
        e_first_startshock.append(aba.getMedianVelMulti(datasets[i], (0,900), smoothWinLen = sm))
        e_first_endshock.append(aba.getMedianVelMulti(datasets[i], tRange=[-endWinLen, -0], smoothWinLen = sm))
        
    for i in range(len(datasets)/2): 
        mean_line.append(np.transpose(np.hstack((np.mean(e_first_startshock[i]), np.mean(e_first_endshock[i])))))

    print e_first_startshock, e_first_endshock
    
    #plot data
    pylab.figure()
    pylab.suptitle('Drug Pilot Results')
    for i,plt in zip(range(numfish), range(1,5,2)):
        ax = pylab.subplot(suby, subx, plt)
        pylab.plot(0, [e_first_startshock[0][i]], '.')
        pylab.plot(1, [e_first_endshock[0][i]], '.')
        #pylab.title(datanames[i])
        ax.set_xticks((0,1))
        ax.set_xticklabels(('first 15', 'last 5'))
        pylab.xlim((-.25, 1.25))
        pylab.ylim((0,4))
        #pylab.plot(mean_line[i], 'k', lw=3)
        pylab.ylabel('Median speed (mm/s)')
        ax2 = pylab.subplot(suby, subx, plt+1)
        eVelocity, velWindow = plot_velocity_trace(datasets[0][i])
        for i in range(len(eVelocity)):
            xax = velWindow[1:]
            pylab.plot(xax,eVelocity[i],'k',alpha=.3)
        pylab.plot(xax,eVelocity[1],'g',lw=3)
        pylab.plot(xax,eVelocity[2],'b',lw=3)
        pylab.plot(xax,np.mean(eVelocity,0),'k',lw=3)
        pylab.errorbar(xax, np.mean(eVelocity,0),lw=3, fmt='ok',yerr=scipy.stats.sem(eVelocity))
        pylab.ylim((0,4))
        #pylab.xlim((500, 3200))
        ax2.set_yticks([0.0,1.0,2.0,3.0,4.0])
        pylab.xlabel('Time (s)')
        pylab.ylabel('Median Speed (mm/s)')

def plot_velocity_trace(fish_data):
    sm=15
    durations = []
    durations.append(fish_data['warpedTracking'][:,0][-1]-fish_data['warpedTracking'][:,0][0])
    duration = min(durations)
    windowSize = 60
    velWindow = np.arange(600, duration, windowSize)
    startshock=15*60
    endshock=30*60+30*2
    eVelocity = np.zeros((len(fish_data), len(velWindow)-1))
    for i in range(len(velWindow)-1):
        startT = velWindow[i]
        endT = velWindow[i+1]
        for exp in range(len(fish_data)):
            [expVel, et] = aba.getVelRaw(fish_data,tRange=(startT, endT), smoothWinLen = sm)
            eVelocity[exp,i] = np.median(expVel)
    return eVelocity, velWindow


            
"""
[tv, control_experimental_start] = scipy.stats.ttest_ind(cBaseVel_1a, eBaseVel5_1a)
#convert to array
eBV5_1a = np.array([np.array([eBaseVel5_1a[n]]) for n in range(len(eBaseVel5_1a))])
pylab.plot(5, [cBaseVel_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],'o-k',lw=3)
pylab.axvline(x=1.5, color = 'k', lw=3, ls='dashed')
pylab.axvline(x=3.5, color = 'k', lw=3, ls='dashed')
patch5 = mpl.patches.Rectangle((2.25,0), .5, 10, color=[1,.5,.5], fill=True)
pyplot.gca().add_patch(patch5)
"""
pyplot.show()
