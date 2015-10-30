import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy
import math
import itertools

##assume vanessa-style naming
def plot_data(datasets, datanames, plotTraces=False, startVel = 0.0):

    #initialize arrays and timing
    e_first_startshock = []
    e_first_endshock = []
    e_second_start = []
    e_second_end = []
    e_second_pre_probe = []
    e_second_post_probe = []
    mean_line = []
    trace_data =[]
    sm = 15
    endWinLen = 5*60 #amount of tracking at end

    for i in range(0,len(datasets),2):
        ndx =[]
        vel = aba.getMedianVelMulti(datasets[i], tRange=[0, 900], smoothWinLen = sm)
        for pos,sv in enumerate(vel):
            if sv<startVel:
                print "you lost a fish with starting velocity lower than {} in {}".format(startVel, datanames[int(math.floor(i/2))])
                ndx.append(pos)
        startshock = aba.getMedianVelMulti(datasets[i], tRange=[0, 900], smoothWinLen = sm)
        endshock = aba.getMedianVelMulti(datasets[i], tRange=[-5*60, -0], smoothWinLen = sm)
        end_first = aba.getMedianVelMulti(datasets[i+1], tRange=[0, 15*60], smoothWinLen = sm)
        end_second = aba.getMedianVelMulti(datasets[i+1], tRange=[15*60, 30*60], smoothWinLen = sm)
        end_start_probe = aba.getMedianVelMulti(datasets[i+1], tRange=[25*60, 30*60], smoothWinLen = sm)
        end_end_probe = aba.getMedianVelMulti(datasets[i+1], stateRange=[8, 8], smoothWinLen = sm)

        startshock=np.delete(startshock, ndx)
        endshock=np.delete(endshock, ndx)
        end_first=np.delete(end_first, ndx)
        end_second=np.delete(end_second, ndx)
        end_start_probe = np.delete(end_start_probe, ndx)
        end_end_probe = np.delete(end_end_probe, ndx)

        e_first_startshock.append(startshock)
        e_first_endshock.append(endshock)
        e_second_start.append(end_first)
        e_second_end.append(end_second)
        e_second_pre_probe.append(end_start_probe)
        e_second_post_probe.append(end_end_probe)
            
    for i in range(0,len(datasets)/2): 
        mean_line.append(np.transpose(np.hstack((np.mean(e_first_startshock[i]), np.mean(e_first_endshock[i]), np.mean(e_second_start[i]), np.mean(e_second_end[i]), np.mean(e_second_pre_probe[i]), np.mean(e_second_post_probe[i])))))
        if plotTraces:
            trace_data.append(np.vstack((e_first_startshock[i],e_first_endshock[i], e_second_start[i], e_second_end[i], e_second_pre_probe[i], e_second_post_probe[i])))
    print e_first_startshock, e_first_endshock, mean_line

#plot all the data together
    subx = len(datasets)/4
    suby = 1
    
    pylab.figure()

    for i in range(0,len(datasets)/2):
        ax=pylab.subplot(1,len(datasets)/2,i+1)
        if plotTraces:
            print "plotting all fish traces"
            pylab.plot(trace_data[i],'grey')
        pylab.plot([0,1,2,3,4,5],[np.mean(e_first_startshock[i]), np.mean(e_first_endshock[i]), np.mean(e_second_start[i]), np.mean(e_second_end[i]), np.mean(e_second_pre_probe[i]), np.mean(e_second_post_probe[i])], lw=3, label=datanames[i])
        ax.set_xticks((0,1,2,3,4,5))
        ax.set_xticklabels(('first 15', 'last 5', '15m new', '15-30', '30-45', '5m post probe'))
        pylab.xlim((-.25, 5.25))
        pylab.ylim((0,3.5))
        pylab.gca()
        pylab.plot(mean_line[i], lw=3)
        pylab.ylabel('Median speed (mm/s)')
        patch = mpl.patches.Rectangle((.25,0), .5, 10, color=[1,.5,.5], fill=True)
        patch2 = mpl.patches.Rectangle((4.25,0),.5, 10, color=[1,.5,.5], fill=True)
        pyplot.gca().add_patch(patch)
        pylab.gca().add_patch(patch2)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)

pyplot.show()
