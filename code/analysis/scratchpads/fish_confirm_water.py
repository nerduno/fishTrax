import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy
import os

#this is fish that is shocked and then replaced in same tank with new water
e_shock = [
 '/home/vburns/Dropbox/ConchisData/2014-03-31/f01193/f01193_2014-03-31-13-19-56.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-31/f01194/f01194_2014-03-31-13-20-05.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-31/f01195/f01195_2014-03-31-13-20-17.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-31/f01196/f01196_2014-03-31-13-20-28.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-31/f01197/f01197_2014-03-31-13-20-38.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-31/f01198/f01198_2014-03-31-13-20-51.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-31/f01199/f01199_2014-03-31-13-21-03.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-31/f01200/f01200_2014-03-31-13-21-18.json',
]
e_shock = aba.loadMultipleDataFiles(e_shock)

e_sec = [
 '/home/vburns/Dropbox/ConchisData/2014-03-31/f01193/f01193_2014-03-31-14-18-56.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-31/f01194/f01194_2014-03-31-14-19-14.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-31/f01195/f01195_2014-03-31-14-19-26.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-31/f01196/f01196_2014-03-31-14-19-48.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-31/f01197/f01197_2014-03-31-14-20-00.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-31/f01198/f01198_2014-03-31-14-20-11.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-31/f01199/f01199_2014-03-31-14-20-23.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-31/f01200/f01200_2014-03-31-14-20-41.json',
]
e_sec = aba.loadMultipleDataFiles(e_sec)

print 'Done loading fish'
