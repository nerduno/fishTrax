import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

#first is 30 min in safe tank, then standard shocking, then 30 min in safe tank
#note that currents from march were measured at 5ms, giving a lot of variation?
all_fish = [
'/home/vburns/Dropbox/ConchisData/2013-03-29/f00239/f00239_2013-03-29-17-14-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00240/f00240_2013-03-29-17-14-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00241/f00241_2013-03-29-17-14-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00242/f00242_2013-03-29-17-14-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00243/f00243_2013-03-29-17-15-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00244/f00244_2013-03-29-17-15-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00245/f00245_2013-03-29-17-15-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00246/f00246_2013-03-29-17-15-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00366/f00366_2013-04-29-09-53-50.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00368/f00368_2013-04-29-09-53-44.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00369/f00369_2013-04-29-09-53-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00372/f00372_2013-04-29-09-55-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00373/f00373_2013-04-29-09-55-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00358/f00358_2013-04-22-09-50-37.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00360/f00360_2013-04-22-09-50-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00361/f00361_2013-04-22-09-50-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00362/f00362_2013-04-22-09-48-34.json',#low starting velocity in second base
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00363/f00363_2013-04-22-09-48-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00364/f00364_2013-04-22-09-48-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00365/f00365_2013-04-22-09-48-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00375/f00375_2013-04-29-13-23-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00376/f00376_2013-04-29-13-23-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00377/f00377_2013-04-29-13-26-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00378/f00378_2013-04-29-13-27-22.json', #low starting velocity #and weird current #and tracking
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00380/f00380_2013-04-29-13-30-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00381/f00381_2013-04-29-13-30-24.json',
'/home/vburns/Dropbox/ConchisData/2013-03-30/f00255/f00255_2013-03-30-09-13-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00256/f00256_2013-03-30-09-13-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00257/f00257_2013-03-30-09-13-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00258/f00258_2013-03-30-09-13-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00259/f00259_2013-03-30-09-15-56.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00260/f00260_2013-03-30-09-15-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00261/f00261_2013-03-30-09-15-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00262/f00262_2013-03-30-09-15-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00382/f00382_2013-04-29-15-53-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00383/f00383_2013-04-29-15-53-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00384/f00384_2013-04-29-15-53-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00385/f00385_2013-04-29-15-53-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00386/f00386_2013-04-29-15-54-54.json', #has current when not supposed to? nothing else wrong
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00387/f00387_2013-04-29-15-54-52.json', #low starting velocity
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00388/f00388_2013-04-29-15-54-50.json',
]
all_fish = aba.loadMultipleDataFiles(all_fish)

#velocity analysis 
sm = 15; #smooth over 15 frames.
endWinLen = 5 * 60; #seconds

all_fish_vel = aba.getMedianVelMulti(all_fish, (0,900), smoothWinLen = sm)

#convert to array

pylab.figure()
pylab.suptitle('Distribution of Starting Velocities')
ax = pylab.subplot(1,1,1)
pylab.hist(all_fish_vel, bins=len(all_fish))
pylab.ylabel('Number of Fish')
pylab.xlabel('Velocity (mm/s)')
#pylab.xticks(np.array(xrange(0,14))/2.0)
pylab.show()
