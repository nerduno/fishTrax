import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

allfish = [
'/home/vburns/Dropbox/ConchisData/2013-04-21/f00350/f00350_2013-04-21-14-01-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00351/f00351_2013-04-21-14-01-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00352/f00352_2013-04-21-14-01-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00353/f00353_2013-04-21-14-01-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00354/f00354_2013-04-21-13-56-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00355/f00355_2013-04-21-13-56-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00356/f00356_2013-04-21-13-56-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00357/f00357_2013-04-21-13-56-21.json'
]
allfish = aba.loadMultipleDataFiles(allfish)

sm = 15
sections = 15

fish_vel0 = aba.getMedianVelMulti(allfish, (0,900), smoothWinLen=sm)
fish_vel1 = aba.getMedianVelMulti(allfish, (900,1800), smoothWinLen=sm)
fish_vel2 = aba.getMedianVelMulti(allfish, (1800,2700), smoothWinLen=sm)
fish_vel3 = aba.getMedianVelMulti(allfish, (2700,3600), smoothWinLen=sm)

vel0 = np.array([np.array([fish_vel0[n]]) for n in range(len(fish_vel0))])
vel1 = np.array([np.array([fish_vel1[n]]) for n in range(len(fish_vel1))])
vel2 = np.array([np.array([fish_vel2[n]]) for n in range(len(fish_vel2))])
vel3 = np.array([np.array([fish_vel3[n]]) for n in range(len(fish_vel3))])

allvelocity = np.transpose(np.hstack((vel0, vel1, vel2, vel3)))

pylab.figure()
pylab.suptitle('Fish Velocity over 1 hour - no noise or shocking')
ax = pylab.subplot(1,1,1)
pylab.plot(allvelocity)
pylab.plot(0, [fish_vel0], 'r.')
pylab.plot(1, [fish_vel1], 'r.')
pylab.plot(2, [fish_vel2], 'r.')
pylab.plot(3, [fish_vel3], 'r.')
pylab.plot([0, 1, 2, 3], [np.mean(fish_vel0), np.mean(fish_vel1), np.mean(fish_vel2), np.mean(fish_vel3)], 'o-k', lw=3)
ax.set_xticks((0,1,2,3))
ax.set_xticklabels(('0-15', '15-30','30-45', '45-60'))
pylab.xlim((-.25, 3.5))
pylab.ylim((0, 5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.show()
