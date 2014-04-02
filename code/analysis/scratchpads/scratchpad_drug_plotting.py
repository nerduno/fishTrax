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
    if subx*suby != len(datasets)/2: 
        print "warning, wrong plotting or data lengths" 
    
    #initialize arrays and timing
    e_first_startshock = []
    e_first_endshock = []
    e_sec_2a = []
    e_sec_2b = []
    mean_line = []
    sm = 15
    endWinLen = 5*60 #amount of tracking at end

    for i in range(0,len(datasets),2): 
        e_first_startshock.append(aba.getMedianVelMulti(datasets[i], (0,900), smoothWinLen = sm))
        e_first_endshock.append(aba.getMedianVelMulti(datasets[i], tRange=[-endWinLen, -0], smoothWinLen = sm))
        e_sec_2a.append(aba.getMedianVelMulti(datasets[i+1], (0,900), smoothWinLen = sm))
        e_sec_2b.append(aba.getMedianVelMulti(datasets[i+1], (900,1800), smoothWinLen = sm))
        
    for i in range(len(datasets)/2): 
        mean_line.append(np.transpose(np.hstack((np.mean(e_first_startshock[i]), np.mean(e_first_endshock[i]), np.mean(e_sec_2a[i]), np.mean(e_sec_2b[i])))))

    #plot data
    pylab.figure()
    pylab.suptitle('Drug Pilot Results')
    for i in range(subx*suby):
        ax = pylab.subplot(subx, suby, i+1)
        pylab.plot(0, [e_first_startshock[i]], '.')
        pylab.plot(1, [e_first_endshock[i]], '.')
        pylab.plot(2, [e_sec_2a[i]], '.')
        pylab.plot(3, [e_sec_2b[i]], '.')
        yerr = (2*scipy.stats.sem(e_first_startshock[i]), 2*scipy.stats.sem(e_first_endshock[i]), 2*scipy.stats.sem(e_sec_2a[i]),2*scipy.stats.sem(e_sec_2b[i]))
        pylab.plot([0,1,2,3],[np.mean(e_first_startshock[i]), np.mean(e_first_endshock[i]), np.mean(e_sec_2a[i]), np.mean(e_sec_2b[i])], 'ok', lw=3)
        pylab.errorbar([0,1,2,3],[np.mean(e_first_startshock[i]), np.mean(e_first_endshock[i]), np.mean(e_sec_2a[i]), np.mean(e_sec_2b[i])], fmt='ok', yerr = yerr, lw=3)
        pylab.title(datanames[i])
        ax.set_xticks((0,1,2,3))
        ax.set_xticklabels(('first 15', 'last 5', 'post 0-15', 'post 15-30'))
        pylab.xlim((-.25, 3.25))
        pylab.ylim((0,4))
        pylab.plot(mean_line[i], 'k', lw=3)
        pylab.ylabel('Median speed (mm/s)')
'''
#plot all the data together
    pylab.figure()
    import itertools
    pylab.suptitle('Young Fish')
    for i,color in itertools.izip(range(len(datasets)/2),['b', 'r','k']):
        yerr = (2*scipy.stats.sem(e_first_startshock[i]), 2*scipy.stats.sem(e_first_endshock[i]), 2*scipy.stats.sem(e_sec_2a[i]),2*scipy.stats.sem(e_sec_2b[i]))
        pylab.plot([0,1,2,3],[np.mean(e_first_startshock[i]), np.mean(e_first_endshock[i]), np.mean(e_sec_2a[i]), np.mean(e_sec_2b[i])], color, lw=3)
        pylab.errorbar([0,1,2,3],[np.mean(e_first_startshock[i]), np.mean(e_first_endshock[i]), np.mean(e_sec_2a[i]), np.mean(e_sec_2b[i])], fmt=color, yerr = yerr, lw=3)
        ax.set_xticks((0,1,2,3))
        ax.set_xticklabels(('first 15', 'last 5', 'post 0-15', 'post 15-30'))
        pylab.xlim((-.25, 3.25))
        pylab.ylim((0,4))
        pylab.plot(mean_line[i], color, lw=3)
    pylab.ylabel('Median speed (mm/s)')
'''            
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
