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

#velocity analysis 
sm = 15; #smooth over 15 frames.
endWinLen = 5 * 60; #seconds

#find durations and make index of times
durations = []
for exp,cnt in zip(range(len(e_shock)), range(len(c_shock))):
    durations.append(e_shock[cnt]['warpedTracking'][:,0][-1]-e_shock[cnt]['warpedTracking'][:,0][0])
    durations.append(c_shock[cnt]['warpedTracking'][:,0][-1]-c_shock[cnt]['warpedTracking'][:,0][0])

duration = min(durations)

windowSize = 60
velWindow = np.arange(600, duration, windowSize)

startshock=15*60
endshock=30*60+30*2

eVelocity = np.zeros((len(e_shock), len(velWindow)-1))
cVelocity = np.zeros((len(c_shock), len(velWindow)-1))
for i in range(len(velWindow)-1):
    startT = velWindow[i]
    endT = velWindow[i+1]
    for exp in range(len(e_shock)):
        [expVel, et] = aba.getVelRaw(e_shock[exp],tRange=(startT, endT), smoothWinLen = sm)
        eVelocity[exp,i] = np.median(expVel)
    for cnt in range(len(c_shock)):
        [cntVel, ct] = aba.getVelRaw(c_shock[cnt],tRange=(startT, endT), smoothWinLen = sm)
        cVelocity[cnt,i] = np.median(cntVel)

fig = pylab.figure(100, figsize=(6.5,6))
pylab.clf()
pylab.suptitle('Fish velocity traces during shocking')
ax = pylab.subplot(111)
for i in range(len(eVelocity)):
    xax = velWindow[1:]
    pylab.plot(xax,eVelocity[i],'k',alpha=.3)
    #pylab.plot(xax,eVelocity[i])
pylab.plot(xax,eVelocity[1],'g',lw=3)
pylab.plot(xax,eVelocity[2],'b',lw=3)
pylab.plot(xax,np.mean(eVelocity,0),'k',lw=3)
pylab.errorbar(xax, np.mean(eVelocity,0),lw=3, fmt='ok',yerr=scipy.stats.sem(eVelocity))
pylab.ylim((0,4))
pylab.xlim((500, 3200))
ax.set_yticks([0.0,1.0,2.0,3.0,4.0])
pylab.xlabel('Time (s)')
pylab.ylabel('Median Speed (mm/s)')
patch1=mpl.patches.Rectangle((startshock,0), endshock, 8,color=[1,.5,.5], fill=True)
pyplot.gca().add_patch(patch1)
'''
ax = pylab.subplot(212)
pylab.vlines((startshock,startshock+endshock),ymin=0,ymax=4, color=[1,.5,.5],lw=3)
for i in range(len(cVelocity)):
    pylab.plot(xax,cVelocity[i],'k', alpha=.3)
pylab.plot(xax,np.mean(cVelocity,0),'k',lw=3)
pylab.errorbar(xax, np.mean(cVelocity,0),lw=3, fmt='ok',yerr=scipy.stats.sem(cVelocity))
pylab.xlabel('Time (s)')
pylab.ylim((0,4))
ax.set_yticks([0.0,1.0,2.0,3.0,4.0])
pylab.xlim((550,3150))
pylab.ylabel('Median Speed (mm/s)')
'''
pylab.show()
