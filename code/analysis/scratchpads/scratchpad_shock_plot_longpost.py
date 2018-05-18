import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy
import itertools

##assume vanessa-style naming
def plot_data(datasets, datanames, plotTraces=False, startVel = 0.0):

    #initialize arrays and timing
    e_first_startshock = []
    e_first_endshock = []
    e_first_end = []
    mean_line = []
    trace_data =[]
    sm = 15
    endWinLen = 5*60 #amount of tracking at end

    for i in range(0,len(datasets)):
        ndx =[]
        vel = aba.getMedianVelMulti(datasets[i], tRange=[0, 900], smoothWinLen = sm)
        for pos,sv in enumerate(vel):
            if sv<startVel:
                print "you lost a fish with starting velocity lower than {} in {}".format(startVel, datanames[i])
                ndx.append(pos)
        startshock = aba.getMedianVelMulti(datasets[i], tRange=[0, 900], smoothWinLen = sm)
        endshock = aba.getMedianVelMulti(datasets[i], tRange=[50*60, 55*60], smoothWinLen = sm)
        end = aba.getMedianVelMulti(datasets[i], tRange=[-15*60, -0], smoothWinLen = sm)
        startshock=np.delete(startshock, ndx)
        endshock=np.delete(endshock, ndx)
        end=np.delete(end, ndx)
        e_first_startshock.append(startshock)
        e_first_endshock.append(endshock)
        e_first_end.append(end)
            
        #for i in range(len(datasets)): 
        mean_line.append(np.transpose(np.hstack((np.mean(e_first_startshock[i]), np.mean(e_first_endshock[i]), np.mean(e_first_end[i])))))
        if plotTraces:
            trace_data.append(np.vstack((e_first_startshock[i],e_first_endshock[i], e_first_end[i])))
    print e_first_startshock, e_first_endshock, e_first_end

#plot all the data together
    subx = len(datasets)/2
    suby = 1
    
    pylab.figure()

    for i in range(len(datasets)):
        ax=pylab.subplot(1,len(datasets),i+1)
        if plotTraces:
            print "plotting all fish traces"
            pylab.plot(trace_data[i],'grey')
        #yerr = (2*scipy.stats.sem(e_first_startshock[i]), 2*scipy.stats.sem(e_first_endshock[i]), 2*scipy.stats.sem(e_first_end[i]))
        pylab.plot([0,1,2],[np.mean(e_first_startshock[i]), np.mean(e_first_endshock[i]), np.mean(e_first_end[i])], lw=3, label=datanames[i])
       # pylab.errorbar([0,1,2],[np.mean(e_first_startshock[i]), np.mean(e_first_endshock[i]), np.mean(e_first_end[i])], yerr = yerr, lw=3)
        ax.set_xticks((0,1,2))
        ax.set_xticklabels(('first 15', 'last 5', '30m later'))
        pylab.xlim((-.25, 2.25))
        pylab.ylim((0,2.0))
        pylab.gca()
        pylab.plot(mean_line[i], lw=3)
        pylab.ylabel('Median speed (mm/s)')
        patch = mpl.patches.Rectangle((.25,0), .5, 10, color=[1,.5,.5], fill=True)
        pyplot.gca().add_patch(patch)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)

pyplot.show()
